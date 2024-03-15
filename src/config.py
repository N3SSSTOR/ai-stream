import os 
import dotenv 

from person import objects as persons
from person.objects import ASSETS_DIR

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
SPEECH_TOKEN = os.getenv("SPEECH_TOKEN")
DONATION_ID = os.getenv("DONATION_ID")
DONATION_SECRET = os.getenv("DONATION_SECRET")
STREAM_KEY = os.getenv("STREAM_KEY_2")
STREAM_URL = os.getenv("STREAM_URL")

PERSON_1 = persons.BrokeMaxMaxbetov
PERSON_2 = persons.BrokeSaveliiJournalistov

DB_CONNECTION_URL = "sqlite+aiosqlite:///db.sqlite"
ECHO = False  

FPS = 10
MAIN_FONT_PATH = ASSETS_DIR + "font/FulboArgenta.ttf"