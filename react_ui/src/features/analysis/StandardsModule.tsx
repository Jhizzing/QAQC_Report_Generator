import React, { useState, useMemo } from 'react';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
    ReferenceLine, ResponsiveContainer, Legend
} from 'recharts';
import { TrendingUp, AlertTriangle, CheckCircle2, Info } from 'lucide-react';
import type { StandardsAnalysisResults } from './standardsEngine';

interface StandardsModuleProps {
    results: StandardsAnalysisResults;
}

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
    const chartData = useMemo(() => {
        return filteredResults.map(r => ({
            sampleNumber: r.sampleNumber,
            value: r.measuredValue,
            certified: r.certifiedValue,
            pass: r.pass,
            sampleId: r.sampleId
        }));
    }, [filteredResults]);

    const certifiedValue = filteredResults[0]?.certifiedValue || 0;
    const upperLimit = filteredResults[0]?.upperLimit || 0;
    const lowerLimit = filteredResults[0]?.lowerLimit || 0;

    // Calculate summary metrics
    const totalSamples = filteredResults.length;
    const passedSamples = filteredResults.filter(r => r.pass).length;
    const failedSamples = totalSamples - passedSamples;
    const passRate = totalSamples > 0 ? (passedSamples / totalSamples) * 100 : 0;

    return (
        <div className="space-y-6">
            {/* Header & CRM Selector */}
            <div className="flex items-center justify-between">
                <div>
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                        <TrendingUp className="w-6 h-6 text-primary" />
                        Standards Control Chart
                    </h3>
                    <p className="text-sm text-gray-500 mt-1">
                        Monitor CRM accuracy against certified values
                    </p>
                </div>

                <div className="w-64">
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Select CRM / Element
                    </label>
                    <select
                        value={selectedCRM}
                        onChange={(e) => setSelectedCRM(e.target.value)}
                        className="w-full px-4 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary/50 outline-none"
                    >
                        {crmElements.map(({ key, crm, element }) => (
                            <option key={key} value={key}>
                                {crm} - {element}
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
                            <p className="text-sm text-gray-500">Total Samples</p>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">{totalSamples}</p>
                        </div>
                        <Info className="w-8 h-8 text-blue-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Passed</p>
                            <p className="text-2xl font-bold text-green-600">{passedSamples}</p>
                        </div>
                        <CheckCircle2 className="w-8 h-8 text-green-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Failed</p>
                            <p className="text-2xl font-bold text-red-600">{failedSamples}</p>
                        </div>
                        <AlertTriangle className="w-8 h-8 text-red-500" />
                    </div>
                </div>

                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm text-gray-500">Pass Rate</p>
                            <p className={`text-2xl font-bold ${passRate >= 95 ? 'text-green-600' : passRate >= 85 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {passRate.toFixed(1)}%
                            </p>
                        </div>
                        <TrendingUp className={`w-8 h-8 ${passRate >= 95 ? 'text-green-500' : passRate >= 85 ? 'text-yellow-500' : 'text-red-500'}`} />
                    </div>
                </div>
            </div>

            {/* Control Chart */}
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-6">
                <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                    Control Chart
                </h4>

                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
                        <XAxis
                            dataKey="sampleNumber"
                            label={{ value: 'Sample Sequence', position: 'insideBottom', offset: -5 }}
                            stroke="#6b7280"
                        />
                        <YAxis
                            label={{ value: `${selectedCRM.split('|')[1]} (${filteredResults[0]?.unit || ''})`, angle: -90, position: 'insideLeft' }}
                            stroke="#6b7280"
                        />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#fff', border: '1px solid #e0e0e0', borderRadius: '8px' }}
                            formatter={(value: any, name: string) => {
                                if (name === 'value') return [value.toFixed(4), 'Measured'];
                                if (name === 'certified') return [value.toFixed(4), 'Certified'];
                                return [value, name];
                            }}
                            labelFormatter={(label) => {
                                const sample = chartData.find(d => d.sampleNumber === label);
                                return sample ? `Sample: ${sample.sampleId}` : `Sample ${label}`;
                            }}
                        />
                        <Legend />

                        {/* Certified value line */}
                        <ReferenceLine
                            y={certifiedValue}
                            stroke="#3b82f6"
                            strokeDasharray="5 5"
                            label={{ value: 'Certified', fill: '#3b82f6', fontSize: 12 }}
                        />

                        {/* Upper control limit */}
                        <ReferenceLine
                            y={upperLimit}
                            stroke="#ef4444"
                            strokeDasharray="3 3"
                            label={{ value: 'UCL', fill: '#ef4444', fontSize: 12 }}
                        />

                        {/* Lower control limit */}
                        <ReferenceLine
                            y={lowerLimit}
                            stroke="#ef4444"
                            strokeDasharray="3 3"
                            label={{ value: 'LCL', fill: '#ef4444', fontSize: 12 }}
                        />

                        <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#4A7C59"
                            strokeWidth={2}
                            name="Measured Value"
                            dot={(props: any) => {
                                const { cx, cy, payload } = props;
                                return (
                                    <circle
                                        cx={cx}
                                        cy={cy}
                                        r={5}
                                        fill={payload.pass ? '#10b981' : '#ef4444'}
                                        stroke="#fff"
                                        strokeWidth={2}
                                    />
                                );
                            }}
                        />
                    </LineChart>
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
                            <p className="text-sm text-gray-500">Mean</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.mean.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Std Dev (SD)</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.sd.toFixed(4)}
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">RSD (%)</p>
                            <p className="text-lg font-semibold text-gray-900 dark:text-white">
                                {statistics.rsd.toFixed(2)}%
                            </p>
                        </div>

                        <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                            <p className="text-sm text-gray-500">Pass Rate</p>
                            <p className={`text-lg font-semibold ${statistics.passRate >= 95 ? 'text-green-600' : statistics.passRate >= 85 ? 'text-yellow-600' : 'text-red-600'}`}>
                                {statistics.passRate.toFixed(1)}%
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

            {/* Flagged Batches Alert */}
            {results.flaggedBatches.length > 0 && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <div className="flex gap-3">
                        <AlertTriangle className="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                        <div>
                            <h4 className="font-semibold text-red-900 dark:text-red-100">
                                Flagged Batches ({results.flaggedBatches.length})
                            </h4>
                            <p className="text-sm text-red-800 dark:text-red-200 mt-1">
                                The following batches have consecutive standard failures and should be reviewed:
                            </p>
                            <ul className="list-disc list-inside text-sm text-red-800 dark:text-red-200 mt-2">
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
