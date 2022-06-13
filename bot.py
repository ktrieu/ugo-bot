from dotenv import load_dotenv
import discord

import argparse
import os
import sys
import asyncio

GENERAL_CHANNEL_ID = '822531930384891948'
# Hardcode this, since client.user is not supported in this version
BOT_USER_ID = 985926656684343356

MESSAGE = 'UGO-BOT TEST: ALL EMPLOYEES IGNORE'

EMOTES = {'🍆': 'Eitan', '❓': 'Kevin', '🛏️': 'Justin', '🙆🏻‍♀️': 'Bobby', '💩': 'Lily', '🍠': 'Hanyuan'}

async def get_gen_chan(client: discord.Client) -> discord.TextChannel:
    gen_chan = await client.fetch_channel(GENERAL_CHANNEL_ID)
    if gen_chan is None or not isinstance(gen_chan, discord.TextChannel):
        raise RuntimeError('Could not find general channel.')

    return gen_chan

async def cmd_ping(client: discord.Client):
    gen_chan = await get_gen_chan(client)
    message: discord.Message = await gen_chan.send(MESSAGE)

    for emote in EMOTES.keys():
        await message.add_reaction(emote)

    await client.close()

async def get_last_ping_msg(chan: discord.TextChannel) -> discord.Message:
     async for m in chan.history():
        if m.author.id == BOT_USER_ID and m.content == MESSAGE:
            return m

def compose_check_message(not_present):
    num_avail = len(EMOTES) - len(not_present)
    not_present_lines = '\n'.join(not_present)

    return f'{num_avail}/{len(EMOTES)} available for scrum.\n\nNot available:\n{not_present_lines}'

async def cmd_check(client: discord.Client):
    gen_chan = await get_gen_chan(client)
    last_ping = await get_last_ping_msg(gen_chan)

    not_present = []

    for r in last_ping.reactions:
        if r.count != 2 and r.emoji in EMOTES:
            not_present.append(EMOTES[r.emoji])

    await gen_chan.send(compose_check_message(not_present))

    await client.close()

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', required=True)

ping = subparsers.add_parser('ping')
ping.set_defaults(command=cmd_ping)
check = subparsers.add_parser('check')
check.set_defaults(command=cmd_check)

async def start():
    load_dotenv()
    args = parser.parse_args()

    intents = discord.Intents()
    intents.guilds = True
    intents.messages = True
    client = discord.Client(intents=intents)
    token = os.environ.get('DISCORD_TOKEN', None)
    if not token:
        print('No bot token found. Provide one via the DISCORD_TOKEN environment variable.')
        sys.exit(1)
    await client.login(token)

    await args.command(client)

if __name__ == '__main__':
    asyncio.run(start())

