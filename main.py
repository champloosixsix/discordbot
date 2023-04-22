import discord
from discord import app_commands
import os
import requests
import json
import random
import logging

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
encouragements = ["Hey, don't be sad", "We don't do that here... turn that frown upside down", "Hey kid, you good?", "Hang in there, you're doing great!"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return(quote)

@tree.command(name = "commandname", description = "My first app Command", guild=discord.Object(id=812168543461179393))
async def first_command(interaction):
    await interaction.response.send_message("Hello!")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=812168543461179393))
    print("Ready!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('how big is your ween champ?'):
        await message.channel.send('Champ\'s ween is of monsterous proportions. Trust me, I know')

    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    
    msg=message.content
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(encouragements))

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        await guild.system_channel.send(f'Yo {member.mention}! Welcome to the {guild.name}. Go check out the rules and introduce yourself.')    

client.run('TOKEN', log_handler=handler, log_level=logging.DEBUG)
