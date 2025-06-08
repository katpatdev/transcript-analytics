import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    BENZINGA_API_KEY = os.getenv('BENZINGA_API_KEY')
    BENZINGA_API_URL = "https://api.benzinga.com/api/v1/transcripts/calls"