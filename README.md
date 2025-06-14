# Plugins Dev Bot

Bot for selling ready-made plugins for minecraft servers, as well as for ordering your own unique plugins at the user's request

## Platforms supported
✅ Telegram (aiogram)
<br>
❌ VK

## Abstractness
The code is written in such a style that at any time it would be easy to implement another platform for the bot to work on

## Running
1. Install poetry
```
pip install poetry
```
2. Install project
```
poetry install
```
3. Register on YooMoney, do a verification
4. Fill `.env` file:
```env
TOKEN=your telegram token
YOOMONEY_WALLET=your telegram wallet
YOOMONEY_SECRET=your yoomoney notification secret
```
5. Start the bot
```
poetry run python src/main.py
```
