#Bot Details - Sensitive Data

api_id = "User Telegram API"
api_hash = "User Telegram Hash"
downloader_bot_api = "User Telegram Downloader Bot API"
bot_test_api = "User Telegram API" # Optional

##Usernames

client_username = "User Telegram Username"
downloader_bot_username = "User Telegram Downloader Bot Username"
test_bot_username = "User Telegram Test Bot Username" # Optional

##Chat Names (Optional - If not used, remove the functions from telegrambot.py)

album_chats = ["username1","username1","username1"] # Usernames of chats from which albums can be forwarded
forward_chat = "useranme_of_group/channel" # Username of group/channel where to forward the albums from above chats

##Personal Array (Optional)

classic_array = ["option1","option2","option3"] # Classic Array for extra options to be used for user defined logic

##Personal Keyboard (Optional - To be used if above classic array is used)
from telethon import Button
async def classic_keyboard_fn(event):
    classic_keyboard = [ [Button.inline('OP1', data=f'OP1_{event.query.data}'), Button.inline('OP2', data=f'OP2_{event.query.data}'), Button.inline('OP3', data=f'OP3_{event.query.data}')]]
    return classic_keyboard