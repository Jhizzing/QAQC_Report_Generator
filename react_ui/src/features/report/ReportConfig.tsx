import React from 'react';
import { CheckSquare } from 'lucide-react';

export interface JORCReportConfig {
    competentPerson: string;
    companyName: string;
    laboratory: string;
    drillingCompany: string;
    sampleType: string;
    comments: string;
}

export interface FiguresConfig {
    includeScatterPlots: boolean;
    includeControlCharts: boolean;
    includeHistograms: boolean;
    includeTables: boolean;

    // Advanced options (can be expanded later)
    controlChartStyle?: 'shewhart' | 'cusum';
    scatterPlotType?: 'original-vs-duplicate' | 'rpd-vs-grade';
}

interface ReportConfigFormProps {
    config: JORCReportConfig;
    onChange: (config: JORCReportConfig) => void;
}

interface FiguresConfigFormProps {
    config: FiguresConfig;
    onChange: (config: FiguresConfig) => void;
}

export const ReportConfigForm: React.FC<ReportConfigFormProps> = ({ config, onChange }) => {
    const handleChange = (field: keyof JORCReportConfig, value: string) => {
        onChange({ ...config, [field]: value });
    };

    return (
        <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Competent Person</label>
                    <input
                        type="text"
                        value={config.competentPerson}
                        onChange={(e) => handleChange('competentPerson', e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white"
                        placeholder="e.g. John Doe"
                    />
                </div>
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Company Name</label>
                    <input
                        type="text"
                        value={config.companyName}
                        onChange={(e) => handleChange('companyName', e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white"
                        placeholder="e.g. Mining Corp"
                    />
                </div>
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Laboratory</label>
                    <input
                        type="text"
                        value={config.laboratory}
                        onChange={(e) => handleChange('laboratory', e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white"
                        placeholder="e.g. ALS Geochemistry"
                    />
                </div>
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Drilling Company</label>
                    <input
                        type="text"
                        value={config.drillingCompany}
                        onChange={(e) => handleChange('drillingCompany', e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white"
                        placeholder="e.g. Drill Co"
                    />
                </div>
                <div className="space-y-2">
                    <label className="text-sm font-medium text-gray-300">Sample Type</label>
                    <input
                        type="text"
                        value={config.sampleType}
                        onChange={(e) => handleChange('sampleType', e.target.value)}
                        className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white"
                        placeholder="e.g. RC Chips"
                    />
                </div>
            </div>
            <div className="space-y-2">
                <label className="text-sm font-medium text-gray-300">Comments / Notes</label>
                <textarea
                    value={config.comments}
                    onChange={(e) => handleChange('comments', e.target.value)}
                    className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent text-white h-32"
                    placeholder="Additional context for the report..."
                />
            </div>
        </div>
    );
};

export const FiguresConfigForm: React.FC<FiguresConfigFormProps> = ({ config, onChange }) => {
    const toggle = (field: keyof FiguresConfig) => {
        onChange({ ...config, [field]: !config[field] });
    };

    return (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
                onClick={() => toggle('includeControlCharts')}
                className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-4 ${config.includeControlCharts
                    ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-primary/50 hover:bg-gray-800'
                    }`}
            >
                <div className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${config.includeControlCharts ? 'bg-primary border-primary text-white' : 'border-gray-500'
                    }`}>
                    {config.includeControlCharts && <CheckSquare className="w-4 h-4" />}
                </div>
                <div>
                    <div className={`font-bold ${config.includeControlCharts ? 'text-primary' : 'text-white'}`}>Control Charts</div>
                    <div className="text-sm text-gray-400">Standard performance plots</div>
                </div>
            </button>

            <button
                onClick={() => toggle('includeScatterPlots')}
                className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-4 ${config.includeScatterPlots
                    ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-primary/50 hover:bg-gray-800'
                    }`}
            >
                <div className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${config.includeScatterPlots ? 'bg-primary border-primary text-white' : 'border-gray-500'
                    }`}>
                    {config.includeScatterPlots && <CheckSquare className="w-4 h-4" />}
                </div>
                <div>
                    <div className={`font-bold ${config.includeScatterPlots ? 'text-primary' : 'text-white'}`}>Scatter Plots</div>
                    <div className="text-sm text-gray-400">Duplicate precision analysis</div>
                </div>
            </button>

            <button
                onClick={() => toggle('includeHistograms')}
                className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-4 ${config.includeHistograms
                    ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-primary/50 hover:bg-gray-800'
                    }`}
            >
                <div className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${config.includeHistograms ? 'bg-primary border-primary text-white' : 'border-gray-500'
                    }`}>
                    {config.includeHistograms && <CheckSquare className="w-4 h-4" />}
                </div>
                <div>
                    <div className={`font-bold ${config.includeHistograms ? 'text-primary' : 'text-white'}`}>Histograms</div>
                    <div className="text-sm text-gray-400">Distribution analysis</div>
                </div>
            </button>

            <button
                onClick={() => toggle('includeTables')}
                className={`p-4 rounded-xl border-2 text-left transition-all flex items-center gap-4 ${config.includeTables
                    ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                    : 'border-gray-700 bg-gray-800/50 hover:border-primary/50 hover:bg-gray-800'
                    }`}
            >
                <div className={`w-6 h-6 rounded border-2 flex items-center justify-center flex-shrink-0 transition-colors ${config.includeTables ? 'bg-primary border-primary text-white' : 'border-gray-500'
                    }`}>
                    {config.includeTables && <CheckSquare className="w-4 h-4" />}
                </div>
                <div>
                    <div className={`font-bold ${config.includeTables ? 'text-primary' : 'text-white'}`}>Summary Tables</div>
                    <div className="text-sm text-gray-400">Statistical summaries</div>
                </div>
            </button>
        </div>
    );
};
