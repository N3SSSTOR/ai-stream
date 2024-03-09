import os 
import dotenv 

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
SPEECH_TOKEN = os.getenv("SPEECH_TOKEN")
DONATION_ID = os.getenv("DONATION_ID")
DONATION_SECRET = os.getenv("DONATION_SECRET")