from web3 import Web3
from eth_account import Account  # Import thư viện eth_account
import time
from web3.middleware import geth_poa_middleware
from web3 import Web3


# load the contract ABI and address

abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "spender",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Approval",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "value",
                "type": "uint256",
            },
        ],
        "name": "Transfer",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "owner", "type": "address"},
            {"internalType": "address", "name": "spender", "type": "address"},
        ],
        "name": "allowance",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "approve",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"},
        ],
        "name": "decreaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "spender", "type": "address"},
            {"internalType": "uint256", "name": "addedValue", "type": "uint256"},
        ],
        "name": "increaseAllowance",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "from", "type": "address"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "amount", "type": "uint256"},
        ],
        "name": "transferFrom",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


w3 = Web3(Web3.HTTPProvider("https://1rpc.io/sepolia"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

private_key = "cffff36bfff02a0f3b121cf67bf2784101aa73c6333921691f06cc75fcf6d579"

private_key_sendETH = "f2d542b369a3fb1181f0e63bccf5161023f86cebeb5cf07751706aaa3fbca675"

address_hack_wallet = "0xF9Ff24b5e7792b7162F42FfeE5e586700ec4eC58"

hack_wallet_address = "0xF9Ff24b5e7792b7162F42FfeE5e586700ec4eC58"

account = Account.from_key(private_key)

accountSendETH = Account.from_key(private_key_sendETH)

nonce = w3.eth.get_transaction_count(accountSendETH.address, "pending")

# nonce2 = w3.eth.get_transaction_count(account.address, "pending")


w3.eth.default_account = account.address

# token
address = "0x91C16c2f4B318fE67c752A1F6E31e0F989FA8985"

safe_address = "0xC77E5F3B7099bA3b3A4b20292d010696b97177fc"

contract = w3.eth.contract(address=address, abi=abi)


def send_transaction(func):
    tx = func.build_transaction(
        {"nonce": w3.eth.get_transaction_count(account.address)}
    )
    tx_create = w3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt


def checkBalance():
    balance = contract.functions.balanceOf(account.address).call()
    return balance


def approve(address_approve, amount):
    tx_receipt = send_transaction(contract.functions.approve(address_approve, amount))
    return tx_receipt


def transfer(address_transfer, amount):
    tx_receipt = send_transaction(contract.functions.transfer(address_transfer, amount))
    return tx_receipt


def get_eth_balance():
    return w3.eth.get_balance(account.address)


def transfer_all_tokens_if_possible(token_balance):
    # Xây dựng giao dịch để chuyển token
    tx_receipt = contract.functions.transfer(safe_address, token_balance)

    return tx_receipt


def main():
    print("Running...")
    flag = True

    token_balance = checkBalance()

    # transfer eth
    tx = {
        "nonce": nonce,
        "to": hack_wallet_address,
        "value": w3.to_wei(0.3, "ether"),
        "gas": 100000,
        "gasPrice": w3.to_wei("100", "gwei"),
    }

    signed_tx = w3.eth.account.sign_transaction(tx, private_key_sendETH)
    print("Sending ETH...")
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Sent ETH. Transaction hash:", tx_hash.hex())
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # transfer token
    print("Sending token...")
    tx2 = contract.functions.transfer(safe_address, token_balance).build_transaction(
        {
            "nonce": w3.eth.get_transaction_count(account.address, "pending"),
            "gas": 90000,
            "gasPrice": w3.to_wei("70", "gwei"),
        }
    )

    tx_create2 = w3.eth.account.sign_transaction(tx2, private_key=private_key)
    tx_hash2 = w3.eth.send_raw_transaction(tx_create2.rawTransaction)
    print("Sent token. Transaction hash:", tx_hash2.hex())
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # while flag:
    #     try:
    #         tx_receipt = transfer(safe_address, token_balance)

    #     except Exception as e:
    #         print("An error occurred:", str(e))

    print("Done.")


main()
