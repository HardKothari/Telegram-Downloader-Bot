import datetime
import logging
from telethon import TelegramClient, events, sync, utils, functions, types, helpers, errors, Button
from telethon.tl.types import InputMessagesFilterPhotos
import asyncio
#import cryptg
import time
from datetime import datetime, date, timezone, timedelta
from FastTelethon import download_file, upload_file
from pytube import YouTube
from functions import identify_message, message_details, file_details, get_all_chats, get_all_messages_with_text, get_all_filters, get_all_messages_filter, guided_download_fn, all_download_fn, youtube_Downloader,\
    all_download_fn_new, get_all_messages_date, download_all_messages_new, direct_downloads_fn, direct_links_downloads_fn, get_all_messages_with_text, get_all_chats_keyboard
import ffmpeg
from userdata import api_id, api_hash, bot_test_api, downloader_bot_api, client_username , downloader_bot_username, test_bot_username, forward_chat, album_chats,classic_keyboard_fn, classic_array,\
    download_chats, codex_chat
import sys, os, re


#Enabling Logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# Initializing the download paths where program will download the media. Please use the path based on your computer directory wher
# Generic Download Path. Below is the folder that will be used to download and create sub folders. This path can be edited as required.
# main_download_path = 'D:\\Telegram\\' ## Windows Path
main_download_path = "/Volumes/Hard 2TB/Telegram/"  ##Mac OS Path
# Download path for YoutTube Links as Audio
# audio_download_path = 'D:\\Telegram\\Normal\\audio\\'
# Download path for YoutTube Links as Video
# video_downlad_path = 'D:\\Telegram\\Normal\\video\\'
# Download path for Other Userdefined Downloads and Options
# classic_downlad_path = 'D:\\Telegram\\Classic\\'

#Intializing Client (Owner) and Bots
client = TelegramClient(client_username, api_id, api_hash) # Client/User Initialize
downloader_bot = TelegramClient(downloader_bot_username, api_id, api_hash).start(bot_token=downloader_bot_api) # Downloader Bot Initialize
test_bot = TelegramClient(test_bot_username, api_id, api_hash).start(bot_token=bot_test_api) # Test Bot Initialize (Optional - 1)
download_extensions = [".mkv", ".mp4", ".avi", ".zip", ".tar", ".rar"]

# Intiailizing arrays to store messages for downloading
messages_array = []
messages_downloader_bot_array = []

# This can be used as main function. But currently its only used to log in console the chat in which new message arrives.
async def main():
    #await all_download_fn(event)
    pass

#New Mesage Event for Client. Any new message to client will trigger this event function
@client.on(events.NewMessage())
async def client_newmessage_handler(event):
    await message_details(event)

    if "/downloadall" in (event.message.message):
        # await all_download_fn(event, client)
        # await all_download_fn_new(event, client)
        pass

#New Mesage Event for Downloader Bot. Any new message to downloader bot will trigger this event function
@downloader_bot.on(events.NewMessage())
async def downloader_bot_newmessage_handler(event):
    try:
        # Below line of code is used to test code, can be commented in live run
        #file_details(event.message)
        #print(event.message)


        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        chat_username = event.chat.username
        sender_id = event.sender_id
        type = identify_message(event.message)


        # YouTube Keyboard
        YouTube_keyboard = [[Button.inline('Download as Video', data=f'YTVideo_{event.message.id}'),
                         Button.inline('Download as Audio', data=f'YTAudio_{event.message.id}')],
                        [Button.inline('DND', data=f'DND_{event.message.id}')]]

        # Telegram Media Download Keyboard
        Download_Keyboard = [[Button.inline('Normal', data=f'Norm_{event.message.id}'), Button.inline('Classic', data=f'Class_{event.message.id}')],
                              [Button.inline('DND', data=f'DND_{event.message.id}')]]

        # Codex Group External Link Download Keyboard
        Download_Index_Keyboard = [[Button.inline('Yes', data=f'YDirect_{event.message.id}')],
                              [Button.inline('DND', data=f'DND_{event.message.id}')]]

        # Codex Group Multiple External Links Download Keyboard
        Download_Index_Links_Keyboard = [[Button.inline('Yes', data=f'YDirectLinks_{event.message.id}')],
                              [Button.inline('DND', data=f'DND_{event.message.id}')]]
        
        if "/getchatId" in (event.message.message):
            print(event.message)
            #textsearch = f"textsearch | {event.message.message[14:]}"
            await get_all_chats_keyboard(event, client, callback_text = "getchatId")

        if "/textsearch" in (event.message.message):
            date = datetime.now()
            msg = str(event.message.message)
            chatid = int(msg.split(" ")[1])
            text = msg.split(" ",2)[2]

            print(f"Inside textsearch function with ChatId: {str(chatid)} and text: {text}")

            all_messages = await get_all_messages_with_text(client,chat_id = str(chatid),text=text)
            # all_messages = await get_all_messages_date(client, chatid, date, 'photo', main_download_path)
            #print(all_messages)
            for msg in all_messages:
                try:
                    message = msg["message"]
                    print(msg["message"])
                    # await client.send_message(entity=downloader_bot_username, message=message["message"])
                    file_name = message.file.name if message.file is not None else "NoFileName"
                    type = identify_message(message)

                    path = await message.download_media(f'{main_download_path}Normal/{type}/{file_name}')
                    print('\nFile saved to', path)

                except Exception as e:
                    print("Error Generated in TextSearch Message Send Event!!")
                    print(str(e))



        if "/downloadall" in (event.message.message):
            # await all_download_fn(event, client)
            # await all_download_fn_new(event, client)
            await get_all_chats_keyboard(event, client, callback_text="DOWNLOADALL")


        if "/olddownloadall" in (event.message.message):
            # await all_download_fn(event, client)
            await all_download_fn(event, client)
        # If message is webpage and link is YouTube, then give an option to download as Audio or Video
        if type in ("webpage"):
            # print(event.message.message)
            url = str(event.message.message)
            messages_downloader_bot_array.append(event.message)
            if 'youtu' in url:
                await event.reply("Test", buttons=YouTube_keyboard)
            elif any(ext in event.message.message for ext in download_extensions) and 'http' in url:
                print(event.message.message)
                print("Direct Download Link!!!!")
                await event.reply("Donwloading the file now!!")
                download_path = f"{main_download_path}"
                await direct_links_downloads_fn(event.message.message, download_path, download_extensions)
                await event.delete()

        # If message is media, then give an option to download as Normal or Classic
        if type in ("photo", "video", "contact", "audio", "document", "gif"):
            print("Inside Download Choose Function!!")
            messages_downloader_bot_array.append(event.message)
            await event.reply("Test", buttons=Download_Keyboard)


        try:
            # Below code block is only for codex messages from codex group
            print(event.message.reply_markup.rows[0])
            if 'Index' in event.message.reply_markup.rows[0].buttons[1].text:
                index_download_url = event.message.reply_markup.rows[0].buttons[1].url
            print("Inside Download Index link!!")
            #download_extensions = [".mkv",".mp4",".avi",".zip",".tar",".rar"]
            if any(ext in  index_download_url for ext in download_extensions):
              messages_downloader_bot_array.append(event.message)
              await event.reply("Donwload?", buttons=Download_Index_Keyboard)
            else:
                messages_downloader_bot_array.append(event.message)
                await event.reply("Donwload all Links?", buttons=Download_Index_Links_Keyboard)
        except:
            try:
                if 'codexcloud.me' in str(event.message):
                    print(event.message.message)
                    print("Cloudx Link!!!!")
                    download_path = f"{main_download_path}"
                    await direct_links_downloads_fn(event.message.message, download_path, download_extensions)
                    await event.delete()
            except:
                print("Error in downloading direct link file...!!!")

    except errors.FloodWaitError as e:
        print('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)
    except NameError as e:
        print(f"Error Occured: {e}")
    except Exception as e:
        print("Error Generated in Downloader_Bot New Message Event!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))


# Downloader Bot Button Callback. Button callbacks response for downloader bot.
@downloader_bot.on(events.CallbackQuery())
async  def downloader_bot_callback_handler(event):
    print("Inside Download Bot - Button Callback!!")

    chat = await event.get_chat()
    # sender = await event.get_sender()
    # chat_id = event.chat_id
    # chat_username = event.chat.username
    # sender_id = event.sender_id
    # type = identify_message(event.message)
    print(f'\nCallback Query Data: {event.query.data}')
    split = str(event.query.data).replace("b'","").replace("b","").replace('"','').replace("'","").split("_")[0]
    print(f'SPLIT: {split}')
    print(f'\nMessages in Array before download: {len(messages_downloader_bot_array)}')

    # Classic Keyboard - Defined based on personal userdata file
    classic_keyboard = await classic_keyboard_fn(event)

    # Block to get the ID of a chat
    try:
        if "getchatId" in str(event.query.data):
            chatid = int(split[:-10]) # -1001277402899
            # chatid = int(split.split("|")[0])
            # chatname = int(split.split("|")[1])
            # print(f'\n{date}')
            print(f'CallbackData: {event.query.data} | ChatId:{chatid}')
            await downloader_bot.send_message(chat, str(chatid))
            # await get_all_messages_date(client, chatid , date, 'photovideo',main_download_path )
            await event.delete()
    except Exception as e:
        print("Inside getchatId Callback Option!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))

    try:
        if "YTVideo_" in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                   link = iter.message
                   url = YouTube(str(link))
                   # print(f"URL: {url.title}")
                   title = re.sub('[^0-9a-zA-Z.]+', '_', url.title)# str(url.title).replace(" ","_").replace("|","").replace(",","").replace(".","").replace("★","")
                   await youtube_Downloader(link, title, main_download_path)
                   await event.delete()
                   await downloader_bot.delete_messages(entity=None, message_ids=iter)
                   messages_downloader_bot_array.remove(iter)
    except Exception as e:
        print("Inside YTVideo Callback Option!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))

    try:
        if "YTAudio_" in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                   link = iter.message
                   # print(link)
                   url = YouTube(str(link))
                   title = re.sub('[^0-9a-zA-Z.]+', '_', url.title)# str(url.title).replace(" ","_").replace("|","").replace(",","").replace(".","").replace("★","")
                   # print(f"Title: {title}")
                   await youtube_Downloader(link, title, main_download_path, vid=False)
                   await event.delete()
                   await downloader_bot.delete_messages(entity=None, message_ids=iter)
                   messages_downloader_bot_array.remove(iter)

    except Exception as e:
        print("Inside YTAudio Callback Option!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))

    try:
        if 'DND' in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    await event.delete()
                    await downloader_bot.delete_messages(entity=None, message_ids=iter)
                    messages_downloader_bot_array.remove(iter)
        elif 'YDirect_' in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    link = str(iter.reply_markup.rows[0].buttons[1].url)
                    print(link)
                    download_path = f"{main_download_path}"
                    await direct_downloads_fn(link, download_path)
                    await event.delete()
                    await downloader_bot.delete_messages(entity=None, message_ids=iter)
                    messages_downloader_bot_array.remove(iter)

        elif 'YDirectLinks_' in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    link = str(iter.reply_markup.rows[0].buttons[1].url)
                    print(link)
                    download_path = f"{main_download_path}"
                    await direct_links_downloads_fn(link, download_path, download_extensions)
                    await event.delete()
                    await downloader_bot.delete_messages(entity=None, message_ids=iter)
                    messages_downloader_bot_array.remove(iter)

        elif 'Norm' in str(event.query.data):
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    download_path = f"{main_download_path}Normal/"
                    type = identify_message(iter)
                    if (iter.file.size /  1000000) < 20480:
                        await guided_download_fn(event, iter, download_path, downloader_bot)
                    else:
                        pass
                        # print("Inside NORMAL Large file download Function")
                        # print(iter)
                        # print(iter.id)
                        # msg = await client.get_messages('downloader_bot',ids=iter.id)
                        # print(msg)
                        # file_name = iter.media.document.attributes[1].file_name
                        # with open(f'{download_path}{type}/{file_name}', 'wb') as fd:
                        #     async for chunk in downloader_bot.iter_download(iter.media):
                        #         fd.write(chunk)
                    await event.delete()
                    await downloader_bot.delete_messages(entity=None, message_ids=iter)
                    messages_downloader_bot_array.remove(iter)

        # Below 2 conditions are based on personal usage to download files in different folders based on requirements. Can be skipped and removed.
        elif split == 'Class':
            for iter in messages_downloader_bot_array:
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    await downloader_bot.send_message(chat,'Please select the folder to download the file:', reply_to=iter, buttons=classic_keyboard)
            await event.delete()

        elif split in classic_array:
            for iter in messages_downloader_bot_array:
                print(event.query.data)
                print(iter.id)
                if str(iter.id) in str(event.query.data):
                    print(iter)
                    download_path = f"{main_download_path}Classic/{split}/"
                    await guided_download_fn(event, iter, download_path, client)
                    await event.delete()
                    await downloader_bot.delete_messages(entity=None, message_ids=iter)
                    messages_downloader_bot_array.remove(iter)

    except Exception as e:
        print("Inside Download Callback Option for Normal or Classic!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))

    try:
        date = datetime.now()
        if str(event.query.data)[-12:][:-1] == 'DOWNLOADALL':
            chatid = int(split[:-12]) # -1001277402899
            # chatid = int(split.split("|")[0])
            # chatname = int(split.split("|")[1])
            # print(f'\n{date}')
            print(f'CallbackData: {event.query.data} | ChatId:{chatid}')
            kb = [[Button.inline('Photos', data = f'{chatid}|allphoto'), Button.inline('Videos', data = f'{chatid}|allvideo')],
                  [Button.inline('Audio', data=f'{chatid}|allaudio'), Button.inline('Gifs', data=f'{chatid}|allgif')],
                  [Button.inline('Documents', data=f'{chatid}|alldocument'), Button.inline('Everything', data=f'{chatid}|allall') ]]
            await downloader_bot.send_message(chat, "Select the type of data to download for chat!!", buttons=kb)
            # await get_all_messages_date(client, chatid , date, 'photovideo',main_download_path )
            await event.delete()
        elif str(event.query.data)[-9:][:-1] == 'allphoto':
            print(str(event.query.data)[-9:][:-1])
            chatid = int(split[:-9])
            all_messages = await get_all_messages_date(client, chatid, date, 'photo', main_download_path)
            print(chatid)
            print(f"Total Messages: {len(all_messages)} in ChatId: {chatid}")
            # await download_all_messages_new(client, chatid, all_messages, main_download_path, 'photo')
            await event.delete()
        elif str(event.query.data)[-9:][:-1] == 'allvideo':
            print(str(event.query.data)[-9:][:-1])
            chatid = int(split[:-9])
            all_messages = await get_all_messages_date(client, chatid, date, 'video', main_download_path)
            await download_all_messages_new(client, chatid, all_messages, main_download_path, 'video')
            await event.delete()
        elif str(event.query.data)[-9:][:-1] == 'allaudio':
            print(str(event.query.data)[-9:][:-1])
            chatid = int(split[:-9])
            all_messages = await get_all_messages_date(client, chatid, date, 'audio', main_download_path)
            await download_all_messages_new(client, chatid, all_messages, main_download_path, 'audio')
            await event.delete()
        elif str(event.query.data)[-7:][:-1] == 'allgif':
            print(str(event.query.data)[-7:][:-1])
            chatid = int(split[:-7])
            all_messages = await get_all_messages_date(client, chatid, date, 'gif', main_download_path)
            await download_all_messages_new(client, chatid, all_messages, main_download_path, 'gif')
            await event.delete()
        elif str(event.query.data)[-12:][:-1] == 'alldocument':
            print(str(event.query.data)[-12:][:-1])
            chatid = int(split[:-12])
            all_messages = await get_all_messages_date(client, chatid, date, 'document', main_download_path)
            await download_all_messages_new(client, chatid, all_messages, main_download_path, 'document')
            await event.delete()
        elif str(event.query.data)[-7:][:-1] == 'allall':
            print(f'Callback: {str(event.query.data)[-12:][:-1]}')
            chatid = int(split[:-12])
            print("Getting all the messages!!")
            all_messages = await get_all_messages_date(client, chatid, date, 'allall', main_download_path)
            print("Downloading all the messages!!")
            await download_all_messages_new(client, chatid, all_messages, main_download_path, 'allall')
            await event.delete()
        else:
            # Add the logic to warn the user with some warning/error
            print(str(event.query.data))
            await event.delete()

    except Exception as e:
        print("Inside Download Callback Option for Download All!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))


# Button Callback for Test Bot. (Optional - 1)
@test_bot.on(events.CallbackQuery())
async  def test_bot_callback_handler(event):
    pass

# New Message Event for Test Bot. (Optional - 1)
@test_bot.on(events.NewMessage())
async def test_bot_newmessage_handler(event):
    pass

# # Any album in album_chat Channels/Groups will forward the album to my fowrward_chat Channel. (Optional - 2)
# @client.on(events.Album(chats=album_chats))
# async def client_album_handler(event):
#     try:
#         #print(event.grouped_id)
#         #print(f'I am into BOT Album event')
#         #print(f'Length of EVENT: {len(event)}')
#         #print("==========================")
#         #print(event.messages)
#         await client.send_file(entity=forward_chat, file=event.messages, caption=event.text)
#
#     except Exception as e:
#         print("Error Generated in Aliexpress Album New Message Event!!")
#         print(str(e))
#
# # Any message in album_chat Channels/Groups will forward the album to my fowrward_chat Channel. (Optional - 2)
# @client.on(events.NewMessage(chats=album_chats))
# async def client_newmessage_handler(event):
#     try:
#         if event.grouped_id:
#             pass
#         else:
#             await client.send_message(entity=forward_chat, message=event.message)
#     except Exception as e:
#         print("Error Generated in Aliexpress New Message Event!!")
#         print(str(e))
#
#
# # Any message in Channels/Groups will forward to my downloader BOT. (Optional - 2)
# @client.on(events.NewMessage(chats=download_chats))
# async def client_newmessage_handler(event):
#     try:
#         await client.send_message(entity=downloader_bot_username, message=event.message)
#     except Exception as e:
#         print("Error Generated in MK Archives New Message Event!!")
#         print(str(e))
#
# Any message in codex chat will forwarded to my downloader BOT. (Optional - 2)
@client.on(events.NewMessage(chats=codex_chat))
async def client_newmessage_handler(event):
    try:
        await client.send_message(entity=downloader_bot_username, message=event.message)
    except Exception as e:
        print("Error Generated in Codex Chat New Message Event!!")
        print(str(e))

# Any message in codex chat will forwarded to my downloader BOT. (Optional - 2)
@client.on(events.NewMessage(chats="hard_test_bot"))
async def client_newmessage_handler(event):
    try:
        pass
        # print("In the TEST BOT Chat New Message Event!!")
        # # await message_details(event)
        # print(event.message.media)
        # print(event.message.media.document.attributes[1].file_name)
        # file_name = event.message.media.document.attributes[1].file_name
        # # Streaming `media` to an output file
        # # After the iteration ends, the sender is cleaned up
        # with open(file_name, 'wb') as fd:
        #     async for chunk in client.iter_download(event.message.media):
        #         fd.write(chunk)

    except Exception as e:
        print("Error Generated in TEST BOT Chat New Message Event!!")
        print(str(e))

print('Telegram is staring ... !!!!')
#Client Start
client.start()
print('\nTelegram has started ... !!!!')
# Run the loop until program is disconnected..!!
client.run_until_disconnected()
