# ALU Logo Registry and Token

## Project overview
This project records the ALU logo's file hash on an Ethereum blockchain. It has two contracts:

* `ALUAssetRegistry` is an ERC-721 contract. It saves the file name, type, SHA-256 hash, registering wallet, and registration time. `verifyLogoIntegrity()` compares a supplied hash with the one saved for a token. The same hash cannot be registered twice.
* `ALULogoToken` is an ERC-20 contract. It creates 1,000,000 ALUT tokens. The owner can send tokens to other wallets, and `ownershipPercentage()` reports a wallet's share of the supply.

The NFT records the file and its hash. The ALUT tokens represent shares. Registering a hash gives a way to check whether a file matches; it does not by itself prove legal ownership or stop anyone copying the logo.

## Logo hash
SHA-256 hash for `alu-logo.jpg`:
```
0xa6dce4c6366746b3bd84170898440af9514335fa53cfea100d6c53672cd6fc84
```
To check it, run `npm run hash`. On Windows you can also run `certutil -hashfile alu-logo.jpg SHA256`.

Before submitting, make sure `alu-logo.jpg` is the official logo file you chose. If you replace it, run `npm run hash` and update the hash above. The tests and deployment script calculate the hash from the file.

## Versions
| Tool | Version |
|---|---|
| Solidity | 0.8.26 |
| Hardhat | 2.22.17 |
| OpenZeppelin Contracts | 5.0.2 |
| ethers.js | 6.x |
| Node.js | 22 (18 or newer works) |

## Setup and use
1. Install Node.js, then open a terminal in this project folder.
2. Install the packages:
   ```bash
   npm install --legacy-peer-deps
   ```
3. Compile the contracts:
   ```bash
   npx hardhat compile
   ```
4. Run the tests:
   ```bash
   npx hardhat test
   ```
5. To start a local blockchain, run this and leave the terminal open. Hardhat prints test wallet addresses:
   ```bash
   npx hardhat node
   ```
6. In a second terminal, deploy both contracts and register the logo:
   ```bash
   npx hardhat run scripts/deploy.js --network localhost
   ```
   The deployer receives all 1,000,000 ALUT. Without a local node, `npx hardhat run scripts/deploy.js` uses a temporary local network.

## Optional: Sepolia testnet
To deploy to Sepolia, get test ETH and an RPC URL, then copy `.env.example` to `.env` and add `SEPOLIA_RPC_URL` and `PRIVATE_KEY`. Use a test wallet, not a wallet holding real funds. Run:
```bash
npx hardhat run scripts/deploy.js --network sepolia
```

## Optional: Remix
The contracts can also be compiled in Remix with Solidity 0.8.26. Deploy `ALUAssetRegistry` without constructor arguments. Deploy `ALULogoToken` with the logo owner's wallet address.

## Main files
```
contracts/ALUAssetRegistry.sol   ERC-721 registration contract
contracts/ALULogoToken.sol       ERC-20 share token
scripts/deploy.js                deploys both contracts + registers the logo
scripts/hash-logo.js             prints the SHA-256 hash of alu-logo.jpg
test/ALUAssetRegistry.test.js    8 automated tests
alu-logo.jpg                     the logo file that is hashed
hardhat.config.js                Hardhat configuration
```

## A few implementation details
* Token IDs start at 1, and `registerAsset()` returns the new ID.
* The registry saves the metadata before calling `_safeMint()`, since minting can call the receiving contract.
* ALUT uses 0 decimals, so 500,000 tokens out of 1,000,000 is 50%. Percentages are rounded down to whole numbers.
* The registry rejects empty names, empty file types, and an empty hash.

## Setup issues and fixes
* Package installation had a peer dependency conflict, so `npm install --legacy-peer-deps` was used.
* The project uses Hardhat 2 with the ethers and chai matcher plugins directly instead of `hardhat-toolbox`.
* OpenZeppelin Contracts 5 requires an owner address in the `Ownable` constructor. `ALULogoToken` passes in `logoOwner`.
* Ethers 6 returns `BigInt` values in tests, so the expected values use BigInt literals such as `1n`.
