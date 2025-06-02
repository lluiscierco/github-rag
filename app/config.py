from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env into os.environ

GITHUB_KEY = os.getenv("GITHUB_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")

# from app import config
# token = config.GITHUB_KEY