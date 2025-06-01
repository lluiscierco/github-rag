import pytest
from unittest.mock import patch, MagicMock, ANY
from app.loaders.github_loader import load_github_docs

@patch("app.loaders.github_loader.GithubFileLoader")
@patch("app.loaders.github_loader.os.getenv", return_value="fake_token")
def test_load_github_docs(mock_getenv, mock_loader_cls):
    mock_loader = MagicMock()
    mock_loader.load.return_value = ["doc1", "doc2"]
    mock_loader_cls.return_value = mock_loader

    result = load_github_docs("owner/repo", branch="main", filter_file_extension=[".md", ".py"])

    mock_getenv.assert_called_once_with("GITHUB_KEY")
    mock_loader_cls.assert_called_once_with(
        repo="owner/repo",
        branch="main",
        access_token="fake_token",
        github_api_url="https://api.github.com",
        file_filter=ANY,
    )
    mock_loader.load.assert_called_once()
    assert result == ["doc1", "doc2"]

