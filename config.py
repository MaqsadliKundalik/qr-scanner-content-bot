from dotenv import load_dotenv
from os import getenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")
ADMINS = list(map(int, getenv("ADMINS", "").split(",")))