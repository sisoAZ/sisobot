import os
import asyncio
import subprocess
from subprocess import PIPE

ffmpeg_path = os.getcwd() + "/ffmpeg"

async def nightcore_encode_ffmpeg(mp3, pitch = 1, speed = 1):
    loop = asyncio.get_event_loop()

    filename = os.path.splitext(os.path.basename(mp3))[0]
    dirname = os.path.dirname(mp3)
    proc = subprocess.Popen(
        rf'{ffmpeg_path} -i "{mp3}" -filter:a "atempo={speed},asetrate=44100*{pitch}" "{dirname + "/" + filename + "-Nightcore" + ".mp3"}" -y',
        shell=True, stdout=PIPE, stderr=PIPE, encoding="utf-8")
    try:
        await loop.run_in_executor(None, proc.communicate, "timeout=15")
    except Exception:
        proc.kill()
        return "Error"
    return dirname + "/" + filename + "-Nightcore" + ".mp3"