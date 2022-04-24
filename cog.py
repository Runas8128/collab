import discord
from discord.ext import commands

from database import DB
from error import NotExistPart

class Cog(commands.Cog):
    """The description for Cog goes here."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.CollabNotice: discord.TextChannel = None
        self.progMsg: discord.Message = None
        self.db = DB()
    
    def makeEmbed(self, guild: discord.Guild) -> discord.Embed:
        embed = discord.Embed(
            title="TremENDous",
            description="이 임베드는 자동으로 수정됩니다."
        )
        for partNo, time, chart, cSub, vfx, vSub in self.db.getData():
            value = ''

            if cSub != -1:
                mem: discord.Member = guild.get_member(chart)
                sub = '✅' if cSub == 1 else '❌'
                value += f'채보: {mem.mention} ({sub})'
            else:
                value += '채보: - (➖)'

            if vSub != -1:
                mem: discord.Member = guild.get_member(vfx)
                sub = '✅' if vSub == 1 else '❌'
                value += f'이펙트: {mem.mention} ({sub})'
            else:
                value += '이펙트: - (➖)'
            
            embed.add_field(
                name=f'#{partNo}: {time}',
                value=value
            )
        return embed
    
    @commands.command()
    async def exit(self):
        self.db.close()
        self.exit()
    
    @commands.Cog.listener()
    async def on_ready(self):
        #self.CollabNotice = self.bot.get_channel(967365739227013140)
        self.CollabNotice = self.bot.get_channel(823359663973072960)
        msgID = self.db.getProgMsgID()
        if msgID != 0:
            self.progMsg = self.CollabNotice.fetch_message(msgID)
    
    @commands.command()
    @commands.is_owner()
    async def init(self, ctx: commands.Context):
        self.db.init()

        self.progMsg = await self.CollabNotice.send(
            embed=self.makeEmbed(ctx.guild)
        )
        self.db.setProgMsgID(self.progMsg.id)

        message: discord.Message = ctx.message
        message.add_reaction('👍')
    
    @commands.command(name="파트")
    async def editTime(
        self, ctx: commands.Context,
        partNo: int, *time: str
    ):
        try:
            edited = self.db.editTime(partNo, ' '.join(time))
            self.progMsg.edit(embed=self.makeEmbed(ctx.guild))
        except NotExistPart as part:
            await ctx.send(part.msg)
    
    @commands.command(name="채보", aliases=['chart', '차트'])
    async def editChart(
        self, ctx: commands.Context,
        partNo: int, newMem: discord.Member
    ):
        try:
            edited = self.db.editChart(partNo, newMem.id)
            self.progMsg.edit(embed=self.makeEmbed(ctx.guild))
        except NotExistPart as part:
            await ctx.send(part.msg)
    
    @commands.command(name="이펙트", aliases=['vfx', '이펙'])
    async def editVFX(
        self, ctx: commands.Context,
        partNo: int, newMem: discord.Member
    ):
        try:
            edited = self.db.editVFX(partNo, newMem.id)
            self.progMsg.edit(embed=self.makeEmbed(ctx.guild))
        except NotExistPart as part:
            await ctx.send(part.msg)

    @commands.command(name="제출")
    async def submit(self, ctx: commands.Context):
        try:
            uid = ctx.author.id
            parts = self.db.getData()
            part = [part for part in parts if uid in [part[2], part[4]]][0]

            if part[2] == uid:
                self.db.chartSubmit(part[0])
            else:
                self.db.vfxSubmit(part[0])
            
            self.progMsg.edit(embed=self.makeEmbed(ctx.guild))
        except NotExistPart as part:
            await ctx.send(part.msg)

def setup(bot):
    bot.add_cog(Cog(bot))
