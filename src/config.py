import os 
import dotenv 

from person import objects as persons
from person._types import TextModel

dotenv.load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PROXY_URL = os.getenv("PROXY_URL")
TTS_TOKEN = os.getenv("TTS_TOKEN")
DONATION_ID = os.getenv("DONATION_ID")
DONATION_SECRET = os.getenv("DONATION_SECRET")
STREAM_KEY = os.getenv("STREAM_KEY")
STREAM_URL = os.getenv("STREAM_URL")

MAIN_DIR = os.getcwd() + "/"
ASSETS_DIR = "assets/"
UPLOAD_DIR = "upload/"

AUDIO_DIR = UPLOAD_DIR + "audio/"
RESULT_DIR = UPLOAD_DIR + "video/result/"
IN_PROCESS_DIR = UPLOAD_DIR + "video/in_process/"

MAIN_FONT_PATH = ASSETS_DIR + "font/FulboArgenta.ttf"
INFO_PATH = "info.json"

TEXT_MODEL = TextModel.LARGE.value 

PERSON_1 = persons.MaxMaxbetov
PERSON_2 = persons.SaveliiJournalistov
WIPE_PERSON_MEMORY_AFTER = 10

DB_CONNECTION_URL = "sqlite+aiosqlite:///db.sqlite"
ECHO = False  

FPS = 10
TEMPERATURE = 0.5 