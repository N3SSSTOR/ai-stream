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

PERSON_1 = persons.BrokeMaxMaxbetov
PERSON_2 = persons.BrokeSaveliiJournalistov

DB_CONNECTION_URL = "sqlite+aiosqlite:///db.sqlite"
ECHO = False  

PAUSE_SCENE_PATH = ASSETS_DIR + "video/scenes/pause.mp4"
PAUSE_SCENE_DURATION = 0

FPS = 12 
MAIN_FONT_PATH = ASSETS_DIR + "font/FulboArgenta.ttf"