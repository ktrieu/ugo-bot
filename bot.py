from dotenv import load_dotenv
import discord

import argparse
import os
import sys
import asyncio

GENERAL_CHANNEL_ID = '822531930384891948'

MESSAGE = 'UGO-BOT TEST: ALL EMPLOYEES IGNORE'

EMOTE_LIST = ['🍆', '❓', '🛏️', '🙆🏻‍♀️', '💩', '🍠']

async def cmd_ping(client: discord.Client):
    gen_chan = await client.fetch_channel(GENERAL_CHANNEL_ID)
    if gen_chan is None:
        raise RuntimeError('Could not find general channel.')

    message: discord.Message = await gen_chan.send(MESSAGE)

    for emote in EMOTE_LIST:
        await message.add_reaction(emote)

    await client.close()


def cmd_check(client: discord.Client):
    print("Checking...")

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

