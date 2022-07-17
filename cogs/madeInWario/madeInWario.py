import discord
import os
import asyncio
from discord.ext import commands
from cogs.madeInWario.wario_video import makeVideo
from util import check_file_size, getAttachmentsImage, getAttachmentsVideo
from cogs.madeInWario.wario_overlay import mergeImage

class madeInWario(commands.Cog, name="メイドインワリオ"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="wario", help="/wario [メッセージ]", description="画像や動画をメイドンワリオ風にできます！")
    @commands.cooldown(1, 20, type=commands.BucketType.user)
    async def makeMadeInWario(self, ctx, *, text: str = None):
        file = await getAttachmentsImage(ctx.message)
        if file == None:
            file = await getAttachmentsVideo(ctx.message)
            filetype = "VIDEO"
            if file == None:
                await ctx.channel.send("Image file or video file is not found.")
                return
        else:
            filetype = "IMAGE"
        filename = file.filename
        attachmentFilePath = os.getcwd() + "/downloaded_files/" + filename
        await file.save(attachmentFilePath)
        loop = asyncio.get_event_loop()
        if filetype == "IMAGE":
            imagePath = await loop.run_in_executor(None, lambda: mergeImage(attachmentFilePath, text))
        if filetype == "VIDEO":
            try:
                imagePath = await loop.run_in_executor(None, lambda: makeVideo(attachmentFilePath, text))
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
    return bot.add_cog(madeInWario(bot))