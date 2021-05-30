# Telegram-Bot

# Description:
This program is specifically used to download media to the computer folder where this program is installed. It can be moidifed to save the media in specific folder which user wants to.
Once this program is started the downloader bot is the chat where we need to forward any media which needs to be dowloaded. As soon as you forward the message, bot will give you the option to download it.

# YouTube links:
Youtube links can directly be used to either save the link as video or audio. Once you share the link in this bot, it will ask you the relevant options.

# Pre-requisites:
- Downloader Bot needs to be created before using this code
- Another Test Bot (optional) to be used for testing certain codes. It can be ignored. If not used, make sure to comment the test bot functions from telegrambot.py file.

# Library Dependencies: 
- telethon (pip install telethon)
- asyncio
- time
- datetime
- pytube (pip install pytube)
- ffmpeg((pip install ffmpeg)
- sys
- os
- re
- logging (optional)
- cryptg (pip install cryptg)

# Notes: 

- Installing cryptg will increase the download speed significantly and is recommended.
- userdata-dummy.py is the dummy file for the actual userdata.py file that should be customized based on personal data. Use the dummy file to build your own userdata.py file

# Userdata_Dummy.py Explained:

### Please rename the file to userdata.py once the file has been edited with personal data.

#Bot Details - Sensitive Data

api_id = "_User Telegram API_"

api_hash = "_User Telegram Hash_"

downloader_bot_api = "_User Telegram Downloader Bot API_" 

bot_test_api = "_User Telegram API_" _# Optional_

##Usernames

client_username = "_User Telegram Username_"

downloader_bot_username = "_User Telegram Downloader Bot Username_"

test_bot_username = "_User Telegram Test Bot Username_" _# Optional_

##Chat Names (Optional - If not used, remove the functions from telegrambot.py) 

album_chats = _["username1","username1","username1"]  # Usernames of chats from which albums can be forwarded_

forward_chat = _"useranme_of_group/channel"  # Username of group/channel where to forward the albums from above chats_


##Personal Array (Optional)

classic_array = _["option1","option2","option3"]  # Classic Array for extra options to be used for user defined logic_

##Personal Keyboard (Optional - To be used if above classic array is used)

from telethon import Button
async def classic_keyboard_fn(event):
    classic_keyboard = [
        [Button.inline('OP1', data=f'OP1_{event.query.data}'), Button.inline('OP2', data=f'OP2_{event.query.data}'),
         Button.inline('OP3', data=f'OP3_{event.query.data}')]]
    return classic_keyboard
    
   
