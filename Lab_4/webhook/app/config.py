import os


BOT_TOKEN = os.getenv("BOT_TOKEN", "1985406226:AATk2MB7fzbuJBCfZxOXqoylpBmONG_9KyU")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://b63b-37-215-55-53.ngrok.io")
URL_WEB = os.getenv("URL_WEB", "https://e955-37-215-55-53.ngrok.io")
TELEGRAM_URL = "https://api.telegram.org"
DATA = {"url": WEBHOOK_URL}
SET_WEBHOOK_URL = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/setWebhook"
BOT_URL = f"{TELEGRAM_URL}/bot{BOT_TOKEN}/"
