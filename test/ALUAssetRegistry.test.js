// Tests for the registry and share token.
const { expect } = require("chai");
const { ethers } = require("hardhat");
const path = require("path");
const { hashFile } = require("../scripts/hash-logo");

// Use the hash of the logo file in the project.
const LOGO_HASH = hashFile(path.join(__dirname, "..", "alu-logo.jpg"));
// Change one digit to make a hash that should not match.
const FAKE_HASH = LOGO_HASH.slice(0, -1) + (LOGO_HASH.endsWith("0") ? "1" : "0");

describe("ALUAssetRegistry (ERC-721)", function () {
  let registry, owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    const Registry = await ethers.getContractFactory("ALUAssetRegistry");
    registry = await Registry.deploy();
    await registry.waitForDeployment();
  });

  it("1. registers the ALU logo successfully and returns a token ID", async function () {
    // Use staticCall to check the returned token ID without sending a transaction.
    const returnedId = await registry.registerAsset.staticCall("ALU Official Logo", "image/jpeg", LOGO_HASH);
    expect(returnedId).to.equal(1n);

    await expect(registry.registerAsset("ALU Official Logo", "image/jpeg", LOGO_HASH))
      .to.emit(registry, "AssetRegistered");
    expect(await registry.ownerOf(1)).to.equal(owner.address); // The caller gets the NFT.
  });

  it("2. rejects registering the same hash a second time", async function () {
    await registry.registerAsset("ALU Official Logo", "image/jpeg", LOGO_HASH);
    await expect(registry.registerAsset("Copy", "image/jpeg", LOGO_HASH))
      .to.be.revertedWith("Asset already registered: duplicate content hash");
  });

  it("3. verifyLogoIntegrity() returns true for the correct hash", async function () {
    await registry.registerAsset("ALU Official Logo", "image/jpeg", LOGO_HASH);
    const [ok, msg] = await registry.verifyLogoIntegrity(1, LOGO_HASH);
    expect(ok).to.equal(true);
    expect(msg).to.equal("Logo is authentic.");
  });

  it("4. verifyLogoIntegrity() returns false for an incorrect hash", async function () {
    await registry.registerAsset("ALU Official Logo", "image/jpeg", LOGO_HASH);
    const [ok, msg] = await registry.verifyLogoIntegrity(1, FAKE_HASH);
    expect(ok).to.equal(false);
    expect(msg).to.equal("Warning: logo does not match.");
  });

  it("5. getAsset() returns the correct asset name and file type", async function () {
    await registry.registerAsset("ALU Official Logo", "image/jpeg", LOGO_HASH);
    const asset = await registry.getAsset(1);
    expect(asset.name).to.equal("ALU Official Logo");
    expect(asset.fileType).to.equal("image/jpeg");
    expect(asset.contentHash).to.equal(LOGO_HASH);
    expect(asset.registeredBy).to.equal(owner.address);
    expect(asset.timestamp).to.be.gt(0n);
  });
});

describe("ALULogoToken (ERC-20)", function () {
  let token, logoOwner, faculty;

  beforeEach(async function () {
    [logoOwner, faculty] = await ethers.getSigners();
    const Token = await ethers.getContractFactory("ALULogoToken");
    token = await Token.deploy(logoOwner.address);
    await token.waitForDeployment();
  });

  it("6. mints the full 1,000,000 ALUT supply to the logo owner", async function () {
    expect(await token.name()).to.equal("ALU Logo Token");
    expect(await token.symbol()).to.equal("ALUT");
    expect(await token.totalSupply()).to.equal(1_000_000n);
    expect(await token.balanceOf(logoOwner.address)).to.equal(1_000_000n);
  });

  it("7. distributeShares() transfers tokens to the recipient", async function () {
    await token.distributeShares(faculty.address, 100_000);
    expect(await token.balanceOf(faculty.address)).to.equal(100_000n);
    expect(await token.balanceOf(logoOwner.address)).to.equal(900_000n);
    // Check that only the owner can send tokens and that zero is rejected.
    await expect(token.connect(faculty).distributeShares(faculty.address, 1)).to.be.reverted;
    await expect(token.distributeShares(faculty.address, 0))
      .to.be.revertedWith("Amount must be greater than zero");
  });

  it("8. ownershipPercentage() returns the correct percentage", async function () {
    await token.distributeShares(faculty.address, 500_000);
    expect(await token.ownershipPercentage(faculty.address)).to.equal(50n);
    expect(await token.ownershipPercentage(logoOwner.address)).to.equal(50n);
  });
});
