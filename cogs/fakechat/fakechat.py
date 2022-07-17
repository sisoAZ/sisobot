import discord
import os
from discord.ext import commands
from util import getAttachmentsImage
from util import check_file_size
from cogs.fakechat.mergeText import drawText

class fakeChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="fakechat", hidden=True)
    async def makeMadeInWario(self, ctx, *text):
        file = await getAttachmentsImage(ctx.message)
        if file == None:
            await ctx.channel.send("Image file is not found or file extension is not .png or .jpg")
            return
        if len(text) <= 0:
            await ctx.channel.send("Use: -fakechat (text) with image file")
            return
        filename = file.filename
        attachmentFilePath = os.getcwd() + "/downloaded_files/" + filename
        await file.save(attachmentFilePath)
        imagePath = await drawText(attachmentFilePath, text)
        if check_file_size(imagePath) == True:
            await ctx.channel.send(file=discord.File(imagePath))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(imagePath)
        os.remove(attachmentFilePath)

def setup(bot):
    return bot.add_cog(fakeChat(bot))