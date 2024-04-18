import multiprocessing
import os


def run_telegram_bot():
    os.system("python telegram_bot.py")


def run_discord_bot():
    os.system("python discord_bot.py")


if __name__ == '__main__':
    telegram_process = multiprocessing.Process(target=run_telegram_bot)
    discord_process = multiprocessing.Process(target=run_discord_bot)

    telegram_process.start()
    discord_process.start()

    telegram_process.join()
    discord_process.join()
