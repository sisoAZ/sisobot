import discord
import os
from discord.ext import commands
import requests
from cogs.iei.merge_iei import merge_iei
import asyncio

from util import check_file_size


class iei(commands.Cog, name="勝手に殺すな！！"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command(name="iei", help="/iei [USERID|MENTION]", description="人を殺めました", hidden=True)
    async def makeMadeInWario(self, ctx, user_id: str = None, text: str = None):
        if ctx.message.reference != None:
            message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
            user = message.author
        elif user_id == None:
            await ctx.channel.send("-iei (UserID|Mention)")
        #Non mention
        elif len(ctx.message.mentions) <= 0:
            try:
                user = await self.bot.fetch_user(int(user_id))
            except Exception:
                await ctx.channel.send("User is not found")
                return
        #Mention
        else:
            user = ctx.message.mentions[0]
        image_url = user.avatar_url_as(format="png", size=1024)
        file_name = str(user.id)
        loop = asyncio.get_event_loop()
        res = await loop.run_in_executor(None, requests.get, image_url)
        get_image = res.content
        with open("./downloaded_files/" + file_name + ".png", 'wb') as img_file:
            img_file.write(get_image)
        image_path = os.path.abspath(os.getcwd() + "/downloaded_files/" + file_name + ".png")
        file_name = merge_iei(image_path, text)
        if check_file_size(file_name) == True:
            await ctx.channel.send(file=discord.File(file_name))
        else:
            await ctx.channel.send("`ERROR -> Over file size (8MB)`")
        os.remove(file_name)

def setup(bot):
    return bot.add_cog(iei(bot))