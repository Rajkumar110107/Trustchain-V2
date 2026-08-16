import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle2, AlertTriangle, ShieldAlert, Info } from 'lucide-react';

const AnalysisTab = ({ result }) => {
  if (!result) return null;

  const classification = result.classification || (result.result?.includes('REAL') ? 'AUTHENTIC' : 'LIKELY FORGED');
  const score = result.authenticity_score ?? parseFloat(result.confidence || 0);

  const getBadgeStyle = () => {
    switch (classification) {
      case 'AUTHENTIC':
        return { color: 'text-emerald-400', border: 'border-t-emerald-500', glow: 'text-glow-green', icon: CheckCircle2 };
      case 'SUSPICIOUS':
        return { color: 'text-yellow-400', border: 'border-t-yellow-500', glow: '', icon: AlertTriangle };
      case 'LIKELY FORGED':
        return { color: 'text-red-500', border: 'border-t-red-500', glow: 'text-glow-red', icon: ShieldAlert };
      default:
        return { color: 'text-slate-400', border: 'border-t-slate-500', glow: '', icon: Info };
    }
  };

  const style = getBadgeStyle();
  const IconComponent = style.icon;

  return (
    <div className={`glass-card p-8 min-h-[400px] flex flex-col justify-center border-t-4 ${style.border}`}>
      
      <div className="flex flex-col md:flex-row gap-8 items-center justify-between mb-8">
        <div className="flex-1 text-center md:text-left">
          <p className="text-slate-400 font-medium mb-2 uppercase tracking-widest text-xs">Authenticity Classification</p>
          <motion.h2 
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className={`text-4xl md:text-5xl font-bold tracking-tight mb-2 flex items-center justify-center md:justify-start gap-3 ${style.color} ${style.glow}`}
          >
            <IconComponent className="w-10 h-10 shrink-0" />
            {classification}
          </motion.h2>
          <p className="text-slate-400 text-sm mt-2">{result.analysis_note}</p>
        </div>
        
        <div className="flex-1 flex justify-center">
          <div className="relative">
            <svg className="w-40 h-40 transform -rotate-90">
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                className="text-slate-800"
              />
              <motion.circle
                cx="80"
                cy="80"
                r="70"
                stroke="currentColor"
                strokeWidth="8"
                fill="transparent"
                strokeDasharray="440"
                initial={{ strokeDashoffset: 440 }}
                animate={{ strokeDashoffset: 440 - (440 * score) / 100 }}
                transition={{ duration: 1.5, ease: "easeOut" }}
                className={classification === 'AUTHENTIC' ? "text-emerald-500" : classification === 'SUSPICIOUS' ? "text-yellow-500" : "text-red-500"}
              />
            </svg>
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <span className={`text-3xl font-bold ${style.color}`}>
                {score.toFixed(1)}%
              </span>
              <span className="text-[10px] text-slate-400 uppercase tracking-wider">Score</span>
            </div>
          </div>
        </div>
      </div>

      {result.explanations && result.explanations.length > 0 && (
        <div className="bg-slate-900/50 rounded-xl p-6 border border-slate-800/80">
          <h3 className="text-lg font-medium text-slate-200 mb-4 flex items-center gap-2">
            <Info className="w-5 h-5 text-cyan-400" />
            Explainable Forensic Rationale
          </h3>
          <div className="flex flex-col gap-2">
            {result.explanations.map((exp, idx) => (
              <div key={idx} className="flex items-start gap-2.5 text-sm text-slate-300 bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                <span className="w-2 h-2 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                <span>{exp}</span>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};

export default AnalysisTab;
