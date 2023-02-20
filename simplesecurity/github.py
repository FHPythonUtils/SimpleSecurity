import os
import requests
from simplesecurity.types import Finding
class GithubAnnotationsAndComments(object):
    def __init__(self,
                 github_access_token: str,
                 github_repo_url: str,
                 github_workflow_run_id: str,
                 findings: list[Finding],
                 logger
                 ):
        self.github_access_token = github_access_token
        self.github_repo_url = github_repo_url
        self.github_workflow_run_id = github_workflow_run_id
        self.findings = findings
        self.annotations_list = []
        self.check_suite_runs = None
        self.workflow_run = None
        self.headers = None
        self.logger = logger


    def _process_findings(self) -> bool:
        """
        This helper function does something
        :return:
        """
        if len(self.findings) > 0:
            for find in self.findings:
                # if the comments are not on a file level, we will parse them as comments instead
                if type(find['line']) != int:
                    self.logger.info(f"Found project level comment, commenting in PR accordingly {find}")
                    self._post_comment(find)
                # if the files are associated to particular files, we can annotate that within the code.
                else:
                    # if we have an endline, use it, otherwise we use the beginning line as endline.
                    try:
                        end = find['_other']['end']
                    except:
                        end = find["line"]

                    self.annotations_list.append(
                        {
                            "path": self._get_relative_path(find["file"],
                                                      "home/runner/work/SimpleSecurity/SimpleSecurity/"),
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

        issue_number = self.workflow_run["pull_requests"][0]["number"]
        comment_url = f"{self.github_repo_url}/issues/{issue_number}/comments"
        owner = f"{self.workflow_run['repository']['owner']['login']}"
        repo_name = f"{self.workflow_run['repository']['name']}"

        comment = {
                "body": f"SimpleSecurity Comment: \n{str(find)}",
            }

        # Do POST Request

        try:
            resp = requests.post(
                comment_url.format(owner=owner, repo=repo_name, issue_number=issue_number),
                json=comment,
                headers=self.headers,
            )
        except Exception as e:
            self.logger.warning(f"Patch request produced error, {e}")

        self.logger.info(f"Posted Comment and got return status: {resp.status_code}")

        if resp.status_code != 200:
            self.logger.warning(f"Failed to post comment, the comment was {find} \n The Return was code {resp.status_code}\n The contents was: {resp.content}")


    def _search_check_suite(self):
        self.headers = {
            "Authorization": f"Bearer {self.github_access_token}",
            "Accept": "application/vnd.github+json",
        }

        workflow_url = f"{self.github_repo_url}/actions/runs/{self.github_workflow_run_id}"
        workflow_run_resp = requests.get(workflow_url, headers=self.headers)
        self.workflow_run = workflow_run_resp.json()
        self.logger.info(f"Status for checking workflow run ID: {workflow_run_resp.status_code}")


        check_suite_runs_url = f"{self.workflow_run['check_suite_url']}/check-runs"

        check_suite_runs_resp = requests.get(check_suite_runs_url, headers=self.headers)
        self.check_suite_runs = check_suite_runs_resp.json()
        self.check_suite_run_url = self.check_suite_runs["check_runs"][0]["url"]
        self.logger.info(f"Status for check suite run ID: {check_suite_runs_resp.status_code}")

    def _upload_batchwise_annotations(self):

        # Extracting owner, repo, and run id for the header in the patch request
        repo_name = f"{self.workflow_run['repository']['name']}"
        owner = f"{self.workflow_run['repository']['owner']['login']}"
        runID = self.check_suite_runs["check_runs"][0]["id"]

        # The GitHub API only accepts 50 annotations per call.
        batches = {}
        for i in range(0, len(self.annotations_list), 50):
            batches[i] = self.annotations_list[i:i + 50]

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
                self.check_suite_run_url.format(owner=owner, repo=repo_name, run_id=runID),
                json=check_suite_payload,
                headers=self.headers,
            )
            self.logger.info(f"Sending batch nr {key_batch}, response code {resp}")

            if resp.status_code != 200:
                self.logger.warning(f"failed to send annotations for batch {key_batch}, the payload was \n {value_batch} \n that returned: {resp.status_code}, with boy {resp.content}")


    def annotate_and_comment_in_pr(self):
        """
        This Function uses a list of findings that are found with code scanner and annotates a GitHub PR. It therefore
        requires GitHub credentials to send the annotations.

        :param github_access_token: GitHub Access token, ideally provided within environment of execution.
        :param github_repo_url: GitHub Repo, is provided within a GitHub Action environment.
        :param github_workflow_run_id: GitHub workflow run id, is provided within a Github Action environment.
        :param findings: List of Findings objects (dicts) that detail findings of the scanners.
        """
        # Getting all Params for doing requests
        self._search_check_suite()
        # Processing findings and commenting all non-annotations into PR
        found_findings = self._process_findings()
        # Patch annotations into PR
        if found_findings:
            self._upload_batchwise_annotations()
        else:
            self.logger.info("No annotations were found, therefore not executing any annotations in PR")

    @staticmethod
    def _get_relative_path(absolute_path, base_path):
        """
        This Function takes and absolute path and extracts the relative path using the os library and
        then replace the originated ../ format with an empty space.
        """
        result = os.path.relpath(absolute_path, base_path)
        path = result.replace("../", "")
        return path
