from langchain_community.document_loaders import GithubFileLoader
from app import config
import asyncio


class GithubRepoLoader:
    def __init__(self):
        self.GITHUB_KEY = config.GITHUB_KEY
        self.github_api_url = "https://api.github.com"

    async def load_github_docs(
        self,
        repo_name: str,
        branch: str,
        filter_file_extension: list[str] | None,  # set default inside
    ) -> list:
        """
        Download a github repo by using the specified url and file extensions

        Args:
            repo_name (str): github name like: "langchain-ai/langchain"
            branch (str, optional): Branch to download. Defaults to "master".
            filter_file_extension (list[str], optional): Files extensions to download. Defaults to ".md".

        Returns:
            list: of downloaded documents (langchain class)
        """
        binary_extensions = [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".pdf",
            ".exe",
            ".dll",
            ".so",
            ".zip",
            ".tar",
            ".gz",
        ]
        loader = GithubFileLoader(
            repo=repo_name,
            branch=branch,
            access_token=self.GITHUB_KEY,
            github_api_url=self.github_api_url,
            file_filter=lambda path: (
                True
                if filter_file_extension is None
                else any(path.endswith(ext) for ext in filter_file_extension)
            )
            and not any(path.endswith(ext) for ext in binary_extensions),
        )
        documents = await loader.aload()

        return documents
