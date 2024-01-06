from re import search
import aiohttp
import discord
import discord.ext.commands.context
import os

async def getAttachmentsImage(message: discord.Message):
    if message.reference != None:
        replyMessage = await message.channel.fetch_message(message.reference.message_id)

    #Check attachmets
    if message.reference == None:
        if len(message.attachments) < 1:
            return None
    if message.reference != None:
        if len(replyMessage.attachments) < 1:
            return None
    
    if message.reference == None:
        file = message.attachments[0]
    else:
        file = replyMessage.attachments[0]
    
    #Check extension
    filename = file.filename
    extension = os.path.splitext(filename)[1]
    if extension not in [".png", ".jpeg", ".jpg"]:
        return None
    
    return file

async def getAttachmentsVideo(message: discord.Message):
    if message.reference != None:
        replyMessage = await message.channel.fetch_message(message.reference.message_id)

    #Check attachmets
    if message.reference == None:
        if len(message.attachments) < 1:
            return None
    if message.reference != None:
        if len(replyMessage.attachments) < 1:
            return None
    
    if message.reference == None:
        file = message.attachments[0]
    else:
        file = replyMessage.attachments[0]
    
    #Check extension
    filename = file.filename
    extension = os.path.splitext(filename)[1]
    if extension not in [".mp4", ".mov", ".avi", ".webm", ".wmv", ".mpeg"]:
        return None
    
    return file

async def getAttachmentsAudio(message: discord.Message):
    if message.reference != None:
        replyMessage = await message.channel.fetch_message(message.reference.message_id)

    #Check attachmets
    if message.reference == None:
        if len(message.attachments) < 1:
            return None
    if message.reference != None:
        if len(replyMessage.attachments) < 1:
            return None
    
    if message.reference == None:
        file = message.attachments[0]
    else:
        file = replyMessage.attachments[0]
    
    #Check extension
    filename = file.filename
    extension = os.path.splitext(filename)[1]
    if extension not in [".mp3", ".aac", ".wav", ".m4a"]:
        return None
    
    return file

async def async_get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
    
def check_file_size(url):
    byte = os.path.getsize(url)
    #if 8mb over
    if byte > 8388608:
        return False
    else:
        return True

def sort_args(text) -> list:
    result = []
    if " " not in text and "　" not in text:
        result.append(text)
        return result
    if " " in text:
        return text.split(" ")
    if "　" in text:
        return text.split("　")
    return result