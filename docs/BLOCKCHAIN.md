# ⛓️ TrustChain Blockchain Architecture & Smart Contract Spec

## Smart Contract Specification (`DocumentRegistry.sol`)

- **Solidity Version**: `^0.8.20`
- **Compiler Target**: EVM Paris (`runs: 200`)

### State Structure
```solidity
struct DocumentRecord {
    address registrant;
    uint256 timestamp;
    bool isRegistered;
}

mapping(bytes32 => DocumentRecord) private _registry;
```

### Methods
1. `registerDocument(bytes32 docHash)`
   - Computes mapping write if `!_registry[docHash].isRegistered`.
   - Records `msg.sender` and `block.timestamp`.
   - Emits `event DocumentRegistered(bytes32 indexed docHash, address indexed registrant, uint256 timestamp)`.
2. `verifyDocument(bytes32 docHash) -> (bool isRegistered, address registrant, uint256 timestamp)`
   - Performs constant-time lookup.

## Web3 RPC Status Codes

| Status Code | Description |
| :--- | :--- |
| `VERIFIED` | Hash found on-chain; returned with registrant address & timestamp. |
| `STORED` | Hash newly registered on-chain via transaction. |
| `NOT_REGISTERED` | Hash query succeeded, but hash has not been registered on-chain yet. |
| `BLOCKCHAIN_UNAVAILABLE` | Local RPC node (`http://127.0.0.1:8545`) is offline or unreachable. |
| `TRANSACTION_FAILED` | Transaction submission failed or reverted. |
