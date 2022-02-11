from telethon import events,functions,errors,Button
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import Config
import asyncio
import threading
import requests
import re
from urllib.parse import quote

def cronjob():
    threading.Timer(60*5, cronjob).start()
    requests.get(Config.DOMAIN)
    
if "heroku" in Config.DOMAIN:
    cronjob()

client = TelegramClient(
            StringSession(),
            Config.API_ID,
            Config.API_HASH,
            # proxy=("socks5","127.0.0.1",9050)
            ).start(bot_token=Config.TOKEN)

username_bot = client.get_me().username

def get_file_name(message):
    if message.file.name:
        return quote(message.file.name)
    ext = message.file.ext or ""
    return f"file{ext}"

@client.on(events.NewMessage)
async def download(event):
 
    if str(event.chat_id) in Config.AUTHX:
        chatz = int(Config.AUTHX[str(event.chat_id)])
        if event.file :
            if not event.file.size > 10_000_000:
                    msg = await event.client.send_message(chatz, message=event.message)
                    return
            msgx = await event.client.send_message(entity=chatz,message="Getting Message ID")
            idx = int(msgx.id)+1
            namezx = str(event.message.file.name)
            punc = '''!()[]|{};:'="\,<>./?@#$%^&*~'''
            for ele in namezx:
              if ele in punc:
                namezx = namezx.replace(ele, "_")
            namec = namezx.replace('  ', '_').replace(' ', '_')
            msg = await event.client.send_file(
                chatz,
                file=event.message.media,caption=event.message.message,buttons=(
      [
        Button.url('💾 Download', f'{Config.DOMAIN}/{idx}/{chatz}/(Sahil_Nolia)~{namec}'),Button.url('📺 Watch', f'{Config.DOMAIN}/{idx}/sahil/stream/{chatz}'),
      ],[
        Button.url('💞 Contact Sahil Nolia 💞', f'https://t.me/sahil_nolia')
      ]
    ))
            await event.client.delete_messages(entity=chatz, message_ids=msgx.id)
        
        else :
            await event.client.send_message(chatz, message=event.message)                   
                    
client.run_until_disconnected()
