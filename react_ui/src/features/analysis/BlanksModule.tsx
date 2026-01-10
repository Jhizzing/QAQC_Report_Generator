import React, { useState, useMemo, useCallback } from 'react';
import { Droplet, AlertTriangle, CheckCircle2, Info, TrendingDown, Table, BarChart3 } from 'lucide-react';
import { PlotlyHistogram, type HistogramDataPoint } from '../../components/charts';
import { SyncedDataTable, type TableColumn } from '../../components/common/SyncedDataTable';
import type { BlanksAnalysisResults } from './blanksEngine';

interface BlanksModuleProps {
    results: BlanksAnalysisResults;
}

interface BlankDataPoint {
    index: number;
    sampleNumber: number;
    sampleId: string;
    measuredValue: number;
    status: 'pass' | 'warning' | 'fail';
    pass: boolean;
    contaminated: boolean;
    detectionLimit: number;
    contaminationThreshold: number;
    unit: string;
}

type ViewMode = 'chart' | 'table' | 'both';

export const BlanksModule: React.FC<BlanksModuleProps> = ({ results }) => {
    // Get unique elements
    const elements = useMemo(() => {
        const unique = new Set(results.results.map(r => r.element));
        return Array.from(unique);
    }, [results]);

    const [selectedElement, setSelectedElement] = useState(elements[0] || '');
    const [selectedIndices, setSelectedIndices] = useState<number[]>([]);
    const [viewMode, setViewMode] = useState<ViewMode>('both');

    // Filter data for selected element
    const filteredResults = useMemo(() => {
        return results.results
            .filter(r => r.element === selectedElement)
            .sort((a, b) => a.sampleNumber - b.sampleNumber);
    }, [selectedElement, results]);

    const statistics = useMemo(() => {
        return results.statistics.find(s => s.element === selectedElement);
    }, [selectedElement, results]);

    // Prepare table data
    const tableData: BlankDataPoint[] = useMemo(() => {
        return filteredResults.map((r, index) => ({
            index,
            sampleNumber: r.sampleNumber,
            sampleId: r.sampleId,
            measuredValue: r.measuredValue,
            status: r.status,
            pass: r.pass,
            contaminated: r.contaminated,
            detectionLimit: r.detectionLimit,
            contaminationThreshold: r.contaminationThreshold,
            unit: r.unit,
        }));
    }, [filteredResults]);

    // Prepare histogram data
    const histogramData: HistogramDataPoint[] = useMemo(() => {
        return tableData.map(d => ({
            index: d.index,
            value: d.measuredValue,
            sampleId: d.sampleId,
            pass: d.pass,
        }));
    }, [tableData]);

    const detectionLimit = filteredResults[0]?.detectionLimit || 0;
    const contaminationThreshold = filteredResults[0]?.contaminationThreshold || 0;

    // Table columns
    const tableColumns: TableColumn<BlankDataPoint>[] = useMemo(() => [
        { key: 'sampleNumber', header: '#', width: '60px', align: 'center' },
        { key: 'sampleId', header: 'Sample ID', width: '150px' },
        { key: 'measuredValue', header: 'Value', align: 'right', format: (v) => (v as number).toFixed(4) },
        { key: 'detectionLimit', header: 'Det. Limit', align: 'right', format: (v) => (v as number).toFixed(4) },
        { 
            key: 'status', 
            header: 'Status', 
            align: 'center',
            render: (v) => {
                if (v === 'pass') return (
                    <span className="inline-flex items-center gap-1 text-status-success text-xs">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Pass
                    </span>
                );
                if (v === 'warning') return (
                    <span className="inline-flex items-center gap-1 text-status-warning text-xs">
                        <AlertTriangle className="w-3.5 h-3.5" /> Warning
                    </span>
                );
                return (
                    <span className="inline-flex items-center gap-1 text-status-error text-xs">
                        <AlertTriangle className="w-3.5 h-3.5" /> Fail
                    </span>
                );
            }
        },
        { 
            key: 'contaminated', 
            header: 'Contaminated', 
            align: 'center',
            render: (v) => v ? (
                <span className="text-status-error font-semibold">Yes</span>
            ) : (
                <span className="text-slate-500">No</span>
            )
        },
    ], []);

    // Calculate summary metrics
    const totalBlanks = filteredResults.length;
    const passedBlanks = filteredResults.filter(r => r.pass).length;
    const warningBlanks = filteredResults.filter(r => r.status === 'warning').length;
    const contaminatedBlanks = filteredResults.filter(r => r.contaminated).length;

    // Handle table row click
    const handleRowClick = useCallback((index: number) => {
        setSelectedIndices(prev => 
            prev.includes(index) 
                ? prev.filter(i => i !== index) 
                : [...prev, index]
        );
    }, []);

    return (
        <div className="space-y-6">
            {/* Header & Controls */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h3 className="text-2xl font-bold text-slate-50 flex items-center gap-2">
                        <Droplet className="w-6 h-6 text-cyan-400" />
                        Blanks Contamination Monitor
                    </h3>
                    <p className="text-sm text-slate-400 mt-1">
                        Track blank samples for contamination and detection limit compliance
                    </p>
                </div>

                <div className="flex items-center gap-4">
                    {/* View Mode Toggle */}
                    <div className="flex items-center bg-surface-dark rounded-lg p-1 border border-secondary-dark">
                        <button
                            onClick={() => setViewMode('chart')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'chart' ? 'bg-cyan-500 text-white' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <BarChart3 className="w-3.5 h-3.5" />
                            Chart
                        </button>
                        <button
                            onClick={() => setViewMode('table')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'table' ? 'bg-cyan-500 text-white' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <Table className="w-3.5 h-3.5" />
                            Table
                        </button>
                        <button
                            onClick={() => setViewMode('both')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'both' ? 'bg-cyan-500 text-white' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            Both
                        </button>
                    </div>

                    {/* Element Selector */}
                    <div className="w-48">
                        <select
                            value={selectedElement}
                            onChange={(e) => {
                                setSelectedElement(e.target.value);
                                setSelectedIndices([]);
                            }}
                            className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-cyan-500/50 outline-none"
                        >
                            {elements.map(element => (
                                <option key={element} value={element}>
                                    {element}
                                </option>
                            ))}
                        </select>
                    </div>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Total Blanks</p>
                            <p className="text-2xl font-bold text-slate-50">{totalBlanks}</p>
                        </div>
                        <Info className="w-8 h-8 text-accent" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Below Detection</p>
                            <p className="text-2xl font-bold text-status-success">{passedBlanks}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-status-success" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Warning</p>
                            <p className="text-2xl font-bold text-status-warning">{warningBlanks}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-status-warning" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Contaminated</p>
                            <p className="text-2xl font-bold text-status-error">{contaminatedBlanks}</p>
                        </div>
                        <TrendingDown className="w-8 h-8 text-status-error" />
                    </div>
                </div>
            </div>

            {/* Detection Limit Info */}
            <div className="bg-cyan-500/10 border border-cyan-500/30 rounded-lg p-4">
                <div className="flex items-start gap-3">
                    <Info className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 className="font-semibold text-cyan-300">
                            Detection & Contamination Thresholds
                        </h4>
                        <p className="text-sm text-cyan-200/80 mt-1">
                            <strong>Detection Limit:</strong> {detectionLimit.toFixed(4)} {filteredResults[0]?.unit || ''}
                            <span className="mx-3">|</span>
                            <strong>Contamination Threshold:</strong> {contaminationThreshold.toFixed(4)} {filteredResults[0]?.unit || ''} (3× DL)
                        </p>
                    </div>
                </div>
            </div>

            {/* Chart & Table Layout */}
            <div className={`grid gap-6 ${viewMode === 'both' ? 'lg:grid-cols-2' : ''}`}>
                {/* Histogram */}
                {(viewMode === 'chart' || viewMode === 'both') && (
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <h4 className="text-lg font-semibold text-slate-50 mb-2">
                            Blank Value Distribution
                        </h4>
                        <PlotlyHistogram
                            data={histogramData}
                            title=""
                            xAxisLabel={`${selectedElement} (${filteredResults[0]?.unit || ''})`}
                            threshold={contaminationThreshold}
                            thresholdLabel="Contamination"
                            binCount={15}
                            height={viewMode === 'both' ? 380 : 450}
                        />
                    </div>
                )}

                {/* Data Table */}
                {(viewMode === 'table' || viewMode === 'both') && (
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <h4 className="text-lg font-semibold text-slate-50 mb-4 flex items-center gap-2">
                            <Table className="w-5 h-5 text-cyan-400" />
                            Blank Samples
                        </h4>
                        <SyncedDataTable
                            data={tableData}
                            columns={tableColumns}
                            selectedIndices={selectedIndices}
                            onRowClick={handleRowClick}
                            pageSize={15}
                            maxHeight={viewMode === 'both' ? '340px' : '450px'}
                            exportFilename={`blanks_${selectedElement}`}
                        />
                    </div>
                )}
            </div>

            {/* Statistics Table */}
            {statistics && (
                <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-slate-50 mb-4">
                        Statistical Summary
                    </h4>

                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Maximum</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.max.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Mean</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.mean.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Median</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.median.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Contamination Rate</p>
                            <p className={`text-lg font-semibold ${statistics.contaminationRate === 0 ? 'text-status-success' : statistics.contaminationRate < 5 ? 'text-status-warning' : 'text-status-error'}`}>
                                {statistics.contaminationRate.toFixed(1)}%
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Count</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.count}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Flagged Blanks Alert */}
            {results.flaggedBlanks.length > 0 && (
                <div className="bg-status-error/10 border border-status-error/30 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-status-error flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-status-error">
                                Contaminated Blanks ({results.flaggedBlanks.length})
                            </h4>
                            <p className="text-sm text-status-error/80 mt-1">
                                The following blanks exceed the contamination threshold ({contaminationThreshold.toFixed(3)} {filteredResults[0]?.unit}):
                            </p>
                            <div className="mt-3 max-h-40 overflow-y-auto">
                                <table className="min-w-full text-sm">
                                    <thead className="bg-status-error/20">
                                        <tr>
                                            <th className="px-3 py-2 text-left text-status-error">Sample ID</th>
                                            <th className="px-3 py-2 text-left text-status-error">Element</th>
                                            <th className="px-3 py-2 text-right text-status-error">Value</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {results.flaggedBlanks.map((blank, idx) => (
                                            <tr key={idx} className="border-t border-status-error/30">
                                                <td className="px-3 py-2 text-status-error/80">{blank.sampleId}</td>
                                                <td className="px-3 py-2 text-status-error/80">{blank.element}</td>
                                                <td className="px-3 py-2 text-right text-status-error/80 font-mono">
                                                    {blank.measuredValue.toFixed(4)} {blank.unit}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
