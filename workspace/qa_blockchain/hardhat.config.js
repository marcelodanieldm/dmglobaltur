// Hardhat config for Soroban contract testing (if using EVM-compatible tools)
// For native Soroban, use soroban-cli and adapt scripts accordingly
require("dotenv").config();

module.exports = {
  solidity: "0.8.19",
  networks: {
    // Configure for local/testnet as needed
  },
  paths: {
    tests: "./test"
  }
};
