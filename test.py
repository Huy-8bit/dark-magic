from web3 import Web3
from eth_account import Account
import json
from eth_account.messages import encode_defunct
from eth_account.messages import encode_structured_data

# Initialize Web3 connection
web3 = Web3(Web3.HTTPProvider("https://rpc1.sepolia.org"))

# ABI definitions (assuming they are filled in JavaScript code)
erc20ABI = [
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
abiMinimalForwarder = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [], "name": "InvalidShortString", "type": "error"},
    {
        "inputs": [{"internalType": "string", "name": "str", "type": "string"}],
        "name": "StringTooLong",
        "type": "error",
    },
    {"anonymous": False, "inputs": [], "name": "EIP712DomainChanged", "type": "event"},
    {
        "inputs": [],
        "name": "eip712Domain",
        "outputs": [
            {"internalType": "bytes1", "name": "fields", "type": "bytes1"},
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "version", "type": "string"},
            {"internalType": "uint256", "name": "chainId", "type": "uint256"},
            {"internalType": "address", "name": "verifyingContract", "type": "address"},
            {"internalType": "bytes32", "name": "salt", "type": "bytes32"},
            {"internalType": "uint256[]", "name": "extensions", "type": "uint256[]"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "gas", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "internalType": "struct MinimalForwarder.ForwardRequest",
                "name": "req",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
        ],
        "name": "execute",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"},
            {"internalType": "bytes", "name": "", "type": "bytes"},
        ],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "from", "type": "address"}],
        "name": "getNonce",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {
                "components": [
                    {"internalType": "address", "name": "from", "type": "address"},
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "uint256", "name": "value", "type": "uint256"},
                    {"internalType": "uint256", "name": "gas", "type": "uint256"},
                    {"internalType": "uint256", "name": "nonce", "type": "uint256"},
                    {"internalType": "bytes", "name": "data", "type": "bytes"},
                ],
                "internalType": "struct MinimalForwarder.ForwardRequest",
                "name": "req",
                "type": "tuple",
            },
            {"internalType": "bytes", "name": "signature", "type": "bytes"},
        ],
        "name": "verify",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
]

# Contract addresses
erc20Address = "0x91C16c2f4B318fE67c752A1F6E31e0F989FA8985"
minimalForwarderAddress = "0x57662d60116d76067A0d7292080d2D4248dA2E0A"

# Create contract instances
erc20Contract = web3.eth.contract(address=erc20Address, abi=erc20ABI)
minimalForwarderContract = web3.eth.contract(
    address=minimalForwarderAddress, abi=abiMinimalForwarder
)

# User information and transaction details
userAddress = "0xF9Ff24b5e7792b7162F42FfeE5e586700ec4eC58"
privateKey = "cffff36bfff02a0f3b121cf67bf2784101aa73c6333921691f06cc75fcf6d579"

spender = "0x3ecD869BDA8680EE20ec581049492e71C21Fe74A"
amount = web3.to_wei(100, "ether")


# Generate approve transaction data
approve_data = erc20Contract.functions.approve(spender, amount).build_transaction(
    {
        "gas": 2000000,
        "from": userAddress,
        "nonce": web3.eth.get_transaction_count(userAddress),
    }
)

# Sign the approve transaction
signed_approve_txn = web3.eth.account.sign_transaction(approve_data, privateKey)

# Get nonce for minimalForwarder
nonce = minimalForwarderContract.functions.getNonce(userAddress).call()

forward_request = {
    "types": {
        "EIP712Domain": [
            {"name": "name", "type": "string"},
            {"name": "version", "type": "string"},
            {"name": "chainId", "type": "uint256"},
            {"name": "verifyingContract", "type": "address"},
        ],
        "ForwardRequest": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "gas", "type": "uint256"},
            {"name": "nonce", "type": "uint256"},
            {"name": "data", "type": "bytes"},
        ],
    },
    "primaryType": "ForwardRequest",
    "domain": {
        "name": "MinimalForwarder",
        "version": "0.0.1",
        "chainId": 11155111,  # Sửa lại chainId phù hợp
        "verifyingContract": minimalForwarderAddress,
    },
    "message": {
        "from": userAddress,
        "to": erc20Address,
        "value": 0,
        "gas": 1000000,  # Điều chỉnh gas
        "nonce": web3.eth.get_transaction_count(userAddress),
        "data": signed_approve_txn.rawTransaction.hex(),
    },
}

#  Convert HexBytes to hexadecimal string (without '0x' prefix)
hex_data = signed_approve_txn.rawTransaction.hex()

# The hex() method should automatically strip the '0x' prefix,
# but let's double check and remove it if present.
if hex_data.startswith("0x"):
    hex_data = hex_data[2:]

# Convert the clean hex string to bytes
forward_request["message"]["data"] = bytes.fromhex(hex_data)

# Ký yêu cầu với EIP712
encoded_message = encode_structured_data(forward_request)
signed_message = web3.eth.account.sign_message(encoded_message, private_key=privateKey)

# Gửi yêu cầu tới hợp đồng
tx = minimalForwarderContract.functions.execute(
    forward_request["message"],  # Yêu cầu chuyển tiếp
    signed_message.signature,  # Chữ ký
).transact({"from": userAddress})

# # Prepare forward request
# forwardRequest = {
#     "from": userAddress,
#     "to": erc20Address,
#     "value": 0,
#     "gas": 1000000,  # Adjust gas limit as needed
#     "nonce": web3.eth.get_transaction_count(userAddress),
#     "data": signed_approve_txn.rawTransaction.hex(),  # Convert HexBytes to hex string
# }

# # Encode forward request
# encoded_forward_request = encode_defunct(text=json.dumps(forwardRequest))

# # Sign the forward request
# signed_forward_request = web3.eth.account.sign_message(
#     encoded_forward_request, private_key=privateKey
# )

# # Send the forward request
# tx_hash = minimalForwarderContract.functions.execute(
#     forwardRequest, signed_forward_request.signature
# ).transact({"from": userAddress})

# # Get transaction receipt
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# print(f"Transaction successful: {tx_receipt}")


# # Generate transaction data for 'approve'
# data = erc20Contract.functions.approve(spender, amount).build_transaction(
#     {
#         "nonce": web3.eth.get_transaction_count(userAddress),
#         "gas": 2000000,
#     }
# )

# # Sign the transaction
# signed_txn = web3.eth.account.sign_transaction(data, private_key=privateKey)

# # Send the transaction
# tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

# # Get transaction receipt
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# print(f"Transaction successful: {tx_receipt}")
