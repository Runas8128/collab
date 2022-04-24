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

bot = Bot()

bot.run(config.token)
