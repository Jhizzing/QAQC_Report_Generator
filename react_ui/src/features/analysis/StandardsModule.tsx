import React, { useState, useMemo, useCallback } from 'react';
import { TrendingUp, AlertTriangle, CheckCircle2, Info, Table, BarChart3 } from 'lucide-react';
import { PlotlyControlChart, type ControlChartDataPoint, type ChartSelection } from '../../components/charts';
import { SyncedDataTable, type TableColumn } from '../../components/common/SyncedDataTable';
import type { StandardsAnalysisResults } from './standardsEngine';

interface StandardsModuleProps {
    results: StandardsAnalysisResults;
}

type ViewMode = 'chart' | 'table' | 'both';

export const StandardsModule: React.FC<StandardsModuleProps> = ({ results }) => {
    // Get unique CRM/element combinations
    const crmElements = useMemo(() => {
        const unique = new Set(results.results.map(r => `${r.crmId}|${r.element}`));
        return Array.from(unique).map(key => {
            const [crm, element] = key.split('|');
            return { crm, element, key };
        });
    }, [results]);

    const [selectedCRM, setSelectedCRM] = useState(crmElements[0]?.key || '');
    const [selectedIndices, setSelectedIndices] = useState<number[]>([]);
    const [viewMode, setViewMode] = useState<ViewMode>('both');

    // Filter data for selected CRM
    const filteredResults = useMemo(() => {
        if (!selectedCRM) return [];
        const [crm, element] = selectedCRM.split('|');
        return results.results
            .filter(r => r.crmId === crm && r.element === element)
            .sort((a, b) => a.sampleNumber - b.sampleNumber);
    }, [selectedCRM, results]);

    const statistics = useMemo(() => {
        return results.statistics.find(s => `${s.crm}|${s.element}` === selectedCRM);
    }, [selectedCRM, results]);

    // Prepare chart data
    const chartData: ControlChartDataPoint[] = useMemo(() => {
        return filteredResults.map(r => ({
            sampleNumber: r.sampleNumber,
            sampleId: r.sampleId,
            measuredValue: r.measuredValue,
            certifiedValue: r.certifiedValue,
            upperLimit: r.upperLimit,
            lowerLimit: r.lowerLimit,
            pass: r.pass,
            zScore: (r as unknown as { zScore?: number }).zScore,
            batchId: r.batchId,
        }));
    }, [filteredResults]);

    // Table columns
    const tableColumns: TableColumn<ControlChartDataPoint>[] = useMemo(() => [
        { key: 'sampleNumber', header: '#', width: '60px', align: 'center' },
        { key: 'sampleId', header: 'Sample ID', width: '140px' },
        { key: 'measuredValue', header: 'Measured', align: 'right', format: (v) => (v as number).toFixed(4) },
        { key: 'certifiedValue', header: 'Certified', align: 'right', format: (v) => (v as number).toFixed(4) },
        { 
            key: 'zScore', 
            header: 'Z-Score', 
            align: 'right', 
            format: (v) => v !== undefined ? (v as number).toFixed(2) : '-' 
        },
        { 
            key: 'pass', 
            header: 'Status', 
            align: 'center',
            render: (v) => v ? (
                <span className="inline-flex items-center gap-1 text-status-success">
                    <CheckCircle2 className="w-4 h-4" /> Pass
                </span>
            ) : (
                <span className="inline-flex items-center gap-1 text-status-error">
                    <AlertTriangle className="w-4 h-4" /> Fail
                </span>
            )
        },
        { key: 'batchId', header: 'Batch', width: '100px' },
    ], []);

    // Calculate summary metrics
    const totalSamples = filteredResults.length;
    const passedSamples = filteredResults.filter(r => r.pass).length;
    const failedSamples = totalSamples - passedSamples;
    const passRate = totalSamples > 0 ? (passedSamples / totalSamples) * 100 : 0;

    // Handle chart selection
    const handleChartSelection = useCallback((selection: ChartSelection) => {
        setSelectedIndices(selection.indices);
    }, []);

    // Handle point click
    const handlePointClick = useCallback((index: number) => {
        setSelectedIndices(prev => 
            prev.includes(index) 
                ? prev.filter(i => i !== index) 
                : [...prev, index]
        );
    }, []);

    // Handle table row click
    const handleRowClick = useCallback((index: number) => {
        setSelectedIndices(prev => 
            prev.includes(index) 
                ? prev.filter(i => i !== index) 
                : [...prev, index]
        );
    }, []);

    // Get CRM name and element for display
    const [crmName, element] = selectedCRM.split('|');

    return (
        <div className="space-y-6">
            {/* Header & Controls */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h3 className="text-2xl font-bold text-slate-50 flex items-center gap-2">
                        <TrendingUp className="w-6 h-6 text-primary" />
                        Standards Control Chart
                    </h3>
                    <p className="text-sm text-slate-400 mt-1">
                        Monitor CRM accuracy against certified values
                    </p>
                </div>

                <div className="flex items-center gap-4">
                    {/* View Mode Toggle */}
                    <div className="flex items-center bg-surface-dark rounded-lg p-1 border border-secondary-dark">
                        <button
                            onClick={() => setViewMode('chart')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'chart' ? 'bg-primary text-slate-900' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <BarChart3 className="w-3.5 h-3.5" />
                            Chart
                        </button>
                        <button
                            onClick={() => setViewMode('table')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'table' ? 'bg-primary text-slate-900' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <Table className="w-3.5 h-3.5" />
                            Table
                        </button>
                        <button
                            onClick={() => setViewMode('both')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'both' ? 'bg-primary text-slate-900' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            Both
                        </button>
                    </div>

                    {/* CRM Selector */}
                    <div className="w-64">
                        <select
                            value={selectedCRM}
                            onChange={(e) => {
                                setSelectedCRM(e.target.value);
                                setSelectedIndices([]);
                            }}
                            className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                        >
                            {crmElements.map(({ key, crm, element }) => (
                                <option key={key} value={key}>
                                    {crm} - {element}
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
                            <p className="text-sm text-slate-400">Total Samples</p>
                            <p className="text-2xl font-bold text-slate-50">{totalSamples}</p>
                        </div>
                        <Info className="w-8 h-8 text-accent" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Passed</p>
                            <p className="text-2xl font-bold text-status-success">{passedSamples}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-status-success" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Failed</p>
                            <p className="text-2xl font-bold text-status-error">{failedSamples}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-status-error" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Pass Rate</p>
                            <p className={`text-2xl font-bold ${passRate >= 95 ? 'text-status-success' : passRate >= 85 ? 'text-status-warning' : 'text-status-error'}`}>
                                {passRate.toFixed(1)}%
                            </p>
                        </div>
                        <TrendingUp className={`w-8 h-8 ${passRate >= 95 ? 'text-status-success' : passRate >= 85 ? 'text-status-warning' : 'text-status-error'}`} />
                    </div>
                </div>
            </div>

            {/* Chart & Table Layout */}
            <div className={`grid gap-6 ${viewMode === 'both' ? 'lg:grid-cols-2' : ''}`}>
                {/* Control Chart */}
                {(viewMode === 'chart' || viewMode === 'both') && (
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <PlotlyControlChart
                            data={chartData}
                            crmName={crmName}
                            element={element}
                            selectedIndices={selectedIndices}
                            onSelectionChange={handleChartSelection}
                            onPointClick={handlePointClick}
                            height={viewMode === 'both' ? 380 : 450}
                        />
                    </div>
                )}

                {/* Data Table */}
                {(viewMode === 'table' || viewMode === 'both') && (
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <h4 className="text-lg font-semibold text-slate-50 mb-4 flex items-center gap-2">
                            <Table className="w-5 h-5 text-primary" />
                            Sample Data
                        </h4>
                        <SyncedDataTable
                            data={chartData}
                            columns={tableColumns}
                            selectedIndices={selectedIndices}
                            onRowClick={handleRowClick}
                            pageSize={15}
                            maxHeight={viewMode === 'both' ? '340px' : '450px'}
                            exportFilename={`standards_${crmName}_${element}`}
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
                            <p className="text-sm text-slate-400">Mean</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.mean.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Std Dev (SD)</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.sd.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">RSD (%)</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.rsd.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Pass Rate</p>
                            <p className={`text-lg font-semibold ${statistics.passRate >= 95 ? 'text-status-success' : statistics.passRate >= 85 ? 'text-status-warning' : 'text-status-error'}`}>
                                {statistics.passRate.toFixed(1)}%
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

            {/* Flagged Batches Alert */}
            {results.flaggedBatches.length > 0 && (
                <div className="bg-status-error/10 border border-status-error/30 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-status-error flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-status-error">
                                Flagged Batches ({results.flaggedBatches.length})
                            </h4>
                            <p className="text-sm text-status-error/80 mt-1">
                                The following batches have consecutive standard failures and should be reviewed:
                            </p>
                            <ul className="list-disc list-inside text-sm text-status-error/80 mt-2">
                                {results.flaggedBatches.map(batch => (
                                    <li key={batch}>{batch}</li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
