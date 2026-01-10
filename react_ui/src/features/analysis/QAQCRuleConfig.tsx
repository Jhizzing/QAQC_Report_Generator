import React, { useState, useEffect } from 'react';
import { ArrowRight, ArrowLeft, CheckCircle2, AlertTriangle, Info } from 'lucide-react';
import { getCRMsByCategory, type CRMValue } from '../../data/crmDatabase';

interface QAQCRuleConfigProps {
    category: 'gold' | 'pxrf' | 'multi' | 'photon';
    methodologyConfig: any;
    onComplete: (config: QAQCConfig) => void;
}

export interface QAQCConfig {
    standards: StandardsConfig;
    blanks: BlanksConfig;
    duplicates: DuplicatesConfig;
}

interface StandardsConfig {
    selectedCRMs: string[];
    toleranceType: 'percentage' | 'absolute' | 'sd';
    toleranceValue: number;
    failureThreshold: number; // consecutive failures to flag
}

interface BlanksConfig {
    detectionLimit: number;
    detectionLimitUnit: 'ppm' | 'ppb' | 'pct';
    contaminationMultiplier: number; // e.g., 3x detection limit
}

interface DuplicatesConfig {
    precisionTarget: number; // RPD% or HARD%
    precisionMethod: 'rpd' | 'hard';
    failureThreshold: number;
}

export const QAQCRuleConfig: React.FC<QAQCRuleConfigProps> = ({ category, methodologyConfig, onComplete }) => {
    const [currentTab, setCurrentTab] = useState<'standards' | 'blanks' | 'duplicates'>('standards');
    const [availableCRMs, setAvailableCRMs] = useState<CRMValue[]>([]);

    useEffect(() => {
        // Load CRMs based on category
        let dbCategory: 'gold' | 'pxrf' | 'multi-element';
        if (category === 'photon') {
            dbCategory = 'gold';
        } else if (category === 'multi') {
            dbCategory = 'multi-element';
        } else {
            dbCategory = category;
        }

        const crms = getCRMsByCategory(dbCategory);

        if (category === 'photon') {
            const photonCRMs = crms.filter(crm =>
                Object.values(crm.elements).some(el => el.method === 'PhotonAssay')
            );
            setAvailableCRMs(photonCRMs.length > 0 ? photonCRMs : crms);
        } else {
            setAvailableCRMs(crms);
        }
    }, [category]);

    // Log methodology config for future integration
    console.log('Methodology config:', methodologyConfig);

    const [standardsConfig, setStandardsConfig] = useState<StandardsConfig>({
        selectedCRMs: [],
        toleranceType: 'percentage',
        toleranceValue: 10,
        failureThreshold: 3
    });

    const [blanksConfig, setBlanksConfig] = useState<BlanksConfig>({
        detectionLimit: category === 'gold' ? 0.01 : 1,
        detectionLimitUnit: category === 'gold' ? 'ppm' : 'ppm',
        contaminationMultiplier: 3
    });

    const [duplicatesConfig, setDuplicatesConfig] = useState<DuplicatesConfig>({
        precisionTarget: 20,
        precisionMethod: 'hard',
        failureThreshold: 3
    });

    const handleComplete = () => {
        const config: QAQCConfig = {
            standards: standardsConfig,
            blanks: blanksConfig,
            duplicates: duplicatesConfig
        };
        onComplete(config);
    };

    const isValid = standardsConfig.selectedCRMs.length > 0;

    return (
        <div className="max-w-5xl mx-auto mt-8">
            {/* Header */}
            <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-slate-50 mb-2">
                    Configure QAQC Rules
                </h2>
                <p className="text-slate-400">
                    Set acceptance criteria for standards, blanks, and duplicates
                </p>
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-6 border-b border-secondary-dark">
                {(['standards', 'blanks', 'duplicates'] as const).map((tab) => (
                    <button
                        key={tab}
                        onClick={() => setCurrentTab(tab)}
                        className={`
              px-6 py-3 font-semibold capitalize transition-all relative
              ${currentTab === tab
                                ? 'text-primary border-b-2 border-primary'
                                : 'text-slate-400 hover:text-slate-200'
                            }
            `}
                    >
                        {tab}
                        {tab === 'standards' && standardsConfig.selectedCRMs.length > 0 && (
                            <CheckCircle2 className="w-4 h-4 text-status-success absolute -top-1 -right-1" />
                        )}
                    </button>
                ))}
            </div>

            {/* Tab Content */}
            <div className="bg-surface rounded-xl border border-secondary-dark p-8 min-h-[400px]">
                {currentTab === 'standards' && (
                    <div className="space-y-6">
                        <div>
                            <h3 className="text-lg font-bold text-slate-50 mb-4">
                                Select Certified Reference Materials (CRMs)
                            </h3>
                            <div className="space-y-2">
                                {availableCRMs.map((crm) => {
                                    const isSelected = standardsConfig.selectedCRMs.includes(crm.id);
                                    const gradeString = Object.entries(crm.elements)
                                        .map(([el, data]) => `${data.certified} ${data.unit} ${el}`)
                                        .join(', ');

                                    return (
                                        <button
                                            key={crm.id}
                                            onClick={() => {
                                                setStandardsConfig({
                                                    ...standardsConfig,
                                                    selectedCRMs: isSelected
                                                        ? standardsConfig.selectedCRMs.filter(c => c !== crm.id)
                                                        : [...standardsConfig.selectedCRMs, crm.id]
                                                });
                                            }}
                                            className={`
                                        w-full text-left p-4 rounded-xl border-2 transition-all flex items-center justify-between group
                                        ${isSelected
                                                    ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                                                    : 'border-secondary-light bg-surface-light hover:border-primary/50 hover:bg-surface'
                                                }
                                    `}
                                        >
                                            <div>
                                                <div className="flex items-center gap-2">
                                                    <span className={`font-bold ${isSelected
                                                            ? 'text-primary'
                                                            : 'text-slate-50 group-hover:text-primary transition-colors'
                                                        }`}>
                                                        {crm.name}
                                                    </span>
                                                    {isSelected && (
                                                        <span className="px-2 py-0.5 rounded-full bg-primary/20 text-primary text-xs font-medium">
                                                            Selected
                                                        </span>
                                                    )}
                                                </div>
                                                <div className="text-sm text-slate-400 mt-1">
                                                    {gradeString}
                                                </div>
                                            </div>
                                            <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${isSelected
                                                    ? 'border-primary bg-primary text-slate-50'
                                                    : 'border-secondary-light group-hover:border-primary'
                                                }`}>
                                                {isSelected && <CheckCircle2 className="w-4 h-4" />}
                                            </div>
                                        </button>
                                    );
                                })}
                                {availableCRMs.length === 0 && (
                                    <div className="text-center py-8 text-slate-500">
                                        No standards found for this category.
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6 border-t border-secondary-dark">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Tolerance Type
                                </label>
                                <select
                                    value={standardsConfig.toleranceType}
                                    onChange={(e) => setStandardsConfig({
                                        ...standardsConfig,
                                        toleranceType: e.target.value as 'percentage' | 'absolute' | 'sd'
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                >
                                    <option value="percentage">Percentage (±%)</option>
                                    <option value="absolute">Absolute Value</option>
                                    <option value="sd">Standard Deviations (±SD)</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Tolerance Value
                                </label>
                                <input
                                    type="number"
                                    value={standardsConfig.toleranceValue}
                                    onChange={(e) => setStandardsConfig({
                                        ...standardsConfig,
                                        toleranceValue: parseFloat(e.target.value)
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    step="0.1"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Consecutive Failures to Flag
                                </label>
                                <input
                                    type="number"
                                    value={standardsConfig.failureThreshold}
                                    onChange={(e) => setStandardsConfig({
                                        ...standardsConfig,
                                        failureThreshold: parseInt(e.target.value)
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    min="1"
                                    max="10"
                                />
                                <p className="text-xs text-slate-500 mt-1">
                                    Flag batch if this many consecutive standards fail
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {currentTab === 'blanks' && (
                    <div className="space-y-6">
                        <div className="bg-accent/10 border border-accent/30 p-4 rounded-lg flex gap-3">
                            <Info className="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
                            <div className="text-sm text-accent/90">
                                Blanks are used to monitor contamination. Set the detection limit and contamination threshold.
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Detection Limit
                                </label>
                                <div className="flex gap-2">
                                    <input
                                        type="number"
                                        value={blanksConfig.detectionLimit}
                                        onChange={(e) => setBlanksConfig({
                                            ...blanksConfig,
                                            detectionLimit: parseFloat(e.target.value)
                                        })}
                                        className="flex-1 px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                        step="0.001"
                                    />
                                    <select
                                        value={blanksConfig.detectionLimitUnit}
                                        onChange={(e) => setBlanksConfig({
                                            ...blanksConfig,
                                            detectionLimitUnit: e.target.value as 'ppm' | 'ppb' | 'pct'
                                        })}
                                        className="px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    >
                                        <option value="ppm">ppm</option>
                                        <option value="ppb">ppb</option>
                                        <option value="pct">%</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Contamination Multiplier
                                </label>
                                <input
                                    type="number"
                                    value={blanksConfig.contaminationMultiplier}
                                    onChange={(e) => setBlanksConfig({
                                        ...blanksConfig,
                                        contaminationMultiplier: parseFloat(e.target.value)
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    step="0.5"
                                    min="1"
                                    max="10"
                                />
                                <p className="text-xs text-slate-500 mt-1">
                                    Flag if blank {">"} {blanksConfig.contaminationMultiplier}× detection limit
                                </p>
                            </div>
                        </div>

                        <div className="bg-status-warning/10 border border-status-warning/30 p-4 rounded-lg flex gap-3">
                            <AlertTriangle className="w-5 h-5 text-status-warning flex-shrink-0 mt-0.5" />
                            <div className="text-sm text-status-warning">
                                Current threshold: Blanks exceeding <strong>{(blanksConfig.detectionLimit * blanksConfig.contaminationMultiplier).toFixed(3)} {blanksConfig.detectionLimitUnit}</strong> will be flagged
                            </div>
                        </div>
                    </div>
                )}

                {currentTab === 'duplicates' && (
                    <div className="space-y-6">
                        <div className="bg-accent/10 border border-accent/30 p-4 rounded-lg flex gap-3">
                            <Info className="w-5 h-5 text-accent flex-shrink-0 mt-0.5" />
                            <div className="text-sm text-accent/90">
                                Duplicates measure analytical precision. Choose your precision calculation method and target.
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Precision Method
                                </label>
                                <select
                                    value={duplicatesConfig.precisionMethod}
                                    onChange={(e) => setDuplicatesConfig({
                                        ...duplicatesConfig,
                                        precisionMethod: e.target.value as 'rpd' | 'hard'
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                >
                                    <option value="rpd">RPD (Relative Percent Difference)</option>
                                    <option value="hard">HARD (Half Absolute Relative Difference)</option>
                                </select>
                                <p className="text-xs text-slate-500 mt-1">
                                    {duplicatesConfig.precisionMethod === 'rpd'
                                        ? 'RPD = |A-B| / ((A+B)/2) × 100%'
                                        : 'HARD = |A-B| / MAX(A,B) × 100%'
                                    }
                                </p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Target Precision (%)
                                </label>
                                <input
                                    type="number"
                                    value={duplicatesConfig.precisionTarget}
                                    onChange={(e) => setDuplicatesConfig({
                                        ...duplicatesConfig,
                                        precisionTarget: parseFloat(e.target.value)
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    step="1"
                                    min="1"
                                    max="50"
                                />
                                <p className="text-xs text-slate-500 mt-1">
                                    Flag if {duplicatesConfig.precisionMethod.toUpperCase()} {">"} {duplicatesConfig.precisionTarget}%
                                </p>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-2">
                                    Consecutive Failures to Flag
                                </label>
                                <input
                                    type="number"
                                    value={duplicatesConfig.failureThreshold}
                                    onChange={(e) => setDuplicatesConfig({
                                        ...duplicatesConfig,
                                        failureThreshold: parseInt(e.target.value)
                                    })}
                                    className="w-full px-4 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    min="1"
                                    max="10"
                                />
                            </div>
                        </div>
                    </div>
                )}
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between mt-8">
                <button
                    onClick={() => setCurrentTab(
                        currentTab === 'standards' ? 'standards' :
                            currentTab === 'blanks' ? 'standards' : 'blanks'
                    )}
                    disabled={currentTab === 'standards'}
                    className="flex items-center gap-2 px-6 py-3 text-slate-400 hover:text-slate-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Previous
                </button>

                {currentTab === 'duplicates' ? (
                    <button
                        onClick={handleComplete}
                        disabled={!isValid}
                        className="flex items-center gap-2 px-8 py-3 bg-status-success text-slate-50 rounded-xl font-bold hover:bg-status-success/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                    >
                        <CheckCircle2 className="w-5 h-5" />
                        Complete Configuration
                    </button>
                ) : (
                    <button
                        onClick={() => setCurrentTab(
                            currentTab === 'standards' ? 'blanks' : 'duplicates'
                        )}
                        className="flex items-center gap-2 px-6 py-3 bg-primary text-slate-50 rounded-xl font-semibold hover:bg-primary-dark transition-all"
                    >
                        Next
                        <ArrowRight className="w-4 h-4" />
                    </button>
                )}
            </div>
        </div>
    );
};
