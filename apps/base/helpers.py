from datetime import datetime

from django.db.models import Sum
from django.utils import timezone

from .models import Transaction
from .conf import settings

import os
import json


def _init_web3():
    from web3 import Web3, HTTPProvider

    if settings.ICO_ACTIVENET == 'testnet':
        return Web3(HTTPProvider(settings.ICO_TESTNET_URL))
    elif settings.ICO_ACTIVENET == 'mainnet':
        return Web3(HTTPProvider(settings.ICO_MAINNET_URL))


def _init_token_contract():
    web3 = _init_web3()

    with open(os.path.join(settings.BASE_DIR, 'token.abi'), 'r') as abi_definition:
        abi = json.load(abi_definition)

    return web3.eth.contract(address=settings.ICO_TOKEN_ADDRESS, abi=abi)


def create_account(password):
    web3 = _init_web3()
    return web3.eth.account.create(password)


def get_token_balance(address):
    token_contract = _init_token_contract()
    from decimal import Decimal
    return float(Decimal(token_contract.functions.balanceOf(address).call() / (10 ** settings.ICO_TOKEN_DECIMALS)))


def is_ongoing():
    start = datetime.strptime(settings.ICO_START, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    end = datetime.strptime(settings.ICO_END, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    tokens_sold = Transaction.objects.filter(
        status="confirmed"
    ).aggregate(sold=Sum('amount'))['sold'] or 0.0

    return start <= timezone.now() <= end and (tokens_sold * settings.ICO_PRICE) < settings.ICO_HARDCAP


def is_ended():
    end = datetime.strptime(settings.ICO_END, '%Y-%m-%d').replace(tzinfo=timezone.utc)

    return end < timezone.now() and not is_ongoing()


def calculate_bought(amount):
    bought = (amount / settings.ICO_PRICE)
    bought += (settings.ICO_BONUS / 100 * bought)

    return bought


def get_rate(currency):
    import requests

    dollar_rate = float()

    settings.ICO_ACTIVENET == 'mainnet':
        dollar_rate = float(requests.get(
            f'https://api.coinbase.com/v2/prices/{currency.upper()}-USD/buy'
        ).json()['data']['amount'])

    return dollar_rate


def transfer_tokens(user, amount):
    amount = float(amount)

    web3 = _init_web3()
    token_contract = _init_token_contract()

    owner_address = web3.eth.account.privateKeyToAccount(
        settings.ICO_TOKEN_OWNER_PRIVATE_KEY
    ).address

    send_token_txn = token_contract.functions.transfer(
        user.address,
        int(amount * 10 ** settings.ICO_TOKEN_DECIMALS),
    ).buildTransaction({
        'chainId': {
            'testnet': 3,
            'mainnet': 1
        }[settings.ICO_ACTIVENET],
        'gas': 1000000,
        'gasPrice': web3.eth.gasPrice,
        'nonce': web3.eth.getTransactionCount(owner_address)
    })

    signed = web3.eth.account.signTransaction(
        send_token_txn,
        settings.ICO_TOKEN_OWNER_PRIVATE_KEY
    )

    tx_hash = web3.toHex(web3.eth.sendRawTransaction(signed.rawTransaction))

    return tx_hash

