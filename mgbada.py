from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = '8756735194:AAFN1hKux62C_984Z_y1IfzujV8wu2DDcFs'

# Step 1: The Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Base bot active. Ready to build.")

# Step 2: Initialize & Launch
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot starting up...")
app.run_polling()
