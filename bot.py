import discord
from discord.ext import commands, tasks
import discord.utils
import discord_slash
from discord_slash.utils.manage_commands import create_option, create_choice
import os, json, asyncio
import urllib.request
import re
import requests
from bs4 import BeautifulSoup
import datetime, math
from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")
with open('settings.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='?', intents=intents)
slash = discord_slash.SlashCommand(bot, sync_commands=True)

# FUNCTIONS
# 
# 
# 

lst = ["no", "never", "not", "gay", "nah", "u"]
def check_word(str, lst):
    for i in range(len(lst)):
        if f' {lst[i]} ' in str.lower() or str.lower().endswith(f' {lst[i]}') or str.lower().startswith(f'{lst[i]} ') or str.lower() == lst[i]:
            return lst[i]
    return None

async def update_member():
    await bot.wait_until_ready()
    while not bot.is_closed():
        guild = jdata["guild"]
        await bot.get_channel(jdata["members-channel"]).edit(name=f"Members: {bot.get_guild(guild).member_count - 7}")
        await asyncio.sleep(600)
bot.loop.create_task(update_member())

# EVENTS
# 
# 
# 

@bot.event
async def on_ready():
    print('\n\n\n>> Bot is online <<')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Trespasser")
    await member.add_roles(role)
    await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} joined and Trespasser given')
    print(f'{member} joined!')

@bot.event
async def on_member_remove(member):
    await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} left')
    print(f'{member} left!')

@bot.event
async def on_message(msg):
    if 'apple' in msg.content.lower() and msg.author != bot.user:
        await msg.channel.send('Yes. Apple.')

    skrub_role = discord.utils.get(msg.author.guild.roles, id=683546760525906015)
    word = check_word(msg.content, lst)
    if word != None and msg.author != bot.user and (skrub_role in msg.author.roles):
        guild = msg.author.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await msg.author.add_roles(mutedRole, reason=f'This naughty kid said "{word}"')
        await msg.channel.send(f"Muted {msg.author.mention} for... saying \"{word}\" :\\")
        await asyncio.sleep(3)
        await msg.author.remove_roles(mutedRole)
        await msg.channel.send(f"Unmuted {msg.author.mention}")
    
    with open('settings.json', 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)

    if msg.channel == bot.get_channel(jdata["what-how-channel"]):
        if ('how' in msg.content.lower() or 'what' in msg.content.lower()) and msg.content.lower().endswith('??') and msg.author != bot.user:
            text = msg.content
            text1 = text.replace(' ', '+').replace('?', '')
            html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={text1}')
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            await msg.channel.send(f'https://www.youtube.com/watch?v={video_ids[0]}')
            embed=discord.Embed(title=f"Other results for {text}", color=0x00f900)
            embed.set_author(name="Remu chan", url="https://imgur.com/a/cVfP2En")
            embed.add_field(name=requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_ids[1]}').text.partition('\"title\":\"')[2].partition('\",\"')[0], value=f'https://www.youtube.com/watch?v={video_ids[1]}', inline=False)
            embed.add_field(name=requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_ids[2]}').text.partition('\"title\":\"')[2].partition('\",\"')[0], value=f'https://www.youtube.com/watch?v={video_ids[2]}', inline=False)
            embed.add_field(name=requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_ids[3]}').text.partition('\"title\":\"')[2].partition('\",\"')[0], value=f'https://www.youtube.com/watch?v={video_ids[3]}', inline=False)
            embed.add_field(name=requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_ids[4]}').text.partition('\"title\":\"')[2].partition('\",\"')[0], value=f'https://www.youtube.com/watch?v={video_ids[4]}', inline=False)
            embed.add_field(name=requests.get(f'https://noembed.com/embed?url=https://www.youtube.com/watch?v={video_ids[5]}').text.partition('\"title\":\"')[2].partition('\",\"')[0], value=f'https://www.youtube.com/watch?v={video_ids[5]}', inline=False)
            await msg.channel.send(embed=embed)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{msg.author} wants to know {text}')
    await bot.process_commands(msg)

@bot.event
async def on_raw_reaction_add(payload):
    member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id) 
    msg = await channel.fetch_message(payload.message_id) 
    emoji = payload.emoji.name
    if payload.channel_id == jdata["code-of-conducts"] and payload.message_id == jdata["rules-msg"] and member.top_role == discord.utils.get(member.guild.roles, name="Trespasser"):
        role = discord.utils.get(member.guild.roles, name="Peasant")
        await member.edit(roles=[role])
        await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} reacted to the rules and became a Peasant')
    
    if payload.channel_id == jdata["knighting-ceremonies"] and payload.message_id == jdata["knighting-msg"]:
        if emoji == 'piggy_warrior':
            role = discord.utils.get(member.guild.roles, name="The Royal Warrior")
            await member.add_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was knighted The Royal Warrior')
        elif emoji == 'spinningminecraftsteve':
            role = discord.utils.get(member.guild.roles, name="Pixel Protector")
            await member.add_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was knighted Pixel Protector')
        elif emoji == 'PikaPickaxe':
            role = discord.utils.get(member.guild.roles, name="Bloody Miner")
            await member.add_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was knighted Bloody Miner')

@bot.event
async def on_raw_reaction_remove(payload):
    member = bot.get_guild(payload.guild_id).get_member(payload.user_id)
    channel = bot.get_channel(payload.channel_id) 
    msg = await channel.fetch_message(payload.message_id) 
    emoji = payload.emoji.name
    if payload.channel_id == jdata["code-of-conducts"] and payload.message_id == jdata["rules-msg"]:
        role = discord.utils.get(member.guild.roles, name="Trespasser")
        await member.edit(roles=[role])
        await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} decided not to accept the rules and became a Trespasser')

    if payload.channel_id == jdata["knighting-ceremonies"] and payload.message_id == jdata["knighting-msg"]:
        if emoji == 'piggy_warrior':
            role = discord.utils.get(member.guild.roles, name="The Royal Warrior")
            await member.remove_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was deknighted The Royal Warrior')
        elif emoji == 'spinningminecraftsteve':
            role = discord.utils.get(member.guild.roles, name="Pixel Protector")
            await member.remove_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was deknighted Pixel Protector')
        elif emoji == 'PikaPickaxe':
            role = discord.utils.get(member.guild.roles, name="Bloody Miner")
            await member.remove_roles(role)
            await bot.get_channel(jdata["remu-chan-log"]).send(f'{member} was deknighted Bloody Miner')

# MAINS
# 
# 
# 

@slash.slash(name='ping',description='Get Responded with "Pong" and response time')
async def ping(ctx: discord_slash.SlashContext):
    await ctx.send('Pong')
    await ctx.channel.send('And stfu')
    await ctx.channel.send(f'{round(bot.latency*1000)} (ms)')

@slash.slash(name='hi',description='Get Responded with "hi"')
async def hi(ctx: discord_slash.SlashContext):
    await ctx.send('hi')

# REACT
# 
# 
# 

@slash.slash(name='sup',description='Get Responded with "sup dude"')
async def sup(ctx: discord_slash.SlashContext):
    await ctx.send('sup dude')
    await bot.get_channel(jdata["remu-chan-log"]).send(f'{ctx.author} said sup')

@slash.slash(name='repeat',description='Repeats what the message says',
                options=[
                    create_option(name="msg",description="The context you want the bot to repeat",option_type=3,required=False)
                ])
async def repeat(ctx: discord_slash.SlashContext, msg: str):
    await ctx.send(msg)
    await bot.get_channel(jdata["remu-chan-log"]).send(f'Remu chan repeated \"{msg}\" by {ctx.author}')

@bot.command()
async def l(ctx):
    await ctx.guild.leave()

@slash.slash(name='purge',description='Purges a certain amount of messages',
            options=[
                create_option(name="num",description="The amount of messages the bot needs to delete",option_type=4,required=False)
            ])
async def purge(ctx, num:int):
    await ctx.channel.purge(limit=num+1)
    await bot.get_channel(jdata["remu-chan-log"]).send(f'{num} messages in {ctx.channel.mention} are purged')

@slash.slash(name='rules',description='Declares the rules',)
async def rules(ctx):
    embed=discord.Embed(title="LA PALACE Code of Conduct", description="Core rules", color=0x00f900)
    embed.add_field(name="1. No flaming, scolding, and spamming", value="We dont want the server filled with negativity.", inline=False)
    embed.add_field(name="2. Reduce frequency of inappropriate words", value="We want to make this place a peaceful and pure community.", inline=False)
    embed.add_field(name="3. Respect and follow the moderators' instructions", value="There might be some extra rules, but please follow the mods' instructons and decisions at all times.", inline=False)
    embed.add_field(name="4. Keep the chat topic the same as the channel", value="This helps with channel cleanness, topic continuity, and history tracing.", inline=False)
    embed.add_field(name="5. Last but not least, HAIL DA KING!", value="No explanation. Just Do It ", inline=False)
    await ctx.send(embed=embed)
    await bot.get_channel(jdata["remu-chan-log"]).send(f'rules requested in {ctx.channel.mention}')

@slash.slash(name='meme',description='Sends 3 memes according to the content you want',
            options=[
                create_option(name="content",description="The topic of your meme",option_type=3,required=False)
            ])
async def meme(ctx, content:str):
    URL = f"https://knowyourmeme.com/search?context=images&sort=relevance&q={content.replace(' ','+')}+category_name%3Ameme"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="infinite-scroll-wrapper")
    photo_elements = results.find_all("a", {"class": "photo"})
    await ctx.send(photo_elements[0].find("img")["data-src"])
    await ctx.send(photo_elements[1].find("img")["data-src"])
    await ctx.send(photo_elements[2].find("img")["data-src"])
    await bot.get_channel(jdata["remu-chan-log"]).send(f'{ctx.author} memed {content} in {ctx.guild}')

@slash.slash(name='comp',description='Operates Josh\'s debt',
            options=[
                create_option(name="action",description="what you want to do with Josh's debt",option_type=3,required=True,choices=[
                    create_choice(name="help",value="help"),
                    create_choice(name="set",value="set"),
                    create_choice(name="rate",value="rate"),
                    create_choice(name="add",value="add"),
                    create_choice(name="subtract",value="subtract"),
                    create_choice(name="check",value="check")
                ]),
                create_option(name="content",description="The amount of money",option_type=3,required=False)
            ])
async def comp(ctx, action, *, content=None):
    with open("settings.json", "r") as jsonFile:
        jdata = json.load(jsonFile)

    if action == 'help':
        await ctx.send('Enter \";comp set <amount>\" to set what josh owes rn\nEnter \";comp rate <amount>%\" to set the rate of josh\'s compound to <amount>%\nEnter \";comp add <amount>\" to add an amount to what josh owes\nEnter \";comp subtract <amount>\" to subtract an amount from what josh owes\nEnter \";comp check\" to check how much josh owes')
    
    elif action == 'set':
        jdata["money"] = float(content)
        jdata["compound-datetime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        await ctx.send(f'Josh\'s debt has been set to {jdata["money"]}')
        await ctx.channel.send(f'Current time is {datetime.datetime.now().strftime("%m/%d/%y %H:%M")}')
    elif action == 'rate':
        jdata["rate"] = float(content)
        await ctx.send(f'Josh\'s debt rate has been set to {jdata["rate"]}')
        await ctx.channel.send(f'Current time is {datetime.datetime.now().strftime("%m/%d/%y %H:%M")}')
    
    elif action == 'add':
        format = "%Y-%m-%d"
        original_week = datetime.datetime.strptime(jdata["compound-datetime"], format)
        week_elapsed = datetime.datetime.now().isocalendar()[1] - original_week.isocalendar()[1]
        jdata["money"] = round((float(jdata["money"]) * math.pow((1+int(jdata['rate'])/100), week_elapsed)),2)
        jdata["money"] += float(content)
        jdata["compound-datetime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        await ctx.send(f'Josh\'s debt has been increased to {jdata["money"]}')
        await ctx.channel.send(f'Current time is {datetime.datetime.now().strftime("%m/%d/%y %H:%M")}')
    
    elif action == 'subtract':
        format = "%Y-%m-%d"
        original_week = datetime.datetime.strptime(jdata["compound-datetime"], format)
        week_elapsed = datetime.datetime.now().isocalendar()[1] - original_week.isocalendar()[1]
        jdata["money"] = round((float(jdata["money"]) * math.pow((1+int(jdata['rate'])/100), week_elapsed)),2)
        jdata["money"] -= float(content)
        jdata["compound-datetime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        await ctx.send(f'Josh\'s debt has been decreased to {jdata["money"]}')
        await ctx.channel.send(f'Current time is {datetime.datetime.now().strftime("%m/%d/%y %H:%M")}')
    
    elif action == 'check':
        format = "%Y-%m-%d"
        original_week = datetime.datetime.strptime(jdata["compound-datetime"], format)
        week_elapsed = datetime.datetime.now().isocalendar()[1] - original_week.isocalendar()[1]
        jdata["money"] = round((float(jdata["money"]) * math.pow((1+int(jdata['rate'])/100), week_elapsed)),2)
        jdata["compound-datetime"] = datetime.datetime.now().strftime("%Y-%m-%d")
        await ctx.send(f'Josh\'s debt is currently {jdata["money"]}')
        await ctx.channel.send(f'Josh\'s rate is currently {jdata["rate"]}')
        await ctx.channel.send(f'Last updated time is {jdata["compound-datetime"]}')
        await ctx.channel.send(f'Current time is {datetime.datetime.now().strftime("%m/%d/%y %H:%M")}')


    with open("settings.json", "w") as jsonFile:
        json.dump(jdata, jsonFile, indent=4)

# 
#     RUN BOT
# 
# 

if __name__ == '__main__':
    try:
        bot.run(os.environ["BOTTOKEN"])
    except:
        bot.run(token)

