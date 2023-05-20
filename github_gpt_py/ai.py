from langchain.prompts import PromptTemplate


class Prompts:
    gitdiff_pull_title = PromptTemplate(
        input_variables=["diff"],
        template="""
            Provide a concise title for a GitHub pull request for this git diff:\n\n{diff}",
        """
    )

    gitdiff_pull_body = PromptTemplate(
        input_variables=["diff"],
        template="""
            Provide a concise body for a GitHub pull request for this git diff:\n\n{diff}",
        """
    )