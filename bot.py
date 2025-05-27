import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

logging.basicConfig(level=logging.INFO)

async def forward_to_webhook(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        payload = {
            'user_id': update.effective_user.id,
            'username': update.effective_user.username,
            'text': update.message.text,
        }

        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            logging.info("Forwarded to webhook: %s", response.status_code)
        except Exception as e:
            logging.error("Error sending to webhook: %s", e)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_webhook))

if __name__ == '__main__':
    app.run_polling()
