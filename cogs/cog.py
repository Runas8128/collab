from discord.ext import commands
import discord

class Cog(commands.Cog):
    """The description for Cog goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.CollabNotice: discord.TextChannel = None
    
    @commads.Cog.listener()
    async def on_ready(self):
        self.CollabNotice = self.bot.get_channel(967365739227013140)
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = channel.fetch_message(payload.message_id)
        await message.pin()
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = channel.fetch_message(payload.message_id)
        await message.unpin()
    
    

def setup(bot):
    bot.add_cog(Cog(bot))
