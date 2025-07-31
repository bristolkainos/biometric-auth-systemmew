// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BiometricToken is ERC721URIStorage, Ownable {
    uint256 public nextTokenId = 1;
    
    // Map tokenId to userId and biometric hash for easy lookup
    mapping(uint256 => string) public userIds;
    mapping(uint256 => string) public biometricHashes;
    mapping(uint256 => string) public biometricTypes;

    event BiometricTokenMinted(
        address indexed to, 
        uint256 indexed tokenId, 
        string userId, 
        string biometricHash,
        string biometricType
    );

    constructor() ERC721("BiometricToken", "BIO") Ownable(msg.sender) {}

    function mintBiometricToken(
        address to,
        string memory userId,
        string memory biometricHash,
        string memory biometricType,
        string memory tokenURI
    ) public onlyOwner returns (uint256) {
        uint256 tokenId = nextTokenId;
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);

        userIds[tokenId] = userId;
        biometricHashes[tokenId] = biometricHash;
        biometricTypes[tokenId] = biometricType;

        emit BiometricTokenMinted(to, tokenId, userId, biometricHash, biometricType);

        nextTokenId += 1;
        return tokenId;
    }

    function getBiometricData(uint256 tokenId) public view returns (
        string memory userId,
        string memory biometricHash,
        string memory biometricType
    ) {
        // Check if token exists by trying to get owner - will revert if token doesn't exist
        ownerOf(tokenId);
        return (userIds[tokenId], biometricHashes[tokenId], biometricTypes[tokenId]);
    }

    function getTokensByUser(string memory userId) public view returns (uint256[] memory) {
        uint256[] memory userTokens = new uint256[](nextTokenId - 1);
        uint256 count = 0;
        
        for (uint256 i = 1; i < nextTokenId; i++) {
            if (keccak256(bytes(userIds[i])) == keccak256(bytes(userId))) {
                userTokens[count] = i;
                count++;
            }
        }
        
        // Resize array to actual count
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = userTokens[i];
        }
        
        return result;
    }
} 