import asyncio

import discord
from discord.ext.commands import Bot, check

# https://discordapp.com/api/oauth2/authorize?client_id=559341956824825866&permissions=0&scope=bot

PREFIX = "bn "
client = Bot(command_prefix=PREFIX)


class Server:
    def __init__(self, bean_role):
        self.bean_role = bean_role
servers = []


@client.command()
async def ping():
    await client.say("pong!")

@client.command(pass_context=True)
async def config(ctx, *args):
    mentions = ctx.message.
#client.remove_command("help")
#@client.command(pass_context=True)
#async def help(ctx, *args):
#    pass

#@client.command(pass_context=True, aliases=["flip", "f", "cf"])
#async def coinflip(ctx, *args):


@client.event
async def on_ready():
    print("BeanBot is in operation!")
    await client.change_presence(game=discord.Game(name='beans!!!'))

if __name__ == "__main__":
    # Will try and get a token from code/token.txt
    # If this fails (file does not exist) then it asks for the token and creates the file
    try:
        f = open("../data/token.txt")
    except FileNotFoundError:
        token = input("Please input the Discord Token: ")
        f = open("../data/token.txt", "w+")
        f.write(token)
    else:
        token = f.read()
    finally:
        f.close()
        #client.loop.create_task(loop())
        client.run(token)
