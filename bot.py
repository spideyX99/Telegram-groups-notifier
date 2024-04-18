import logging
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


CHAT_IDS_FILE = "chat_ids.json"

# Function to load chat IDs from file
def load_chat_ids():
    try:
        with open(CHAT_IDS_FILE, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()

# Function to save chat IDs to file
def save_chat_ids(chat_ids):
    with open(CHAT_IDS_FILE, "w") as file:
        json.dump(list(chat_ids), file)

async def handle_new_chat_members(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    chat_ids = load_chat_ids()
    chat_ids.add(chat_id)
    save_chat_ids(chat_ids)
    if update.message:
        await update.message.reply_text("Thanks for adding me to this group!")
    else:
        logger.warning("No message received for new chat members.")

async def send_notification(update: Update, context: CallbackContext):
    message = "Hello Groups"
    chat_ids = load_chat_ids()
    for chat_id in chat_ids:
        try:
            await context.bot.send_message(chat_id, message)
        except Exception as e:
            logger.error(f"Failed to send message to chat {chat_id}: {e}")


# Initialize the application
application = Application.builder().token("Your Bot Token").build()

# Add command handlers
application.add_handler(CommandHandler("start", handle_new_chat_members))
application.add_handler(CommandHandler("send", send_notification))

# Start the bot
application.run_polling(allowed_updates=Update.ALL_TYPES)
