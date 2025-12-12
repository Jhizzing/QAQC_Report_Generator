import React, { useState } from 'react';
import { FileText, Image, ArrowLeft, Download, ChevronRight } from 'lucide-react';
import { ReportConfigForm, FiguresConfigForm, type JORCReportConfig, type FiguresConfig } from './ReportConfig';
import type { QAQCAnalysisOutput } from '../analysis/qaqcAnalysis';

interface ReportWorkflowProps {
    results: QAQCAnalysisOutput;
    onBack: () => void;
    onGenerate: (type: 'report' | 'figures', config: JORCReportConfig | FiguresConfig) => void;
}

type WorkflowStep = 'selection' | 'config';
type ReportType = 'report' | 'figures' | null;

export const ReportWorkflow: React.FC<ReportWorkflowProps> = ({ onBack, onGenerate }) => {
    const [step, setStep] = useState<WorkflowStep>('selection');
    const [reportType, setReportType] = useState<ReportType>(null);

    const [jorcConfig, setJorcConfig] = useState<JORCReportConfig>({
        competentPerson: '',
        companyName: '',
        laboratory: '',
        drillingCompany: '',
        sampleType: '',
        comments: ''
    });

    const [figuresConfig, setFiguresConfig] = useState<FiguresConfig>({
        includeControlCharts: true,
        includeScatterPlots: true,
        includeHistograms: true,
        includeTables: true
    });

    const handleSelectType = (type: 'report' | 'figures') => {
        setReportType(type);
        setStep('config');
    };

    const handleGenerate = () => {
        if (reportType === 'report') {
            onGenerate('report', jorcConfig);
        } else if (reportType === 'figures') {
            onGenerate('figures', figuresConfig);
        }
    };

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-950 p-6">
            <div className="max-w-4xl mx-auto">
                {/* Header */}
                <div className="flex items-center gap-4 mb-8">
                    <button
                        onClick={step === 'selection' ? onBack : () => setStep('selection')}
                        className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
                    >
                        <ArrowLeft className="w-6 h-6 text-gray-600 dark:text-gray-300" />
                    </button>
                    <div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                            {step === 'selection' ? 'Report Generation' : reportType === 'report' ? 'Report Configuration' : 'Figures Configuration'}
                        </h1>
                        <p className="text-gray-500 dark:text-gray-400">
                            {step === 'selection' ? 'Choose your export format' : 'Customize your output'}
                        </p>
                    </div>
                </div>

                {/* Selection Step */}
                {step === 'selection' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <button
                            onClick={() => handleSelectType('figures')}
                            className="group relative p-8 rounded-2xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-primary hover:bg-gray-50 dark:hover:bg-gray-800 transition-all text-left"
                        >
                            <div className="w-16 h-16 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <Image className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Figures & Plots Only</h3>
                            <p className="text-gray-500 dark:text-gray-400 mb-6">
                                Export high-quality charts and data tables for use in your own documents. Perfect for quick updates or custom presentations.
                            </p>
                            <div className="flex items-center text-primary font-medium">
                                Configure Output <ChevronRight className="w-4 h-4 ml-1" />
                            </div>
                        </button>

                        <button
                            onClick={() => handleSelectType('report')}
                            className="group relative p-8 rounded-2xl border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900 hover:border-primary hover:bg-gray-50 dark:hover:bg-gray-800 transition-all text-left"
                        >
                            <div className="w-16 h-16 rounded-2xl bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                                <FileText className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                            </div>
                            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Complete JORC Report</h3>
                            <p className="text-gray-500 dark:text-gray-400 mb-6">
                                Generate a comprehensive QAQC report with JORC-compliant metadata, executive summary, and detailed analysis sections.
                            </p>
                            <div className="flex items-center text-primary font-medium">
                                Configure Report <ChevronRight className="w-4 h-4 ml-1" />
                            </div>
                        </button>
                    </div>
                )}

                {/* Config Step */}
                {step === 'config' && (
                    <div className="bg-white dark:bg-gray-900 rounded-2xl border border-gray-200 dark:border-gray-800 p-8">
                        {reportType === 'report' ? (
                            <ReportConfigForm config={jorcConfig} onChange={setJorcConfig} />
                        ) : (
                            <FiguresConfigForm config={figuresConfig} onChange={setFiguresConfig} />
                        )}

                        <div className="mt-8 flex justify-end">
                            <button
                                onClick={handleGenerate}
                                className="px-8 py-3 bg-primary text-white rounded-xl font-bold hover:bg-primary/90 transition-colors flex items-center gap-2 shadow-lg shadow-primary/20"
                            >
                                <Download className="w-5 h-5" />
                                {reportType === 'report' ? 'Generate Full Report' : 'Export Figures'}
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};
