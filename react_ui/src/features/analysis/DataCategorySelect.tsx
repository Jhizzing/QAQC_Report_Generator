import React from 'react';
import { Beaker, Layers, ArrowRight, Check, Zap } from 'lucide-react';

interface DataCategorySelectProps {
    onComplete: (category: 'gold' | 'pxrf' | 'multi' | 'photon') => void;
}

export const DataCategorySelect: React.FC<DataCategorySelectProps> = ({ onComplete }) => {
    const [selected, setSelected] = React.useState<'gold' | 'pxrf' | 'multi' | 'photon' | null>(null);

    const handleSelect = (category: 'gold' | 'pxrf' | 'multi' | 'photon') => {
        setSelected(category);
    };

    const handleConfirm = () => {
        if (selected) {
            onComplete(selected);
        }
    };

    return (
        <div className="max-w-6xl mx-auto mt-12">
            <div className="text-center mb-12">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                    Select Analysis Category
                </h2>
                <p className="text-gray-300 max-w-2xl mx-auto">
                    Choose the primary focus of your QAQC analysis. This will tailor the subsequent methodology questions and report templates.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                {/* Gold Category */}
                <div
                    onClick={() => handleSelect('gold')}
                    data-tour="category-gold"
                    className={`
            relative group cursor-pointer rounded-2xl border-2 p-6 transition-all
            ${selected === 'gold'
                            ? 'border-primary bg-primary/5 ring-4 ring-primary/10'
                            : 'border-gray-200 dark:border-gray-800 hover:border-primary/50 hover:bg-gray-50 dark:hover:bg-gray-800/50'
                        }
          `}
                >
                    {selected === 'gold' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-primary text-white rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'gold' ? 'bg-primary text-white' : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'}
          `}>
                        <Layers className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Gold (Au) Analysis</h3>
                    <p className="text-gray-300 text-sm leading-relaxed">
                        Fire Assay or Leachwell gold analysis with nugget effect and coarse duplicate checks.
                    </p>
                </div>

                {/* pXRF / Multi-element Category */}
                <div
                    onClick={() => handleSelect('pxrf')}
                    className={`
            relative group cursor-pointer rounded-2xl border-2 p-6 transition-all
            ${selected === 'pxrf'
                            ? 'border-secondary bg-secondary/5 ring-4 ring-secondary/10'
                            : 'border-gray-200 dark:border-gray-800 hover:border-secondary/50 hover:bg-gray-50 dark:hover:bg-gray-800/50'
                        }
          `}
                >
                    {selected === 'pxrf' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-secondary text-white rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'pxrf' ? 'bg-secondary text-white' : 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'}
          `}>
                        <Beaker className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">pXRF / Multi-element</h3>
                    <p className="text-gray-300 text-sm leading-relaxed">
                        Portable XRF or ICP-MS multi-element suites with elemental ratios and interference checks.
                    </p>
                </div>

                {/* Chrysos PhotonAssay Category */}
                <div
                    onClick={() => handleSelect('photon')}
                    className={`
            relative group cursor-pointer rounded-2xl border-2 p-6 transition-all
            ${selected === 'photon'
                            ? 'border-purple-600 bg-purple-50 dark:bg-purple-900/10 ring-4 ring-purple-600/10'
                            : 'border-gray-200 dark:border-gray-800 hover:border-purple-500/50 hover:bg-gray-50 dark:hover:bg-gray-800/50'
                        }
          `}
                >
                    {selected === 'photon' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'photon' ? 'bg-gradient-to-br from-purple-500 to-indigo-600 text-white' : 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-400'}
          `}>
                        <Zap className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">Chrysos PhotonAssay</h3>
                    <p className="text-gray-300 text-sm leading-relaxed">
                        High-energy X-ray analysis for Au, Ag, Cu. Non-destructive, large samples (500g), rapid results.
                    </p>
                </div>
            </div>

            <div className="flex justify-center">
                <button
                    disabled={!selected}
                    onClick={handleConfirm}
                    className="flex items-center gap-2 px-8 py-4 bg-gray-900 dark:bg-white text-white dark:text-gray-900 rounded-xl font-bold text-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-xl"
                >
                    Continue to Methodology
                    <ArrowRight className="w-5 h-5" />
                </button>
            </div>
        </div>
    );
};
