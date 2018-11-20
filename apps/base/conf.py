import os

from django.conf import settings
from appconf import AppConf
    

class ICOConf(AppConf):
    TOKEN_NAME = os.getenv("TOKEN_NAME")
    TOKEN_SYMBOL = os.getenv("TOKEN_SYMBOL").upper()
    TOKEN_TOTAL_SUPPLY = int(os.getenv("TOKEN_TOTAL_SUPPLY"))
    TOKEN_DECIMALS = float(os.getenv("TOKEN_DECIMALS"))
    STAGE = os.getenv("STAGE").upper()
    START = os.getenv("START")
    END = os.getenv("END")
    PRICE = float(os.getenv("PRICE")) # in dollars
    BONUS = float(os.getenv("BONUS")) # in percentage
    DAILY_CAP_PER_ACCOUNT = int(os.getenv("DAILY_CAP_PER_ACCOUNT")) # in tokens
    MINIMUM_PURCHASE = float(os.getenv("MINIMUM_PURCHASE"))
    SOFTCAP = float(os.getenv("SOFTCAP")) # in dollars
    HARDCAP = float(os.getenv("HARDCAP")) # in dollars
    TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
    TOKEN_OWNER_PRIVATE_KEY = os.getenv("TOKEN_OWNER_PRIVATE_KEY")
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