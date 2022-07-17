import io
from PIL import Image
import requests
from cogs.fakemessage.discordmsg import discordMsg
import discord
from discord.ext import commands
import os

from cogs.your_message_was_seen.image import mergeImage


class YourMessageWasSeen(commands.Cog, name="あなたの発言見られてますよ"):
    def __init__(self, bot):
        self.bot = bot

    def _downloadExternalImg(self, url: str) -> Image.Image:
        response: requests.Response = requests.get(url)
        im = Image.open(io.BytesIO(response.content))
        return im

    def _serve_pil_image(self, pil_img):
        img_io = io.BytesIO()
        pil_img.save(img_io, 'PNG')
        img_io.seek(0)
        # return img_io

    @commands.command(name="seen", help="/seen", description="こんにちはインターネット")
    # @commands.guild_only()
    async def seen_message(self, ctx):
        if ctx.message.reference != None:
            message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        else:
            message = ctx.message

        avatar_img = self._downloadExternalImg(message.author.avatar_url_as(size=128))
        try:
            patternAppliedImg = await discordMsg(avatar_img, message.content, message.author.name, "#FFFFFF")
        except Exception as e:
            await ctx.send("Error")
        
        # return _serve_pil_image(patternAppliedImg)
        # TODO Get a way to server pil images in discord chat

        final_image = mergeImage(patternAppliedImg)
        imagePath = f"downloaded_files/{message.id}.png"
        final_image.save(imagePath)
        await ctx.channel.send(file=discord.File(imagePath))
        os.remove(imagePath)


def setup(bot):
    bot.add_cog(YourMessageWasSeen(bot))
