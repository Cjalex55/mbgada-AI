from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request
import os
import logging
import asyncio
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
flask_app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # e.g., https://your-app.onrender.com
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot active with Gemini AI!\n\nJust type a message and I'll respond with AI-powered answers.")

# Chat handler: Send to Gemini and reply
async def echo_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # Show typing indicator
    await update.message.chat.send_action("typing")
    
    try:
        # Get response from Gemini
        response = model.generate_content(user_text)
        reply_text = response.text
        
        # Split long messages (Telegram has 4096 char limit)
        if len(reply_text) > 4096:
            for i in range(0, len(reply_text), 4096):
                await update.message.reply_text(reply_text[i:i+4096])
        else:
            await update.message.reply_text(reply_text)
            
    except Exception as e:
        logger.error(f"Error calling Gemini: {str(e)}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

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
