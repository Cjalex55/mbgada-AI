from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import http.server
import threading

# 1. Background web server for Render's free port check
def run_fake_server():
    server_address = ('', int(os.environ.get("PORT", 8080)))
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_fake_server, daemon=True).start()

# 2. Telegram Bot Configuration
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")

# /start command response
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Base bot active. Ready to build.")

# Chat handler: Echoes back whatever you type
async def echo_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply_text = f"Bot received: {user_text} ✅ (Connection is working!)"
    await update.message.reply_text(reply_text)

# Build app and register behaviors
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# This line listens for any normal text messages that aren't commands
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_chat))

print("Bot starting up...")
app.run_polling()
