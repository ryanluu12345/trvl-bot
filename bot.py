# Python base
import os
import random

# Python external
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv

# Package internal
from yelp import Yelp

TOKEN = None
GUILD = None
load_dotenv()
bot = commands.Bot(command_prefix='!')
yelp = Yelp()


def get_env():
    global TOKEN, GUILD
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')

# Consider the "bot" layer as the API view layer (kinda like routes)
@bot.command(name='random_location')
async def random_location(ctx):
    locations = ['bali', 'paris', 'hong kong']
    response = random.choice(locations)
    await ctx.send(response)


@bot.command(name='top_recs')
async def top_recs(ctx, keyword: str = "", location: str = "San Francisco", number_of_recs: int = 3):
    yelp_data = yelp.get_businesses(keyword, location, number_of_recs)

    for rec in yelp_data:
        rec_data = yelp_data[rec]
        embed = Embed()
        embed.description = f"[{rec_data['name']}]({rec_data['url']})"
        embed.set_image(url = rec_data['image_url'])
        await ctx.send(embed = embed)


@bot.command(name='details')
async def details(ctx, location: str):
    detail_map = {
        "wynn buffet": "amazing buffet; top notch vegas",
        "lemongrass": "asian fusion at its finest",
        "bacchannal": "dessert island"
    }
    response = detail_map.get(location, "not recognized!")
    await ctx.send(response)

get_env()
bot.run(TOKEN)
