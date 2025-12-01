import React, { useState, useMemo } from 'react';
import {
    ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
    ReferenceLine, ResponsiveContainer, BarChart, Bar
} from 'recharts';
import { Copy, AlertTriangle, CheckCircle2, Info, TrendingUp } from 'lucide-react';
import type { DuplicatesAnalysisResults } from './duplicatesEngine';
import { generatePrecisionHistogram } from './duplicatesEngine';

interface DuplicatesModuleProps {
    results: DuplicatesAnalysisResults;
}

export const DuplicatesModule: React.FC<DuplicatesModuleProps> = ({ results }) => {
    // Get unique elements
    const elements = useMemo(() => {
        const unique = new Set(results.results.map(r => r.element));
        return Array.from(unique);
    }, [results]);

    const [selectedElement, setSelectedElement] = useState(elements[0] || '');

    // Filter data for selected element
    const filteredResults = useMemo(() => {
        return results.results
            .filter(r => r.element === selectedElement)
            .sort((a, b) => a.pairNumber - b.pairNumber);
    }, [selectedElement, results]);

    const statistics = useMemo(() => {
        return results.statistics.find(s => s.element === selectedElement);
    }, [selectedElement, results]);

    // Prepare scatter plot data (Original vs Duplicate)
    const scatterData = useMemo(() => {
        return filteredResults.map(r => ({
            original: r.originalValue,
            duplicate: r.duplicateValue,
            pass: r.pass,
            rpd: r.rpd,
            hard: r.hard,
            originalId: r.originalSampleId,
            duplicateId: r.duplicateSampleId
        }));
    }, [filteredResults]);

    // Prepare precision histogram data
    const precisionMethod = filteredResults[0]?.precisionMethod || 'rpd';
    const histogramData = useMemo(() => {
        const values = filteredResults.map(r => precisionMethod === 'rpd' ? r.rpd : r.hard);
        return generatePrecisionHistogram(values, 10);
    }, [filteredResults, precisionMethod]);

    const targetPrecision = filteredResults[0]?.targetPrecision || 20;

    // Calculate summary metrics
    const totalPairs = filteredResults.length;
    const passedPairs = filteredResults.filter(r => r.pass).length;
    const failedPairs = totalPairs - passedPairs;
    const passRate = totalPairs > 0 ? (passedPairs / totalPairs) * 100 : 0;

    // Calculate max value for 1:1 line
    const maxValue = Math.max(
        ...scatterData.map(d => Math.max(d.original, d.duplicate)),
        1
    );

    return (
        <div className="space-y-6">
            {/* Header & Element Selector */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                        <Copy className="w-6 h-6 text-purple-500" />
                        Duplicates Precision Analysis
                    </h3>
                    <p className="text-sm text-gray-300 mt-1">
                        Monitor analytical precision through duplicate sample pairs
                    </p>
                </div>

                <div className="w-64">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Select Element
                    </label>
                    <select
                        value={selectedElement}
                        onChange={(e) => setSelectedElement(e.target.value)}
                        className="w-full px-4 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary/50 outline-none"
                    >
                        {elements.map(element => (
                            <option key={element} value={element}>
                                {element}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-300">Total Pairs</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalPairs}</p>
                        </div>
                        <Info className="w-8 h-8 text-blue-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-300">Within Target</p>
                            <p className="text-2xl font-bold text-green-600">{passedPairs}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-green-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-300">Poor Precision</p>
                            <p className="text-2xl font-bold text-red-600">{failedPairs}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-red-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-300">Pass Rate</p>
                            <p className={`text-2xl font-bold ${passRate >= 90 ? 'text-green-600' : passRate >= 75 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {passRate.toFixed(1)}%
                            </p>
                        </div>
                        <TrendingUp className={`w-8 h-8 ${passRate >= 90 ? 'text-green-500' : passRate >= 75 ? 'text-yellow-500' : 'text-red-500'}`} />
                    </div>
                </div>
            </div>

            {/* Precision Method Info */}
            <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
                <div className="flex items-start gap-3">
                    <Info className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                    <div>
                        <h4 className="font-semibold text-blue-900 dark:text-blue-100">
                            Precision Method: {precisionMethod.toUpperCase()}
                        </h4>
                        <p className="text-sm text-blue-800 dark:text-blue-200 mt-1">
                            {precisionMethod === 'rpd' && (
                                <>
                                    <strong>RPD (Relative Percent Difference)</strong>: RPD = |Original - Duplicate| / ((Original + Duplicate) / 2) × 100%
                                    <br />
                                    Target: ≤{targetPrecision}%
                                </>
                            )}
                            {precisionMethod === 'hard' && (
                                <>
                                    <strong>HARD (Half Absolute Relative Difference)</strong>: HARD = |Original - Duplicate| / MAX(Original, Duplicate) × 100%
                                    <br />
                                    Target: ≤{targetPrecision}%
                                </>
                            )}
                        </p>
                    </div>
                </div>
            </div>

            {/* Original vs Duplicate Scatter Plot */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Original vs Duplicate Values
                </h4>

                <ResponsiveContainer width="100%" height={400}>
                    <ScatterChart>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis
                            dataKey="original"
                            label={{ value: `Original (${filteredResults[0]?.unit || ''})`, position: 'insideBottom', offset: -5 }}
                            stroke="#6b7280"
                        />
                        <YAxis
                            label={{ value: `Duplicate (${filteredResults[0]?.unit || ''})`, angle: -90, position: 'insideLeft' }}
                            stroke="#6b7280"
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e0e0e0', borderRadius: '8px' }}
                            formatter={(value: any, name: string) => {
                                if (name === 'original' || name === 'duplicate') {
                                    return [value.toFixed(4), name.charAt(0).toUpperCase() + name.slice(1)];
                                }
                                return [value, name];
                            }}
                            labelFormatter={(_, payload) => {
                                if (payload && payload[0]) {
                                    const data = payload[0].payload;
                                    return `Pair: ${data.originalId} / ${data.duplicateId}`;
                                }
                                return 'Duplicate Pair';
                            }}
                        />

                        {/* 1:1 Perfect agreement line */}
                        <ReferenceLine
                            segment={[{ x: 0, y: 0 }, { x: maxValue, y: maxValue }]}
                            stroke="#3b82f6"
                            strokeDasharray="5 5"
                            label={{ value: '1:1 Perfect Agreement', fill: '#3b82f6', fontSize: 12, position: 'insideTopRight' }}
                        />

                        <Scatter
                            name="Duplicate Pairs"
                            data={scatterData}
                            fill="#8b5cf6"
                            shape={(props: any) => {
                                const { cx, cy, payload } = props;
                                const color = payload.pass ? '#10b981' : '#ef4444'; // green or red

                                return (
                                    <circle
                                        cx={cx}
                                        cy={cy}
                                        r={5}
                                        fill={color}
                                        stroke="#fff"
                                        strokeWidth={2}
                                    />
                                );
                            }}
                        />
                    </ScatterChart>
                </ResponsiveContainer>
            </div>

            {/* Precision Distribution Histogram */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    {precisionMethod.toUpperCase()} Distribution
                </h4>

                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={histogramData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis
                            dataKey="bin"
                            label={{ value: `${precisionMethod.toUpperCase()} Range`, position: 'insideBottom', offset: -5 }}
                            stroke="#6b7280"
                        />
                        <YAxis
                            label={{ value: 'Frequency', angle: -90, position: 'insideLeft' }}
                            stroke="#6b7280"
                        />
                        <Tooltip />
                        <ReferenceLine
                            x={`${targetPrecision.toFixed(1)}`}
                            stroke="#ef4444"
                            strokeDasharray="3 3"
                            label={{ value: 'Target', fill: '#ef4444', fontSize: 12 }}
                        />
                        <Bar dataKey="count" fill="#8b5cf6" />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Statistics Table */}
            {statistics && (
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Statistical Summary
                    </h4>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-300">Mean RPD</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.meanRPD.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-300">Mean HARD</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.meanHARD.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-300">Within Target</p>
                            <p className={`text-lg font-semibold ${statistics.withinTarget >= 90 ? 'text-green-600' : statistics.withinTarget >= 75 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {statistics.withinTarget.toFixed(1)}%
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-300">Pair Count</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.count}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Flagged Pairs Alert */}
            {results.flaggedPairs.length > 0 && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-red-900 dark:text-red-100">
                                Poor Precision Pairs ({results.flaggedPairs.length})
                            </h4>
                            <p className="text-sm text-red-800 dark:text-red-200 mt-1">
                                The following duplicate pairs exceed the target precision ({targetPrecision}% {precisionMethod.toUpperCase()}):
                            </p>
                            <div className="mt-3 max-h-40 overflow-y-auto">
                                <table className="min-w-full text-sm">
                                    <thead className="bg-red-100 dark:bg-red-900/30">
                                        <tr>
                                            <th className="px-3 py-2 text-left text-red-900 dark:text-red-100">Original</th>
                                            <th className="px-3 py-2 text-left text-red-900 dark:text-red-100">Duplicate</th>
                                            <th className="px-3 py-2 text-left text-red-900 dark:text-red-100">Element</th>
                                            <th className="px-3 py-2 text-right text-red-900 dark:text-red-100">RPD</th>
                                            <th className="px-3 py-2 text-right text-red-900 dark:text-red-100">HARD</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {results.flaggedPairs.map((pair, idx) => (
                                            <tr key={idx} className="border-t border-red-200 dark:border-red-800">
                                                <td className="px-3 py-2 text-red-800 dark:text-red-200">{pair.originalSampleId}</td>
                                                <td className="px-3 py-2 text-red-800 dark:text-red-200">{pair.duplicateSampleId}</td>
                                                <td className="px-3 py-2 text-red-800 dark:text-red-200">{pair.element}</td>
                                                <td className="px-3 py-2 text-right text-red-800 dark:text-red-200 font-mono">
                                                    {pair.rpd.toFixed(2)}%
                                                </td>
                                                <td className="px-3 py-2 text-right text-red-800 dark:text-red-200 font-mono">
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
