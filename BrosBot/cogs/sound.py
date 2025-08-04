import discord
from discord.ext import commands
from discord.ext import tasks
from discord import FFmpegPCMAudio
import random

class SoundCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vc = {}
        self.vc_client = None
        self.loop = self.blinker_checkpoint
        self.stop_counter = 0
        self.stops = {
            0: "penjamin_town.mp3",
            1: "blinker_city.mp3",
            2: "yartville.mp3"
        }

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot Started')

    async def join_vc(self, ctx, channel):
        if ctx.voice_client is None:
            self.vc_client = await channel.connect()
            self.play_entrance()
            print('test2')
        else:
            await ctx.voice_client.move_to(channel)

    @commands.command(name="start")
    async def start(self, ctx):
        if ctx.author.voice:
            currentChannel = ctx.author.voice.channel
            await self.join_vc(ctx, currentChannel)
            await ctx.send('Bot joined vc')
            self.loop.start()
        else:
            await ctx.send("You are not in a vc")

    @commands.command(name="stop")
    async def stop(self, ctx):
        if ctx.author.voice:
            if ctx.voice_channel is not None:
                await ctx.voice_channel.disconnect()
                self.vc_client = None
            self.loop.cancel()
            await ctx.send('Bot has left vc')
        else:
            await ctx.send('Bot is not in a vc')

    @tasks.loop(minutes = random.randint(13,18))
    async def blinker_checkpoint(self):
        # do blinker checkpoint
        self.play_stop()

        # change time interval
        newInterval = random.randint(13,18)
        self.blinker_checkpoint.change_interval(minutes=newInterval)

    async def play_entrance(self):
        if self.vc_client.is_playing():
            self.vc_client.stop()

        source = FFmpegPCMAudio('jr_notification.mp3')
        await self.vc_client.play(source)
        source = FFmpegPCMAudio('blinker_announcement.mp3')
        await self.vc_client.play(source)
    
    def play_stop(self):
        if self.vc_client.is_playing():
            self.vc_client.stop()

        tempSource = FFmpegPCMAudio('japan_station_tone.mp3')
        player = self.vc_client.play(tempSource)

        tempSource2 = FFmpegPCMAudio(self.stops[self.stop_counter])
        player = self.vc_client.play(tempSource2)
        self.stop_counter += 1
        self.stop_counter %= 3
        
async def setup(bot):
    await bot.add_cog(SoundCog(bot))