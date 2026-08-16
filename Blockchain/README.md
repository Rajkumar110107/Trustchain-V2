# ⛓️ TrustChain Blockchain Layer

This directory contains the Solidity smart contracts, compilation artifacts, unit tests, and deployment scripts for **TrustChain**.

## Smart Contract Details

- **Contract Name**: `DocumentRegistry.sol`
- **Solidity Version**: `^0.8.20`
- **Stored Data**: Cryptographic 32-byte hashes (`bytes32`), registrant wallet address (`address`), and timestamp (`uint256`).

## Commands

```bash
# Install dependencies
npm install

# Compile contracts
npm run compile

# Run contract tests
npm test

# Deploy to local network
npm run deploy:local

# Deploy to Sepolia testnet
npm run deploy:sepolia
```
