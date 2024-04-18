from telegram.ext import filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, Application, ContextTypes, MessageHandler, CallbackQueryHandler
import os
import requests


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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


async def choose_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channels = get_discord_channels()
    reply_markup = build_channel_menu(channels)
    await update.message.reply_text('Выберите канал для отправки:', reply_markup=reply_markup)


async def handle_channel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    channel_id = query.data.split('_')[1]
    url = 'http://localhost:5000/set_channel'
    data = {'channel_id': int(channel_id)}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        await query.edit_message_text(text=f"Канал успешно обновлен")
    else:
        await query.edit_message_text(text="Ошибка при обновлении канала.")


def get_discord_channels():
    url = 'http://localhost:5000/get_channels'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['channels']
    else:
        print(f"Failed to get channels: {response.status_code}")
        return []


def build_channel_menu(channels):
    keyboard = [[InlineKeyboardButton(channel['name'], callback_data=f"sendto_{channel['id']}")] for channel in
                channels]
    return InlineKeyboardMarkup(keyboard)


telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'

application = Application.builder().token(telegram_token).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("choose_channel", choose_channel))
application.add_handler(CallbackQueryHandler(handle_channel_callback, pattern='^sendto_'))
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

if __name__ == '__main__':
    application.run_polling()
