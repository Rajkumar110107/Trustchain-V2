import React, { useState } from 'react';
import axios from 'axios';
import { Shield, Loader2, Upload, Search } from 'lucide-react';
import { motion } from 'framer-motion';
import UploadBox from './components/UploadBox';
import Tabs from './components/Tabs';
import { API_BASE_URL } from './config';

function App() {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('analysis');
  const [selectedLanguage, setSelectedLanguage] = useState('eng');

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setResult(null);
    setError(null);
    setActiveTab('analysis'); // Reset to default tab
  };

  const handleAnalyze = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('lang', selectedLanguage);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {

        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.error || 'Failed to connect to the analysis server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
    setActiveTab('analysis');
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 flex flex-col items-center">
      <header className="mb-8 text-center flex flex-col items-center pt-8">
        <div className="flex items-center gap-3 mb-2">
          <Shield className="w-10 h-10 text-emerald-400" />
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-emerald-400 to-cyan-500">
            Trustchain
          </h1>
        </div>
        <p className="text-slate-400 text-lg">AI Forensic Analysis & Blockchain Verification</p>
      </header>

      <main className="w-full max-w-4xl flex flex-col gap-8">
        {!result && !loading && (
          <UploadBox 
            file={file} 
            previewUrl={previewUrl} 
            onFileChange={handleFileChange} 
            onAnalyze={handleAnalyze} 
            selectedLanguage={selectedLanguage}
            onLanguageChange={setSelectedLanguage}
          />
        )}

        {loading && (
          <div className="glass-card p-8 flex flex-col md:flex-row items-center justify-center gap-12 w-full min-h-[400px] overflow-hidden relative">
            <div className="relative w-full md:w-1/2 h-72 rounded-xl overflow-hidden border border-emerald-500/30 bg-slate-950/80 group">
              <img src={previewUrl} alt="Scanning" className="absolute inset-0 w-full h-full object-contain opacity-60" />
              
              {/* Scan Line */}
              <motion.div 
                className="absolute left-0 right-0 h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_20px_rgba(34,211,238,0.8)] z-10"
                animate={{ top: ['0%', '100%', '0%'] }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
              />
              
              {/* Magnifier Glass Effect */}
              <motion.div
                className="absolute w-28 h-28 rounded-full border border-cyan-400 shadow-[0_0_25px_rgba(34,211,238,0.4)] z-20 pointer-events-none flex items-center justify-center"
                style={{
                  backdropFilter: 'blur(3px) brightness(1.2) contrast(1.1)',
                  WebkitBackdropFilter: 'blur(3px) brightness(1.2) contrast(1.1)',
                }}
                animate={{ 
                  left: ['10%', '60%', '30%', '10%'],
                  top: ['20%', '10%', '50%', '20%'],
                }}
                transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
              >
                <div className="absolute inset-2 rounded-full border border-cyan-300/30"></div>
                <Search className="w-8 h-8 text-cyan-400 opacity-50" />
              </motion.div>
              
              <div className="absolute inset-0 bg-gradient-to-b from-transparent via-emerald-500/5 to-transparent pointer-events-none" />
            </div>

            <div className="flex flex-col gap-6 w-full md:w-1/3 text-left">
              <h2 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">Forensic Scan Active</h2>
              
              <div className="flex flex-col gap-4">
                <motion.div 
                  initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }}
                  className="flex items-center gap-3 text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800"
                >
                  <Loader2 className="w-5 h-5 text-emerald-400 animate-spin" />
                  <span className="text-sm font-medium">Uploading</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1.0 }}
                  className="flex items-center gap-3 text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800"
                >
                  <Loader2 className="w-5 h-5 text-cyan-400 animate-spin" />
                  <span className="text-sm font-medium">OCR Extraction</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 1.8 }}
                  className="flex items-center gap-3 text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800"
                >
                  <Loader2 className="w-5 h-5 text-blue-400 animate-spin" />
                  <span className="text-sm font-medium">ELA Analysis</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 2.6 }}
                  className="flex items-center gap-3 text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800"
                >
                  <Loader2 className="w-5 h-5 text-violet-400 animate-spin" />
                  <span className="text-sm font-medium">ML Prediction</span>
                </motion.div>
                <motion.div 
                  initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 3.4 }}
                  className="flex items-center gap-3 text-slate-300 bg-slate-900/50 p-3 rounded-lg border border-slate-800"
                >
                  <Loader2 className="w-5 h-5 text-indigo-400 animate-spin" />
                  <span className="text-sm font-medium">Blockchain Verification</span>
                </motion.div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="glass-card p-6 border-red-500/50 bg-red-500/10 text-center">
            <p className="text-red-400 font-medium">{error}</p>
            <button 
              onClick={() => setError(null)}
              className="mt-4 px-6 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition"
            >
              Try Again
            </button>
          </div>
        )}

        {result && !loading && (
          <div className="flex flex-col gap-6 w-full fade-in">
            <div className="flex justify-between items-center bg-slate-900/50 backdrop-blur pb-2">
              <h2 className="text-xl font-medium text-slate-300">Analysis Results</h2>
              <button 
                onClick={handleReset}
                className="flex items-center gap-2 px-4 py-2 text-sm text-slate-300 hover:text-white glass-button"
              >
                <Upload className="w-4 h-4" />
                Upload New
              </button>
            </div>
            
            <Tabs 
              activeTab={activeTab} 
              setActiveTab={setActiveTab} 
              result={result} 
              originalImage={previewUrl}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;