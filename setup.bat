@echo off
set /p TELEGRAM_TOKEN=Enter your Telegram bot token: 

echo Telegram bot token: %TELEGRAM_TOKEN%

echo %TELEGRAM_TOKEN% > resources/telegram_token.txt

python -m venv myenv

call myenv\Scripts\activate

pip install torch
pip install transformers
pip install telebot
pip install pandas

python install_neural_network_model.py