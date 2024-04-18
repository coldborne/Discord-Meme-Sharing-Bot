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


@flask_application.route('/get_channels', methods=['GET'])
def get_channels():
    guild = client.get_guild(discord_server_id)

    if not guild:
        return {"error": "Guild not found"}, 404

    channels = [{"id": channel.id, "name": channel.name} for channel in guild.text_channels]
    return {"channels": channels}, 200


@flask_application.route('/set_channel', methods=['POST'])
def set_channel():
    data = request.json
    global discord_channel_id
    discord_channel_id = data['channel_id']
    return {"message": "Channel updated"}, 200


async def send_photo_to_discord(file_path):
    channel = client.get_channel(discord_channel_id)

    if channel is None:
        print(f"Канал с ID {discord_channel_id} не найден.")
        return

    file: BinaryIO
    with open(file_path, 'rb') as file:
        await channel.send(file=discord.File(file))


discord_token = 'YOUR_DISCORD_APPLICATION_TOKEN'
discord_server_id = 12345
discord_channel_id = 12345

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
