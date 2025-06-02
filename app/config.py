from dotenv import load_dotenv
import os

load_dotenv()  # loads from .env into os.environ

GITHUB_KEY = os.getenv("GITHUB_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")
PC_KEY = os.getenv("PC_KEY")
PC_INDEX = os.getenv("PC_INDEX")

# from app import config
# token = config.GITHUB_KEY