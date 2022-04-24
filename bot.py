#!/usr/bin/env python3

from discord.ext import commands
import discord
import config

class Bot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            **kwargs
        )

        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print(f'Could not load extension {cog} due to {exc.__class__.__name__}: {exc}')

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')

bot = Bot()

bot.run(config.token)
