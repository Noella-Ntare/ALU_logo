// Hardhat configuration for the ALU Logo Registry project.
require("@nomicfoundation/hardhat-ethers");
require("@nomicfoundation/hardhat-chai-matchers");
require("dotenv").config(); // loads SEPOLIA_RPC_URL / PRIVATE_KEY from .env (optional)

const { SEPOLIA_RPC_URL, PRIVATE_KEY } = process.env;

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.26",
    settings: { optimizer: { enabled: true, runs: 200 } },
  },
  networks: {
    // "hardhat" (in-process) and "localhost" (npx hardhat node) work out of the box.
    localhost: { url: "http://127.0.0.1:8545" },
    // Optional public testnet - only enabled if you filled in your .env file.
    ...(SEPOLIA_RPC_URL && PRIVATE_KEY
      ? { sepolia: { url: SEPOLIA_RPC_URL, accounts: [PRIVATE_KEY] } }
      : {}),
  },
};
