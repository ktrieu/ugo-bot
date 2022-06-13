from dotenv import load_dotenv

import argparse
import sys

def cmd_ping():
    print("Pinging...")

def cmd_check():
    print("Checking...")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command', required=True)

ping = subparsers.add_parser('ping')
ping.set_defaults(command=cmd_ping)
check = subparsers.add_parser('check')
check.set_defaults(command=cmd_check)

if __name__ == '__main__':
    load_dotenv()
    args = parser.parse_args()

    args.command()


