import discord
from discord.ext import commands
import pytesseract
from PIL import Image
import io
import aiohttp
from vars import LOGS_BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has successfully connected to Discord!')


def filter_log_lines(text):
    lines = text.split('\n')
    filtered_lines = [line for line in lines if any(
        keyword in line for keyword in ["ERR", "DEBUG", "Error:", "TRC", "WRN"])]
    return '\n'.join(filtered_lines)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # If the message is in a thread under the 'i-need-help' forum channel and contains attachments
    if isinstance(message.channel, discord.Thread) and message.channel.parent.name == '🙋🏻│i-need-help' and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.avif', '.webp')):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status != 200:
                                await message.channel.send('Unable to download the image.')
                                return
                            image_data = await resp.read()

                    image = Image.open(io.BytesIO(image_data))
                    text = pytesseract.image_to_string(image)

                    filtered_text = filter_log_lines(text)

                    if filtered_text:
                        # Send as code block
                        await message.channel.send(f"Extracted log lines containing ERR, DEBUG, TRC, WRN or Error: from {attachment.filename}:")

                        for i in range(0, len(filtered_text), 1900):
                            await message.channel.send(f"{filtered_text[i:i+1900]}")

                except Exception as e:
                    await message.channel.send(f"An error occurred while processing the image: {str(e)}")

    await bot.process_commands(message)

bot.run(LOGS_BOT_TOKEN)
