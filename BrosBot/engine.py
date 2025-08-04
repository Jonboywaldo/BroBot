import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import asyncio

discord.utils.setup_logging()

# get token for bot
load_dotenv()
bot_token = os.getenv('BOT_TOKEN')
intents = discord.Intents.all()

# Make bot and add intents (all intents enabled)
bot = commands.Bot(command_prefix="!", intents=intents)


async def load():
    for filename in os.listdir(os.getcwd() + r'\\BrosBot\\cogs'):
        if filename.endswith('.py'):
            print('test')
            await bot.load_extension('cogs.' + filename[:-3])

async def main():
    await load()
    await bot.start(bot_token)

asyncio.run(main())