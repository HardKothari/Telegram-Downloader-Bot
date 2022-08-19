from FastTelethon import download_file, upload_file
from telethon import TelegramClient, events, sync, utils, functions, types, helpers, errors, Button
from telethon.tl.types import InputMessagesFilterPhotos, InputMessagesFilterVideo, InputMessagesFilterGif, InputMessagesFilterMusic, InputMessagesFilterDocument , InputMessagesFilterPhotoVideo
import sys, os, re
from pytube import YouTube
import datetime
import requests
from userdata import album_chats
from bs4 import BeautifulSoup
from selenium import  webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from datetime import time

# Intialize this to test some functions or debugging the code. Don't touch it if you are not aware of the code below.
trial=False

# identifying the type of message. Based on this identification folders are created in the download path.
def identify_message(message):
    if str(message.media) == 'None':
        return "text"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaPhoto":
        return "photo"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaWebPage":
        return  "webpage"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaPoll":
        return  "poll"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaGeo":
        return  "location"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaContact":
        return  "contact"
    elif str(message.media)[:str(message.media).index("(")] == "MessageMediaDocument":
        if 'gif' in str(utils.get_extension(message.file)):
            return "gif"
        elif str(message.file.mime_type)[:str(message.file.mime_type).index("/")] == 'video':
            return "video"
        elif str(message.file.mime_type)[:str(message.file.mime_type).index("/")] == 'audio':
            return "audio"
        else:
            return "document"
    else:
        return "unknown"


# Identifying the file details for the message recieved.
def file_details(message):
    print(f'file duration:  {message.file.duration}s')
    print(f'file emoji:     {message.file.emoji}')
    print(f'file ext:       {message.file.ext}')
    print(f'file height:    {message.file.height}')
    print(f'file id:        {message.file.id}')
    print(f'file mime_type: {message.file.mime_type}')
    print(f'file Name:      {message.file.name}')
    print(f'file performer: {message.file.performer}')
    print(f'file Size:      {float(message.file.size) / 1000000} Mb')
    print(f'file StickerSet:{message.file.sticker_set}')
    print(f'file title:     {message.file.title}')
    print(f'file width:     {message.file.width}')
    print(f'Is File GIF:     {utils.is_gif(message.file)}')
    print(f'File Attributes:     {utils.get_attributes(message.file)}')
    print(f'File Extension:     {utils.get_extension(message.file)}')


# List of all current chats with indexing
async def get_all_chats(client):
    all_chats = []
    y = 0
    async for dialog in client.iter_dialogs():
        all_chats.append({"sr": y + 1,"title": dialog.title, "userid": dialog.id, "is_user": dialog.is_user, "title": dialog.title})
        y = y + 1
    return all_chats


# list of all messages with indexing
async def get_all_messages(chat_id, minimum, maximum):
    c = 0
    all_messages = []

    # async for messages in client.iter_messages(chat_id, wait_time = 5):
    #     c = c + 1
    #     if c >= minimum and c <= maximum:
    #         all_messages.append({"sr": c, "message": messages})
    #     elif c < minimum:
    #         pass
    #     else:
    #         break
    # return all_messages


# Get all messages from specific date
async def get_all_messages_date(client, chat_id, date, type, main_download_path ,trial = trial):
    all_messages = []
    c=0
    if type == 'photo':
        filter = InputMessagesFilterPhotos
    elif type == 'video':
        filter = InputMessagesFilterVideo
    elif type == 'gif':
        filter = InputMessagesFilterGif
    elif type == 'audio':
        filter = InputMessagesFilterMusic
    elif type == 'document':
        filter = InputMessagesFilterDocument
    else:
        filter = InputMessagesFilterPhotoVideo

    directory_exist = False
    type_exist = False
    files_exist = False
    all_files = []
    chat_name = ""

    i = await get_all_chats(client)
    y = 0
    for iter in i:
        # print(f'Iteration: {i[y]["userid"]} - {chat_id}')
        if str(i[y]["userid"]) == str(chat_id):
            chat_name = i[y]["title"]
            break
        y = y + 1


    with os.scandir(f"{main_download_path}") as it:
        for entry in it:
            # print(f'Directory: {entry.name}')
            if str(chat_id) in entry.name:
                directory_exist = True
                os.rename(f'{main_download_path}{entry.name}', f'{main_download_path}{chat_id}_{chat_name}')
                with os.scandir(f"{main_download_path}{chat_id}_{chat_name}/") as ty:
                    for entry1 in ty:
                        # print(f'Type Directory: {entry1.name}')
                        # Please change the logic here to ensure when allall files are selected ==========================================
                        if str(type) in entry1.name:
                            type_exist = True
                            with os.scandir(f"{main_download_path}{chat_id}_{chat_name}/{entry1.name}/") as fl:
                                for entry2 in fl:
                                    # print(f'FileName: {entry2.name}')
                                    if 'D' == str(entry2.name)[0:1] and 'ID' in str(entry2.name) :
                                        all_files.append(entry2.name)
                            if all_files != []:
                                print("\n EXISTING DIRECTORY AND FILES!!!")
                                all_files.sort(reverse=True)
                                last_file = all_files[0]
                                print(f"All Files: {all_files[0]}")
                                date = datetime.datetime(int(last_file[1:5]), int(last_file[6:8]), int(last_file[9:11]),
                                                         int(last_file[12:14]), int(last_file[15:17]),
                                                         int(last_file[18:20]))
                                print(f"Date of Last File: {date}")
                                files_exist = True
                            else:
                                files_exist = False
                            break

    if directory_exist and type_exist and files_exist == False:
        pass
    elif directory_exist and type_exist == False and files_exist == False:
        # i = await get_all_chats(client)
        # # print("Inside create Directory!!!")
        # y = 0
        # for iter in i:
        #     # print(f'Iteration: {i[y]["userid"]} - {chat_id}')
        #     if str(i[y]["userid"]) == str(chat_id):
        #         helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{i[y]["title"]}/{type}/')
        #         break
        #     y = y + 1
        helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{chat_name}/{type}/')
    elif directory_exist == False and type_exist == False and files_exist == False:
        # i = await get_all_chats(client)
        # print("Inside create Directory!!!")
        # y = 0
        # for iter in i:
        #     print(f'Iteration: {i[y]["userid"]} - {chat_id}')
        #     if str(i[y]["userid"]) == str(chat_id):
        #         helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{i[y]["title"]}/{type}/')
        #         break
        #     y = y + 1
        helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{chat_name}/{type}/')

    if files_exist:
        print(f"\nInside get messages: filter is {filter}")

        if trial == True:
            print("\nInside Trial IF loop and getting messages")
            id = 0
            async for messages in client.iter_messages(chat_id, offset_date=date, reverse=False, limit=1):
                id = messages.id
                print(f'ID = {id}')
            async for messages in client.iter_messages(chat_id, wait_time=2, min_id=id, reverse=False, filter=filter):
                c = c + 1
                all_messages.append({"sr": c, "message": messages})
                # print(f'\nMessage: {messages}')
                # print(f'\n{messages.date.strftime("%Y-%m-%dT%H_%M_%S")}')
            print(f"\nIf loop complete")
            print(f"Total Messages to Download: {c}")
        else:
            print("\nInside Actual loop and getting messages for exisitng files and folder")
            id = 0
            async for messages in client.iter_messages(chat_id, offset_date=date, reverse=False, limit=1):
                id = messages.id
                print(f'ID = {id}')
            async for messages in client.iter_messages(chat_id, wait_time=2, min_id=id, reverse=False, filter=filter):
                c = c + 1
                all_messages.append({"sr": c, "message": messages})
                # print(f'\nMessage: {messages}')
                # print(f'\n{messages.date.strftime("%Y-%m-%dT%H_%M_%S")}')
            print(f"\nIf loop complete")
            print(f"Total Messages to Download: {c}")
    else:
        if trial == True:
            print("\nInside Trial IF loop and getting messages for non existing folders")
            async for messages in client.iter_messages(chat_id, wait_time=2, filter=filter):
                c = c + 1
                all_messages.append({"sr": c, "message": messages})
                # print(f'\nMessage: {messages}')
                # print(f'\n{messages.date.strftime("%Y-%m-%dT%H_%M_%S")}')
            print(f"\nIf loop complete")
            print(f"Total Messages to Download: {c}")
        else:
            print("\nInside Actual loop and getting messages for non existing folders")

            async for messages in client.iter_messages(chat_id, wait_time=2, filter=filter):
                c = c + 1
                all_messages.append({"sr": c, "message": messages})
                # print(f'\nMessage: {messages}')
                # print(f'\n{messages.date.strftime("%Y-%m-%dT%H_%M_%S")}')
            print(f"\nIf loop complete")
            print(f"Total Messages to Download: {c}")

    return all_messages


# Definition used to download all media from any given chat/group/channel.
async def download_all_messages_new(client,chat_id, all_messages, main_download_path,type, trial = trial):

    i = await get_all_chats(client)
    y = 0
    for iter in i:
        # print(f'Iteration: {i[y]["userid"]} - {chat_id}')
        if str(i[y]["userid"]) == str(chat_id):
            chat_name = i[y]["title"]
            break
        y = y + 1

    # with os.scandir(main_download_path) as it:
    #     for entry in it:
    #         print(entry.name)
    #         if str(chat_id) in str(entry.name):
    #             os.chdir(main_download_path)
    #             os.rename(f'{entry.name}', f'{chat_id}_{chat_name}')
    # exit()

    for message in all_messages:
        print(f'\nMessage: {message["message"]}')
        print(f'\nFile: {message["message"].file}')
        print(f'Doc Size{float(message["message"].file.size) / 1000000} MB')
        file_size = float(message["message"].file.size) / 1000000

        if file_size < 5:
            if type != 'allall':
                helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{chat_name}/{type}/D{message["message"].date.strftime("%Y-%m-%dT%H_%M_%S")}ID{chat_id}')
                path = await message["message"].download_media(f'{main_download_path}{chat_id}_{chat_name}/{type}/D{message["message"].date.strftime("%Y-%m-%dT%H_%M_%S")}ID{chat_id}')
            if type == 'allall':
                type = identify_message(message)
                helpers.ensure_parent_dir_exists(f'{main_download_path}{chat_id}_{chat_name}/{type}/D{message["message"].date.strftime("%Y-%m-%dT%H_%M_%S")}ID{chat_id}')
                path = await message["message"].download_media(f'{main_download_path}{chat_id}_{chat_name}/{type}/D{message["message"].date.strftime("%Y-%m-%dT%H_%M_%S")}ID{chat_id}')
            if trial:
                break


# Function used to download the media in message by creating specific directory name and folder.
async def guided_download_fn(event, iter, download_path, client):
    try:
        file_name = iter.file.name if iter.file is not None else "NoFileName"
        type = identify_message(iter)
        print(f"\nStarting to download in hard_bot_downloader. File size: {float(iter.file.size) / 1000000} Mb")
#        helpers.ensure_parent_dir_exists(f'{download_path}{type}\\D{iter.date.strftime("%Y-%m-%dT%H_%M_%S")}_{file_name}')
        helpers.ensure_parent_dir_exists(f'{download_path}{type}/{file_name}')
        # print(event)
#        path = await iter.download_media(f'{download_path}{type}\\D{iter.date.strftime("%Y-%m-%dT%H_%M_%S")}_{file_name}')
        path = await iter.download_media(f'{download_path}{type}/{file_name}')
        print('\nFile saved to', path)

    except errors.FloodWaitError as e:
        print('Have to sleep', e.seconds, 'seconds')
        time.sleep(e.seconds)
    except NameError as e:
        print(f"Error Occured: {e}")
    except Exception as e:
        try:
            print("Downloading File in Chunk")
            if "too large" in str(e):
                with open(f'{download_path}{type}/{file_name}', 'wb') as fd:
                    async for chunk in client.iter_download(iter.media):
                        fd.write(chunk)
                print('\nFile saved to', path)
        except Exception as e:
            print("Error Generated in guided_download_fn !!")
            print(str(e))
            print("\nError on line {}".format(sys.exc_info()[-1].tb_lineno))


# Function specifically used to download media from youtube links
async def youtube_Downloader(link, title, download_path, vid=True):
    try:
        url =YouTube(str(link))
        print(str(link))
        # video = url.streams.filter(is_dash=False).get_highest_resolution()  #url.streams.first()
        # video.download()
        print(url.streams.filter(is_dash=False).get_highest_resolution())
        if vid:
            video = url.streams.filter(is_dash=False).get_highest_resolution()  # url.streams.first()
            video.download(output_path=f"{download_path}Normal/video/", filename=title)
            print(f'File saved to {download_path}Normal/video/{title}.mp4')
        else:
            audio = url.streams.filter(is_dash=False).get_lowest_resolution()  # url.streams.first()
            if audio is not None:
                audio.download(output_path=f"{download_path}Normal/audio/", filename=title)
                cmd = f'ffmpeg -i {download_path}Normal/audio/{title}.mp4 {download_path}Normal/audio/{title}.mp3'
                cmd2 = f'{download_path}Normal/audio/{title}.mp4'
                os.system(cmd)
                os.remove(cmd2)
                print(f'File saved to {download_path}Normal/video/{title}.mp3')
            else:
                print("No Audio there to download!!")
    except Exception as e:
        print("Inside youtube_Downloader DEFINITION!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}".format(sys.exc_info()[-1].tb_lineno))


# Initial Function used to download all media from a given caht.
async def all_download_fn_new(event, client):
    chat = await event.get_chat()
    sender = await event.get_sender()
    chat_id = event.chat_id
    chat_username = event.chat.username
    sender_id = event.sender_id

    # Getting all the chats for client
    chats = await get_all_chats(client)
    chats_keyboard = []

    print(chats)

    # Logic to overcome limitation of max 100 buttons in a Keyboard
    if len(chats) <= 100:
        z = 1
    else:
        z = len(chats)//100 + 1

    y = 0

    for iter in range(1,z+1):
        for i in chats:
            # print(f'{chats[y]["sr"]}    :   {chats[y]["title"]}  -  {chats[y]["userid"]} - is_user: {chats[y]["is_user"]}')
            # title = re.sub('[^0-9a-zA-Z.]+', '', chats[y]["title"])
            # print(f'\nTitle: {title}')
            chats_keyboard.append([Button.inline(f'{chats[y]["title"]}', data = f'{chats[y]["userid"]}|DOWNLOADALL')])
            y = y + 1
            if y == iter * 100 or y > len(chats)-1:
                break

        if y <= len(chats):
            print(chats_keyboard)
            await event.reply("Select the chat!!", buttons=chats_keyboard)
            chats_keyboard = []
        else:
            break


# Every new message detail for client
async def message_details(event):
    try:
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        chat_username = event.chat.username
        sender_id = event.sender_id
        #await main()
        print(f'You have a new message in "{chat_username}" : ChatdId: {chat_id} : SenderId: {sender_id}')

        # For TEST
        #print(event)
        #print(event.message)

        if chat_username in album_chats:# or 1==1:
            type = identify_message(event.message)
            if type == "text":
                print(f'The Message is text: {event.message.message}')
                print(" ")
            elif type == "location":
                print("The message contains location")
                print(f'latitude: {event.message.media.geo.lat}')
                print(f'longitude: {event.message.media.geo.long}')
                print(" ")
            elif type == "webpage":
                print("The message contains website")
                print(f'web_id: {event.message.media.webpage.id}')
                print(f'web_url: {event.message.media.webpage.url}')
                print(f'display_url: {event.message.media.webpage.display_url}')
                print(f'hash: {event.message.media.webpage.hash}')
                print(f'type: {event.message.media.webpage.type}')
                print(f'site_name: {event.message.media.webpage.site_name}')
                print(f'title: {event.message.media.webpage.title}')
                print(f'description: {event.message.media.webpage.description}')
                print(f'photo: {event.message.media.webpage.photo}')
                print(f'embed_url: {event.message.media.webpage.embed_url}')
                print(f'embed_type: {event.message.media.webpage.embed_type}')
                print(f'embed_width: {event.message.media.webpage.embed_width}')
                print(f'embed_height: {event.message.media.webpage.embed_height}')
                print(f'duration: {event.message.media.webpage.duration}')
                print(f'author: {event.message.media.webpage.author}')
                print(f'document: {event.message.media.webpage.document}')
                print(f'cached_page: {event.message.media.webpage.cached_page}')
                print(f'webpageattribute: {event.message.media.webpage.webpageattribute}')
                #print(f'photo_size: {event.message.media.webpage.photo.sizes[3].size}')
                print(" ")
            elif type == "photo":
                print("The message contains photo")
                #print(f'Length of EVENT: {len(event)}')
                print(f'Photo Caption: {event.message.message}')
                print(f'Stickers: {event.message.photo.has_stickers}')
                file_details(event.message)
                #await main()
                #print(f'Photo Size: {event.message.photo.sizes[3].size}')
                #await client.send_message(entity="hard_test_bot", message=event.message)
                #message1 = event.message
                #await test_bot.send_message(entity="hardk_aliexpress", message=message1)
                #await bot_event_handler_1(event)
                print(" ")
            elif type == "video":
                print("The message contains video")
                print(f'Video Caption: {event.message.message}')
                #print(f'Streaming: {event.message.document.attributes[0].supports_streaming}')
                file_details(event.message)
                #await main()
                #path = await event.message.download_media()
                #print('File saved to', path)
                print(" ")
            elif type == "gif":
                print("The message contains gif")
                print(f'Gif Caption: {event.message.message}')
                #print(f'Streaming: {event.message.document.attributes[0].supports_streaming}')
                file_details(event.message)
                #await main()
                #path = await event.message.download_media()
                #print('File saved to', path)
                print(" ")
            elif type == "audio":
                print("The message contains audio")
                print(f'Audio Caption: {event.message.message}')
                file_details(event.message)
                print(" ")
            elif type == "poll":
                print("The message contains poll")
                print(f'poll: {event.message.poll}')
                print(f'poll question: {event.message.poll.poll.question}')
                for i in range(0,len(event.message.poll.poll.answers)):
                    print(f'poll answers {i}: Text: {event.message.poll.poll.answers[i].text}  Option: {event.message.poll.poll.answers[i].option}')
                print(f'poll closed: {event.message.poll.poll.closed}')
                print(f'poll public_voters: {event.message.poll.poll.public_voters}')
                print(f'poll multiple_choice: {event.message.poll.poll.multiple_choice}')
                print(f'poll quiz: {event.message.poll.poll.quiz}')
                print(f'poll close_period: {event.message.poll.poll.close_period}')
                print(f'poll close_date: {event.message.poll.poll.close_date}')
                print(f'=== ')
                print(f'poll pollresults: {event.message.poll}')
                for i in range(0, len(event.message.poll.results.results)):
                    print(f'poll results {i}: {event.message.poll.results.results[i]}')
                print(f'poll pollresults: {event.message.poll.results.min}')
                print(f'poll total_voters: {event.message.poll.results.total_voters}')
                print(f'poll recent_voters: {event.message.poll.recent_voters}')
                print(f'poll solution: {event.message.poll.solution}')
                print(f'poll solution_entities: {event.message.poll.solution_entities}')
                print(" ")
            elif type == 'contact':
                print("The message contains contact")
                print(event.message.contact)
                print(f"Phone_Number: {event.message.contact.phone_number}")
                print(f"first_name: {event.message.contact.first_name}")
                print(f"last_name: {event.message.contact.last_name}")
                print(f"user_id: {event.message.contact.user_id}")
            else:
                print("The message contains document")
                print(event.message)
                #file_details(event.message)
                print(" ")
        else:
            pass
    except Exception as e:
        print("Error Generated!!")
        print(str(e))


# Direct Link Downloads
async def direct_downloads_fn(url, download_path, filename = ""):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        print(f"Downloading {url} started........")
        if filename == "":
            local_filename = url.split('/')[-1]
        else:
            local_filename = filename + "." + url.split('.')[-1]
        # NOTE the stream=True parameter below
        with requests.get(url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(f"{download_path}Normal/video/{local_filename}", 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    if chunk:
                      f.write(chunk)
        #return local_filename
        print(f"Downloading {url} complete...")
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


# Direct All Link Downloads
async def direct_links_downloads_fn(url, download_path, download_extensions, filename = ""):
    try:
        driver = webdriver.Edge(executable_path="C:/Hard - Data/Python/Python - Projects/Hard-Telegram-Bot/venv/msedgedriver.exe")
        driver.get(url)
        elements = WebDriverWait(driver, 10).until(expected_conditions.presence_of_all_elements_located((By.CLASS_NAME, 'list-group-item-action')))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        codex = 'https://codex.codexcloud.me'
        driver.quit()
        for link in soup.find_all('a', class_='list-group-item-action'):
            link_local = f'{codex}{link.get("href")}'
            # print(f'Title: {link.text} - Link:{codex}{link.get("href")}')
            link_download = link_local.replace('?a=view', '')
            #if 'mkv' in link_local:
            if any(ext in link_local for ext in download_extensions):
                await direct_downloads_fn(link_download, download_path)
            # print(link1.replace('?a=view', ''))
    except Exception as e:
        print("Error Generated in direct_links_downloads_fn!!")
        print(f'Error occured in Main code logic: {e} ')
        print(f'Error occured in Main code logic: {e.args} ')
        print("Error on line {}\n".format(sys.exc_info()[-1].tb_lineno))


# =============================================== BELOW ARE THE FUNCTIONS NOT USED CURRENTLY AND PRESENT FOR TESTING ======================================================

# Below is the function to call for downloading messages using command line inputs (NOT USED)
async def all_download_fn(event, client):
    print(" ")
    # async for message in client.iter_messages('hard_test_bot'):
    #   print(message.id, message.text)
    print("====== Downloading Function Starts!! =========")
    # async for i in client.iter_participants('hardk_aliexpress'):
    #   print(f'{i.first_name}')
    # print(f'{dialog.id}, {dialog.unread_count}, {dialog.is_user}, {dialog.title}' )
    chats = await get_all_chats(client)
    # print(chats)
    y = 0
    for i in chats:
        print(f'{chats[y]["sr"]}    :   {chats[y]["title"]}  -  {chats[y]["userid"]} - is_user: {chats[y]["is_user"]}')
        y = y + 1

    select = input("""
Select your chat:  """)
    lower = int(input("""Message Index to start:    """))
    upper = int(input("""Message Index to end:  """))
    type = input("What type? video/photo/audio/document:    ")
    all_messages = await get_all_messages_filter(client, chats[(int(select) - 1)]["userid"], minimum=lower,
                                                 maximum=upper)
    # z = 0
    time_start = datetime.datetime.now()
    print(f"""  
    =========================
    Downloading started.... {time_start}
        """)
    for i in range(0, upper - lower):
        await download_messages(client, all_messages[i]["message"], type, id=chats[(int(select) - 1)]["userid"],
                                chat=chats[(int(select) - 1)]["title"])
    time_end = datetime.datetime.now()
    delta = time_end - time_start
    print(f"""  
    File Download Completed at: {datetime.datetime.now()} - Total Time =  {round((delta.total_seconds() / 60), 2)} mins                                 
    =========================""")

    # async for chat in client.get_chat():
    #   print(f'{chat}' )


# Downloader function with filesize limit and type checking (NOT USED)
async def download_messages(client, message, type, id=0, chat="Unknown"):
    try:
        if identify_message(message) == type:
            if message.photo or message.video:
                file_size = float(message.file.size) / 1000000
            else:
                file_size = 0
            #print(f'{identify_message(message)} - file Size: {file_size} Mb')
            #file_name = event.message.file.name if event.message.file is not None else "NoFileName"

            download_path = "/Volumes/Hard 2TB/Telegram/" ##"D:\Telegram\\"  # main_download_path #"O:/downloads/Telegram/"
            if (message.contact or message.photo or message.video or message.geo ) and file_size < 200:
                helpers.ensure_parent_dir_exists(f'{download_path}{id}_{chat}/{type}/D{message.date.strftime("%Y-%m-%dT%H_%M_%S")}ID{id}')
                path = await message.download_media(f'{download_path}{id}_{chat}/{type}/D{message.date.strftime("%Y-%m-%dT%H_%M_%S")}ID{id}')
                #print('File saved to', path)  # printed after download is done
                # await download_file
                # await download_file(client, location = message ,out='C:/Users/hardk/Desktop/TEST_FOLDER/test')#,progress_callback=prog)
            elif message.audio:
                # print(message.media)
                # print(message.media.document)
                # print(message.media.document.attributes[0].title)
                try:
                    if message.media.document.attributes[0].title is not None:
                        title = message.media.document.attributes[0].title
                    elif message.media.document.attributes[1].file_name is not None:
                        title = message.media.document.attributes[1].file_name
                    else:
                        title = "No Title"

                except:
                    title = None

                # print(title)

                audio_exist = False

                with os.scandir(f"{download_path}{id}_{chat}/{type}/") as it:
                    for entry in it:
                        if str(title) in str(entry.name):
                            audio_exist = True
                            # print(entry.name)
                            # print("Audio already exists!!")
                            break
                        else:
                            pass
                            # print("Audio does NOT exists and we will download it!!")
                            # print(entry.name)

                if audio_exist is True:
                   print("Audio already exists!!")
                else:
                    print("Audio does NOT exists and we will download it!!")
                    print(title)
                    helpers.ensure_parent_dir_exists(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')
                    path = await message.download_media(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')

                # if title is None:
                #     # print(message.media.document)
                #
                #     print(message.media.document.attributes[1].file_name)
                #     helpers.ensure_parent_dir_exists(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[1].file_name}')
                #     path = await message.download_media(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[1].file_name}')
                # else:
                #     print(title)
                #     helpers.ensure_parent_dir_exists(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')
                #     path = await message.download_media(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')
                # helpers.ensure_parent_dir_exists(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')
                # path = await message.download_media(f'{download_path}{id}_{chat}/{type}/{message.media.document.attributes[0].title}')
            else:
                print("File is large and cannot be downloaded")

        else:
            print(f"Message is not video/photo/audio/document/contact: You gave us {type} as file type to download!!")
    except Exception as e:
        print("Error Generated in Hard_Downloader_Bot New Message Event!!")
        print(str(e))


# all messages with specific filters (NOT USED)
async def get_all_messages_filter(client, chat_id, minimum, maximum, filter="InputMessagesFilterPhotos"):
    c = 0
    all_messages = []
    intial_messages = []
    counter = 0
    #last_message.id = 99999999
    async for  i in client.iter_messages(chat_id, wait_time=5, limit= 1):
        last_message = i
        counter = counter +1
    print(counter)
    #print(f'last_message_id: {last_message.id}')
    #print(f'last_message_id: {last_message.date}')

    if maximum-0 > 1000:
        iter = (maximum-0) // 1000
        remain = (maximum-0) % 1000
    else:
        iter = 1
    #print(iter)
    for loop in range(0,iter+1):
        async for messages in client.iter_messages(chat_id, wait_time = 5, limit = min(1000,maximum), max_id = last_message.id):
            c = c + 1
            if c >= minimum and c <= maximum:
                all_messages.append({"sr": c, "message": messages})
                last_message = all_messages[len(all_messages) - 1]["message"]
            elif c < minimum:
                intial_messages.append({"sr": c, "message": messages})
                last_message = intial_messages[len(intial_messages) - 1]["message"]
            else:
                break
    #print(f"last_message_id = {last_message.id} and count: {len(all_messages)}")
    return all_messages


# filters for message types (NOT USED)
async def get_all_filters(type, client):
    if type == 'photo':
        return InputMessagesFilterPhotos
    elif type == 'video':
        return InputMessagesFilterVideo
    else:
        return 'unknown'
