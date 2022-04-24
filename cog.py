import discord
from discord.ext import commands

from database import DB

class Cog(commands.Cog):
    """The description for Cog goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.CollabNotice: discord.TextChannel = None
        self.db = DB()
    
    @commands.command()
    async def exit(self):
        self.db.close()
        self.exit()
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.CollabNotice = self.bot.get_channel(967365739227013140)
    
    

def setup(bot):
    bot.add_cog(Cog(bot))
