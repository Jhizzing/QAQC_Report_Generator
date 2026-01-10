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
                <h2 className="text-3xl font-bold text-slate-50 mb-4">
                    Select Analysis Category
                </h2>
                <p className="text-slate-400 max-w-2xl mx-auto">
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
                            : 'border-secondary-dark hover:border-primary/50 hover:bg-surface-light'
                        }
          `}
                >
                    {selected === 'gold' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-primary text-slate-50 rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'gold' ? 'bg-primary text-slate-50' : 'bg-primary/20 text-primary'}
          `}>
                        <Layers className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-50 mb-2">Gold (Au) Analysis</h3>
                    <p className="text-slate-400 text-sm leading-relaxed">
                        Fire Assay or Leachwell gold analysis with nugget effect and coarse duplicate checks.
                    </p>
                </div>

                {/* pXRF / Multi-element Category */}
                <div
                    onClick={() => handleSelect('pxrf')}
                    className={`
            relative group cursor-pointer rounded-2xl border-2 p-6 transition-all
            ${selected === 'pxrf'
                            ? 'border-accent bg-accent/5 ring-4 ring-accent/10'
                            : 'border-secondary-dark hover:border-accent/50 hover:bg-surface-light'
                        }
          `}
                >
                    {selected === 'pxrf' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-accent text-slate-50 rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'pxrf' ? 'bg-accent text-slate-50' : 'bg-accent/20 text-accent'}
          `}>
                        <Beaker className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-50 mb-2">pXRF / Multi-element</h3>
                    <p className="text-slate-400 text-sm leading-relaxed">
                        Portable XRF or ICP-MS multi-element suites with elemental ratios and interference checks.
                    </p>
                </div>

                {/* Chrysos PhotonAssay Category */}
                <div
                    onClick={() => handleSelect('photon')}
                    className={`
            relative group cursor-pointer rounded-2xl border-2 p-6 transition-all
            ${selected === 'photon'
                            ? 'border-purple-500 bg-purple-500/10 ring-4 ring-purple-500/10'
                            : 'border-secondary-dark hover:border-purple-500/50 hover:bg-surface-light'
                        }
          `}
                >
                    {selected === 'photon' && (
                        <div className="absolute top-4 right-4 w-8 h-8 bg-purple-500 text-slate-50 rounded-full flex items-center justify-center">
                            <Check className="w-5 h-5" />
                        </div>
                    )}
                    <div className={`
            w-14 h-14 rounded-xl flex items-center justify-center mb-4 transition-colors
            ${selected === 'photon' ? 'bg-gradient-to-br from-purple-500 to-indigo-600 text-slate-50' : 'bg-purple-500/20 text-purple-400'}
          `}>
                        <Zap className="w-7 h-7" />
                    </div>
                    <h3 className="text-lg font-bold text-slate-50 mb-2">Chrysos PhotonAssay</h3>
                    <p className="text-slate-400 text-sm leading-relaxed">
                        High-energy X-ray analysis for Au, Ag, Cu. Non-destructive, large samples (500g), rapid results.
                    </p>
                </div>
            </div>

            <div className="flex justify-center">
                <button
                    disabled={!selected}
                    onClick={handleConfirm}
                    className="flex items-center gap-2 px-8 py-4 bg-primary text-surface-dark rounded-xl font-bold text-lg hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-xl shadow-primary/20"
                >
                    Continue to Methodology
                    <ArrowRight className="w-5 h-5" />
                </button>
            </div>
        </div>
    );
};
