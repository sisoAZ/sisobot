import asyncio
import os
import youtube_dl

async def youtube_dl_mp3(url):
    loop = asyncio.get_event_loop()

    dl_dir = os.getcwd() + "/files/nightcore/"

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': dl_dir + "%(id)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl_info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=True))
    except Exception as e:
        return "Error"
    
    return dl_dir + ydl_info["id"] + ".mp3"