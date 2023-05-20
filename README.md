# GitHubGPTPy

GitHubGPTPy is a Python module that helps with automating the process of creating pull requests on GitHub using the power of OpenAI's language model.

This tool fetches the diff between the current active branch and the default branch of your Git repository, generates a descriptive pull request title and body with OpenAI's language model, and creates or updates a pull request on GitHub.

## Features

- Automates the creation and update of pull requests.
- Generates descriptive pull request titles and bodies with OpenAI's language model.
- Automatically pushes changes to the remote repository.
- Supports dry runs for creating pull requests.

## Installation

The required dependencies are GitPython, PyGithub, and OpenAI's language model.

## Environment Variables

Before using GitHubGPTPy, ensure you have the following environment variables set:

- `OPENAI_API_KEY`: Your OpenAI API Key. This is used to generate descriptive pull request titles and bodies.
- `GITHUB_TOKEN`: Your GitHub Token. This is used to create and update pull requests on GitHub. If this is not set, the tool will attempt to get the token using the `gh` command-line tool.

## Usage

You can use GitHubGPTPy by running it as a standalone Python script:

```bash
python github_gpt_py.py [path_to_your_repo]
```

If no path is provided, the current directory will be used as the default.

## API

The GitHubGPTPy module has several main components:

- `GitHubRepo`: Represents a GitHub repository. It has methods for getting a diff from the head of the repo, checking if there are open pull requests, creating pull requests, and pushing changes to the remote repo.
- `gh_auth_token`: If `GITHUB_TOKEN` is not found in environment variables, this function will attempt to authenticate using the `gh` command-line tool.
- `make_git_diff`: Generates a diff string from a list of change files.
- `main`: The main function that ties everything together. It fetches the diff, generates the pull request title and body, pushes changes to the remote repo, and finally creates or updates the pull request on GitHub.

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

GitHubGPTPy is licensed under the [MIT license](https://opensource.org/licenses/MIT).

## Disclaimer

This project is not officially supported by OpenAI or GitHub. Use at your own risk.
