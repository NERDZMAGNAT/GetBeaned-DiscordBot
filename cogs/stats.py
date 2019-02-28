import asyncio
import json

import aiohttp
import json
from discord.ext import commands

with open("credentials.json", "r") as f:
    credentials = json.load(f)

DISCORDBOTS_ORG_TOKEN = credentials["discordbots_org_token"]

DISCORD_BOTS_ORG_API = 'https://discordbots.org/api'


class Carbonitex(commands.Cog):
    """Cog for updating bots.discord.pw bot information."""

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    def __unload(self):
        # pray it closes
        self.bot.loop.create_task(self.session.close())

    async def update(self):

        payload = json.dumps({
            'server_count': len(self.bot.guilds)
        })

        ## DISCORD BOTS ORG ##
        headers = {
            'authorization': DISCORDBOTS_ORG_TOKEN,
            'content-type' : 'application/json'
        }
        url = '{0}/bots/{1.user.id}/stats'.format(DISCORD_BOTS_ORG_API, self.bot)
        async with self.session.post(url, data=payload, headers=headers) as resp:
            self.bot.logger.info('discordbots.org statistics returned {0.status} for {1}'.format(resp, payload))

    @commands.Cog.listener()
    async def on_guild_join(self, server):
        self.bot.logger.info("## New server {name} + {members} members ##".format(name=server.name, members=server.member_count))
        await self.update()

    @commands.Cog.listener()
    async def on_guild_remove(self, server):
        self.bot.logger.info("## Server removed {name} - {members} members ##".format(name=server.name, members=server.member_count))
        await self.update()

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(60*2)  # To be sure we see everyone
        await self.update()


def setup(bot):
    bot.add_cog(Carbonitex(bot))
