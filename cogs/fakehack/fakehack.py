import discord
from discord.ext import commands
import os
from util import getAttachmentsImage
from util import check_file_size
from cogs.fakehack.mergeOverlay import mergeGui

class fakeHack(commands.Cog, name="フェイクハック"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="fakehack", hidden=True)
    async def on_message(self, ctx, *, overlay_type = "wurst"):
        file = await getAttachmentsImage(ctx.message)
        if overlay_type == "help":
            await ctx.channel.send("-fakehack (wurst|vape|pvp) with image file")
            return
        if file == None:
            await ctx.channel.send("Image file is not found or file extension is not .png or .jpg")
            return
        filename = file.filename
        attachmentFilePath = os.getcwd() + "/downloaded_files/" + filename
        await file.save(attachmentFilePath)

        if overlay_type == "wurst":
            gui_filename = "wurst.png"
        elif overlay_type == "pvp":
            gui_filename = "other.png"
        elif overlay_type == "vape":
            gui_filename = "vape.png"

        guiPath = os.getcwd() + "/files/hackgui/" + gui_filename
        imagePath = await mergeGui(attachmentFilePath, guiPath)
        if check_file_size(imagePath) == True:
            await ctx.channel.send(file=discord.File(imagePath))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(imagePath)
        os.remove(attachmentFilePath)

def setup(bot):
    return bot.add_cog(fakeHack(bot))