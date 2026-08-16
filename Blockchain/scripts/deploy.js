const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  console.log("🚀 Deploying DocumentRegistry Smart Contract...");

  const DocumentRegistry = await hre.ethers.getContractFactory("DocumentRegistry");
  const contract = await DocumentRegistry.deploy();

  await contract.waitForDeployment();

  const contractAddress = await contract.getAddress();
  const deploymentTx = contract.deploymentTransaction();

  console.log(`✅ DocumentRegistry deployed successfully!`);
  console.log(`📍 Contract Address: ${contractAddress}`);
  console.log(`📜 Transaction Hash: ${deploymentTx ? deploymentTx.hash : 'N/A'}`);

  // Prepare ABI and Deployment metadata
  const artifactPath = path.join(__dirname, "../artifacts/contracts/DocumentRegistry.sol/DocumentRegistry.json");
  let abi = [];
  if (fs.existsSync(artifactPath)) {
    const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));
    abi = artifact.abi;
  }

  const deploymentData = {
    address: contractAddress,
    transactionHash: deploymentTx ? deploymentTx.hash : null,
    network: hre.network.name,
    chainId: hre.network.config.chainId,
    deployedAt: new Date().toISOString(),
    abi: abi
  };

  // Export to blockchain/abi and backend/abi
  const abiDir = path.join(__dirname, "../abi");
  const backendAbiDir = path.join(__dirname, "../../backend/abi");

  if (!fs.existsSync(abiDir)) fs.mkdirSync(abiDir, { recursive: true });
  if (!fs.existsSync(backendAbiDir)) fs.mkdirSync(backendAbiDir, { recursive: true });

  fs.writeFileSync(path.join(abiDir, "DocumentRegistry.json"), JSON.stringify(deploymentData, null, 2));
  fs.writeFileSync(path.join(backendAbiDir, "DocumentRegistry.json"), JSON.stringify(deploymentData, null, 2));

  console.log(`📁 Deployment metadata saved to blockchain/abi/DocumentRegistry.json and backend/abi/DocumentRegistry.json`);
}

main().catch((error) => {
  console.error("❌ Deployment failed:", error);
  process.exitCode = 1;
});
