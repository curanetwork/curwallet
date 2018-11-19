import os
import json

from django.conf import settings
from appconf import AppConf
    

class ICOConf(AppConf):
    TOKEN_ABI = json.load(os.getenv("TOKEN_ABI"))
    TOKEN_NAME = os.getenv("TOKEN_NAME")
    TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL")
    TOKEN_TOTAL_SUPPLY = os.getenv("TOKEN_TOTAL_SUPPLY")
    TOKEN_DECIMALS = os.getenv("TOKEN_DECIMALS")
    STAGE = os.getenv("STAGE")
    START = os.getenv("START")
    END = os.getenv("END")
    PRICE = os.getenv("PRICE") # in dollars
    BONUS = os.getenv("BONUS") # in percentage
    DAILY_CAP_PER_ACCOUNT = os.getenv("DAILY_CAP_PER_ACCOUNT")
    MINIMUM_PURCHASE = os.getenv("MINIMUM_PURCHASE")
    SOFTCAP = os.getenv("SOFTCAP") # in dollars
    HARDCAP = os.getenv("HARDCAP") # in dollars
    TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
    TOKEN_OWNER_PRIVATE_KEY = os.getenv("TOKEN_ADDRESS")
    CURRENCIES = (
    	('BTC', 'Bitcoin'),
    	('ETH', 'Ethereum'),
        ('LTC', 'Litecoin'),
        ('BCH', 'Bitcoin Cash')
    )
    ACTIVENET = os.getenv("ACTIVENET") # testnet or mainnet
    TESTNET_URL = 'https://ropsten.infura.io/' + os.getenv("INFURA_API_KEY")
    MAINNET_URL = 'https://mainnet.infura.io/' + os.getenv("INFURA_API_KEY")
    COINBASE_API_KEY = os.getenv("COINBASE_API_KEY")
    COINBASE_WEBHOOK_SECRET = os.getenv("COINBASE_WEBHOOK_SECRET")

    class Meta:
        prefix = 'ico'