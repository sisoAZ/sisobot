import os
import shutil
from discord.ext import commands
import discord

command_prefix = "/"

def main():
    client = commands.Bot(command_prefix=command_prefix, help_command=JapaneseHelpCommand(), activity=discord.Game("/help"))

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected to Discord.")

        os.makedirs("downloaded_files", exist_ok=True)
        shutil.rmtree("downloaded_files")
        os.makedirs("downloaded_files", exist_ok=True)
        # load all cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename[:-3]} Cog Loaded!")
        for root, dirs, files in os.walk("./cogs"):
            for dir in dirs:
                for filename in os.listdir(f"./cogs/{dir}"):
                    if filename.endswith(".py"):
                        try:
                            client.load_extension(f"cogs.{dir}.{filename[:-3]}")
                            print(f"{filename[:-3]} Cog Loaded!")
                        except Exception as e:
                            if "has no 'setup' function" not in str(e):
                                print(f"Cog load error:\n{e}")
    client.run("")

class JapaneseHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.commands_heading = "コマンド:"
        self.no_category = "その他"
        self.command_attrs["help"] = "コマンド一覧と簡単な説明を表示"

    def get_ending_note(self):
        return (f"各コマンドの説明: {command_prefix}help <コマンド名>")

if __name__ == '__main__':
    main()