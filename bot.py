#!/usr/bin/python3

import os
import argparse

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

##### argparse
parser = argparse.ArgumentParser()
parser.add_argument('--apikey', help='set api key', type=str)
parser.add_argument('--apisec', help='set api secret', type=str)
parser.add_argument('-t', '--testnet', help='use testnet api', action='store_true')

parser.add_argument('-s', '--symbol', help='maker symbol (default BTCUSDT)', type=str, default='BTCUSDT')
parser.add_argument('-l', '--leverage', help='change leverage ratio (default 5)', type=int, default=5)

parser.add_argument('-v', '--verbose', action='store_true')
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
    print("Can not find api key and secret")
    exit()

# open client
client = Client(api_key, api_secret)
print('Connected to Binance')
# change the api endpoint url of the library (because the library does not have support for the demo environment)
if args.testnet:
    client.API_URL = 'https://testnet.binance.vision/api'

##### init trader bot
# get market symbol
symbol = args.symbol
# get fees
trade_fee = client.get_trade_fee(symbol=symbol)
# check if the symbol is available
if len(trade_fee['tradeFee']) != 1:
    print('ERROR: Symbol \'%s\' not found' % symbol)
    exit()
# extract maker and taker fees
maker_trade_fee = float(trade_fee['tradeFee'][0]['maker'])
taker_trade_fee = float(trade_fee['tradeFee'][0]['taker'])
print('Current trade fees on \'%s\': maker:%.4f%%, taker%.4f%%' % (symbol, maker_trade_fee * 100, taker_trade_fee * 100))

# get future account
future_account = client.futures_account()
# check if trade is enabled
if future_account['canTrade'] != True:
    print('ERROR: Trade in future is disabled')
    exit()
# get future balance
available_balance = float(future_account['availableBalance'])
print('Available balance in future: %f USDT' % available_balance)

# set leverage
leverage = args.leverage
change_leverage = client.futures_change_leverage(symbol=symbol, leverage=leverage)
# check if leverage is activated correctly
if change_leverage['leverage'] != leverage:
    print('ERROR: Leverage ratio can not be change')
    exit()
