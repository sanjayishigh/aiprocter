from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COMPILE_URL = "https://emkc.org/api/v2/piston/execute"
HF_TOKEN = os.getenv("HF_TOKEN")