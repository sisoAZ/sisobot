import discord
from discord.ext import commands
import os
from util import getAttachmentsImage
from util import check_file_size
from cogs.nintendo.image import mergeImage

class Nintendo(commands.Cog, name="ニンテンドーパッケージ"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="nintendo", aliases=['package', 'switch'], help="/nintendo [a|b|c|d|z]", description="ついに...ゲーム化したのだな...")
    async def on_message(self, ctx, *, cero = "a"):
        file = await getAttachmentsImage(ctx.message)
        if cero == "help":
            await ctx.channel.send("-nintendo (a|b|c|d|z)")
            return
        if file == None:
            await ctx.channel.send("Image file is not found or file extension is not .png or .jpg")
            return
        filename = file.filename
        attachmentFilePath = os.getcwd() + "/downloaded_files/" + filename
        await file.save(attachmentFilePath)

        imagePath = await mergeImage(attachmentFilePath, cero)
        if check_file_size(imagePath) == True:
            await ctx.channel.send(file=discord.File(imagePath))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(imagePath)
        os.remove(attachmentFilePath)

def setup(bot):
    return bot.add_cog(Nintendo(bot))