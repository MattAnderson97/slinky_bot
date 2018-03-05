import asyncio
import discord
import time

import rss.feed_monitor as feed_monitor, setup, settings

client = discord.Client()


async def watch_rss():
    print("watching rss feed")
    while not client.is_closed:
        entries = feed_monitor.get_new_entries()
        for entry in entries:
            await send_feed(entry)
        time.sleep(600)

@client.event
async def on_ready():
    print("bot logged in")
    client.loop.create_task(watch_rss())


@client.event
async def on_member_join(member: discord.Member):
    if (member.bot):
        return
    else:
        await client.add_roles(member, discord.utils.get(member.server.roles, name="kwargs"))


async def send_feed(entry):
    embed = discord.embeds.Embed(title="{}[{}] {}".format(entry.title, entry.link, entry.published), colour=discord.Colour.green(), description="{}".format(entry.author))
    await client.send_message(client.get_channel("419632912690970624"), embed=embed)


if __name__ == "__main__":
    client.run(settings.TOKEN)