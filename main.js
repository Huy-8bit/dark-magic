const { Web3 } = require("web3");
const EthereumTx = require("ethereumjs-tx").Transaction;

const web3 = new Web3(
  new Web3.providers.HttpProvider("https://rpc1.sepolia.org")
);

// ABI and Contract Address of the ERC20 Token
const erc20ABI = [
  {
    inputs: [],
    stateMutability: "nonpayable",
    type: "constructor",
  },
  {
    anonymous: false,
    inputs: [
      {
        indexed: true,
        internalType: "address",
        name: "owner",
        type: "address",
      },
      {
        indexed: true,
        internalType: "address",
        name: "spender",
        type: "address",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "value",
        type: "uint256",
      },
    ],
    name: "Approval",
    type: "event",
  },
  {
    anonymous: false,
    inputs: [
      {
        indexed: true,
        internalType: "address",
        name: "from",
        type: "address",
      },
      {
        indexed: true,
        internalType: "address",
        name: "to",
        type: "address",
      },
      {
        indexed: false,
        internalType: "uint256",
        name: "value",
        type: "uint256",
      },
    ],
    name: "Transfer",
    type: "event",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "owner",
        type: "address",
      },
      {
        internalType: "address",
        name: "spender",
        type: "address",
      },
    ],
    name: "allowance",
    outputs: [
      {
        internalType: "uint256",
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "spender",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "amount",
        type: "uint256",
      },
    ],
    name: "approve",
    outputs: [
      {
        internalType: "bool",
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "account",
        type: "address",
      },
    ],
    name: "balanceOf",
    outputs: [
      {
        internalType: "uint256",
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "decimals",
    outputs: [
      {
        internalType: "uint8",
        name: "",
        type: "uint8",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "spender",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "subtractedValue",
        type: "uint256",
      },
    ],
    name: "decreaseAllowance",
    outputs: [
      {
        internalType: "bool",
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "spender",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "addedValue",
        type: "uint256",
      },
    ],
    name: "increaseAllowance",
    outputs: [
      {
        internalType: "bool",
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [],
    name: "name",
    outputs: [
      {
        internalType: "string",
        name: "",
        type: "string",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "symbol",
    outputs: [
      {
        internalType: "string",
        name: "",
        type: "string",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "totalSupply",
    outputs: [
      {
        internalType: "uint256",
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "to",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "amount",
        type: "uint256",
      },
    ],
    name: "transfer",
    outputs: [
      {
        internalType: "bool",
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [
      {
        internalType: "address",
        name: "from",
        type: "address",
      },
      {
        internalType: "address",
        name: "to",
        type: "address",
      },
      {
        internalType: "uint256",
        name: "amount",
        type: "uint256",
      },
    ],
    name: "transferFrom",
    outputs: [
      {
        internalType: "bool",
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
];

const abiMinimalForwarder = [
  { inputs: [], stateMutability: "nonpayable", type: "constructor" },
  { inputs: [], name: "InvalidShortString", type: "error" },
  {
    inputs: [{ internalType: "string", name: "str", type: "string" }],
    name: "StringTooLong",
    type: "error",
  },
  { anonymous: false, inputs: [], name: "EIP712DomainChanged", type: "event" },
  {
    inputs: [],
    name: "eip712Domain",
    outputs: [
      { internalType: "bytes1", name: "fields", type: "bytes1" },
      { internalType: "string", name: "name", type: "string" },
      { internalType: "string", name: "version", type: "string" },
      { internalType: "uint256", name: "chainId", type: "uint256" },
      { internalType: "address", name: "verifyingContract", type: "address" },
      { internalType: "bytes32", name: "salt", type: "bytes32" },
      { internalType: "uint256[]", name: "extensions", type: "uint256[]" },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      {
        components: [
          { internalType: "address", name: "from", type: "address" },
          { internalType: "address", name: "to", type: "address" },
          { internalType: "uint256", name: "value", type: "uint256" },
          { internalType: "uint256", name: "gas", type: "uint256" },
          { internalType: "uint256", name: "nonce", type: "uint256" },
          { internalType: "bytes", name: "data", type: "bytes" },
        ],
        internalType: "struct MinimalForwarder.ForwardRequest",
        name: "req",
        type: "tuple",
      },
      { internalType: "bytes", name: "signature", type: "bytes" },
    ],
    name: "execute",
    outputs: [
      { internalType: "bool", name: "", type: "bool" },
      { internalType: "bytes", name: "", type: "bytes" },
    ],
    stateMutability: "payable",
    type: "function",
  },
  {
    inputs: [{ internalType: "address", name: "from", type: "address" }],
    name: "getNonce",
    outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [
      {
        components: [
          { internalType: "address", name: "from", type: "address" },
          { internalType: "address", name: "to", type: "address" },
          { internalType: "uint256", name: "value", type: "uint256" },
          { internalType: "uint256", name: "gas", type: "uint256" },
          { internalType: "uint256", name: "nonce", type: "uint256" },
          { internalType: "bytes", name: "data", type: "bytes" },
        ],
        internalType: "struct MinimalForwarder.ForwardRequest",
        name: "req",
        type: "tuple",
      },
      { internalType: "bytes", name: "signature", type: "bytes" },
    ],
    name: "verify",
    outputs: [{ internalType: "bool", name: "", type: "bool" }],
    stateMutability: "view",
    type: "function",
  },
];

async function main() {
  // Địa chỉ và ABI của ERC20 và MinimalForwarder
  const erc20Address = "0x91C16c2f4B318fE67c752A1F6E31e0F989FA8985";
  const minimalForwarderAddress = "0x57662d60116d76067A0d7292080d2D4248dA2E0A";

  // Tạo instance cho ERC20 và MinimalForwarder
  const erc20Contract = new web3.eth.Contract(erc20ABI, erc20Address);
  const minimalForwarderContract = new web3.eth.Contract(
    abiMinimalForwarder,
    minimalForwarderAddress
  );

  // Thông tin người dùng và giao dịch
  const userAddress = "0xF9Ff24b5e7792b7162F42FfeE5e586700ec4eC58"; // Địa chỉ của người dùng
  const privateKey = Buffer.from(
    "cffff36bfff02a0f3b121cf67bf2784101aa73c6333921691f06cc75fcf6d579",
    "hex"
  ); // Khóa riêng của người dùng

  const spender = "0x3ecD869BDA8680EE20ec581049492e71C21Fe74A"; // Địa chỉ được phê duyệt
  const amount = web3.utils.toWei("100", "ether"); // Số lượng token

  // Tạo dữ liệu giao dịch approve
  const data = erc20Contract.methods.approve(spender, amount).encodeABI();

  // Lấy nonce của người dùng từ MinimalForwarder
  const nonce = await minimalForwarderContract.methods
    .getNonce(userAddress)
    .call();

  // Tạo yêu cầu forward
  const forwardRequest = {
    from: userAddress,
    to: erc20Address,
    value: 0,
    gas: 1000000, // Đặt giới hạn gas
    nonce: nonce,
    data: data,
  };

  // Ký yêu cầu
  const requestHash = web3.utils.solidityKeccak256(
    ["address", "address", "uint256", "uint256", "uint256", "bytes"],
    [
      forwardRequest.from,
      forwardRequest.to,
      forwardRequest.value,
      forwardRequest.gas,
      forwardRequest.nonce,
      forwardRequest.data,
    ]
  );

  const signature = await web3.eth.accounts.sign(requestHash, privateKey);

  // Gửi yêu cầu tới MinimalForwarder
  const tx = minimalForwarderContract.methods
    .execute(forwardRequest, signature.signature)
    .send({ from: userAddress });

  tx.on("receipt", (receipt) => {
    console.log("Giao dịch thành công: ", receipt);
  }).on("error", (error) => {
    console.error("Lỗi giao dịch: ", error);
  });
}

main().catch((error) => {
  console.error("Lỗi: ", error);
});
