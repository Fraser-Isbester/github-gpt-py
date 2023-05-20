"""Base module for github_gpt_py"""
import difflib
import logging
import os
import subprocess
import sys

import exceptions as e
import github
from ai import Prompts
from git import repo
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def main():
    """main function for testing"""

    try:
        repo_path = sys.argv[1]
    except IndexError:
        repo_path = "./"

    openai_token = os.environ.get("OPENAI_API_KEY")
    if not openai_token:
        raise e.PreconditionError("OPENAI_API_KEY not found in environment variable.")

    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        github_token = gh_auth_token()
    gh = github.Github(github_token)

    # Load the Repo
    g = GitHubRepo(repo_path, gh)

    # Get the Diff
    diff = g.get_diff_from_head()
    skip = ["poetry.lock"]
    diff_text = make_git_diff(diff, skip=skip)

    chat = ChatOpenAI()

    title = chat(
        [
            SystemMessage(
                content="You produce technical, concise responses to questions."
            ),
            HumanMessage(content=Prompts.gitdiff_pull_title.format(diff=diff_text)),
        ]
    )

    body = chat(
        [
            SystemMessage(
                content="You produce technical, concise, responses to questions."
            ),
            HumanMessage(content=Prompts.gitdiff_pull_body.format(diff=diff_text)),
        ]
    )

    # Push & Open PR
    g.push()
    r = g.create_pull_request(title=title.content, body=body.content)

    print(r)
    print(r.html_url)


class GitHubRepo:
    def __init__(self, repo_path: str, client: github.Github):
        self.repo_path = repo_path
        self.gh = client
        self._git_repo = repo.Repo(repo_path)
        self._gh_repo = self.gh.get_repo(f"{self.owner}/{self.name}")

    def push(self):
        """Pushes current branch to remote"""
        current_branch = self._git_repo.active_branch
        remote = self._git_repo.remote()
        return remote.push(refspec="%s:%s" % (current_branch.name, current_branch.name))

    def get_diff_from_head(self):
        """Gets the diff from the remote head of the repo"""
        r = self._git_repo
        r.remotes.origin.fetch()

        # Get the diff between the current branch and the default branch
        current_branch = r.active_branch
        diff = current_branch.commit.diff(self.default_branch)
        return diff

    def get_pull_request(self):
        """Gets an open pull requests for this repo"""
        r = self._gh_repo

        open_pulls = r.get_pulls(state="open")
        for pull in open_pulls:
            if pull.head.ref == self.active_branch.name:
                return pull
        return None

    def create_pull_request(self, title: str, body: str, atomic=True, dry_run=False):
        """Create a pull request on the repo from the current branch"""

        # Todo: make this type consistent with create_pull
        if dry_run:
            return {
                "title": title,
                "body": body,
                "base": self._gh_repo.default_branch,
                "head": self._git_repo.active_branch.name,
            }

        if atomic:
            # Check if there is already an open pull request
            pull = self.get_pull_request()
            if pull:
                # If there is, update it
                pull.edit(title=title, body=body)
                return pull

        return self._gh_repo.create_pull(
            title=title,
            body=body,
            base=self._gh_repo.default_branch,
            head=self._git_repo.active_branch.name,
        )

    @property
    def owner(self):
        return self._git_repo.remotes.origin.url.split("/")[-2].split(":")[1]

    @property
    def name(self):
        return self._git_repo.remotes.origin.url.split("/")[-1].split(".")[0]

    @property
    def default_branch(self):
        return self._gh_repo.default_branch

    @property
    def active_branch(self):
        return self._git_repo.active_branch


def make_git_diff(diff, skip=[]) -> str:
    """Makes a git diff from changefiles"""

    lines = []
    for item in diff.iter_change_type("M"):
        if item.a_blob.path in skip:
            continue

        lines.append("File: " + item.a_blob.path)
        lines.append("---------------------------------------------------")

        # Get the content of the file in the two versions as lists of lines
        old_content = item.b_blob.data_stream.read().decode().splitlines()
        new_content = item.a_blob.data_stream.read().decode().splitlines()

        # Compute the diff using difflib
        text_diff = difflib.unified_diff(old_content, new_content)

        # Print the diff
        for line in text_diff:
            lines.append(line)
    return "\n".join(lines)


def gh_auth_token() -> str:
    """Login to github using gh auth token"""
    logging.warning(
        "GITHUB_TOKEN not found in environment variable. " + "Attempting gh auth login."
    )
    try:
        # subprocess.run() returns a CompletedProcess instance
        result = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        # check the return code and raise an error if the command failed
        result.check_returncode()
        # return the sanitized output
        return result.stdout.replace("\n", " ").strip()
    except subprocess.CalledProcessError as e:
        logging.error("Error running gh auth token command.")
        raise e


if __name__ == "__main__":
    main()
