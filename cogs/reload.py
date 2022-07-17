import discord
from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    #@commands.Cog.listener(name="on_message")
    @commands.command(name="r", hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cogname = None):
        if ctx.message.author.bot:
            return
        if ctx.message.author.id not in [491064478486626304, 913643383908606002]:
            return
        if cogname == None:
            await ctx.message.channel.send(f"{self.bot.command_prefix}r (folder.filename)")
            return
        try:
            self.bot.reload_extension("cogs." + cogname)
            await ctx.message.channel.send("`Reloaded`")
        except Exception as e:
            await ctx.message.channel.send(f"`ERROR -> {e}`")

def setup(bot):
    return bot.add_cog(ReloadCog(bot))