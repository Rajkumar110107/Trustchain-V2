const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DocumentRegistry Smart Contract", function () {
  let registry;
  let owner;
  let addr1;

  const sampleHash = ethers.keccak256(ethers.toUtf8Bytes("Test Document Content"));
  const unregisteredHash = ethers.keccak256(ethers.toUtf8Bytes("Unregistered Document"));

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const DocumentRegistry = await ethers.getContractFactory("DocumentRegistry");
    registry = await DocumentRegistry.deploy();
    await registry.waitForDeployment();
  });

  it("Should register a document and emit DocumentRegistered event", async function () {
    await expect(registry.connect(owner).registerDocument(sampleHash))
      .to.emit(registry, "DocumentRegistered")
      .withArgs(sampleHash, owner.address, (val) => val > 0);
  });

  it("Should return true for a registered document hash", async function () {
    await registry.connect(owner).registerDocument(sampleHash);

    const [isRegistered, registrant, timestamp] = await registry.verifyDocument(sampleHash);
    expect(isRegistered).to.equal(true);
    expect(registrant).to.equal(owner.address);
    expect(Number(timestamp)).to.be.greaterThan(0);
  });

  it("Should return false for an unregistered document hash", async function () {
    const [isRegistered, registrant, timestamp] = await registry.verifyDocument(unregisteredHash);
    expect(isRegistered).to.equal(false);
    expect(registrant).to.equal(ethers.ZeroAddress);
    expect(Number(timestamp)).to.equal(0);
  });

  it("Should prevent duplicate document registration", async function () {
    await registry.connect(owner).registerDocument(sampleHash);

    await expect(registry.connect(addr1).registerDocument(sampleHash))
      .to.be.revertedWith("Document already registered");
  });

  it("Should reject empty document hash", async function () {
    await expect(registry.connect(owner).registerDocument(ethers.ZeroHash))
      .to.be.revertedWith("Invalid document hash");
  });
});
