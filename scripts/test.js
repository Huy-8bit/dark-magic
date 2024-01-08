// command line: npx hardhat test scripts/test.js --network sepolia

const { expect } = require("chai");
const { ethers } = require("hardhat");
const fs = require("fs");
const { id } = require("ethers/lib/utils");
const utils = ethers.utils;
const ethers = require("ethers");

require("dotenv").config();

tokenAddress = "0x91C16c2f4B318fE67c752A1F6E31e0F989FA8985"; // Replace with actual token address
transferTokenAddress = "0x3ecD869BDA8680EE20ec581049492e71C21Fe74A"; // Replace with actual token address
MinimalForwarderAddress = "0x57662d60116d76067A0d7292080d2D4248dA2E0A";
describe("TransferToken Contract", function () {
  beforeEach(async function () {
    Token = await ethers.getContractFactory("Token");
    token = await Token.attach(tokenAddress);
    TransferToken = await ethers.getContractFactory("TransferToken");
    transferToken = await TransferToken.attach(transferTokenAddress);
    MinimalForwarder = await ethers.getContractFactory("MinimalForwarder");
    minimalForwarder = await MinimalForwarder.attach(MinimalForwarderAddress);

    [owner] = await ethers.getSigners();

    console.log("transferToken address:", transferToken.address);
    console.log("owner address:", owner.address);
  });

  describe("transfer token to user", function () {
    it("should transfer token ", async function () {
      const result = await transferToken.transfer(
        tokenAddress,
        "0xf30607e0cdec7188d50d2bb384073bf1d5b02fa4",
        // ethers.utils.parseUnits("12")
        "1200"
      );
      console.log(result);
    });
  });
});
