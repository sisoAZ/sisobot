import discord
import os
from discord.ext import commands
from util import getAttachmentsVideo
from util import check_file_size
from cogs.epicgamer.epicgamer_overlay import makeEpicGamer
import asyncio

class epicGamer(commands.Cog, name="音割れゲーマー"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="epicgamer", aliases=["gamer"], help="/epicgamer [leftup|rightup|rightdown|leftdown]", description="一生懸命頑張っているゲーマが一緒にゲームしてくれます。")
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def epicGamer(self, ctx, *, position: str = "rightup"):
        file = await getAttachmentsVideo(ctx.message)
        if file == None:
            await ctx.channel.send("Video file is not found or file extension is not .mp4, .mov, etc...")
            return
        filename = file.filename
        attachmentFilePath = os.getcwd() + "/downloaded_files/" + filename
        await file.save(attachmentFilePath)
        await ctx.trigger_typing()

        loop = asyncio.get_event_loop()
        try:
            imagePath = await loop.run_in_executor(None, lambda:makeEpicGamer(attachmentFilePath, os.getcwd() + "/files/epicgamer/epicgamer.mp4", position))
        except Exception as e:
             await ctx.channel.send("ERROR" + str(e))
             return
             
        if check_file_size(imagePath) == True:
            await ctx.channel.send(file=discord.File(imagePath))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(imagePath)
        os.remove(attachmentFilePath)

def setup(bot):
    return bot.add_cog(epicGamer(bot))