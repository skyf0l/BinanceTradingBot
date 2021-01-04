#!/usr/bin/python3

import os
import argparse

from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

##### argparse
parser = argparse.ArgumentParser()
parser.add_argument('--apikey', help='set api key', type=str)
parser.add_argument('--apisec', help='set api secret', type=str)
parser.add_argument('-t', '--testnet', help='use testnet api', action='store_true')
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()

##### init client
api_key = None
api_secret = None

# try to get binance keys from environment
if os.environ.get('binance_api_key') is not None:
    api_key = os.environ['binance_api_key']
if os.environ.get('binance_api_secret') is not None:
    api_secret = os.environ['binance_api_secret']
# try to get binance keys from args
if args.apikey != None:
    api_key = args.apikey
if args.apisec != None:
    api_secret = args.apisec
# exit if keys were not found
if api_key is None or api_secret is None:
    print("Cannot find api key and secret")
    exit()

# open client
client = Client(api_key, api_secret)
print("Connected to Binance!")
# change the api endpoint url of the library (because the library does not have support for the demo environment)
if args.testnet:
    client.API_URL = 'https://testnet.binance.vision/api'



print(client.get_account())