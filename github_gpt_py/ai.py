from langchain.prompts import PromptTemplate


class Prompts:
    gitdiff_pull_title = PromptTemplate(
        input_variables=["diff"],
        template="""
            Provide a concise summary of this git diff in less than 10 words:\n\n{diff}",
        """
    )

    gitdiff_pull_body = PromptTemplate(
        input_variables=["diff"],
        template="""
            Provide a summary of changs from this git diff:\n\n{diff}",
        """
    )

