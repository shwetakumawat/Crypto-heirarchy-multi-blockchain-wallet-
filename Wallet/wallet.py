# Import dependencies
import subprocess
import json
from dotenv import load_dotenv

# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Import constants.py and necessary functions from bit and web3
# YOUR CODE HERE
from constants import * 
import bit
from bit.network import NetworkAPI
from web3 import Web3
from web3.middleware import geth_poa_middleware
import os
import lit
from eth_account import Account

# Sets environment variables
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
 
# Create a function called `derive_wallets`
def derive_wallets(coin):
    cols = 'address,index,path,privkey,pubkey,pubkeyhash,xprv,xpub'
    command = f'derive --mnemonic=mnemonic --cols={cols} --coin={coin} --numderive=3 --format=json -g'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {BTCTEST: derive_wallets(BTCTEST), ETH: derive_wallets(ETH)}

# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return bit.PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        account =  priv_key_to_account(coin, account)
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "chainID": 777,
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }, account
    elif coin == BTCTEST:
        account = priv_key_to_account(coin, account)
        return bit.PrivateKeyTestnest.prepare_transaction(account.address, [(recipient, amount, BTC)]), account

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    tx, account = create_tx(coin, account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    if coin == ETH:
        result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return result
    elif coin == BTCTEST:
        result = NetworkAPI.broadcast_tx_testnet(signed_tx)
        return result
