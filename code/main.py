import asyncio

import discord
from discord.ext.commands import Bot, check

# https://discordapp.com/api/oauth2/authorize?client_id=559341956824825866&permissions=0&scope=bot

PREFIX = "bn "
# Autosave interval is in minutes
autosave_interval = 0.5

client = Bot(command_prefix=PREFIX)

class Server:
    def __init__(self, server, bean_role=None):
        self.bean_role = bean_role
        self.server = server
servers = {}


#client.remove_command("help")
#@client.command(pass_context=True)
#async def help(ctx, *args):
#    pass

@client.command()
async def ping():
    await client.say("pong!")

@client.command(pass_context=True)
async def config(ctx, *args):
    mentions = ctx.message.role_mentions
    print(mentions)
    if mentions == []:
        await client.say("Please mention a role")
        return

    elif not isinstance(mentions[0], discord.Role):
        await client.say("Hmmm, that's not a role....")

    else:
        servers[ctx.message.server] = Server(ctx.message.server, mentions[0])
        await client.say(f"Successfully assigned {mentions[0].name} role to the bean role")
        return

async def save():
    try:
        os.remove("../data/servers.dat")
    except FileNotFoundError:
        pass
    f = open("../data/servers.dat", "wb+")
    pickle.dump(servers, f)
    f.close()

async def reload():
    try:
        f = open("../data/servers.dat", "rb")
    except Exception:
        print("reloading error - no save detected, ignore this error")

    else:
        servers.clear()
        servers.update(pickle.load(f))
        f.close()
        print('reloaded')

async def loop():
    await client.wait_until_ready()
    autosave_counter = 0
    while not client.is_closed:
        await asyncio.sleep(5.0)

        autosave_counter += 1
        if autosave_counter * 5 >= autosave_interval * 60:
            autosave_counter = 0
            await save()

@client.event
async def on_ready():
    print("BeanBot is in operation!")

    await reload()

    await client.change_presence(game=discord.Game(name='beans!!!'))

if __name__ == "__main__":
    # Will try and get a token from code/token.txt
    # If this fails (file does not exist) then it asks for the token and creates the file
    try:
        f = open("../data/token.txt")
    except FileNotFoundError:
        print("Failed to find ../data/token.txt, please make sure the file exists")
    else:
        token = f.read()
        f.close()
        client.loop.create_task(loop())
        client.run(token)
