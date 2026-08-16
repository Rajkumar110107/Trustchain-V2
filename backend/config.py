import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from root directory
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "127.0.0.1")
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "https://trustchain-v2-murex.vercel.app,http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000").split(",")

    
    # Blockchain Settings
    RPC_URL: str = os.getenv("RPC_URL", "http://127.0.0.1:8545")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")
    CHAIN_ID: int = int(os.getenv("CHAIN_ID", 31337))

    # OCR Settings
    TESSERACT_CMD: str = os.getenv("TESSERACT_CMD", r"C:\Program Files\Tesseract-OCR\tesseract.exe")

    # File & Path Settings
    BASE_DIR: Path = BASE_DIR
    MODEL_PATH: Path = BASE_DIR / os.getenv("MODEL_PATH", "model/model.pth")
    UPLOAD_DIR: Path = BASE_DIR / os.getenv("UPLOAD_DIR", "backend/uploads")
    ELA_DIR: Path = BASE_DIR / os.getenv("ELA_DIR", "backend/ela_outputs")
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", 10))

settings = Settings()

# Ensure required runtime directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.ELA_DIR.mkdir(parents=True, exist_ok=True)
