import React, { useState, useMemo } from 'react';
import {
    ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip,
    ReferenceLine, ResponsiveContainer, BarChart, Bar
} from 'recharts';
import { Droplet, AlertTriangle, CheckCircle2, Info, TrendingDown } from 'lucide-react';
import type { BlanksAnalysisResults } from './blanksEngine';
import { generateBlankHistogram } from './blanksEngine';

interface BlanksModuleProps {
    results: BlanksAnalysisResults;
}

export const BlanksModule: React.FC<BlanksModuleProps> = ({ results }) => {
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
            .sort((a, b) => a.sampleNumber - b.sampleNumber);
    }, [selectedElement, results]);

    const statistics = useMemo(() => {
        return results.statistics.find(s => s.element === selectedElement);
    }, [selectedElement, results]);

    // Prepare scatter plot data
    const scatterData = useMemo(() => {
        return filteredResults.map(r => ({
            sampleNumber: r.sampleNumber,
            value: r.measuredValue,
            status: r.status,
            sampleId: r.sampleId
        }));
    }, [filteredResults]);

    // Prepare histogram data
    const histogramData = useMemo(() => {
        const values = filteredResults.map(r => r.measuredValue);
        return generateBlankHistogram(values, 10);
    }, [filteredResults]);

    const detectionLimit = filteredResults[0]?.detectionLimit || 0;
    const contaminationThreshold = filteredResults[0]?.contaminationThreshold || 0;

    // Calculate summary metrics
    const totalBlanks = filteredResults.length;
    const passedBlanks = filteredResults.filter(r => r.pass).length;
    const warningBlanks = filteredResults.filter(r => r.status === 'warning').length;
    const contaminatedBlanks = filteredResults.filter(r => r.contaminated).length;

    return (
        <div className="space-y-6">
            {/* Header & Element Selector */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                        <Droplet className="w-6 h-6 text-blue-500" />
                        Blanks Contamination Monitor
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                        Track blank samples for contamination and detection limit compliance
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
                            <p className="text-sm text-gray-500">Total Blanks</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalBlanks}</p>
                        </div>
                        <Info className="w-8 h-8 text-blue-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Below Detection</p>
                            <p className="text-2xl font-bold text-green-600">{passedBlanks}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-green-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Warning</p>
                            <p className="text-2xl font-bold text-yellow-600">{warningBlanks}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-yellow-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Contaminated</p>
                            <p className="text-2xl font-bold text-red-600">{contaminatedBlanks}</p>
                        </div>
                        <TrendingDown className="w-8 h-8 text-red-500" />
                    </div>
                </div>
            </div>

            {/* Scatter Plot */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Blank Values Over Time
                </h4>

                <ResponsiveContainer width="100%" height={400}>
                    <ScatterChart>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis
                            dataKey="sampleNumber"
                            label={{ value: 'Sample Sequence', position: 'insideBottom', offset: -5 }}
                            stroke="#6b7280"
                        />
                        <YAxis
                            label={{ value: `${selectedElement} (${filteredResults[0]?.unit || ''})`, angle: -90, position: 'insideLeft' }}
                            stroke="#6b7280"
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e0e0e0', borderRadius: '8px' }}
                            formatter={(value: any) => value.toFixed(4)}
                            labelFormatter={(label) => {
                                const sample = scatterData.find(d => d.sampleNumber === label);
                                return sample ? `Sample: ${sample.sampleId}` : `Sample ${label}`;
                            }}
                        />

                        {/* Detection limit line */}
                        <ReferenceLine
                            y={detectionLimit}
                            stroke="#f59e0b"
                            strokeDasharray="5 5"
                            label={{ value: 'Detection Limit', fill: '#f59e0b', fontSize: 12 }}
                        />

                        {/* Contamination threshold line */}
                        <ReferenceLine
                            y={contaminationThreshold}
                            stroke="#ef4444"
                            strokeDasharray="3 3"
                            label={{ value: 'Contamination', fill: '#ef4444', fontSize: 12 }}
                        />

                        <Scatter
                            name="Blank Values"
                            data={scatterData}
                            fill="#3b82f6"
                            shape={(props: any) => {
                                const { cx, cy, payload } = props;
                                let color = '#10b981'; // green - pass
                                if (payload.status === 'warning') color = '#f59e0b'; // yellow
                                if (payload.status === 'fail') color = '#ef4444'; // red

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

            {/* Histogram */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Value Distribution
                </h4>

                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={histogramData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis
                            dataKey="bin"
                            label={{ value: `${selectedElement} Range (${filteredResults[0]?.unit || ''})`, position: 'insideBottom', offset: -5 }}
                            stroke="#6b7280"
                            angle={-45}
                            textAnchor="end"
                            height={80}
                        />
                        <YAxis
                            label={{ value: 'Frequency', angle: -90, position: 'insideLeft' }}
                            stroke="#6b7280"
                        />
                        <Tooltip />
                        <Bar dataKey="count" fill="#3b82f6" />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            {/* Statistics Table */}
            {statistics && (
                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                    <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Statistical Summary
                    </h4>

                    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Maximum</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.max.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Mean</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.mean.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Median</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.median.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Contamination Rate</p>
                            <p className={`text-lg font-semibold ${statistics.contaminationRate === 0 ? 'text-green-600' : statistics.contaminationRate < 5 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {statistics.contaminationRate.toFixed(1)}%
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Count</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.count}
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Flagged Blanks Alert */}
            {results.flaggedBlanks.length > 0 && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-red-900 dark:text-red-100">
                                Contaminated Blanks ({results.flaggedBlanks.length})
                            </h4>
                            <p className="text-sm text-red-800 dark:text-red-200 mt-1">
                                The following blanks exceed the contamination threshold ({contaminationThreshold.toFixed(3)} {filteredResults[0]?.unit}):
                            </p>
                            <div className="mt-3 max-h-40 overflow-y-auto">
                                <table className="min-w-full text-sm">
                                    <thead className="bg-red-100 dark:bg-red-900/30">
                                        <tr>
                                            <th className="px-3 py-2 text-left text-red-900 dark:text-red-100">Sample ID</th>
                                            <th className="px-3 py-2 text-left text-red-900 dark:text-red-100">Element</th>
                                            <th className="px-3 py-2 text-right text-red-900 dark:text-red-100">Value</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {results.flaggedBlanks.map((blank, idx) => (
                                            <tr key={idx} className="border-t border-red-200 dark:border-red-800">
                                                <td className="px-3 py-2 text-red-800 dark:text-red-200">{blank.sampleId}</td>
                                                <td className="px-3 py-2 text-red-800 dark:text-red-200">{blank.element}</td>
                                                <td className="px-3 py-2 text-right text-red-800 dark:text-red-200 font-mono">
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
