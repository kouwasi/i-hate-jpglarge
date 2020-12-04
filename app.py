import discord
from dotenv import load_dotenv
import os, tempfile, io, aiohttp

load_dotenv()
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author.bot and message.attachments is None:
        return

    for attachment in message.attachments:
        file_extension = attachment.filename.split('.')[-1]

        if file_extension != 'jpglarge':
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                if resp.status != 200:
                    return await channel.send('Could not download file...')

                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, attachment.filename.replace('jpglarge', 'jpg')))

client.run(os.environ['DISCORD_TOKEN'])