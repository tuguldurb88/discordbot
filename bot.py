import discord
from discord.ext import commands
import responses
import random
import ollama

intents = discord.Intents.default()
intents.message_content = True  # Subscribe to message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response:  # Check if the response is not empty
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    user_message = str(message.clean_content)
    if not user_message:  # Ignore empty messages
        return
    
    is_private = message.channel.type == discord.ChannelType.private
        

    if user_message[0] == '?':
        user_message = user_message[1:]
        await send_message(message, user_message, is_private=True)
    else:
        await send_message(message, user_message, is_private)

    await bot.process_commands(message)

@bot.command(name='rps', help='Play rock-paper-scissors')
async def rps(ctx, *, user_choice: str):
    choices = ["rock", "paper", "scissors"]
    if user_choice.lower() not in choices:
        await ctx.send("Invalid choice. Please choose rock, paper, or scissors.")
        return

    bot_choice = random.choice(choices)
    if user_choice.lower() == bot_choice:
        await ctx.send(f"Bot chose {bot_choice}. It's a tie!")
    elif (user_choice.lower() == "rock" and bot_choice == "scissors") or (user_choice.lower() == "scissors" and bot_choice == "paper") or (user_choice.lower() == "paper" and bot_choice == "rock"):
        await ctx.send(f"Bot chose {bot_choice}. You win!")
    else:
        await ctx.send(f"Bot chose {bot_choice}. You lose!")

@bot.command(name='ask')
async def ask(ctx, *, message):
    print(message)
    print("===============")
    response = ollama.chat(model='deepseek-r1', messages=[
        {
            'role': 'system',
            'content': 'You are a helpful assistant who provides answers to questions concisely in no more than 1000 words.',
        },
        {
            'role': 'user',
            'content': message,
        },
    ])
    
    response_content = response['message']['content']
    print(response_content)

    # Remove <think> sections if present
    if '<think>' in response_content:
        parts = response_content.split('<think>')
        filtered_parts = []
        for part in parts:
            if '</think>' in part:
                filtered_parts.append(part.split('</think>')[1])
            else:
                filtered_parts.append(part)
        response_content = ''.join(filtered_parts)

    # Check if the response exceeds 2000 characters
    if len(response_content) > 2000:
        for i in range(0, len(response_content), 2000):
            chunk = response_content[i:i + 2000]
            await ctx.send(chunk)  # Send each chunk
    else:
        await ctx.send(response_content)  # Send the full response if it's within the limit

@bot.command(name='rand', help='Get a random ASCII art picture')
async def ascii(ctx):
    ascii_pictures = [
    
        """
 Deez nuts
""",
        """

────█▀█▄▄▄▄─────██▄
────█▀▄▄▄▄█─────█▀▀█
─▄▄▄█─────█──▄▄▄█
██▀▄█─▄██▀█─███▀█
─▀▀▀──▀█▄█▀─▀█▄█▀

""",
        """
───▄▀▀▀▄▄▄▄▄▄▄▀▀▀▄───
───█▒▒░░░░░░░░░▒▒█───
────█░░█░░░░░█░░█────
─▄▄──█░░░▀█▀░░░█──▄▄─
█░░█─▀▄░░░░░░░▄▀─█░░█
""",


        """
x⠄⠄⠄⠄⠄⠄⠄⠄⢀⣠⣴⣶⣶⡶⠤⣄⠄⠄⠄⠄⢀⣤⣴⣶⣶⣦⡀⠄⠄x 
x⠄⠄⠄⠄⠄⠄⣠⣶⣿⣿⣿⣿⣯⣶⣷⣌⠳⣄⠄⣴⣿⣿⣿⣿⣏⢻⡇⠄⠄x 
x⠄⠄⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⡿⣫⣭⡍⠙⢻⣿⣍⢵⣶⡞⠉⢹⣾⡇⠄⠄x 
x⠄⠄⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣼⠿⢿⡷⠾⣳⣿⡿⢷⣽⣻⣤⣿⣿⠃⠄⠄x 
x⠄⠄⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⣋⣿⣿⣦⣽⣿⣿⣿⠇⠄⠄⠄x 
x⠄⠄⠄⠄⢀⣿⣿⣿⣿⣿⡿⠿⠛⠛⠛⠛⠛⠛⠛⣛⣉⣉⣙⡛⠛⠄⠄⠄⠄x 
x⠄⠄⠄⢀⣾⣿⣿⣿⣿⡇⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠄⠄⠄x 
x⠄⠄⢠⣿⣿⣿⣿⣿⣿⣧⠸⢿⣿⣥⣤⣤⣬⣉⣉⣉⣉⣉⣭⣩⣥⣤⣤⠄⠄x 
x⠄⠄⣸⣿⣿⣿⣿⣿⣿⣿⣷⣦⣌⣙⠛⠻⠿⠿⠿⡿⢿⣿⠿⢿⠿⠿⠟⠄⠄x 
x⠰⠄⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⠆⠄⠄⠄⠄⠄x 
x⠈⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣉⠛⠛⠛⢋⣹⣿⣿⣿⠏⠄⠄⠄⠄⠄⠄x 
x⠄⠄⠄⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠄⠄⠄⠄⠄⠄⠄x 
x⠄⠄⢀⣶⣶⣦⣬⣍⣉⣛⣛⠛⠛⠛⠛⠛⠛⢋⣉⣤⣾⣦⠄⠄⠄⠄⠄⠄⠄x

""",

"""
⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⣛⣛⣛⣩⣭⣭⣉⣉⣉⣙⠛⠿⣿⣿⣿⣿⣿ 
⣿⣿⣿⣿⠿⢛⣩⣴⣶⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⡿⡿⡿⠷⣌⠻⣿⣿⣿ 
⣿⣿⣿⢏⠔⣛⢛⣻⢿⣿⣿⣿⠁⡿⡿⠿⠟⠛⣡⠴⠻⣯⠳⣎⢣⠙⣿⣿ 
⣿⣿⡏⡌⣾⢣⡞⣩⡝⣦⢰⢤⣾⣿⣟⢦⠰⡞⣿⣘⣋⣿⢀⣿⢻⡇⢹⣿ 
⣿⣿⡇⢇⢿⣄⠻⣤⠶⣋⣼⣿⣿⣿⣿⣮⣷⣼⣮⣛⣻⣥⣾⢏⣼⠁⣿⣿ 
⣿⣿⣷⢸⣶⣭⣭⣶⣾⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢁⣾⡛⢸⣿⣿ 
⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⡞⣵⡇⣾⣿⣿ 
⣿⣿⣿⣿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⡇⣿⢱⣿⣿⣿ 
⣿⣿⣿⣿⣇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⡄⣿⡏⢸⣿⣿⣿ 
⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢛⠺⣿⡿⣿⣿⡇⣸⣿⣿⣿ 
⣿⣿⣿⣿⣿⡆⢻⣿⣿⣿⡔⠲⠶⠶⠶⢶⣄⢿⣷⣌⠳⣿⣿⢡⣿⣿⣿⣿ 
⣿⣿⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡉⢻⣷⢌⠛⢌⢹⣿⣿⣿ 
⣿⣿⣿⡿⢋⡴⣯⢻⣿⣿⣿⣿⣿⣿⡟⢉⣾⣿⣿⣦⣝⢻⣻⣿⡦⠙⢻⣿ 
⣿⣿⡏⢰⣭⣾⣾⡚⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣜⠛⣛⡓⠚⣸⣿
""",

        """
⣿⡇⣿⣿⣿⠛⠁⣴⣿⡿⠿⠧⠹⠿⠘⣿⣿⣿⡇⢸⡻⣿⣿⣿⣿⣿⣿⣿ 
⢹⡇⣿⣿⣿⠄⣞⣯⣷⣾⣿⣿⣧⡹⡆⡀⠉⢹⡌⠐⢿⣿⣿⣿⡞⣿⣿⣿ 
⣾⡇⣿⣿⡇⣾⣿⣿⣿⣿⣿⣿⣿⣿⣄⢻⣦⡀⠁⢸⡌⠻⣿⣿⣿⡽⣿⣿ 
⡇⣿⠹⣿⡇⡟⠛⣉⠁⠉⠉⠻⡿⣿⣿⣿⣿⣿⣦⣄⡉⠂⠈⠙⢿⣿⣝⣿ 
⠤⢿⡄⠹⣧⣷⣸⡇⠄⠄⠲⢰⣌⣾⣿⣿⣿⣿⣿⣿⣶⣤⣤⡀⠄⠈⠻⢮ 
⠄⢸⣧⠄⢘⢻⣿⡇⢀⣀⠄⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠄⢀ 
⠄⠈⣿⡆⢸⣿⣿⣿⣬⣭⣴⣿⣿⣿⣿⣿⣿⣿⣯⠝⠛⠛⠙⢿⡿⠃⠄⢸ 
⠄⠄⢿⣿⡀⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⡾⠁⢠⡇⢀ 
⠄⠄⢸⣿⡇⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣫⣻⡟⢀⠄⣿⣷⣾ 
⠄⠄⢸⣿⡇⠄⠈⠙⠿⣿⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⡿⢠⠊⢀⡇⣿⣿ 
⠒⠤⠄⣿⡇⢀⡲⠄⠄⠈⠙⠻⢿⣿⣿⠿⠿⠟⠛⠋⠁⣰⠇⠄⢸⣿⣿⣿ 
⠄⠄⠄⣿⡇⢬⡻⡇⡄⠄⠄⠄⡰⢖⠔⠉⠄⠄⠄⠄⣼⠏⠄⠄⢸⣿⣿⣿ 
⠄⠄⠄⣿⡇⠄⠙⢌⢷⣆⡀⡾⡣⠃⠄⠄⠄⠄⠄⣼⡟⠄⠄⠄⠄⢿⣿⣿
""",

        """
⣇⣿⠘⣿⣿⣿⡿⡿⣟⣟⢟⢟⢝⠵⡝⣿⡿⢂⣼⣿⣷⣌⠩⡫⡻⣝⠹⢿⣿⣷ 
⡆⣿⣆⠱⣝⡵⣝⢅⠙⣿⢕⢕⢕⢕⢝⣥⢒⠅⣿⣿⣿⡿⣳⣌⠪⡪⣡⢑⢝⣇ 
⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕⢽ 
⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕⢕ 
⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱⢕ 
⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀⢕ 
⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗⢄ 
⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕⢕ 
⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵⣿ 
⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ 
⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟ 
⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁⣠ 
⡝⡵⡈⢟⢕⢕⢕⢕⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠿⠋⣀⣈⠙ 
⡝⡵⡕⡀⠑⠳⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⡠⡲⡫⡪⡪⡣
""",

"""
⠄⠄⠄⠄ ⠄⠄⠄⠄ ⠄⠄⠄⠄
⠄⠄⡔⠙⠢⡀⠄⠄⠄⢀⠼⠅⠈⢂⠄⠄⠄⠄ 
⠄⠄⡌⠄⢰⠉⢙⢗⣲⡖⡋⢐⡺⡄⠈⢆⠄⠄⠄ 
⠄⡜⠄⢀⠆⢠⣿⣿⣿⣿⢡⢣⢿⡱⡀⠈⠆⠄⠄ 
⠄⠧⠤⠂⠄⣼⢧⢻⣿⣿⣞⢸⣮⠳⣕⢤⡆⠄⠄ 
⢺⣿⣿⣶⣦⡇⡌⣰⣍⠚⢿⠄⢩⣧⠉⢷⡇⠄⠄ 
⠘⣿⣿⣯⡙⣧⢎⢨⣶⣶⣶⣶⢸⣼⡻⡎⡇⠄⠄ 
⠄⠘⣿⣿⣷⡀⠎⡮⡙⠶⠟⣫⣶⠛⠧⠁⠄⠄⠄ 
⠄⠄⠘⣿⣿⣿⣦⣤⡀⢿⣿⣿⣿⣄⠄⠄⠄⠄⠄ 
⠄⠄⠄⠈⢿⣿⣿⣿⣿⣷⣯⣿⣿⣷⣾⣿⣷⡄⠄ 
⠄⠄⠄⠄⠄⢻⠏⣼⣿⣿⣿⣿⡿⣿⣿⣏⢾⠇⠄ 
⠄⠄⠄⠄⠄⠈⡼⠿⠿⢿⣿⣦⡝⣿⣿⣿⠷⢀⠄ 
⠄⠄⠄⠄⠄⠄⡇⠄⠄⠄⠈⠻⠇⠿⠋⠄⠄⢘⡆ 
⠄⠄⠄⠄⠄⠄⠱⣀⠄⠄⠄⣀⢼⡀⠄⢀⣀⡜⠄ 
⠄⠄⠄⠄⠄⠄⠄⢸⣉⠉⠉⠄⢀⠈⠉⢏⠁⠄⠄ 
⠄⠄⠄⠄⠄⠄⡰⠃⠄⠄⠄⠄⢸⠄⠄⢸⣧⠄⠄ 
⠄⠄⠄⠄⠄⣼⣧⠄⠄⠄⠄⠄⣼⠄⠄⡘⣿⡆⠄ 
⠄⠄⠄⢀⣼⣿⡙⣷⡄⠄⠄⠄⠃⠄⢠⣿⢸⣿⡀ 
⠄⠄⢀⣾⣿⣿⣷⣝⠿⡀⠄⠄⠄⢀⡞⢍⣼⣿⠇ 
⠄⠄⣼⣿⣿⣿⣿⣿⣷⣄⠄⠄⠠⡊⠴⠋⠹⡜⠄ 
⠄⠄⣿⣿⣿⣿⣿⣿⣿⣿⡆⣤⣾⣿⣿⣧⠹⠄⠄ 
⠄⠄⢿⣿⣿⣿⣿⣿⣿⣿⢃⣿⣿⣿⣿⣿⡇⠄⠄ 
⠄⠄⠐⡏⠉⠉⠉⠉⠉⠄⢸⠛⠿⣿⣿⡟⠄⠄⠄
""",

"""
⣿⣿⣿⣿⠛⠛⠉⠄⠁⠄⠄⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿ 
⣿⣿⡟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⣿⣿⣿⣿⣿⣿⣿ 
⣿⣿⡇⠄⠄⠄⠐⠄⠄⠄⠄⠄⠄⠄⠠⣿⣿⣿⣿⣿⣿ 
⣿⣿⡇⠄⢀⡀⠠⠃⡐⡀⠠⣶⠄⠄⢀⣿⣿⣿⣿⣿⣿ 
⣿⣿⣶⠄⠰⣤⣕⣿⣾⡇⠄⢛⠃⠄⢈⣿⣿⣿⣿⣿⣿ 
⣿⣿⣿⡇⢀⣻⠟⣻⣿⡇⠄⠧⠄⢀⣾⣿⣿⣿⣿⣿⣿ 
⣿⣿⣿⣟⢸⣻⣭⡙⢄⢀⠄⠄⠄⠈⢹⣯⣿⣿⣿⣿⣿ 
⣿⣿⣿⣭⣿⣿⣿⣧⢸⠄⠄⠄⠄⠄⠈⢸⣿⣿⣿⣿⣿ 
⣿⣿⣿⣼⣿⣿⣿⣽⠘⡄⠄⠄⠄⠄⢀⠸⣿⣿⣿⣿⣿ 
⡿⣿⣳⣿⣿⣿⣿⣿⠄⠓⠦⠤⠤⠤⠼⢸⣿⣿⣿⣿⣿ 
⡹⣧⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⢇⣓⣾⣿⣿⣿⣿⣿ 
⡞⣸⣿⣿⢏⣼⣶⣶⣶⣶⣤⣶⡤⠐⣿⣿⣿⣿⣿⣿⣿ 
⣯⣽⣛⠅⣾⣿⣿⣿⣿⣿⡽⣿⣧⡸⢿⣿⣿⣿⣿⣿⣿ 
⣿⣿⣿⡷⠹⠛⠉⠁⠄⠄⠄⠄⠄⠄⠐⠛⠻⣿⣿⣿⣿ 
⣿⣿⣿⠃⠄⠄⠄⠄⠄⣠⣤⣤⣤⡄⢤⣤⣤⣤⡘⠻⣿ 
⣿⣿⡟⠄⠄⣀⣤⣶⣿⣿⣿⣿⣿⣿⣆⢻⣿⣿⣿⡎⠝ 
⣿⡏⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⠐ 
⣿⡏⣲⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢇⣿⣿⣿⡟⣼ 
⣿⡠⠜⣿⣿⣿⣿⣟⡛⠿⠿⠿⠿⠟⠃⠾⠿⢟⡋⢶⣿ 
⣿⣧⣄⠙⢿⣿⣿⣿⣿⣿⣷⣦⡀⢰⣾⣿⣿⡿⢣⣿⣿ 
⣿⣿⣿⠂⣷⣶⣬⣭⣭⣭⣭⣵⢰⣴⣤⣤⣶⡾⢐⣿⣿
⣿⣿⣿⣷⡘⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣿⣿⢃⣼⣿⣿ 
⣿⣿⣿⣿⣿⢟⣯⣵⣿⣿⣷⣦⣭⣶⣶
""",

"""
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣛⣩⡭⣬⣭⣍⠙⠻⣿⣿⣿⣿⣿x 
⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣴⢻⣿⣷⢹⣌⢯⢿⠝⢣⡘⣿⣿⣿⣿x 
⣿⣿⣿⣿⣿⣿⣿⣿⢡⣿⣿⣸⣿⣿⣧⢻⠄⠟⠁⠄⠚⠸⣿⣿⣿x 
⣿⣿⣿⣿⢛⣿⠿⣿⢸⢿⣿⣆⢿⣷⠏⢸⠗⠄⣷⢠⡸⢁⢿⣿⣿x 
⣿⣿⣿⣿⣼⡘⡄⣿⢸⢸⣿⠙⠈⠇⣤⣆⣢⡄⣷⠘⢱⡟⠈⡝⣿x 
⣿⣿⣿⡿⢑⢧⡇⢿⢸⡀⠂⡐⢴⣾⣿⣿⣿⡇⡜⠄⡋⢣⣀⣴⡆x 
⣿⣿⣿⣇⢣⣵⣮⢊⣧⢁⡆⠹⠈⠛⠽⠷⠟⠄⡉⢠⠄⣼⣯⡾⠣x 
⣿⣿⣿⣿⡌⣿⢡⣿⡇⡆⡇⠄⠁⠄⠄⣠⣾⢰⠃⡼⢸⣿⢛⣤⣄x 
⣿⣿⣿⣿⢃⣿⠸⣿⡧⣡⢶⠅⠄⢀⡰⣿⣿⠈⠄⠃⣿⡇⢸⣿⣿x 
⣿⣿⣿⡟⣸⠿⢃⣋⣨⣭⠕⣂⣤⣴⣾⣿⣿⣦⣤⢰⣿⡇⡸⣿⡿x 
⣿⣿⡿⢃⣵⣾⣿⣿⡿⣣⣾⣿⣿⣿⣿⣿⣿⣿⡿⢸⣿⡇⠁⢹⠇x 
⡿⢫⣴⣿⣿⣿⣿⡿⢱⣿⣿⣿⠿⣿⣿⣿⣿⣿⢃⣿⣿⡇⡇⠈⢰x 
⣧⠻⣿⣿⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣸⣿⣿⡇⡇⢈⠁x 
⣿⣧⠹⣿⣿⣿⣿⣿⠘⢿⣿⣿⣿⣿⣿⣿⡿⠃⣿⣿⣿⡇⠄⡼⢸x 
⣿⣿⣷⣬⣛⡛⠛⣡⣾⣦⣙⡛⠿⠿⠟⣫⣷⡇⢻⣿⠟⠡⢔⢀⣿x 
⣿⣿⣿⣿⡟⠄⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⡀⣰⠁⣾⢄⣾⣿x 
⣿⣿⡿⣋⠈⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠄⢹⡜⢣⣾⣿⣿x 
⣿⣿⣿⣿⢨⣇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣘⠹⡇⣿⣿⣿
""",

"""
░░░░░░░█▐▓▓░████▄▄▄█▀▄▓▓▓▌█ 
░░░░░▄█▌▀▄▓▓▄▄▄▄▀▀▀▄▓▓▓▓▓▌█ 
░░░▄█▀▀▄▓█▓▓▓▓▓▓▓▓▓▓▓▓▀░▓▌█ 
░░█▀▄▓▓▓███▓▓▓███▓▓▓▄░░▄▓▐█▌ 
░█▌▓▓▓▀▀▓▓▓▓███▓▓▓▓▓▓▓▄▀▓▓▐█ 
▐█▐██▐░▄▓▓▓▓▓▀▄░▀▓▓▓▓▓▓▓▓▓▌█▌ 
█▌███▓▓▓▓▓▓▓▓▐░░▄▓▓███▓▓▓▄▀▐█ 
█▐█▓▀░░▀▓▓▓▓▓▓▓▓▓██████▓▓▓▓▐█ 
▌▓▄▌▀░▀░▐▀█▄▓▓██████████▓▓▓▌█▌ 
▌▓▓▓▄▄▀▀▓▓▓▀▓▓▓▓▓▓▓▓█▓█▓█▓▓▌█▌
█▐▓▓▓▓▓▓▄▄▄▓▓▓▓▓▓█▓█▓█▓█▓▓▓
""",
        # Add more ASCII art pictures here
    ]
    await ctx.send(random.choice(ascii_pictures))

def run_discord_bot():
    TOKEN = ''
    bot.run(TOKEN)
