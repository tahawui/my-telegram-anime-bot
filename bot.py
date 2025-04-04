import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_KEY")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحباً بك! أرسل لي صورة وسأحولها إلى أنمي.")

def image_handler(update: Update, context: CallbackContext):
    photo_file = update.message.photo[-1].get_file()
    photo_url = photo_file.file_path

    update.message.reply_text("⏳...جاري تحويل الصورة إلى أنمي")

    output_url = convert_to_anime(photo_url)
    if output_url:
        update.message.reply_photo(photo=output_url)
    else:
        update.message.reply_text("حدث خطأ أثناء تحويل الصورة. حاول مرة أخرى.")

def convert_to_anime(image_url):
    try:
        url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "version": "c76b7dbb6e6c49bba215d37a210e5f3dbd7d54c8a7dbf9f1c2f3b8fe4730d6f5",
            "input": {"image": image_url}
        }
        response = requests.post(url, headers=headers, json=data).json()
        return response["urls"]["get"].replace("/predictions/", "/predictions/") + "/output"
    except:
        return None

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, image_handler))
updater.start_polling()
updater.idle()