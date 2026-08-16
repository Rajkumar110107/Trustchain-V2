// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title DocumentRegistry
 * @dev Production smart contract for registering and verifying document SHA-256 cryptographic fingerprints on Ethereum.
 */
contract DocumentRegistry {

    struct DocumentRecord {
        address registrant;
        uint256 timestamp;
        bool isRegistered;
    }

    // Hash to DocumentRecord mapping
    mapping(bytes32 => DocumentRecord) private _registry;

    // Events
    event DocumentRegistered(
        bytes32 indexed docHash,
        address indexed registrant,
        uint256 timestamp
    );

    /**
     * @dev Registers a new document SHA-256 hash on-chain.
     * @param docHash 32-byte cryptographic digest of the original file.
     */
    function registerDocument(bytes32 docHash) external {
        require(docHash != bytes32(0), "Invalid document hash");
        require(!_registry[docHash].isRegistered, "Document already registered");

        _registry[docHash] = DocumentRecord({
            registrant: msg.sender,
            timestamp: block.timestamp,
            isRegistered: true
        });

        emit DocumentRegistered(docHash, msg.sender, block.timestamp);
    }

    /**
     * @dev Verifies whether a document hash is registered and returns its metadata.
     * @param docHash 32-byte hash to query.
     */
    function verifyDocument(bytes32 docHash) external view returns (
        bool isRegistered,
        address registrant,
        uint256 timestamp
    ) {
        DocumentRecord memory doc = _registry[docHash];
        return (doc.isRegistered, doc.registrant, doc.timestamp);
    }
}
