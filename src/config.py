import os 
import dotenv 

import person.objects as persons

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
SPEECH_TOKEN = os.getenv("SPEECH_TOKEN")
DONATION_ID = os.getenv("DONATION_ID")
DONATION_SECRET = os.getenv("DONATION_SECRET")

DB_CONNECTION_URL = "sqlite+aiosqlite:///db.sqlite"
ECHO = False  

PERSON_1 = persons.BrokeMaxMaxbetov
PERSON_2 = persons.BrokeSaveliiJournalistov