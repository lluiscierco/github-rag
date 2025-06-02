# Create fast api server
from app.loaders.github_loader import load_github_docs

def test_end_to_end():
    docs = load_github_docs(repo_name="langchain-ai/langchain")
    print(docs)

if __name__ == "__main__":
    test_end_to_end()