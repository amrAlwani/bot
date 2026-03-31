import os
from dotenv import load_dotenv

load_dotenv()

MAIN_BOT_TOKEN = os.environ.get("MAIN_BOT_TOKEN", "")
MAIN_BOT_ADMIN = int(os.environ.get("MAIN_BOT_ADMIN", "0"))
DB_PATH = os.environ.get("DB_PATH", "menubuilder.db")
MAX_BOTS_PER_USER = int(os.environ.get("MAX_BOTS_PER_USER", "5"))
MAIL_DELAY = float(os.environ.get("MAIL_DELAY", "0.05"))
