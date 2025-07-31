const hre = require("hardhat");

async function main() {
  console.log("Deploying BiometricToken contract...");

  const BiometricToken = await hre.ethers.getContractFactory("BiometricToken");
  const contract = await BiometricToken.deploy();
  await contract.deployed();

  console.log("✅ BiometricToken deployed to:", contract.address);
  console.log("📝 Contract details:");
  console.log("   - Name: BiometricToken");
  console.log("   - Symbol: BIO");
  console.log("   - Owner: ", await contract.owner());
  console.log("   - Next Token ID: ", await contract.nextTokenId());
  
  console.log("\n🔧 Next steps:");
  console.log("1. Copy this contract address to your backend configuration");
  console.log("2. Copy the ABI from artifacts/contracts/BiometricToken.sol/BiometricToken.json");
  console.log("3. Use the first account's private key from hardhat node output");
}

main().catch((error) => {
  console.error("❌ Deployment failed:", error);
  process.exitCode = 1;
}); 