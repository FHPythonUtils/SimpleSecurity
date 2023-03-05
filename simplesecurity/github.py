import os

import requests

from simplesecurity.types import Finding


class GithubAnnotationsAndComments(object):
    def __init__(
        self,
        github_access_token: str,
        github_repo_url: str,
        github_workflow_run_id: str,
        findings: list[Finding],
        logger,
    ):
        self.github_access_token = github_access_token
        self.github_repo_url = github_repo_url
        self.github_workflow_run_id = github_workflow_run_id
        self.findings = findings
        self.annotations_list = []
        self.check_suite_runs = None
        self.workflow_run = None
        self.headers = None
        self.repo_name = None
        self.owner = None
        self.runID = None
        self.logger = logger

    def _process_findings(self) -> bool:
        """The findings must be processed in order to make them viable for
        annotation. The steps include:

        * filtering for any non-file-specific findings, as they will be commented in the PR instead of annotated
        * retrieving the endline of the finding, when available
        * templating the findings in the correct format for the GitHub API

        The function returns a boolean to flag for the list being empty

        :return: A boolean indicator flagging whether the list contains findings (True) or is empty (False)

        """
        if len(self.findings) > 0:
            for find in self.findings:
                # if the comments are not on a file level, we will parse them as comments instead
                if type(find["line"]) != int:
                    self.logger.info(
                        f"Found project level comment, commenting in PR accordingly {find}"
                    )
                    self._post_comment(find)
                # if the files are associated to particular files, we can annotate that within the code.
                else:
                    # if we have an endline, use it, otherwise we use the beginning line as endline.
                    try:
                        end = find["_other"]["end"]
                    except:
                        end = find["line"]

                    self.annotations_list.append(
                        {
                            "path": self._get_relative_path(
                                find["file"],
                                "home/runner/work/SimpleSecurity/SimpleSecurity/",
                            ),
                            "start_line": find["line"],
                            "end_line": end,
                            "annotation_level": "warning",
                            "message": f"{find['title']}\nLine: {find['line']}\nDescription: {find['description']}"
                            f"\nSeverity: {find['severity']}\nConfidence: {find['confidence']}",
                        }
                    )
            return True
        else:
            return False

    def _post_comment(self, find: dict):
        """This function comments finds that are not file-specific into the
        respective PR. The steps to do so include:

        * retrieving the issue_number
        * retrieving the comment_url
        * posting the comment via the GitHub API

        :param find: A dictionary containing a finding of one of the scanners
        :return: None

        """
        assert (
            self.workflow_run is not None
        ), "workflow_run has not been found, please run _search_check_suite before executing this function"
        assert (
            self.github_repo_url is not None
        ), "github_repo_url has not been found, please run _search_check_suite before executing this function"
        assert (
            self.owner is not None
        ), "owner has not been found, please run _search_check_suite before executing this function"
        assert (
            self.repo_name is not None
        ), "repo_name has not been found, please run _search_check_suite before executing this function"
        assert (
            self.headers is not None
        ), "headers has not been found, please run _search_check_suite before executing this function"

        # Get the correct issue number and comment URL so you can comment to the correct PR
        self.issue_number = self.workflow_run["pull_requests"][0]["number"]
        self.comment_url = (
            f"{self.github_repo_url}/issues/{self.issue_number}/comments"
        )

        # Template the comment in the correct format
        comment = {
            "body": f"SimpleSecurity Comment: \n{str(find)}",
        }

        try:
            resp = requests.post(
                self.comment_url.format(
                    owner=self.owner,
                    repo=self.repo_name,
                    issue_number=self.issue_number,
                ),
                json=comment,
                headers=self.headers,
            )
            self.logger.info(
                f"Posted Comment and got return status: {resp.status_code}"
            )

            if resp.status_code >= 400:
                self.logger.warning(
                    f"Failed to post comment, the comment was {find} \n The Return was code {resp.status_code}\n The contents was: {resp.content}"
                )
        except Exception as e:
            self.logger.warning(f"Post comment request produced error, {e}")

    def _search_check_suite(self):
        """This function retrieve all parameters that are necessary for
        executing the next steps and include:

        * The API Headers
        * The repo name, owner and RunID
        * The workflow and check_suite runs

        This step is essential for all the other consecutive steps and the parameters are cast as attributes to the class

        :return: None

        """
        self.headers = {
            "Authorization": f"Bearer {self.github_access_token}",
            "Accept": "application/vnd.github+json",
        }

        workflow_url = f"{self.github_repo_url}/actions/runs/{self.github_workflow_run_id}"
        workflow_run_resp = requests.get(workflow_url, headers=self.headers)
        self.workflow_run = workflow_run_resp.json()
        self.logger.info(
            f"Status for checking workflow run ID: {workflow_run_resp.status_code}"
        )

        # Extracting owner, repo, and run id for the header in the patch request
        self.repo_name = f"{self.workflow_run['repository']['name']}"
        self.owner = f"{self.workflow_run['repository']['owner']['login']}"

        check_suite_runs_resp = requests.get(
            f"{self.workflow_run['check_suite_url']}/check-runs",
            headers=self.headers,
        )
        self.check_suite_runs = check_suite_runs_resp.json()
        self.check_suite_run_url = self.check_suite_runs["check_runs"][0][
            "url"
        ]
        self.logger.info(
            f"Status for check suite run ID: {check_suite_runs_resp.status_code}"
        )

        self.runID = self.check_suite_runs["check_runs"][0]["id"]

    def _upload_batchwise_annotations(self):
        """This function uses the annotation_list and patches this as
        annotations through the GitHub API. Other parameters include:

        * check_suite_run_url
        * owner
        * repo_name
        * runID
        * headers

        The function executes the patching in batches of 50, as this is the limit provided by GitHub.

        :return: None

        """
        assert (
            len(self.annotations_list) > 0
        ), "annotations_list is empty, please run _search_check_suite before executing this function"
        assert (
            self.check_suite_run_url is not None
        ), "check_suite_run_url has not been found, please run _search_check_suite before executing this function"
        assert (
            self.owner is not None
        ), "owner has not been found, please run _search_check_suite before executing this function"
        assert (
            self.repo_name is not None
        ), "repo_name has not been found, please run _search_check_suite before executing this function"
        assert (
            self.runID is not None
        ), "runID has not been found, please run _search_check_suite before executing this function"
        assert (
            self.headers is not None
        ), "headers has not been found, please run _search_check_suite before executing this function"

        # The GitHub API only accepts 50 annotations per call.
        batches = {}
        for i in range(0, len(self.annotations_list), 50):
            batches[i] = self.annotations_list[i : i + 50]

        for key_batch, value_batch in batches.items():
            # prep payload format
            check_suite_payload = {
                "output": {
                    "title": "Warnings",
                    "summary": f"{len(self.findings)} warning(s) found",
                    "annotations": value_batch,
                }
            }

            # Patch request to send the created annotations to GitHub through their API
            resp = requests.patch(
                self.check_suite_run_url.format(
                    owner=self.owner, repo=self.repo_name, run_id=self.runID
                ),
                json=check_suite_payload,
                headers=self.headers,
            )
            self.logger.info(
                f"Sending batch nr {key_batch}, response code {resp}"
            )

            if resp.status_code >= 400:
                self.logger.warning(
                    f"failed to send annotations for batch {key_batch}, the payload was \n {value_batch} \n that returned: {resp.status_code}, with boy {resp.content}"
                )

    def annotate_and_comment_in_pr(self):
        """
        This function orchestrates the flow of the comment and annotation process. The flow consits out of:
        1. searching the Check Suite and parameterize the class with all necessary tokens
        2. process the findings: comment the non-file related findings and format the file-related findings for annotation
        3. batchwise uploading of annotations for the file-related findings

        :return: None
        """
        # Getting all Params for doing requests
        self._search_check_suite()
        # Processing findings and commenting all non-annotations into PR
        found_findings = self._process_findings()
        # Patch annotations into PR
        if found_findings:
            self._upload_batchwise_annotations()
        else:
            self.logger.info(
                "No annotations were found, therefore not executing any annotations in PR"
            )

    @staticmethod
    def _get_relative_path(absolute_path: str, base_path: str) -> str:
        """This Function takes and absolute path and extracts the relative path
        using the os library and then replace the originated ../ format with an
        empty space.

        :return: path

        """
        result = os.path.relpath(absolute_path, base_path)
        path = result.replace("../", "")
        return path
