#!/usr/bin/env python3

import discord
from discord.ext import commands
import config

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            **kwargs
        )

        try:
            self.load_extension('cog')
        except Exception as exc:
            print(f'Could not load extension due to {exc.__class__.__name__}: {exc}')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')
    
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

bot = Bot()

bot.run(config.token)
