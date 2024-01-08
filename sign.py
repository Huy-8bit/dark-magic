import os

from web3 import Web3
from pydash import get


_privateKeySigner = "cffff36bfff02a0f3b121cf67bf2784101aa73c6333921691f06cc75fcf6d579"  # from BackEnd Dev's Wallet

SEPOLIA = 11155111

_data = {
    "chain_network": SEPOLIA,
    "spender": "0x3ecD869BDA8680EE20ec581049492e71C21Fe74A",
    "amount": 10000000,
    "deadline": 1794725095,
}


def generate_signature():
    _w3 = Web3()
    # approve(address spender, uint256 amount)
    _encode = _w3.codec.encode_abi(
        ["uint256", "address", "uint256", "uint256"],
        [
            get(_data, "chain_network"),
            get(_data, "spender"),
            get(_data, "amount"),
            get(_data, "deadline"),
        ],
    )

    digest = Web3.solidityKeccak(["bytes"], [f"0x{_encode.hex()}"])
    _signed_message = _w3.eth.account.signHash(digest, private_key=_privateKeySigner)

    return _signed_message.signature.hex()


print("* Signature = ", generate_signature())
