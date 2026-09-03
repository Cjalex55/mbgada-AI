from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import os
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # e.g., https://your-app.onrender.com

# /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Base bot active. Ready to build. 🚀")

# Chat handler: Echoes back whatever you type
async def echo_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply_text = f"Bot received: {user_text} ✅ (Connection is working!)"
    await update.message.reply_text(reply_text)

# Build app and register behaviors
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_chat))

# Flask webhook endpoint
@flask_app.route('/', methods=['GET'])
def index():
    return "Bot is running ✅", 200

@flask_app.route('/webhook', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), app.bot)
    await app.process_update(update)
    return "OK", 200

if __name__ == "__main__":
    # Initialize bot
    asyncio.run(app.initialize())
    
    if WEBHOOK_URL:
        asyncio.run(app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook"))
        logger.info(f"✅ Webhook set to: {WEBHOOK_URL}/webhook")
    
    # Start Flask server on Render's PORT
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🚀 Starting Flask server on port {port}")
    flask_app.run(host="0.0.0.0", port=port, debug=False)
