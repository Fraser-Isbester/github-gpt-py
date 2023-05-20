"""Base module for github_gpt_py"""
import logging
import os
import subprocess
import sys

# from github import Github
import github
from git import repo


def main():
    """main function for testing"""

    try:
        repo_path = sys.argv[1]
    except IndexError:
        repo_path = './'

    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        github_token = gh_auth_token()
    gh = github.Github(github_token)

    # Load the Repo
    git_repo = GitHubRepo(repo_path, gh)
    # git_repo = repo.Repo(repo_path)
    # print(git_repo)



    # Get The Diff
    # diff = diff_from_head(git_repo)

    # Generate a PR

class GitHubRepo:

    def __init__(self, repo_path: str, client: github.Github):
        self.repo_path = repo_path
        self.gh = client
        self._git_repo = repo.Repo(repo_path)
        self._gh_repo = self.gh.get_repo(f"{self.owner}/{self.name}")

    def create_pull_request(self, title: str, body: str):
        """Create a pull request on the repo"""
        self._gh_repo.create_pull(
            title=title,
            body=body,
            base=self._gh_repo.default_branch,
            head=self._git_repo.active_branch.name,
        )

    @property
    def owner(self):
        owner = self._git_repo.remotes.origin.url \
            .split('/')[-2] \
            .split(':')[1]
        return owner

    @property
    def name(self):
        repo_name = self._git_repo.remotes.origin.url \
            .split('/')[-1] \
            .split('.')[0]
        return repo_name


def diff_from_head(repo):
    """Get the diff from the head of the repo"""

    # Get Default Branch
    default_branch = repo.git.symbolic_ref("refs/remotes/origin/HEAD")

    # Get the Diff
    diff = repo.git.diff(default_branch)
    return diff

def gh_auth_token() -> str:
    """Login to github using gh auth token"""
    logging.warning(
        "GITHUB_TOKEN not found in environment variable. " +
        "Attempting gh auth login."
    )
    try:
        # subprocess.run() returns a CompletedProcess instance
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        # check the return code and raise an error if the command failed
        result.check_returncode()
        # return the sanitized output
        return result.stdout.replace('\n', ' ').strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error running gh auth token command.")
        raise e


if __name__ == '__main__':
    main()
