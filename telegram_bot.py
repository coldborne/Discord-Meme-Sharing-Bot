from telegram.ext import filters
from telegram import Update
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler
import os
import requests


async def start(update: Update):
    await update.message.reply_text("Привет! Я бот для пересылки мемов в Discord. Отправьте мем, и я перешлю его.")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file_id = photo.file_id

    file_path = f"downloads/{file_id}.jpg"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    file = await context.bot.get_file(file_id)

    path = await file.download_to_drive(custom_path=file_path)

    await send_photo_to_discord(path)


async def send_photo_to_discord(file_path):
    url = 'http://localhost:5000/send_photo'
    data = {'file_path': str(file_path)}

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()

        if response.status_code == 200:
            print("Изображение успешно отправлено в Discord.")
        else:
            print("Не удалось отправить изображение в Discord.")
    except requests.exceptions.RequestException as exception:
        print(f"Ошибка при отправке изображения: {exception}")


telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'

application = Application.builder().token(telegram_token).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == '__main__':
    application.run_polling()
