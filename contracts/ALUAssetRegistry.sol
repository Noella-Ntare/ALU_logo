// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

/// Stores registered files as NFTs and keeps their basic details and file hash.
contract ALUAssetRegistry is ERC721 {
    // Details saved for each registered file.
    struct AssetMetadata {
        string name;           // For example, "ALU Official Logo"
        string fileType;       // e.g. "image/jpeg"
        bytes32 contentHash;   // SHA-256 hash of the file
        address registeredBy;  // Wallet that registered it
        uint256 timestamp;     // When it was registered
    }

    // The first token ID is 1.
    uint256 private _tokenIdCounter;

    // Token ID to file details.
    mapping(uint256 => AssetMetadata) private _assets;

    // Keeps the same file hash from being registered twice.
    mapping(bytes32 => bool) public hashRegistered;

    // Emitted when a file is registered.
    event AssetRegistered(
        uint256 indexed tokenId,
        address indexed registeredBy,
        bytes32 indexed contentHash,
        string name,
        string fileType,
        uint256 timestamp
    );

    constructor() ERC721("ALU Asset Registry", "ALUASSET") {}

    /// Saves the file details and mints an NFT. A hash can only be used once.
    function registerAsset(
        string calldata name,
        string calldata fileType,
        bytes32 contentHash
    ) external returns (uint256 tokenId) {
        // Don't save incomplete details.
        require(bytes(name).length > 0, "Asset name cannot be empty");
        require(bytes(fileType).length > 0, "File type cannot be empty");
        require(contentHash != bytes32(0), "Content hash cannot be empty");

        // Reject a file that has already been registered.
        require(!hashRegistered[contentHash], "Asset already registered: duplicate content hash");

        // Give this file the next token ID.
        _tokenIdCounter += 1;
        tokenId = _tokenIdCounter;

        // Save the details before _safeMint, which can call the NFT receiver.
        _assets[tokenId] = AssetMetadata({
            name: name,
            fileType: fileType,
            contentHash: contentHash,
            registeredBy: msg.sender,
            timestamp: block.timestamp
        });
        hashRegistered[contentHash] = true;

        // Mint the NFT to whoever registered the file.
        _safeMint(msg.sender, tokenId);

        emit AssetRegistered(tokenId, msg.sender, contentHash, name, fileType, block.timestamp);
    }

    /// Checks whether the given file hash matches the hash saved for this token.
    function verifyLogoIntegrity(uint256 tokenId, bytes32 providedHash)
        external
        view
        returns (bool isAuthentic, string memory message)
    {
        _requireOwned(tokenId); // Reverts if this token ID does not exist.

        if (_assets[tokenId].contentHash == providedHash) {
            return (true, "Logo is authentic.");
        }
        return (false, "Warning: logo does not match.");
    }

    /// Returns the details saved for a token.
    function getAsset(uint256 tokenId) external view returns (AssetMetadata memory) {
        _requireOwned(tokenId); // Reverts if this token ID does not exist.
        return _assets[tokenId];
    }

    /// Returns how many files have been registered.
    function totalRegistered() external view returns (uint256) {
        return _tokenIdCounter;
    }
}
