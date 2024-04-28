import io
from PIL import Image
import requests
from cogs.fakemessage.discordmsg import discordMsg
import discord
from discord.ext import commands
import os

from cogs.fakegpt.image import generate
from util import async_get_json


class FakeGPT(commands.Cog, name="FakeGPT"):
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

    @commands.command(name="gpt", aliases=['fakegpt', 'chatgpt'], help="/fakegpt", description="AIがそんなこと言うわけ無いだろ！")
    # @commands.guild_only()
    async def gen(self, ctx, *, text: str = None):
        if ctx.message.reference != None:
            user_message = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        else:
            return

        disaply_name_json = await async_get_json(f"https://dashboard.botghost.com/api/public/tools/user_lookup/{user_message.author.id}")
        if disaply_name_json["global_name"] == None:
            disaply_name = user_message.author.name
        else:
            disaply_name = disaply_name_json["global_name"]

        avatar_img = self._downloadExternalImg(user_message.author.avatar_url_as(size=64))
        
        # return _serve_pil_image(patternAppliedImg)
        # TODO Get a way to server pil images in discord chat

        image_bytes = generate(user_message.content, text, user_name=disaply_name, user_image=avatar_img)
        await ctx.channel.send(file=discord.File(image_bytes, "output.png"))


def setup(bot):
    return bot.add_cog(FakeGPT(bot))
