const { ethers } = require("hardhat");
const fs = require("fs");
require("hardhat-deploy");
require("hardhat-deploy-ethers");
const {
  DefenderRelayProvider,
  DefenderRelaySigner,
} = require("defender-relay-client/lib/ethers");
const utils = ethers.utils;

// command line: npx hardhat run scripts/deploy.js --network sepolia
// command line: npx hardhat verify --network sepolia <contract address> <constructor arguments>
async function main() {
  const [deployer] = await ethers.getSigners();

  console.log("Deploying contracts with the account:", deployer.address);
  console.log("Account balance:", (await deployer.getBalance()).toString());

  // const relaySigner = new DefenderRelaySigner();
  // const provider = new DefenderRelayProvider(relaySigner, {
  //   speed: "fast",
  //   from: deployer.address,
  // });

  const Forwarder = await ethers.getContractFactory("MinimalForwarder");
  const forwarder = await Forwarder.deploy();

  console.log("Forwarder address:", forwarder.address);

  const ForwarderData = {
    name: "Forwarder",
    ForwarderAddress: forwarder.address,
  };

  const ForwarderJsonData = JSON.stringify(ForwarderData, null, 2);
  fs.writeFileSync("./deployment/Forwarder.json", ForwarderJsonData);

  // deploy TransferToken
  const TRANSFER_TOKEN = await ethers.getContractFactory("TransferToken");
  const transferToken = await TRANSFER_TOKEN.deploy(forwarder.address);
  await transferToken.deployed();

  console.log("TRANSFER_TOKEN address:", transferToken.address);
}
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

// // deploy TOKEN
// const TOKEN = await ethers.getContractFactory("Token");
// const token = await TOKEN.deploy();
// await token.deployed();

// console.log("TOKEN address:", token.address);
// console.log("Token total supply:", (await token.totalSupply()).toString());

// const TOKENData = {
//   name: "Token",
//   TOKENAddress: token.address,
// };

// const TOKENJsonData = JSON.stringify(TOKENData, null, 2);
// fs.writeFileSync("./deployment/TOKEN.json", TOKENJsonData);
