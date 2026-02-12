import React, { useState } from 'react';
import { X, Plus, Trash2, Save, AlertCircle } from 'lucide-react';
import { useCRMStore } from '../../stores/crmStore';
import type { CRMValue } from '../../data/crmDatabase';

interface CustomCRMFormProps {
    onClose: () => void;
}

export const CustomCRMForm: React.FC<CustomCRMFormProps> = ({ onClose }) => {
    const { addCustomCRM } = useCRMStore();

    // Form State
    const [name, setName] = useState('');
    const [supplier, setSupplier] = useState('');
    const [matrix, setMatrix] = useState('');
    const [category, setCategory] = useState<'gold' | 'multi-element' | 'pxrf'>('gold');
    const [notes, setNotes] = useState('');

    // Elements State
    const [elements, setElements] = useState<{
        symbol: string;
        value: string;
        uncertainty: string;
        unit: string;
    }[]>([
        { symbol: 'Au', value: '', uncertainty: '', unit: 'ppm' }
    ]);

    const [error, setError] = useState<string | null>(null);

    const handleAddElement = () => {
        setElements([...elements, { symbol: '', value: '', uncertainty: '', unit: 'ppm' }]);
    };

    const handleRemoveElement = (index: number) => {
        if (elements.length > 1) {
            setElements(elements.filter((_, i) => i !== index));
        }
    };

    const handleElementChange = (index: number, field: keyof typeof elements[0], value: string) => {
        const newElements = [...elements];
        newElements[index] = { ...newElements[index], [field]: value };
        setElements(newElements);
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setError(null);

        // Validation
        if (!name || !supplier || !matrix) {
            setError('Please fill in all required fields (Name, Supplier, Matrix).');
            return;
        }

        const cleanElements: CRMValue['elements'] = {};

        for (const el of elements) {
            if (!el.symbol || !el.value) continue;

            const val = parseFloat(el.value);
            const unc = el.uncertainty ? parseFloat(el.uncertainty) : undefined;

            if (isNaN(val)) {
                setError(`Invalid value for element ${el.symbol}`);
                return;
            }

            cleanElements[el.symbol] = {
                certified: val,
                unit: el.unit,
                uncertainty: unc,
                method: category === 'pxrf' ? 'pXRF' : 'Fire Assay'
            };
        }

        if (Object.keys(cleanElements).length === 0) {
            setError('Please add at least one element with a valid value.');
            return;
        }

        const newCRM: CRMValue = {
            id: `CUSTOM-${name.replace(/\s+/g, '-').toUpperCase()}-${Date.now().toString().slice(-4)}`,
            name,
            supplier,
            matrix,
            category,
            elements: cleanElements,
            notes: notes || 'Custom Standard'
        };

        addCustomCRM(newCRM);
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-surface-dark border border-secondary-dark rounded-xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between p-6 border-b border-secondary-dark sticky top-0 bg-surface-dark z-10">
                    <h2 className="text-xl font-bold text-slate-100">Add Custom Standard</h2>
                    <button onClick={onClose} className="text-slate-400 hover:text-white transition-colors">
                        <X className="w-6 h-6" />
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 space-y-6">
                    {error && (
                        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-lg flex items-center gap-2">
                            <AlertCircle className="w-5 h-5" />
                            <span>{error}</span>
                        </div>
                    )}

                    {/* Basic Info */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Standard Name *</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="e.g. MY-STD-01"
                                className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Supplier *</label>
                            <input
                                type="text"
                                value={supplier}
                                onChange={(e) => setSupplier(e.target.value)}
                                placeholder="e.g. Lab X"
                                className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Matrix *</label>
                            <input
                                type="text"
                                value={matrix}
                                onChange={(e) => setMatrix(e.target.value)}
                                placeholder="e.g. Oxide"
                                className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium text-slate-300">Category *</label>
                            <select
                                value={category}
                                onChange={(e) => setCategory(e.target.value as any)}
                                className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none"
                            >
                                <option value="gold">Gold</option>
                                <option value="multi-element">Multi-Element</option>
                                <option value="pxrf">pXRF</option>
                            </select>
                        </div>
                    </div>

                    {/* Elements */}
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <h3 className="text-lg font-semibold text-slate-200">Certified Values</h3>
                            <button
                                type="button"
                                onClick={handleAddElement}
                                className="text-sm text-primary hover:text-primary-light flex items-center gap-1 font-medium"
                            >
                                <Plus className="w-4 h-4" /> Add Element
                            </button>
                        </div>

                        <div className="space-y-3">
                            {elements.map((el, index) => (
                                <div key={index} className="flex gap-3 items-end">
                                    <div className="w-24">
                                        <label className="text-xs text-slate-400 mb-1 block">Element</label>
                                        <input
                                            type="text"
                                            value={el.symbol}
                                            onChange={(e) => handleElementChange(index, 'symbol', e.target.value)}
                                            placeholder="Symbol"
                                            className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 outline-none"
                                        />
                                    </div>
                                    <div className="flex-1">
                                        <label className="text-xs text-slate-400 mb-1 block">Certified Value</label>
                                        <input
                                            type="number"
                                            step="any"
                                            value={el.value}
                                            onChange={(e) => handleElementChange(index, 'value', e.target.value)}
                                            placeholder="Value"
                                            className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 outline-none"
                                        />
                                    </div>
                                    <div className="flex-1">
                                        <label className="text-xs text-slate-400 mb-1 block">Uncertainty (Std Dev)</label>
                                        <input
                                            type="number"
                                            step="any"
                                            value={el.uncertainty}
                                            onChange={(e) => handleElementChange(index, 'uncertainty', e.target.value)}
                                            placeholder="Optional"
                                            className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 outline-none"
                                        />
                                    </div>
                                    <div className="w-24">
                                        <label className="text-xs text-slate-400 mb-1 block">Unit</label>
                                        <select
                                            value={el.unit}
                                            onChange={(e) => handleElementChange(index, 'unit', e.target.value)}
                                            className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 outline-none"
                                        >
                                            <option value="ppm">ppm</option>
                                            <option value="ppb">ppb</option>
                                            <option value="%">%</option>
                                            <option value="g/t">g/t</option>
                                        </select>
                                    </div>
                                    <button
                                        type="button"
                                        onClick={() => handleRemoveElement(index)}
                                        className="p-2 text-slate-500 hover:text-red-400 transition-colors mb-[1px]"
                                        disabled={elements.length === 1}
                                    >
                                        <Trash2 className="w-5 h-5" />
                                    </button>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-medium text-slate-300">Notes (Optional)</label>
                        <textarea
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            placeholder="Additional information..."
                            rows={3}
                            className="w-full bg-surface-darker border border-secondary text-slate-100 rounded-lg px-3 py-2 focus:ring-2 focus:ring-primary focus:border-transparent outline-none resize-none"
                        />
                    </div>

                    <div className="flex justify-end gap-3 pt-4 border-t border-secondary-dark">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-slate-300 hover:text-white hover:bg-surface-light rounded-lg transition-colors"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="px-6 py-2 bg-primary hover:bg-primary-dark text-white font-medium rounded-lg transition-colors flex items-center gap-2"
                        >
                            <Save className="w-4 h-4" />
                            Save Standard
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};
