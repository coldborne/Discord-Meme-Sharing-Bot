import asyncio
from typing import BinaryIO
from flask import Flask, request
import threading
import discord

flask_application = Flask(__name__)


@flask_application.route('/send_photo', methods=['POST'])
def handle_send_photo():
    data = request.json
    file_path = data['file_path']
    asyncio.run_coroutine_threadsafe(send_photo_to_discord(file_path), client.loop)
    return '', 200


async def send_photo_to_discord(file_path):
    channel = client.get_channel(discord_channel_id)

    if channel is None:
        print(f"Канал с ID {discord_channel_id} не найден.")
        return

    file: BinaryIO
    with open(file_path, 'rb') as file:
        await channel.send(file=discord.File(file))


discord_token = 'YOUR_DISCORD_APPLICATION_TOKEN'
discord_channel_id = 12345  # id channel for posting

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} (ID: {client.user.id})')
    print('------')


def run_discord_bot():
    client.run(discord_token)


def run_flask_app():
    flask_application.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    run_discord_bot()
