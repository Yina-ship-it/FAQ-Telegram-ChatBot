from telegram_bot import TelegramBot

def main():
    telegram_token = get_telegram_token()

    bot = TelegramBot(telegram_token)
    bot.setup()
    bot.start() 

def get_telegram_token():
    try:
        with open("/resources/telegram_token.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print("Telegram token file not found. Make sure to run setup.bat first.")
        exit(1)

if __name__ == "__main__":
	main()