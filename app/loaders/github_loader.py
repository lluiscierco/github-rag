
from langchain_community.document_loaders import GithubFileLoader
from dotenv import load_dotenv
import os

load_dotenv()

def load_github_docs(repo_name: str, branch: str="master", filter_file_extension: list[str]=".md") -> list:
    """
    Download a github repo by using the specified url and file extensions

    Args:
        repo_name (str): github name like: "langchain-ai/langchain"
        branch (str, optional): Branch to download. Defaults to "master".
        filter_file_extension (list[str], optional): Files extensions to download. Defaults to ".md".

    Returns:
        list: of downloaded documents (langchain class)
    """
    GITHUB_KEY = os.getenv("GITHUB_KEY")
    loader = GithubFileLoader(
        repo=repo_name,  #,  # the repo name
        branch=branch,  #"master",  # the branch name
        access_token=GITHUB_KEY,
        github_api_url="https://api.github.com",
        file_filter=lambda path: any(path.endswith(ext) for ext in filter_file_extension),  # load all markdowns files.
    )
    documents = loader.load()

    return(documents)