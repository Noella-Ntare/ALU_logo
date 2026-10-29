// Deploy both contracts and register the logo.
const hre = require("hardhat");
const path = require("path");
const { hashFile } = require("./hash-logo");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Deployer wallet:", deployer.address);

  // Get the hash from the logo file in this project.
  const logoPath = path.join(__dirname, "..", "alu-logo.jpg");
  const logoHash = hashFile(logoPath);
  console.log("ALU logo SHA-256:", logoHash);

  // Deploy the registry.
  const Registry = await hre.ethers.getContractFactory("ALUAssetRegistry");
  const registry = await Registry.deploy();
  await registry.waitForDeployment();
  console.log("ALUAssetRegistry deployed to:", await registry.getAddress());

  // Register the logo.
  const tx = await registry.registerAsset("ALU Official Logo", "image/jpeg", logoHash);
  await tx.wait();
  const asset = await registry.getAsset(1);
  console.log("Logo registered as token ID 1 -> name:", asset.name, "| timestamp:", asset.timestamp.toString());

  // The deployer gets all the ALUT tokens at first.
  const Token = await hre.ethers.getContractFactory("ALULogoToken");
  const token = await Token.deploy(deployer.address);
  await token.waitForDeployment();
  console.log("ALULogoToken deployed to:", await token.getAddress());
  console.log("Owner balance:", (await token.balanceOf(deployer.address)).toString(), "ALUT");
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
