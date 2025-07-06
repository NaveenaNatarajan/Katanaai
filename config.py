import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Data file paths
DATA_PATH = os.path.join("data", "tshirt_data.csv")
IMAGE_FOLDER = os.path.join("images")
OUTPUT_FILE = os.path.join("data", "results.csv")

# API Keys (auto-loaded from .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
 
