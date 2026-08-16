import React, { useState } from 'react';
import { Copy, Check, ShieldCheck, Zap, Server, AlertCircle, Clock, Wallet, ExternalLink, Info } from 'lucide-react';
import { motion } from 'framer-motion';

const BlockchainTab = ({ result }) => {
  const [copiedHash, setCopiedHash] = useState(false);
  const [copiedTx, setCopiedTx] = useState(false);

  if (!result) return null;

  const docHash = result.document_hash || result.hash;
  const bcStatus = result.blockchain_status || 'NOT_REGISTERED';
  const txHash = result.transaction_hash;
  const contractAddr = result.contract_address || '0x5FbDB2315678afecb367f032d93F642f64180aa3';
  const registrant = result.registrant;
  const timestamp = result.timestamp;

  // Determine explorer link
  const getExplorerUrl = (tx) => {
    if (!tx) return null;
    if (tx.startsWith('0x') && tx.length === 66) {
      return `https://sepolia.etherscan.io/tx/${tx}`;
    }
    return null;
  };

  const explorerUrl = getExplorerUrl(txHash);

  const copyToClipboard = (text, type) => {
    if (!text) return;
    navigator.clipboard.writeText(text);
    if (type === 'hash') {
      setCopiedHash(true);
      setTimeout(() => setCopiedHash(false), 2000);
    } else {
      setCopiedTx(true);
      setTimeout(() => setCopiedTx(false), 2000);
    }
  };

  const getStatusDisplay = () => {
    switch (bcStatus) {
      case 'VERIFIED':
        return {
          label: '✓ Blockchain Record Found',
          badgeText: 'Registered',
          icon: <ShieldCheck className="w-6 h-6 text-emerald-400" />,
          color: 'text-emerald-400',
          bg: 'bg-emerald-500/10',
          border: 'border-emerald-500/30'
        };
      case 'STORED':
        return {
          label: '⚡ Registered On-Chain',
          badgeText: 'Newly Registered',
          icon: <Server className="w-6 h-6 text-cyan-400" />,
          color: 'text-cyan-400',
          bg: 'bg-cyan-500/10',
          border: 'border-cyan-500/30'
        };
      case 'BLOCKCHAIN_UNAVAILABLE':
        return {
          label: '⚪ Blockchain Unavailable',
          badgeText: 'RPC Offline',
          icon: <AlertCircle className="w-6 h-6 text-slate-400" />,
          color: 'text-slate-400',
          bg: 'bg-slate-800/30',
          border: 'border-slate-700'
        };
      case 'NOT_REGISTERED':
        return {
          label: '○ No Blockchain Record Found',
          badgeText: 'Not Registered',
          icon: <Zap className="w-6 h-6 text-yellow-400" />,
          color: 'text-yellow-400',
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/30'
        };
      default:
        return {
          label: '🔴 Transaction Failed',
          badgeText: 'Failed',
          icon: <AlertCircle className="w-6 h-6 text-red-400" />,
          color: 'text-red-400',
          bg: 'bg-red-500/10',
          border: 'border-red-500/30'
        };
    }
  };

  const status = getStatusDisplay();

  return (
    <div className="glass-card p-8 min-h-[400px] flex flex-col justify-center gap-6">
      
      {/* Status Header */}
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className={`flex items-center justify-between p-6 rounded-2xl border ${status.border} ${status.bg}`}
      >
        <div className="flex items-center gap-4">
          <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800">
            {status.icon}
          </div>
          <div>
            <h3 className={`text-xl font-bold ${status.color}`}>
              {status.label}
            </h3>
            <p className="text-slate-400 text-xs mt-1">Smart Contract: <code className="text-slate-300 font-mono">{contractAddr}</code></p>
          </div>
        </div>
        <span className={`px-3 py-1 text-xs font-semibold rounded-full border ${status.border} ${status.color}`}>
          {status.badgeText}
        </span>
      </motion.div>

      {/* Hash & Registration Metadata Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* SHA-256 Fingerprint */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-slate-900/80 rounded-2xl border border-slate-800 p-6 flex flex-col justify-between"
        >
          <div className="flex justify-between items-center mb-3">
            <h4 className="text-slate-300 font-medium text-xs uppercase tracking-wider flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              Document SHA-256 Fingerprint
            </h4>
            <button 
              onClick={() => copyToClipboard(docHash, 'hash')}
              disabled={!docHash}
              className="flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg transition border border-slate-700"
            >
              {copiedHash ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copiedHash ? 'Copied' : 'Copy'}</span>
            </button>
          </div>
          <div className="bg-[#050505] p-3 rounded-xl border border-slate-800 overflow-x-auto no-scrollbar">
            <code className="text-emerald-400 font-mono text-xs break-all">
              {docHash || 'N/A'}
            </code>
          </div>
        </motion.div>

        {/* Transaction Hash */}
        <motion.div 
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-slate-900/80 rounded-2xl border border-slate-800 p-6 flex flex-col justify-between"
        >
          <div className="flex justify-between items-center mb-3">
            <h4 className="text-slate-300 font-medium text-xs uppercase tracking-wider flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-cyan-400" />
              Transaction Hash
            </h4>
            <div className="flex items-center gap-2">
              {explorerUrl && (
                <a
                  href={explorerUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1 px-2.5 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 text-xs rounded-lg border border-cyan-500/30 transition"
                >
                  <ExternalLink className="w-3 h-3" />
                  <span>Explorer</span>
                </a>
              )}
              {txHash && (
                <button 
                  onClick={() => copyToClipboard(txHash, 'tx')}
                  className="flex items-center gap-1.5 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs rounded-lg transition border border-slate-700"
                >
                  {copiedTx ? <Check className="w-3.5 h-3.5 text-cyan-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedTx ? 'Copied' : 'Copy'}</span>
                </button>
              )}
            </div>
          </div>
          <div className="bg-[#050505] p-3 rounded-xl border border-slate-800 overflow-x-auto no-scrollbar">
            <code className="text-cyan-400 font-mono text-xs break-all">
              {txHash || (result.blockchain_verified ? 'Verified in Genesis Block' : 'No Transaction Hash')}
            </code>
          </div>
        </motion.div>

      </div>

      {/* Wallet Registrant & Timestamp */}
      {(registrant || timestamp) && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 bg-slate-900/50 p-4 rounded-xl border border-slate-800">
          {registrant && (
            <div className="flex items-center gap-3 text-xs text-slate-300">
              <Wallet className="w-4 h-4 text-indigo-400 shrink-0" />
              <span>Registrant Wallet: <code className="font-mono text-indigo-300">{registrant}</code></span>
            </div>
          )}
          {timestamp && (
            <div className="flex items-center gap-3 text-xs text-slate-300">
              <Clock className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Registration Timestamp: <span className="font-mono text-emerald-300">{new Date(timestamp * 1000).toLocaleString()}</span></span>
            </div>
          )}
        </div>
      )}

      {/* Architectural Interpretation Disclaimer */}
      <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-800/80 flex items-start gap-3 text-xs text-slate-400">
        <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
        <p>
          <strong className="text-slate-200">Architectural Note:</strong> Blockchain registration proves cryptographic hash registration & timestamp continuity on-chain. It does not guarantee that the document itself is authentic. AI forensic analysis provides the document visual authenticity rating.
        </p>
      </div>

    </div>
  );
};

export default BlockchainTab;
