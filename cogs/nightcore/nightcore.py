import discord
import os
from discord.ext import commands
from cogs.nightcore.youtube_dl_mp3 import youtube_dl_mp3
from cogs.nightcore.soundcloud_dl_mp3 import dl
from cogs.nightcore.encode_audio_file import nightcore_encode_ffmpeg
from util import check_file_size, getAttachmentsAudio

class nightcore(commands.Cog, name="NightCore"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="nightcore", aliases=["nc"], help="/nightcore (url) (pitch) (speed)", description="NightCoreの意味が分かる人向け。今でも聞いてる人はいるのだろうか...")
    async def makeNightcore(self, ctx, *args):
        file = await getAttachmentsAudio(ctx.message)
        if file == None:
            #args not set
            if len(args) <= 0:
                await ctx.channel.send("-nc (url) (pitch) (speed)")
                await ctx.channel.send("-nc (pitch) (speed) with audio file")
                return
            await ctx.channel.send("`Downloading music...`")
            filename = await downloadAudio(args[0])
            #if pitch is set
            if len(args) >= 2:
                if isfloat(args[1]) == True:
                    pitch = args[1]
                else:
                    pitch = 1
            else:
                pitch = 1
            #if speed is set
            if len(args) >= 3:
                if isfloat(args[2]) == True:
                    speed = args[2]
                else:
                    speed = 1
            else:
                speed = 1
        #Audio file exist
        else:
            attachment_filename = file.filename
            filename= os.getcwd() + "/downloaded_files/" + attachment_filename
            await file.save(filename)
            #if pitch is set
            if len(args) >= 1:
                if isfloat(args[0]) == True:
                    pitch = args[0]
                else:
                    pitch = 1
            else:
                pitch = 1
            #if speed is set
            if len(args) >= 2:
                if isfloat(args[1]) == True:
                    speed = args[1]
                else:
                    speed = 1
            else:
                speed = 1
        await ctx.trigger_typing()
        filePath = await nightcore_encode_ffmpeg(filename, pitch, speed)
        if check_file_size(filePath) == True:
            await ctx.channel.send(file=discord.File(filePath))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(filePath)
        os.remove(filename)

async def downloadAudio(url):
    if "youtube.com" in url or "youtu.be" in url:
        dl_filename = await youtube_dl_mp3(url)
        return dl_filename
    #If soundcloud
    elif "soundcloud.com" in url:
        dl_filename = await dl(url)
        return dl_filename

def isfloat(s):
    try:
        float(s)
    except ValueError:
        return False
    else:
        return True

def setup(bot):
    return bot.add_cog(nightcore(bot))