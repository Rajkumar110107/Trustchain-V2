// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DocumentVerifier {

    mapping(bytes32 => bool) private registered;

    event DocumentRegistered(bytes32 hash, address sender);

    function registerDocument(bytes32 docHash) public {
        require(!registered[docHash], "Already registered");
        registered[docHash] = true;
        emit DocumentRegistered(docHash, msg.sender);
    }

    function verifyDocument(bytes32 docHash) public view returns (bool) {
        return registered[docHash];
    }
}