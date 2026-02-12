import React, { useState, useEffect } from 'react';
import { FileText, Image, ArrowLeft, Download, CheckSquare, Server, FileOutput, Save, Check, AlertCircle } from 'lucide-react';
import type { JORCReportConfig, FiguresConfig } from './ReportConfig';
import type { QAQCAnalysisOutput } from '../analysis/qaqcAnalysis';
import { exportResults } from '../../services/analysisService';
import { useSettingsStore } from '../../stores/settingsStore';

interface ReportWorkflowProps {
    results: QAQCAnalysisOutput;
    onBack: () => void;
    onGenerate: (type: 'report' | 'figures', config: JORCReportConfig | FiguresConfig) => Promise<void>;
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
    const { settings, updateReportSettings, updateExportSettings } = useSettingsStore();
    const [reportType, setReportType] = useState<ReportType>('figures');
    const [isExporting, setIsExporting] = useState(false);
    const [exportError, setExportError] = useState<string | null>(null);
    const [exportSuccess, setExportSuccess] = useState(false);

    // Figures config
    const [figuresConfig, setFiguresConfig] = useState<FiguresConfig>({
        includeControlCharts: true,
        includeScatterPlots: true,
        includeHistograms: true,
        includeTables: true
    });

    // Report config - initialize with settings defaults
    const [jorcConfig, setJorcConfig] = useState<JORCReportConfig>({
        competentPerson: '',
        companyName: '',
        laboratory: '',
        drillingCompany: '',
        sampleType: '',
        comments: '',
        reportTitle: settings.report.defaultTitle,
        colorScheme: settings.report.defaultColorScheme,
        fontSize: settings.report.defaultFontSize,
        pageLayout: settings.report.defaultPageLayout,
        logoUrl: settings.report.defaultLogoUrl,
    });

    // Update config when settings change
    useEffect(() => {
        setJorcConfig(prev => ({
            ...prev,
            reportTitle: settings.report.defaultTitle,
            colorScheme: settings.report.defaultColorScheme,
            fontSize: settings.report.defaultFontSize,
            pageLayout: settings.report.defaultPageLayout,
            logoUrl: settings.report.defaultLogoUrl,
        }));
    }, [settings.report]);

    const handleSaveAsDefault = () => {
        if (reportType === 'report') {
            updateReportSettings({
                defaultTitle: jorcConfig.reportTitle || settings.report.defaultTitle,
                defaultColorScheme: jorcConfig.colorScheme || settings.report.defaultColorScheme,
                defaultFontSize: jorcConfig.fontSize || settings.report.defaultFontSize,
                defaultPageLayout: jorcConfig.pageLayout || settings.report.defaultPageLayout,
                defaultLogoUrl: jorcConfig.logoUrl || settings.report.defaultLogoUrl,
            });
            alert('Report preferences saved as defaults!');
        }
    };

    const toggleFigureOption = (key: keyof FiguresConfig) => {
        setFiguresConfig(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const handleGenerate = async () => {
        setIsExporting(true);
        setExportError(null);
        setExportSuccess(false);
        try {
            if (reportType === 'figures') {
                await onGenerate('figures', figuresConfig);
            } else {
                await onGenerate('report', jorcConfig);
            }
            setExportSuccess(true);
            // Auto-hide success after 5 seconds
            setTimeout(() => setExportSuccess(false), 5000);
        } catch (error) {
            setExportError(error instanceof Error ? error.message : 'Export failed');
        } finally {
            setIsExporting(false);
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
                    className={`relative p-5 rounded-xl border-2 transition-all text-left ${reportType === 'figures'
                            ? 'border-primary bg-primary/10 ring-2 ring-primary/20'
                            : 'border-secondary-dark hover:border-primary/50 hover:bg-surface-light'
                        }`}
                >
                    <div className="flex items-start gap-4">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${reportType === 'figures' ? 'bg-primary text-slate-900' : 'bg-accent/20 text-accent'
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
                    className={`relative p-5 rounded-xl border-2 transition-all text-left ${reportType === 'report'
                            ? 'border-purple-500 bg-purple-500/10 ring-2 ring-purple-500/20'
                            : 'border-secondary-dark hover:border-purple-500/50 hover:bg-surface-light'
                        }`}
                >
                    <div className="flex items-start gap-4">
                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${reportType === 'report' ? 'bg-purple-500 text-slate-50' : 'bg-purple-500/20 text-purple-400'
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
                                    className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-3 ${figuresConfig[opt.key]
                                            ? 'border-primary bg-primary/10'
                                            : 'border-secondary-light bg-surface-light hover:border-primary/50'
                                        }`}
                                >
                                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${figuresConfig[opt.key] ? 'bg-primary border-primary text-slate-900' : 'border-secondary-light'
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
                                <label className="text-xs font-medium text-slate-400">Report Title</label>
                                <input
                                    type="text"
                                    value={jorcConfig.reportTitle || ''}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, reportTitle: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="LogiQore Reporter Analysis Report"
                                />
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Color Scheme</label>
                                <select
                                    value={jorcConfig.colorScheme || 'default'}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, colorScheme: e.target.value as any }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                >
                                    <option value="default">Default</option>
                                    <option value="corporate">Corporate</option>
                                    <option value="minimal">Minimal</option>
                                </select>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Font Size</label>
                                <select
                                    value={jorcConfig.fontSize || 'medium'}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, fontSize: e.target.value as any }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                >
                                    <option value="small">Small</option>
                                    <option value="medium">Medium</option>
                                    <option value="large">Large</option>
                                </select>
                            </div>
                            <div className="space-y-1">
                                <label className="text-xs font-medium text-slate-400">Page Layout</label>
                                <select
                                    value={jorcConfig.pageLayout || 'portrait'}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, pageLayout: e.target.value as any }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                >
                                    <option value="portrait">Portrait</option>
                                    <option value="landscape">Landscape</option>
                                </select>
                            </div>
                            <div className="col-span-2 space-y-1">
                                <label className="text-xs font-medium text-slate-400">Logo URL (optional)</label>
                                <input
                                    type="text"
                                    value={jorcConfig.logoUrl || ''}
                                    onChange={(e) => setJorcConfig(prev => ({ ...prev, logoUrl: e.target.value }))}
                                    className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm focus:ring-2 focus:ring-primary/50 outline-none"
                                    placeholder="https://example.com/logo.png"
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

            {/* Report Options (Cover Page & JORC Table) — inline for convenience */}
            {reportType === 'report' && (
                <div className="bg-surface rounded-xl border border-secondary-dark p-6 mb-6">
                    <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider mb-4">
                        Report Options
                    </h4>
                    <div className="grid grid-cols-2 gap-3">
                        <div
                            className="flex items-center justify-between p-4 bg-surface-light/30 rounded-lg border border-white/5 cursor-pointer hover:bg-surface-light/50 transition-colors"
                            onClick={() => settings.export && updateExportSettings({ includeCoverPage: !settings.export.includeCoverPage })}
                        >
                            <div>
                                <p className="text-sm font-medium text-slate-200">Include Cover Page</p>
                                <p className="text-xs text-slate-500">Add a professional cover page</p>
                            </div>
                            <div className={`
                                w-11 h-6 rounded-full transition-colors relative
                                ${settings.export.includeCoverPage ? 'bg-primary' : 'bg-slate-600'}
                            `}>
                                <div className={`
                                    absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform shadow
                                    ${settings.export.includeCoverPage ? 'left-5.5 translate-x-0.5' : 'left-0.5'}
                                `}>
                                    {settings.export.includeCoverPage && <Check className="w-3 h-3 text-primary absolute top-1 left-1" />}
                                </div>
                            </div>
                        </div>
                        <div
                            className="flex items-center justify-between p-4 bg-surface-light/30 rounded-lg border border-white/5 cursor-pointer hover:bg-surface-light/50 transition-colors"
                            onClick={() => settings.export && updateExportSettings({ includeJORCTable: !settings.export.includeJORCTable })}
                        >
                            <div>
                                <p className="text-sm font-medium text-slate-200">Include JORC Table 1</p>
                                <p className="text-xs text-slate-500">Add editable JORC Table 1 section</p>
                            </div>
                            <div className={`
                                w-11 h-6 rounded-full transition-colors relative
                                ${settings.export.includeJORCTable ? 'bg-primary' : 'bg-slate-600'}
                            `}>
                                <div className={`
                                    absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform shadow
                                    ${settings.export.includeJORCTable ? 'left-5.5 translate-x-0.5' : 'left-0.5'}
                                `}>
                                    {settings.export.includeJORCTable && <Check className="w-3 h-3 text-primary absolute top-1 left-1" />}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Export Success Banner */}
            {exportSuccess && (
                <div className="mb-4 p-4 bg-status-success/10 border border-status-success rounded-lg flex items-center gap-3 animate-fade-in">
                    <div className="w-8 h-8 rounded-full bg-status-success/20 flex items-center justify-center">
                        <Check className="w-5 h-5 text-status-success" />
                    </div>
                    <div>
                        <p className="text-status-success font-medium">Report exported successfully!</p>
                        <p className="text-slate-400 text-sm">Your {reportType === 'figures' ? 'figures' : 'JORC report'} has been downloaded.</p>
                    </div>
                </div>
            )}

            {/* Export Error */}
            {exportError && (
                <div className="mb-4 p-4 bg-status-error/10 border border-status-error rounded-lg flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-status-error/20 flex items-center justify-center">
                        <AlertCircle className="w-5 h-5 text-status-error" />
                    </div>
                    <div>
                        <p className="text-status-error font-medium">Export failed</p>
                        <p className="text-slate-400 text-sm">{exportError}</p>
                    </div>
                </div>
            )}

            {/* Export Buttons */}
            <div className="space-y-3">
                {/* Save as Default Button (only for report type) */}
                {reportType === 'report' && (
                    <button
                        onClick={handleSaveAsDefault}
                        className="w-full py-3 rounded-xl font-medium transition-all flex items-center justify-center gap-2 bg-surface-light border border-secondary-dark hover:border-primary/50 text-slate-300 hover:text-slate-50"
                    >
                        <Save className="w-4 h-4" />
                        Save Report Preferences as Defaults
                    </button>
                )}

                {/* Primary Export - Client Side */}
                <button
                    onClick={handleGenerate}
                    disabled={isExporting}
                    className={`w-full py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center gap-2 shadow-lg disabled:opacity-50 ${reportType === 'figures'
                            ? 'bg-gradient-to-r from-primary to-primary-dark text-slate-900 hover:shadow-primary/20'
                            : 'bg-gradient-to-r from-purple-500 to-purple-700 text-slate-50 hover:shadow-purple-500/20'
                        }`}
                >
                    {isExporting ? (
                        <>
                            <div className="w-5 h-5 border-2 border-current border-t-transparent rounded-full animate-spin" />
                            Exporting...
                        </>
                    ) : (
                        <>
                            <Download className="w-5 h-5" />
                            {reportType === 'figures' ? 'Export Figures (DOCX)' : 'Generate JORC Report (DOCX)'}
                        </>
                    )}
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
