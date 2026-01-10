import React, { useState } from 'react';
import { FileText, Image, ArrowLeft, Download, CheckSquare, Server, FileOutput } from 'lucide-react';
import type { JORCReportConfig, FiguresConfig } from './ReportConfig';
import type { QAQCAnalysisOutput } from '../analysis/qaqcAnalysis';
import { exportResults } from '../../services/analysisService';

interface ReportWorkflowProps {
    results: QAQCAnalysisOutput;
    onBack: () => void;
    onGenerate: (type: 'report' | 'figures', config: JORCReportConfig | FiguresConfig) => void;
    isBackendAvailable?: boolean;
    analysisId?: string | null;
}

type ReportType = 'figures' | 'report';
type ExportFormat = 'docx' | 'excel' | 'pdf';

export const ReportWorkflow: React.FC<ReportWorkflowProps> = ({ 
    onBack, 
    onGenerate,
    isBackendAvailable,
    analysisId
}) => {
    const [reportType, setReportType] = useState<ReportType>('figures');
    const [isExporting, setIsExporting] = useState(false);
    const [exportError, setExportError] = useState<string | null>(null);

    // Figures config
    const [figuresConfig, setFiguresConfig] = useState<FiguresConfig>({
        includeControlCharts: true,
        includeScatterPlots: true,
        includeHistograms: true,
        includeTables: true
    });

    // Report config
    const [jorcConfig, setJorcConfig] = useState<JORCReportConfig>({
        competentPerson: '',
        companyName: '',
        laboratory: '',
        drillingCompany: '',
        sampleType: '',
        comments: ''
    });

    const toggleFigureOption = (key: keyof FiguresConfig) => {
        setFiguresConfig(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleGenerate = () => {
        if (reportType === 'figures') {
            onGenerate('figures', figuresConfig);
        } else {
            onGenerate('report', jorcConfig);
        }
    };

    const handleServerExport = async (format: ExportFormat) => {
        if (!analysisId) {
            setExportError('No analysis ID available for server export');
            return;
        }

        setIsExporting(true);
        setExportError(null);

        try {
            await exportResults(analysisId, format === 'pdf' ? 'pdf' : 'excel');
        } catch (error) {
            setExportError(error instanceof Error ? error.message : 'Export failed');
        } finally {
            setIsExporting(false);
        }
    };

    const figureOptions = [
        { key: 'includeControlCharts' as const, label: 'Control Charts', desc: 'Standard performance plots' },
        { key: 'includeScatterPlots' as const, label: 'Scatter Plots', desc: 'Duplicate precision analysis' },
        { key: 'includeHistograms' as const, label: 'Histograms', desc: 'Distribution analysis' },
        { key: 'includeTables' as const, label: 'Summary Tables', desc: 'Statistical summaries' },
    ];

    return (
        <div className="max-w-3xl mx-auto">
            {/* Header */}
            <div className="flex items-center gap-4 mb-8">
                <button
                    onClick={onBack}
                    className="p-2 rounded-lg hover:bg-surface-light transition-colors"
                >
                    <ArrowLeft className="w-5 h-5 text-slate-400" />
                </button>
                <div>
                    <h1 className="text-2xl font-bold text-slate-50">Export Report</h1>
                    <p className="text-sm text-slate-400">Choose format and configure options</p>
                </div>
            </div>

            {/* Type Selection - Inline Toggle */}
            <div className="grid grid-cols-2 gap-4 mb-8">
                <button
                    onClick={() => setReportType('figures')}
                    className={`relative p-5 rounded-xl border-2 transition-all text-left ${
                        reportType === 'figures'
                            ? 'border-primary bg-primary/10 ring-2 ring-primary/20'
                            : 'border-secondary-dark hover:border-primary/50 hover:bg-surface-light'
                    }`}
                >
                    <div className="flex items-start gap-4">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
                            reportType === 'figures' ? 'bg-primary text-slate-900' : 'bg-accent/20 text-accent'
                        }`}>
                            <Image className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className={`font-bold mb-1 ${reportType === 'figures' ? 'text-primary' : 'text-slate-50'}`}>
                                Figures Only
                            </h3>
                            <p className="text-xs text-slate-400">
                                Charts and tables for presentations
                            </p>
                        </div>
                    </div>
                    {reportType === 'figures' && (
                        <div className="absolute top-3 right-3 w-5 h-5 bg-primary rounded-full flex items-center justify-center">
                            <CheckSquare className="w-3 h-3 text-slate-900" />
                        </div>
                    )}
                </button>

                <button
                    onClick={() => setReportType('report')}
                    className={`relative p-5 rounded-xl border-2 transition-all text-left ${
                        reportType === 'report'
                            ? 'border-purple-500 bg-purple-500/10 ring-2 ring-purple-500/20'
                            : 'border-secondary-dark hover:border-purple-500/50 hover:bg-surface-light'
                    }`}
                >
                    <div className="flex items-start gap-4">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
                            reportType === 'report' ? 'bg-purple-500 text-slate-50' : 'bg-purple-500/20 text-purple-400'
                        }`}>
                            <FileText className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className={`font-bold mb-1 ${reportType === 'report' ? 'text-purple-400' : 'text-slate-50'}`}>
                                JORC Report
                            </h3>
                            <p className="text-xs text-slate-400">
                                Full analysis with metadata
                            </p>
                        </div>
                    </div>
                    {reportType === 'report' && (
                        <div className="absolute top-3 right-3 w-5 h-5 bg-purple-500 rounded-full flex items-center justify-center">
                            <CheckSquare className="w-3 h-3 text-slate-50" />
                        </div>
                    )}
                </button>
            </div>

            {/* Inline Configuration */}
            <div className="bg-surface rounded-xl border border-secondary-dark p-6 mb-6">
                {reportType === 'figures' ? (
                    <div>
                        <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">
                            Include in Export
                        </h4>
                        <div className="grid grid-cols-2 gap-3">
                            {figureOptions.map(opt => (
                                <button
                                    key={opt.key}
                                    onClick={() => toggleFigureOption(opt.key)}
                                    className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-3 ${
                                        figuresConfig[opt.key]
                                            ? 'border-primary bg-primary/10'
                                            : 'border-secondary-light bg-surface-light hover:border-primary/50'
                                    }`}
                                >
                                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${
                                        figuresConfig[opt.key] ? 'bg-primary border-primary text-slate-900' : 'border-secondary-light'
                                    }`}>
                                        {figuresConfig[opt.key] && <CheckSquare className="w-3 h-3" />}
                                    </div>
                                    <div>
                                        <div className={`font-semibold text-sm ${figuresConfig[opt.key] ? 'text-primary' : 'text-slate-50'}`}>
                                            {opt.label}
                                        </div>
                                        <div className="text-xs text-slate-500">{opt.desc}</div>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                ) : (
                    <div>
                        <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">
                            Report Details
                        </h4>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Competent Person</label>
                                <input
                                    type="text"
                                    value={jorcConfig.competentPerson}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, competentPerson: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="e.g. John Doe"
                                />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Company Name</label>
                                <input
                                    type="text"
                                    value={jorcConfig.companyName}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, companyName: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="e.g. Mining Corp"
                                />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Laboratory</label>
                                <input
                                    type="text"
                                    value={jorcConfig.laboratory}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, laboratory: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="e.g. ALS Geochemistry"
                                />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Sample Type</label>
                                <input
                                    type="text"
                                    value={jorcConfig.sampleType}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, sampleType: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="e.g. RC Chips, Diamond Core"
                                />
                            </div>
                            <div className="col-span-2 space-y-1">
                                <label className="text-xs font-medium text-slate-400">Comments (optional)</label>
                                <textarea
                                    value={jorcConfig.comments}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, comments: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none h-20 resize-none"
                                    placeholder="Additional context..."
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Export Error */}
            {exportError && (
                <div className="mb-4 p-4 bg-status-error/10 border border-status-error rounded-lg">
                    <p className="text-status-error text-sm">{exportError}</p>
                </div>
            )}

            {/* Export Buttons */}
            <div className="space-y-3">
                {/* Primary Export - Client Side */}
                <button
                    onClick={handleGenerate}
                    disabled={isExporting}
                    className={`w-full py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 ${
                        reportType === 'figures'
                            ? 'bg-gradient-to-r from-primary to-primary-dark text-slate-900 hover:shadow-primary/20'
                            : 'bg-gradient-to-r from-purple-500 to-purple-700 text-slate-50 hover:shadow-purple-500/20'
                    }`}
                >
                    <Download className="w-5 h-5" />
                    {reportType === 'figures' ? 'Export Figures (DOCX)' : 'Generate JORC Report (DOCX)'}
                </button>

                {/* Server-Side Export Options */}
                {isBackendAvailable && analysisId && (
                    <div className="pt-4 border-t border-secondary-dark">
                        <div className="flex items-center gap-2 mb-3">
                            <Server className="w-4 h-4 text-green-400" />
                            <span className="text-sm text-slate-400">Server-side exports available</span>
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                            <button
                                onClick={() => handleServerExport('excel')}
                                disabled={isExporting}
                                className="py-3 rounded-lg font-medium transition-all flex items-center justify-center gap-2 bg-surface-light border border-secondary-dark hover:border-primary/50 text-slate-300 hover:text-slate-50 disabled:opacity-50"
                            >
                                {isExporting ? (
                                    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                                ) : (
                                    <FileOutput className="w-4 h-4" />
                                )}
                                Excel Report
                            </button>
                            <button
                                onClick={() => handleServerExport('pdf')}
                                disabled={isExporting}
                                className="py-3 rounded-lg font-medium transition-all flex items-center justify-center gap-2 bg-surface-light border border-secondary-dark hover:border-primary/50 text-slate-300 hover:text-slate-50 disabled:opacity-50"
                            >
                                {isExporting ? (
                                    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin" />
                                ) : (
                                    <FileText className="w-4 h-4" />
                                )}
                                PDF Report
                            </button>
                        </div>
                    </div>
                )}

                {!isBackendAvailable && (
                    <p className="text-center text-xs text-slate-500 mt-2">
                        Start the Python backend for Excel and PDF export options
                    </p>
                )}
            </div>
        </div>
    );
};
