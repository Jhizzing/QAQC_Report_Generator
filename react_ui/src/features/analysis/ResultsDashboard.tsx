import React, { useState } from 'react';
import { BarChart3, Download, Info } from 'lucide-react';
import { StandardsModule } from './StandardsModule';
import { BlanksModule } from './BlanksModule';
import { DuplicatesModule } from './DuplicatesModule';
import type { QAQCAnalysisOutput } from './qaqcAnalysis';

interface ResultsDashboardProps {
    results: QAQCAnalysisOutput;
    onExport?: () => void;
}

type TabType = 'standards' | 'blanks' | 'duplicates';

export const ResultsDashboard: React.FC<ResultsDashboardProps> = ({ results, onExport }) => {
    const [activeTab, setActiveTab] = useState<TabType>('standards');

    const { summary } = results;

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-6">
            {/* Header */}
            <div className="mb-6">
                <div className="flex items-center justify-between">
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
                            <BarChart3 className="w-8 h-8 text-primary" />
                            QAQC Analysis Results
                        </h1>
                        <p className="text-sm text-gray-500 mt-1">
                            Comprehensive quality control analysis dashboard
                        </p>
                    </div>

                    {onExport && (
                        <button
                            onClick={onExport}
                            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2"
                        >
                            <Download className="w-4 h-4" />
                            Export Results
                        </button>
                    )}
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Total Samples</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">{summary.totalSamples}</p>
                        </div>
                        <Info className="w-8 h-8 text-blue-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Standards</p>
                    <p className="text-2xl font-bold text-purple-600">{summary.totalStandards}</p>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Blanks</p>
                    <p className="text-2xl font-bold text-blue-600">{summary.totalBlanks}</p>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Duplicates</p>
                    <p className="text-2xl font-bold text-indigo-600">{summary.totalDuplicates}</p>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <p className="text-sm text-gray-500">Overall Pass Rate</p>
                    <p className={`text-2xl font-bold ${summary.overallPassRate >= 90 ? 'text-green-600' : summary.overallPassRate >= 75 ? 'text-yellow-600' : 'text-red-600'}`}>
                        {summary.overallPassRate.toFixed(1)}%
                    </p>
                </div>
            </div>

            {/* Tab Navigation */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
                <div className="flex border-b border-gray-200 dark:border-gray-800">
                    <button
                        onClick={() => setActiveTab('standards')}
                        className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${activeTab === 'standards'
                                ? 'bg-primary text-white'
                                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                            }`}
                    >
                        Standards ({summary.totalStandards})
                    </button>
                    <button
                        onClick={() => setActiveTab('blanks')}
                        className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${activeTab === 'blanks'
                                ? 'bg-primary text-white'
                                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
                            }`}
                    >
                        Blanks ({summary.totalBlanks})
                    </button>
                    <button
                        onClick={() => setActiveTab('duplicates')}
                        className={`flex-1 px-6 py-4 text-sm font-medium transition-colors ${activeTab === 'duplicates'
                                ? 'bg-primary text-white'
                                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800'
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
        </div>
    );
};
