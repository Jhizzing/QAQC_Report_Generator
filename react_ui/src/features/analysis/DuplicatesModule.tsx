import React, { useState, useMemo, useCallback } from 'react';
import { Copy, AlertTriangle, CheckCircle2, Info, TrendingUp, Table, BarChart3 } from 'lucide-react';
import { PlotlyScatterPlot, PlotlyHistogram, type ScatterDataPoint, type HistogramDataPoint, type ChartSelection } from '../../components/charts';
import { SyncedDataTable, type TableColumn } from '../../components/common/SyncedDataTable';
import type { DuplicatesAnalysisResults } from './duplicatesEngine';

interface DuplicatesModuleProps {
    results: DuplicatesAnalysisResults;
}

type ViewMode = 'chart' | 'table' | 'both';

export const DuplicatesModule: React.FC<DuplicatesModuleProps> = ({ results }) => {
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
            .sort((a, b) => a.pairNumber - b.pairNumber);
    }, [selectedElement, results]);

    const statistics = useMemo(() => {
        return results.statistics.find(s => s.element === selectedElement);
    }, [selectedElement, results]);

    // Prepare scatter plot data
    const scatterData: ScatterDataPoint[] = useMemo(() => {
        return filteredResults.map(r => ({
            pairNumber: r.pairNumber,
            originalSampleId: r.originalSampleId,
            duplicateSampleId: r.duplicateSampleId,
            originalValue: r.originalValue,
            duplicateValue: r.duplicateValue,
            rpd: r.rpd,
            hard: r.hard,
            pass: r.pass,
            element: r.element,
        }));
    }, [filteredResults]);

    // Prepare histogram data for RPD distribution
    const precisionMethod = filteredResults[0]?.precisionMethod || 'rpd';
    const targetPrecision = filteredResults[0]?.targetPrecision || 20;
    
    const histogramData: HistogramDataPoint[] = useMemo(() => {
        return filteredResults.map((r, index) => ({
            index,
            value: precisionMethod === 'rpd' ? r.rpd : r.hard,
            sampleId: `${r.originalSampleId}/${r.duplicateSampleId}`,
            pass: r.pass,
        }));
    }, [filteredResults, precisionMethod]);

    // Table columns for scatter data
    const tableColumns: TableColumn<ScatterDataPoint>[] = useMemo(() => [
        { key: 'pairNumber', header: '#', width: '50px', align: 'center' },
        { key: 'originalSampleId', header: 'Original ID', width: '130px' },
        { key: 'originalValue', header: 'Orig. Value', align: 'right', format: (v) => (v as number).toFixed(4) },
        { key: 'duplicateSampleId', header: 'Duplicate ID', width: '130px' },
        { key: 'duplicateValue', header: 'Dup. Value', align: 'right', format: (v) => (v as number).toFixed(4) },
        { key: 'rpd', header: 'RPD (%)', align: 'right', format: (v) => (v as number).toFixed(2) },
        { 
            key: 'pass', 
            header: 'Status', 
            align: 'center',
            render: (v) => v ? (
                <span className="inline-flex items-center gap-1 text-status-success text-xs">
                    <CheckCircle2 className="w-3.5 h-3.5" /> Pass
                </span>
            ) : (
                <span className="inline-flex items-center gap-1 text-status-error text-xs">
                    <AlertTriangle className="w-3.5 h-3.5" /> Fail
                </span>
            )
        },
    ], []);

    // Calculate summary metrics
    const totalPairs = filteredResults.length;
    const passedPairs = filteredResults.filter(r => r.pass).length;
    const failedPairs = totalPairs - passedPairs;
    const passRate = totalPairs > 0 ? (passedPairs / totalPairs) * 100 : 0;

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

    return (
        <div className="space-y-6">
            {/* Header & Controls */}
            <div className="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h3 className="text-2xl font-bold text-slate-50 flex items-center gap-2">
                        <Copy className="w-6 h-6 text-purple-400" />
                        Duplicates Precision Analysis
                    </h3>
                    <p className="text-sm text-slate-400 mt-1">
                        Monitor analytical precision through duplicate sample pairs
                    </p>
                </div>

                <div className="flex items-center gap-4">
                    {/* View Mode Toggle */}
                    <div className="flex items-center bg-surface-dark rounded-lg p-1 border border-secondary-dark">
                        <button
                            onClick={() => setViewMode('chart')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'chart' ? 'bg-purple-500 text-white' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <BarChart3 className="w-3.5 h-3.5" />
                            Charts
                        </button>
                        <button
                            onClick={() => setViewMode('table')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'table' ? 'bg-purple-500 text-white' : 'text-slate-400 hover:text-slate-200'
                            }`}
                        >
                            <Table className="w-3.5 h-3.5" />
                            Table
                        </button>
                        <button
                            onClick={() => setViewMode('both')}
                            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
                                viewMode === 'both' ? 'bg-purple-500 text-white' : 'text-slate-400 hover:text-slate-200'
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
                            className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-purple-500/50 outline-none"
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
                            <p className="text-sm text-slate-400">Total Pairs</p>
                            <p className="text-2xl font-bold text-slate-50">{totalPairs}</p>
                        </div>
                        <Info className="w-8 h-8 text-accent" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Within Target</p>
                            <p className="text-2xl font-bold text-status-success">{passedPairs}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-status-success" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Poor Precision</p>
                            <p className="text-2xl font-bold text-status-error">{failedPairs}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-status-error" />
                    </div>
                </div>

                <div className="bg-surface border border-secondary-dark rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-slate-400">Pass Rate</p>
                            <p className={`text-2xl font-bold ${passRate >= 90 ? 'text-status-success' : passRate >= 75 ? 'text-status-warning' : 'text-status-error'}`}>
                                {passRate.toFixed(1)}%
                            </p>
                        </div>
                        <TrendingUp className={`w-8 h-8 ${passRate >= 90 ? 'text-status-success' : passRate >= 75 ? 'text-status-warning' : 'text-status-error'}`} />
                    </div>
                </div>
            </div>

            {/* Precision Method Info */}
            <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                <div className="flex items-start gap-3">
                    <Info className="w-5 h-5 text-purple-400 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 className="font-semibold text-purple-300">
                            Precision Method: {precisionMethod.toUpperCase()}
                        </h4>
                        <p className="text-sm text-purple-200/80 mt-1">
                            {precisionMethod === 'rpd' && (
                                <>
                                    <strong>RPD (Relative Percent Difference)</strong>: |Original - Duplicate| / ((Original + Duplicate) / 2) × 100%
                                    <span className="ml-2 text-purple-300">Target: ≤{targetPrecision}%</span>
                                </>
                            )}
                            {precisionMethod === 'hard' && (
                                <>
                                    <strong>HARD (Half Absolute Relative Difference)</strong>: |Original - Duplicate| / MAX(Original, Duplicate) × 100%
                                    <span className="ml-2 text-purple-300">Target: ≤{targetPrecision}%</span>
                                </>
                            )}
                        </p>
                    </div>
                </div>
            </div>

            {/* Charts & Table Layout */}
            {(viewMode === 'chart' || viewMode === 'both') && (
                <div className="grid gap-6 lg:grid-cols-2">
                    {/* Scatter Plot */}
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <h4 className="text-lg font-semibold text-slate-50 mb-2">
                            Original vs Duplicate Values
                        </h4>
                        <PlotlyScatterPlot
                            data={scatterData}
                            element={selectedElement}
                            selectedIndices={selectedIndices}
                            onSelectionChange={handleChartSelection}
                            onPointClick={handlePointClick}
                            height={380}
                        />
                    </div>

                    {/* RPD Distribution */}
                    <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                        <h4 className="text-lg font-semibold text-slate-50 mb-2">
                            {precisionMethod.toUpperCase()} Distribution
                        </h4>
                        <PlotlyHistogram
                            data={histogramData}
                            title=""
                            xAxisLabel={`${precisionMethod.toUpperCase()} (%)`}
                            threshold={targetPrecision}
                            thresholdLabel="Target"
                            binCount={15}
                            height={380}
                        />
                    </div>
                </div>
            )}

            {/* Data Table */}
            {(viewMode === 'table' || viewMode === 'both') && (
                <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-slate-50 mb-4 flex items-center gap-2">
                        <Table className="w-5 h-5 text-purple-400" />
                        Duplicate Pairs Data
                    </h4>
                    <SyncedDataTable
                        data={scatterData}
                        columns={tableColumns}
                        selectedIndices={selectedIndices}
                        onRowClick={handleRowClick}
                        pageSize={15}
                        maxHeight="400px"
                        exportFilename={`duplicates_${selectedElement}`}
                    />
                </div>
            )}

            {/* Statistics Table */}
            {statistics && (
                <div className="bg-surface border border-secondary-dark rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-slate-50 mb-4">
                        Statistical Summary
                    </h4>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Mean RPD</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.meanRPD.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Mean HARD</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.meanHARD.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Within Target</p>
                            <p className={`text-lg font-semibold ${statistics.withinTarget >= 90 ? 'text-status-success' : statistics.withinTarget >= 75 ? 'text-status-warning' : 'text-status-error'}`}>
                                {statistics.withinTarget.toFixed(1)}%
                            </p>
                        </div>

                        <div className="p-4 bg-surface-light rounded-lg">
                            <p className="text-sm text-slate-400">Pair Count</p>
                            <p className="text-lg font-semibold text-slate-50">
                                {statistics.count}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Flagged Pairs Alert */}
            {results.flaggedPairs.length > 0 && (
                <div className="bg-status-error/10 border border-status-error/30 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-status-error flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-status-error">
                                Poor Precision Pairs ({results.flaggedPairs.length})
                            </h4>
                            <p className="text-sm text-status-error/80 mt-1">
                                The following duplicate pairs exceed the target precision ({targetPrecision}% {precisionMethod.toUpperCase()}):
                            </p>
                            <div className="mt-3 max-h-40 overflow-y-auto">
                                <table className="min-w-full text-sm">
                                    <thead className="bg-status-error/20">
                                        <tr>
                                            <th className="px-3 py-2 text-left text-status-error">Original</th>
                                            <th className="px-3 py-2 text-left text-status-error">Duplicate</th>
                                            <th className="px-3 py-2 text-left text-status-error">Element</th>
                                            <th className="px-3 py-2 text-right text-status-error">RPD</th>
                                            <th className="px-3 py-2 text-right text-status-error">HARD</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {results.flaggedPairs.map((pair, idx) => (
                                            <tr key={idx} className="border-t border-status-error/30">
                                                <td className="px-3 py-2 text-status-error/80">{pair.originalSampleId}</td>
                                                <td className="px-3 py-2 text-status-error/80">{pair.duplicateSampleId}</td>
                                                <td className="px-3 py-2 text-status-error/80">{pair.element}</td>
                                                <td className="px-3 py-2 text-right text-status-error/80 font-mono">
                                                    {pair.rpd.toFixed(2)}%
                                                </td>
                                                <td className="px-3 py-2 text-right text-status-error/80 font-mono">
                                                    {pair.hard.toFixed(2)}%
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
