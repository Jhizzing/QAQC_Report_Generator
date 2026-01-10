import React, { useState } from 'react';
import { BarChart3, Info } from 'lucide-react';
import { StandardsModule } from './StandardsModule';
import { BlanksModule } from './BlanksModule';
import { DuplicatesModule } from './DuplicatesModule';
import type { QAQCAnalysisOutput } from './qaqcAnalysis';

interface ResultsDashboardProps {
    results: QAQCAnalysisOutput;
    onProceed?: () => void;
}

type TabType = 'standards' | 'blanks' | 'duplicates';

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ results, onProceed }) => {
    const [activeTab, setActiveTab] = useState<TabType>('standards');

    const { summary } = results;

    return (
        <div className="min-h-screen bg-background-dark p-6">
            {/* Header */}
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-slate-50 flex items-center gap-3 tracking-tight">
                            <BarChart3 className="w-8 h-8 text-primary" />
                            QAQC Analysis Results
                        </h1>
                        <p className="text-sm text-slate-400 mt-2 font-medium">
                            Comprehensive quality control analysis dashboard
                        </p>
                    </div>

                    {onProceed && (
                        <button
                            onClick={onProceed}
                            className="px-6 py-3 bg-primary text-slate-50 rounded-xl font-bold hover:bg-primary-dark transition-all flex items-center gap-2 shadow-[0_0_15px_rgba(245,158,11,0.3)] hover:shadow-[0_0_20px_rgba(245,158,11,0.5)] hover:scale-105"
                        >
                            Create Report
                        </button>
                    )}
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
                <div className="bg-surface border border-secondary-dark rounded-xl p-4 shadow-lg">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400 font-medium">Total Samples</p>
                            <p className="text-2xl font-bold text-slate-50">{summary.totalSamples}</p>
                        </div>
                        <Info className="w-8 h-8 text-accent" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-xl p-4 shadow-lg">
                    <p className="text-sm text-slate-400 font-medium">Standards</p>
                    <p className="text-2xl font-bold text-purple-400">{summary.totalStandards}</p>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-xl p-4 shadow-lg">
                    <p className="text-sm text-slate-400 font-medium">Blanks</p>
                    <p className="text-2xl font-bold text-accent">{summary.totalBlanks}</p>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-xl p-4 shadow-lg">
                    <p className="text-sm text-slate-400 font-medium">Duplicates</p>
                    <p className="text-2xl font-bold text-indigo-400">{summary.totalDuplicates}</p>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-xl p-4 shadow-lg">
                    <p className="text-sm text-slate-400 font-medium">Overall Pass Rate</p>
                    <p className={`text-2xl font-bold ${summary.overallPassRate >= 90 ? 'text-status-success' : summary.overallPassRate >= 75 ? 'text-status-warning' : 'text-status-error'}`}>
                        {summary.overallPassRate.toFixed(1)}%
                    </p>
                </div>
            </div>

            {/* Tab Navigation */}
            <div className="bg-surface border border-secondary-dark rounded-xl overflow-hidden shadow-lg mb-6">
                <div className="flex border-b border-secondary-dark">
                    <button
                        onClick={() => setActiveTab('standards')}
                        className={`flex-1 px-6 py-4 text-sm font-bold transition-all border-b-2 ${activeTab === 'standards'
                            ? 'border-primary text-primary bg-primary/5'
                            : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-surface-light'
                            }`}
                    >
                        Standards ({summary.totalStandards})
                    </button>
                    <button
                        onClick={() => setActiveTab('blanks')}
                        className={`flex-1 px-6 py-4 text-sm font-bold transition-all border-b-2 ${activeTab === 'blanks'
                            ? 'border-primary text-primary bg-primary/5'
                            : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-surface-light'
                            }`}
                    >
                        Blanks ({summary.totalBlanks})
                    </button>
                    <button
                        onClick={() => setActiveTab('duplicates')}
                        className={`flex-1 px-6 py-4 text-sm font-bold transition-all border-b-2 ${activeTab === 'duplicates'
                            ? 'border-primary text-primary bg-primary/5'
                            : 'border-transparent text-slate-400 hover:text-slate-200 hover:bg-surface-light'
                            }`}
                    >
                        Duplicates ({summary.totalDuplicates})
                    </button>
                </div>

                {/* Tab Content */}
                <div className="p-6">
                    {activeTab === 'standards' && <StandardsModule results={results.standards} />}
                    {activeTab === 'blanks' && <BlanksModule results={results.blanks} />}
                    {activeTab === 'duplicates' && <DuplicatesModule results={results.duplicates} />}
                </div>
            </div>
        </div >
    );
};
