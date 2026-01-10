import React, { useState } from 'react';
import { ArrowRight, ArrowLeft, CheckCircle, HelpCircle } from 'lucide-react';

interface MethodologyWizardProps {
    category: 'gold' | 'pxrf' | 'multi' | 'photon';
    onComplete: (config: MethodologyConfig) => void;
}

export interface MethodologyConfig {
    category: 'gold' | 'pxrf' | 'multi';
    // Gold-specific
    assayMethod?: 'fire_assay' | 'leachwell' | 'screen_fire_assay';
    duplicateType?: 'coarse' | 'pulp' | 'both';
    gravimetricFinish?: boolean;
    // pXRF-specific
    elements?: string[];
    matrixCorrection?: boolean;
    spectralInterference?: boolean;
    // Common
    insertionRate?: {
        standards: number;
        blanks: number;
        duplicates: number;
    };
}

interface Question {
    id: string;
    label: string;
    type: 'select' | 'multiselect' | 'toggle' | 'number';
    options?: { value: string; label: string; description?: string }[];
    tooltip?: string;
    default?: any;
}

const goldQuestions: Question[] = [
    {
        id: 'assayMethod',
        label: 'Primary Assay Method',
        type: 'select',
        tooltip: 'Select the primary analytical method for gold determination',
        options: [
            { value: 'fire_assay', label: 'Fire Assay (FA)', description: 'Standard 30-50g charge with AAS/ICP finish' },
            { value: 'leachwell', label: 'LeachWELL™', description: 'Cyanide leach with AAS finish' },
            { value: 'screen_fire_assay', label: 'Screen Fire Assay', description: 'Screen metallic & fire assay undersize' }
        ]
    },
    {
        id: 'duplicateType',
        label: 'Duplicate Sample Type',
        type: 'select',
        tooltip: 'Specify which stage duplicates are taken',
        options: [
            { value: 'coarse', label: 'Coarse (Field) Duplicates', description: 'Quarter core or duplicate samples' },
            { value: 'pulp', label: 'Pulp Duplicates', description: 'Lab pulp duplicates only' },
            { value: 'both', label: 'Both Coarse & Pulp', description: 'Full precision hierarchy' }
        ]
    },
    {
        id: 'gravimetricFinish',
        label: 'Use Gravimetric Finish for High-Grade?',
        type: 'toggle',
        tooltip: 'Enable gravimetric finish for samples >10 g/t Au',
        default: false
    }
];

const pxrfQuestions: Question[] = [
    {
        id: 'elements',
        label: 'Target Elements',
        type: 'multiselect',
        tooltip: 'Select elements to include in QAQC analysis',
        options: [
            { value: 'Cu', label: 'Cu (Copper)' },
            { value: 'Pb', label: 'Pb (Lead)' },
            { value: 'Zn', label: 'Zn (Zinc)' },
            { value: 'Ag', label: 'Ag (Silver)' },
            { value: 'As', label: 'As (Arsenic)' },
            { value: 'Fe', label: 'Fe (Iron)' },
            { value: 'Mn', label: 'Mn (Manganese)' },
            { value: 'S', label: 'S (Sulfur)' }
        ]
    },
    {
        id: 'matrixCorrection',
        label: 'Apply Matrix Correction?',
        type: 'toggle',
        tooltip: 'Enable matrix-matched standards for pXRF calibration checks',
        default: true
    },
    {
        id: 'spectralInterference',
        label: 'Check Spectral Interference?',
        type: 'toggle',
        tooltip: 'Flag potential spectral overlaps (e.g., Pb-As, Zn-Cu)',
        default: true
    }
];

const photonQuestions: Question[] = [
    {
        id: 'elements',
        label: 'Target Elements',
        type: 'multiselect',
        tooltip: 'Select elements to include in QAQC analysis',
        options: [
            { value: 'Au', label: 'Au (Gold)' },
            { value: 'Ag', label: 'Ag (Silver)' },
            { value: 'Cu', label: 'Cu (Copper)' },
            { value: 'S', label: 'S (Sulfur)' },
            { value: 'Moisture', label: 'Moisture' }
        ]
    },
    {
        id: 'includeUncertainty',
        label: 'Include Measurement Uncertainty?',
        type: 'toggle',
        tooltip: 'Use reported instrument error for precision calculations',
        default: true
    },
    {
        id: 'jarSize',
        label: 'Sample Jar Size',
        type: 'select',
        tooltip: 'Standard sample mass for analysis',
        options: [
            { value: '500', label: '500g (Standard)', description: 'Standard jar size' },
            { value: '350', label: '350g', description: 'Reduced volume' },
            { value: '650', label: '650g', description: 'Max volume' }
        ]
    }
];

export const MethodologyWizard: React.FC<MethodologyWizardProps> = ({ category, onComplete }) => {
    const questions = category === 'gold' ? goldQuestions :
        category === 'photon' ? photonQuestions :
            pxrfQuestions;
    const [currentStep, setCurrentStep] = useState(0);
    const [answers, setAnswers] = useState<any>({});

    const handleAnswer = (questionId: string, value: any) => {
        setAnswers({ ...answers, [questionId]: value });
    };

    const handleNext = () => {
        if (currentStep < questions.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            // Build final config
            const config: MethodologyConfig = {
                category,
                ...answers,
                insertionRate: {
                    standards: 10, // Default 1:10
                    blanks: 20,    // Default 1:20
                    duplicates: 20  // Default 1:20
                }
            };
            onComplete(config);
        }
    };

    const handleBack = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const currentQuestion = questions[currentStep];
    const progress = ((currentStep + 1) / questions.length) * 100;

    return (
        <div className="max-w-3xl mx-auto mt-12">
            {/* Progress Bar */}
            <div className="mb-12">
                <div className="flex items-center justify-between text-sm text-slate-400 mb-2">
                    <span>Question {currentStep + 1} of {questions.length}</span>
                    <span>{Math.round(progress)}% Complete</span>
                </div>
                <div className="w-full bg-secondary-dark rounded-full h-2">
                    <div
                        className="bg-primary h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>

            {/* Question Card */}
            <div className="bg-surface rounded-2xl shadow-xl border border-secondary-dark p-8">
                <div className="flex items-start gap-3 mb-6">
                    <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                        <span className="text-xl font-bold text-primary">{currentStep + 1}</span>
                    </div>
                    <div className="flex-1">
                        <h3 className="text-2xl font-bold text-slate-50 mb-2">
                            {currentQuestion.label}
                        </h3>
                        {currentQuestion.tooltip && (
                            <div className="flex items-start gap-2 text-sm text-slate-400">
                                <HelpCircle className="w-4 h-4 mt-0.5 flex-shrink-0" />
                                <p>{currentQuestion.tooltip}</p>
                            </div>
                        )}
                    </div>
                </div>

                <div className="mt-8">
                    {/* Select Input */}
                    {currentQuestion.type === 'select' && (
                        <div className="space-y-3">
                            {currentQuestion.options?.map((option) => (
                                <button
                                    key={option.value}
                                    onClick={() => handleAnswer(currentQuestion.id, option.value)}
                                    className={`
                    w-full text-left p-4 rounded-xl border-2 transition-all
                    ${answers[currentQuestion.id] === option.value
                                            ? 'border-primary bg-primary/10 shadow-lg shadow-primary/10'
                                            : 'border-secondary-light bg-surface-light hover:border-primary/50 hover:bg-surface'
                                        }
                  `}
                                >
                                    <div className="flex items-start justify-between">
                                        <div>
                                            <div className="font-semibold text-slate-50">{option.label}</div>
                                            {option.description && (
                                                <div className="text-sm text-slate-400 mt-1">{option.description}</div>
                                            )}
                                        </div>
                                        {answers[currentQuestion.id] === option.value && (
                                            <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
                                        )}
                                    </div>
                                </button>
                            ))}
                        </div>
                    )}

                    {/* Multi-Select Input */}
                    {currentQuestion.type === 'multiselect' && (
                        <div className="space-y-2">
                            {currentQuestion.options?.map((option) => {
                                const selected = answers[currentQuestion.id]?.includes(option.value) || false;
                                return (
                                    <button
                                        key={option.value}
                                        onClick={() => {
                                            const current = answers[currentQuestion.id] || [];
                                            const newValue = selected
                                                ? current.filter((v: string) => v !== option.value)
                                                : [...current, option.value];
                                            handleAnswer(currentQuestion.id, newValue);
                                        }}
                                        className={`
                      w-full text-left p-3 rounded-lg border transition-all flex items-center gap-3
                      ${selected
                                                ? 'border-primary bg-primary/5'
                                                : 'border-secondary-light hover:border-primary/50'
                                            }
                    `}
                                    >
                                        <div className={`
                      w-5 h-5 rounded border-2 flex items-center justify-center
                      ${selected ? 'bg-primary border-primary' : 'border-secondary-light'}
                    `}>
                                            {selected && <CheckCircle className="w-4 h-4 text-slate-50" />}
                                        </div>
                                        <span className="font-medium text-slate-50">{option.label}</span>
                                    </button>
                                );
                            })}
                        </div>
                    )}

                    {/* Toggle Input */}
                    {currentQuestion.type === 'toggle' && (
                        <div className="flex items-center justify-between p-6 bg-surface-light rounded-xl">
                            <span className="text-slate-300">Enable this feature?</span>
                            <button
                                onClick={() => handleAnswer(currentQuestion.id, !answers[currentQuestion.id])}
                                className={`
                  relative w-14 h-8 rounded-full transition-colors
                  ${answers[currentQuestion.id] ? 'bg-primary' : 'bg-secondary'}
                `}
                            >
                                <div className={`
                  absolute top-1 left-1 w-6 h-6 bg-slate-50 rounded-full transition-transform
                  ${answers[currentQuestion.id] ? 'translate-x-6' : 'translate-x-0'}
                `} />
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Navigation */}
            <div className="flex items-center justify-between mt-8">
                <button
                    onClick={handleBack}
                    disabled={currentStep === 0}
                    className="flex items-center gap-2 px-6 py-3 text-slate-400 hover:text-slate-50 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back
                </button>
                <button
                    onClick={handleNext}
                    disabled={!answers[currentQuestion.id] && currentQuestion.type !== 'toggle'}
                    className="flex items-center gap-2 px-8 py-3 bg-primary text-slate-50 rounded-xl font-bold hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg"
                >
                    {currentStep === questions.length - 1 ? 'Complete Setup' : 'Next Question'}
                    <ArrowRight className="w-4 h-4" />
                </button>
            </div>
        </div>
    );
};
