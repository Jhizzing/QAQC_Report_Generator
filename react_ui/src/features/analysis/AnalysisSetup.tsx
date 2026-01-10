import React, { useState, useEffect } from 'react';
import { 
    Layers, Beaker, Zap, ChevronDown, ChevronUp, 
    CheckCircle2, Play, Settings, Info
} from 'lucide-react';
import { getCRMsByCategory, type CRMValue } from '../../data/crmDatabase';
import { HelpTooltip } from '../../components/common/HelpTooltip';
import type { MethodologyConfig } from './MethodologyWizard';
import type { QAQCConfig } from './QAQCRuleConfig';

type AnalysisCategory = 'gold' | 'pxrf' | 'photon';

interface AnalysisSetupProps {
    /** Pre-selected category from demo data or previous state */
    initialCategory?: AnalysisCategory | null;
    onComplete: (result: {
        category: AnalysisCategory;
        methodologyConfig: MethodologyConfig;
        qaqcConfig: QAQCConfig;
    }) => void;
    /** Callback to navigate to Education Center */
    onNavigateToEducation?: (topicId: string) => void;
}

// Default configurations by category
const CATEGORY_DEFAULTS = {
    gold: {
        duplicateType: 'pulp' as const,
        gravimetricFinish: false,
        detectionLimit: 0.01,
        detectionLimitUnit: 'ppm' as const,
        toleranceValue: 10,
        precisionTarget: 20,
    },
    pxrf: {
        elements: ['Cu', 'Pb', 'Zn', 'Fe'],
        matrixCorrection: true,
        spectralInterference: true,
        detectionLimit: 1,
        detectionLimitUnit: 'ppm' as const,
        toleranceValue: 15,
        precisionTarget: 25,
    },
    photon: {
        elements: ['Au', 'Ag'],
        includeUncertainty: true,
        jarSize: '500',
        detectionLimit: 0.005,
        detectionLimitUnit: 'ppm' as const,
        toleranceValue: 10,
        precisionTarget: 15,
    },
};

// Pre-selected CRMs by category (common choices)
const DEFAULT_CRMS: Record<AnalysisCategory, string[]> = {
    gold: ['OREAS-102', 'OREAS-103'],
    pxrf: ['OREAS-100', 'OREAS-102a'],
    photon: ['OREAS-230', 'OREAS-231'],
};

export const AnalysisSetup: React.FC<AnalysisSetupProps> = ({ initialCategory, onComplete, onNavigateToEducation }) => {
    const [selectedCategory, setSelectedCategory] = useState<AnalysisCategory | null>(initialCategory || null);
    
    // If initialCategory changes (e.g., from demo data), update state
    useEffect(() => {
        if (initialCategory) {
            setSelectedCategory(initialCategory);
        }
    }, [initialCategory]);
    const [showAdvanced, setShowAdvanced] = useState(false);
    const [availableCRMs, setAvailableCRMs] = useState<CRMValue[]>([]);

    // Category-specific settings
    const [duplicateType, setDuplicateType] = useState<'coarse' | 'pulp' | 'both'>('pulp');
    const [gravimetricFinish, setGravimetricFinish] = useState(false);
    const [selectedElements, setSelectedElements] = useState<string[]>(['Cu', 'Pb', 'Zn', 'Fe']);
    
    // CRM selection
    const [selectedCRMs, setSelectedCRMs] = useState<string[]>([]);
    
    // Advanced settings
    const [toleranceType, setToleranceType] = useState<'percentage' | 'absolute' | 'sd'>('percentage');
    const [toleranceValue, setToleranceValue] = useState(10);
    const [failureThreshold, setFailureThreshold] = useState(3);
    const [detectionLimit, setDetectionLimit] = useState(0.01);
    const [detectionLimitUnit, setDetectionLimitUnit] = useState<'ppm' | 'ppb' | 'pct'>('ppm');
    const [contaminationMultiplier, setContaminationMultiplier] = useState(3);
    const [precisionTarget, setPrecisionTarget] = useState(20);
    const [precisionMethod, setPrecisionMethod] = useState<'rpd' | 'hard'>('hard');

    // Load CRMs when category changes
    useEffect(() => {
        if (!selectedCategory) {
            setAvailableCRMs([]);
            setSelectedCRMs([]);
            return;
        }

        // Map category to CRM database category
        let dbCategory: 'gold' | 'pxrf' | 'multi-element' = 
            selectedCategory === 'photon' ? 'gold' : 
            selectedCategory === 'pxrf' ? 'pxrf' : 'gold';

        const crms = getCRMsByCategory(dbCategory);
        
        // For photon, filter to PhotonAssay-specific CRMs
        if (selectedCategory === 'photon') {
            const photonCRMs = crms.filter(crm =>
                Object.values(crm.elements).some(el => el.method === 'PhotonAssay')
            );
            setAvailableCRMs(photonCRMs.length > 0 ? photonCRMs : crms.slice(0, 6));
        } else {
            setAvailableCRMs(crms.slice(0, 8)); // Show first 8 for performance
        }

        // Pre-select default CRMs
        setSelectedCRMs(DEFAULT_CRMS[selectedCategory] || []);

        // Apply category defaults with proper type narrowing
        if (selectedCategory === 'gold') {
            const goldDefaults = CATEGORY_DEFAULTS.gold;
            setDetectionLimit(goldDefaults.detectionLimit);
            setDetectionLimitUnit(goldDefaults.detectionLimitUnit);
            setToleranceValue(goldDefaults.toleranceValue);
            setPrecisionTarget(goldDefaults.precisionTarget);
            setDuplicateType(goldDefaults.duplicateType);
            setGravimetricFinish(goldDefaults.gravimetricFinish);
        } else if (selectedCategory === 'pxrf') {
            const pxrfDefaults = CATEGORY_DEFAULTS.pxrf;
            setDetectionLimit(pxrfDefaults.detectionLimit);
            setDetectionLimitUnit(pxrfDefaults.detectionLimitUnit);
            setToleranceValue(pxrfDefaults.toleranceValue);
            setPrecisionTarget(pxrfDefaults.precisionTarget);
            setSelectedElements(pxrfDefaults.elements);
        } else if (selectedCategory === 'photon') {
            const photonDefaults = CATEGORY_DEFAULTS.photon;
            setDetectionLimit(photonDefaults.detectionLimit);
            setDetectionLimitUnit(photonDefaults.detectionLimitUnit);
            setToleranceValue(photonDefaults.toleranceValue);
            setPrecisionTarget(photonDefaults.precisionTarget);
            setSelectedElements(photonDefaults.elements);
        }
    }, [selectedCategory]);

    const handleCategorySelect = (category: AnalysisCategory) => {
        setSelectedCategory(category);
        setShowAdvanced(false);
    };

    const toggleCRM = (crmId: string) => {
        setSelectedCRMs(prev => 
            prev.includes(crmId) 
                ? prev.filter(id => id !== crmId)
                : [...prev, crmId]
        );
    };

    const handleRunAnalysis = () => {
        if (!selectedCategory || selectedCRMs.length === 0) return;

        const methodologyConfig: MethodologyConfig = {
            category: selectedCategory === 'photon' ? 'gold' : selectedCategory,
            assayMethod: selectedCategory === 'gold' ? 'fire_assay' : undefined,
            duplicateType: selectedCategory === 'gold' ? duplicateType : undefined,
            gravimetricFinish: selectedCategory === 'gold' ? gravimetricFinish : undefined,
            elements: selectedCategory !== 'gold' ? selectedElements : undefined,
            insertionRate: {
                standards: 10,
                blanks: 20,
                duplicates: 20,
            },
        };

        const qaqcConfig: QAQCConfig = {
            standards: {
                selectedCRMs,
                toleranceType,
                toleranceValue,
                failureThreshold,
            },
            blanks: {
                detectionLimit,
                detectionLimitUnit,
                contaminationMultiplier,
            },
            duplicates: {
                precisionTarget,
                precisionMethod,
                failureThreshold,
            },
        };

        onComplete({
            category: selectedCategory,
            methodologyConfig,
            qaqcConfig,
        });
    };

    const isValid = selectedCategory && selectedCRMs.length > 0;

    return (
        <div className="max-w-4xl mx-auto mt-8 space-y-8">
            {/* Header */}
            <div className="text-center">
                <h2 className="text-3xl font-bold text-slate-50 mb-2">
                    Analysis Setup
                </h2>
                <p className="text-slate-400">
                    Configure your QAQC analysis in one step
                </p>
            </div>

            {/* Category Selection */}
            <div>
                <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
                    1. Select Analysis Type
                    <HelpTooltip 
                        topicId="fire-assay" 
                        customSummary="Choose the assay method that matches your data. Different methods require different QAQC approaches."
                        onLearnMore={onNavigateToEducation}
                    />
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Gold */}
                    <button
                        onClick={() => handleCategorySelect('gold')}
                        data-tour="category-gold"
                        className={`relative group p-6 rounded-2xl border-2 transition-all text-left ${
                            selectedCategory === 'gold'
                                ? 'border-primary bg-primary/10 ring-4 ring-primary/20'
                                : 'border-secondary-dark hover:border-primary/50 hover:bg-surface-light'
                        }`}
                    >
                        {selectedCategory === 'gold' && (
                            <div className="absolute top-3 right-3 w-6 h-6 bg-primary text-slate-900 rounded-full flex items-center justify-center">
                                <CheckCircle2 className="w-4 h-4" />
                            </div>
                        )}
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-3 transition-colors ${
                            selectedCategory === 'gold' ? 'bg-primary text-slate-900' : 'bg-primary/20 text-primary'
                        }`}>
                            <Layers className="w-6 h-6" />
                        </div>
                        <h4 className="font-bold text-slate-50 mb-1">Gold (Fire Assay)</h4>
                        <p className="text-sm text-slate-400">
                            Standard fire assay with nugget effect checks
                        </p>
                    </button>

                    {/* pXRF */}
                    <button
                        onClick={() => handleCategorySelect('pxrf')}
                        className={`relative group p-6 rounded-2xl border-2 transition-all text-left ${
                            selectedCategory === 'pxrf'
                                ? 'border-accent bg-accent/10 ring-4 ring-accent/20'
                                : 'border-secondary-dark hover:border-accent/50 hover:bg-surface-light'
                        }`}
                    >
                        {selectedCategory === 'pxrf' && (
                            <div className="absolute top-3 right-3 w-6 h-6 bg-accent text-slate-900 rounded-full flex items-center justify-center">
                                <CheckCircle2 className="w-4 h-4" />
                            </div>
                        )}
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-3 transition-colors ${
                            selectedCategory === 'pxrf' ? 'bg-accent text-slate-900' : 'bg-accent/20 text-accent'
                        }`}>
                            <Beaker className="w-6 h-6" />
                        </div>
                        <h4 className="font-bold text-slate-50 mb-1">pXRF / Multi-element</h4>
                        <p className="text-sm text-slate-400">
                            Portable XRF or ICP-MS multi-element analysis
                        </p>
                    </button>

                    {/* PhotonAssay */}
                    <button
                        onClick={() => handleCategorySelect('photon')}
                        className={`relative group p-6 rounded-2xl border-2 transition-all text-left ${
                            selectedCategory === 'photon'
                                ? 'border-purple-500 bg-purple-500/10 ring-4 ring-purple-500/20'
                                : 'border-secondary-dark hover:border-purple-500/50 hover:bg-surface-light'
                        }`}
                    >
                        {selectedCategory === 'photon' && (
                            <div className="absolute top-3 right-3 w-6 h-6 bg-purple-500 text-slate-900 rounded-full flex items-center justify-center">
                                <CheckCircle2 className="w-4 h-4" />
                            </div>
                        )}
                        <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-3 transition-colors ${
                            selectedCategory === 'photon' ? 'bg-purple-500 text-slate-900' : 'bg-purple-500/20 text-purple-400'
                        }`}>
                            <Zap className="w-6 h-6" />
                        </div>
                        <h4 className="font-bold text-slate-50 mb-1">Chrysos PhotonAssay</h4>
                        <p className="text-sm text-slate-400">
                            High-energy X-ray for Au, Ag, Cu
                        </p>
                    </button>
                </div>
            </div>

            {/* Quick Settings (shown when category selected) */}
            {selectedCategory && (
                <div className="animate-fade-in">
                    <h3 className="text-lg font-semibold text-slate-200 mb-4">
                        2. Quick Settings
                    </h3>
                    <div className="bg-surface rounded-xl border border-secondary-dark p-6">
                        {selectedCategory === 'gold' && (
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div>
                                    <label className="block text-sm font-medium text-slate-300 mb-2">
                                        Duplicate Type
                                    </label>
                                    <select
                                        value={duplicateType}
                                        onChange={(e) => setDuplicateType(e.target.value as 'coarse' | 'pulp' | 'both')}
                                        className="w-full px-4 py-2.5 bg-surface-light border border-secondary-light rounded-lg text-slate-200 focus:ring-2 focus:ring-primary/50 outline-none"
                                    >
                                        <option value="pulp">Pulp Duplicates</option>
                                        <option value="coarse">Coarse (Field) Duplicates</option>
                                        <option value="both">Both Coarse & Pulp</option>
                                    </select>
                                </div>
                                <div>
                                    <label className="block text-sm font-medium text-slate-300 mb-2">
                                        Gravimetric Finish (&gt;10 g/t)
                                    </label>
                                    <button
                                        onClick={() => setGravimetricFinish(!gravimetricFinish)}
                                        className={`w-full px-4 py-2.5 rounded-lg border transition-all flex items-center justify-between ${
                                            gravimetricFinish 
                                                ? 'bg-primary/20 border-primary text-primary' 
                                                : 'bg-surface-light border-secondary-light text-slate-400'
                                        }`}
                                    >
                                        <span>{gravimetricFinish ? 'Enabled' : 'Disabled'}</span>
                                        <div className={`w-10 h-5 rounded-full transition-colors relative ${
                                            gravimetricFinish ? 'bg-primary' : 'bg-secondary'
                                        }`}>
                                            <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-transform ${
                                                gravimetricFinish ? 'left-5' : 'left-0.5'
                                            }`} />
                                        </div>
                                    </button>
                                </div>
                            </div>
                        )}

                        {(selectedCategory === 'pxrf' || selectedCategory === 'photon') && (
                            <div>
                                <label className="block text-sm font-medium text-slate-300 mb-3">
                                    Target Elements
                                </label>
                                <div className="flex flex-wrap gap-2">
                                    {(selectedCategory === 'pxrf' 
                                        ? ['Cu', 'Pb', 'Zn', 'Fe', 'Mn', 'As', 'Ag', 'S']
                                        : ['Au', 'Ag', 'Cu', 'S']
                                    ).map(element => (
                                        <button
                                            key={element}
                                            onClick={() => setSelectedElements(prev =>
                                                prev.includes(element)
                                                    ? prev.filter(e => e !== element)
                                                    : [...prev, element]
                                            )}
                                            className={`px-4 py-2 rounded-lg border transition-all font-medium ${
                                                selectedElements.includes(element)
                                                    ? 'bg-primary/20 border-primary text-primary'
                                                    : 'bg-surface-light border-secondary-light text-slate-400 hover:border-primary/50'
                                            }`}
                                        >
                                            {element}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* CRM Selection */}
            {selectedCategory && (
                <div className="animate-fade-in">
                    <h3 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
                        3. Select Reference Materials (CRMs)
                        <HelpTooltip 
                            topicId="standards-crms" 
                            onLearnMore={onNavigateToEducation}
                        />
                    </h3>
                    <div className="bg-surface rounded-xl border border-secondary-dark p-6">
                        <div className="flex items-center gap-2 mb-4 p-3 bg-accent/10 border border-accent/30 rounded-lg">
                            <Info className="w-4 h-4 text-accent flex-shrink-0" />
                            <p className="text-sm text-accent">
                                Common standards pre-selected. Click to add or remove.
                            </p>
                        </div>
                        <div className="space-y-2 max-h-64 overflow-y-auto pr-2">
                            {availableCRMs.map(crm => {
                                const isSelected = selectedCRMs.includes(crm.id);
                                const gradeString = Object.entries(crm.elements)
                                    .slice(0, 2)
                                    .map(([el, data]) => `${data.certified} ${data.unit} ${el}`)
                                    .join(', ');

                                return (
                                    <button
                                        key={crm.id}
                                        onClick={() => toggleCRM(crm.id)}
                                        className={`w-full text-left p-4 rounded-xl border-2 transition-all flex items-center justify-between group ${
                                            isSelected
                                                ? 'border-primary bg-primary/10'
                                                : 'border-secondary-light bg-surface-light hover:border-primary/50'
                                        }`}
                                    >
                                        <div>
                                            <span className={`font-semibold ${isSelected ? 'text-primary' : 'text-slate-200'}`}>
                                                {crm.name}
                                            </span>
                                            <span className="text-sm text-slate-400 ml-3">
                                                {gradeString}
                                            </span>
                                        </div>
                                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors ${
                                            isSelected
                                                ? 'border-primary bg-primary text-slate-900'
                                                : 'border-secondary-light'
                                        }`}>
                                            {isSelected && <CheckCircle2 className="w-3 h-3" />}
                                        </div>
                                    </button>
                                );
                            })}
                        </div>
                        {selectedCRMs.length === 0 && (
                            <p className="text-sm text-status-warning mt-3">
                                Please select at least one CRM
                            </p>
                        )}
                    </div>
                </div>
            )}

            {/* Advanced Settings (Collapsed) */}
            {selectedCategory && (
                <div className="animate-fade-in">
                    <button
                        onClick={() => setShowAdvanced(!showAdvanced)}
                        className="flex items-center gap-2 text-slate-400 hover:text-slate-200 transition-colors"
                    >
                        <Settings className="w-4 h-4" />
                        <span className="text-sm font-medium">Advanced Settings</span>
                        {showAdvanced ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>

                    {showAdvanced && (
                        <div className="mt-4 bg-surface rounded-xl border border-secondary-dark p-6 animate-fade-in">
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {/* Standards Settings */}
                                <div>
                                    <h4 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide flex items-center gap-2">
                                        Standards
                                        <HelpTooltip 
                                            topicId="standards-crms" 
                                            size="sm"
                                            onLearnMore={onNavigateToEducation}
                                        />
                                    </h4>
                                    <div className="space-y-3">
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Tolerance Type</label>
                                            <select
                                                value={toleranceType}
                                                onChange={(e) => setToleranceType(e.target.value as 'percentage' | 'absolute' | 'sd')}
                                                className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                            >
                                                <option value="percentage">Percentage (±%)</option>
                                                <option value="absolute">Absolute Value</option>
                                                <option value="sd">Standard Deviations (±SD)</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Tolerance Value</label>
                                            <input
                                                type="number"
                                                value={toleranceValue}
                                                onChange={(e) => setToleranceValue(parseFloat(e.target.value))}
                                                className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                                step="1"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Blanks Settings */}
                                <div>
                                    <h4 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide flex items-center gap-2">
                                        Blanks
                                        <HelpTooltip 
                                            topicId="blanks" 
                                            size="sm"
                                            onLearnMore={onNavigateToEducation}
                                        />
                                    </h4>
                                    <div className="space-y-3">
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Detection Limit</label>
                                            <div className="flex gap-2">
                                                <input
                                                    type="number"
                                                    value={detectionLimit}
                                                    onChange={(e) => setDetectionLimit(parseFloat(e.target.value))}
                                                    className="flex-1 px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                                    step="0.001"
                                                />
                                                <select
                                                    value={detectionLimitUnit}
                                                    onChange={(e) => setDetectionLimitUnit(e.target.value as 'ppm' | 'ppb' | 'pct')}
                                                    className="px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                                >
                                                    <option value="ppm">ppm</option>
                                                    <option value="ppb">ppb</option>
                                                    <option value="pct">%</option>
                                                </select>
                                            </div>
                                        </div>
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Contamination Multiplier</label>
                                            <input
                                                type="number"
                                                value={contaminationMultiplier}
                                                onChange={(e) => setContaminationMultiplier(parseFloat(e.target.value))}
                                                className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                                step="0.5"
                                                min="1"
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Duplicates Settings */}
                                <div>
                                    <h4 className="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide flex items-center gap-2">
                                        Duplicates
                                        <HelpTooltip 
                                            topicId="duplicates" 
                                            size="sm"
                                            onLearnMore={onNavigateToEducation}
                                        />
                                    </h4>
                                    <div className="space-y-3">
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Precision Method</label>
                                            <select
                                                value={precisionMethod}
                                                onChange={(e) => setPrecisionMethod(e.target.value as 'rpd' | 'hard')}
                                                className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                            >
                                                <option value="hard">HARD (%)</option>
                                                <option value="rpd">RPD (%)</option>
                                            </select>
                                        </div>
                                        <div>
                                            <label className="block text-xs text-slate-400 mb-1">Target Precision (%)</label>
                                            <input
                                                type="number"
                                                value={precisionTarget}
                                                onChange={(e) => setPrecisionTarget(parseFloat(e.target.value))}
                                                className="w-full px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                                step="1"
                                                min="1"
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="mt-4 pt-4 border-t border-secondary-dark">
                                <div>
                                    <label className="block text-xs text-slate-400 mb-1">Consecutive Failures to Flag</label>
                                    <input
                                        type="number"
                                        value={failureThreshold}
                                        onChange={(e) => setFailureThreshold(parseInt(e.target.value))}
                                        className="w-32 px-3 py-2 bg-surface-light border border-secondary-light rounded-lg text-slate-200 text-sm"
                                        min="1"
                                        max="10"
                                    />
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Run Analysis Button */}
            {selectedCategory && (
                <div className="pt-4 animate-fade-in">
                    <button
                        onClick={handleRunAnalysis}
                        disabled={!isValid}
                        className="w-full flex items-center justify-center gap-3 px-8 py-4 bg-gradient-to-r from-primary to-primary-dark text-slate-900 rounded-xl font-bold text-lg hover:shadow-lg hover:shadow-primary/30 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                    >
                        <Play className="w-5 h-5" />
                        Run Analysis
                    </button>
                    {!isValid && (
                        <p className="text-center text-sm text-slate-500 mt-2">
                            Select at least one CRM to continue
                        </p>
                    )}
                </div>
            )}

            {/* CSS for fade-in animation */}
            <style>{`
                @keyframes fade-in {
                    from { opacity: 0; transform: translateY(8px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in {
                    animation: fade-in 0.3s ease-out;
                }
            `}</style>
        </div>
    );
};
