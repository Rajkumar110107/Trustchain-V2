const hre = require("hardhat");

async function main() {
    const DocumentVerifier = await hre.ethers.getContractFactory("DocumentVerifier");

    const contract = await DocumentVerifier.deploy();

    await contract.waitForDeployment();

    const address = await contract.getAddress();

    console.log("Contract deployed to:", address);
}

main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
});