import React, { useState, useEffect } from 'react';
import { CheckSquare, Square } from 'lucide-react';
import { useTemplateStore } from '../../stores/templateStore';
import { DATA_KEYS, type BlockType } from '../../types/reportTemplate';

export const PropertiesPanel: React.FC = () => {
    const {
        activeTemplate,
        selectedSectionId,
        selectedBlockId,
        updateBlock
    } = useTemplateStore();

    const selectedSection = activeTemplate?.sections.find(s => s.id === selectedSectionId);
    const selectedBlock = selectedSection?.blocks.find(b => b.id === selectedBlockId);

    const [formData, setFormData] = useState({
        type: '' as BlockType,
        label: '',
        description: '',
        key: '',
        placeholder: '',
        required: false
    });

    // Reset form when block selection changes
    useEffect(() => {
        if (selectedBlock) {
            setFormData({
                type: selectedBlock.type,
                label: selectedBlock.label,
                description: selectedBlock.description || '',
                key: selectedBlock.key || '',
                placeholder: selectedBlock.placeholder || '',
                required: selectedBlock.required || false
            });
        }
    }, [selectedBlock]);

    const handleUpdate = () => {
        if (!selectedSectionId || !selectedBlockId) return;

        updateBlock(selectedSectionId, selectedBlockId, {
            ...formData,
            description: formData.description || undefined,
            key: formData.key || undefined,
            placeholder: formData.placeholder || undefined
        });

        alert('Block updated successfully!');
    };

    if (!selectedBlock) {
        return (
            <div className="p-6">
                <h2 className="text-lg font-bold text-white mb-4">Block Properties</h2>
                <p className="text-gray-400">Select a block to edit its properties</p>
            </div>
        );
    }

    return (
        <div className="p-6">
            <h2 className="text-lg font-bold text-white mb-6">Block Properties</h2>

            <div className="space-y-4">
                {/* Block ID (Read-only) */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Block ID
                    </label>
                    <input
                        type="text"
                        value={selectedBlock.id}
                        readOnly
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-500 cursor-not-allowed"
                    />
                </div>

                {/* Type */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Type *
                    </label>
                    <select
                        value={formData.type}
                        onChange={(e) => setFormData({ ...formData, type: e.target.value as BlockType })}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                    >
                        <option value="text_auto">text_auto - Auto-generated text</option>
                        <option value="text_user">text_user - User input text</option>
                        <option value="text_mixed">text_mixed - Mixed content</option>
                        <option value="table_auto">table_auto - Auto-generated table</option>
                        <option value="table_user">table_user - User-defined table</option>
                        <option value="figure_auto">figure_auto - Auto-generated figure</option>
                        <option value="meta">meta - Metadata field</option>
                    </select>
                </div>

                {/* Label */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Label *
                    </label>
                    <input
                        type="text"
                        value={formData.label}
                        onChange={(e) => setFormData({ ...formData, label: e.target.value })}
                        placeholder="Block heading or caption"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                    />
                </div>

                {/* Description */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Description
                    </label>
                    <textarea
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="Help text or tooltip"
                        rows={3}
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
                    />
                </div>

                {/* Data Key (Autocomplete) */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Data Key
                    </label>
                    <select
                        value={formData.key}
                        onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                        data-tour="data-key-select"
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent font-mono text-sm"
                    >
                        <option value="">-- Select data key --</option>
                        {Object.entries(DATA_KEYS).map(([key, label]) => (
                            <option key={key} value={key}>
                                {key} ({label})
                            </option>
                        ))}
                    </select>
                    <p className="text-xs text-gray-500 mt-1">
                        Binds this block to data from the analysis engine
                    </p>
                </div>

                {/* Placeholder (for text_user blocks) */}
                {formData.type === 'text_user' && (
                    <div>
                        <label className="block text-sm font-medium text-gray-300 mb-2">
                            Placeholder Text
                        </label>
                        <input
                            type="text"
                            value={formData.placeholder}
                            onChange={(e) => setFormData({ ...formData, placeholder: e.target.value })}
                            placeholder="Placeholder for user input..."
                            className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-primary focus:border-transparent"
                        />
                    </div>
                )}

                {/* Required */}
                <div>
                    <label className="flex items-center gap-3 cursor-pointer">
                        <button
                            type="button"
                            onClick={() => setFormData({ ...formData, required: !formData.required })}
                            className="focus:outline-none focus:ring-2 focus:ring-primary rounded"
                        >
                            {formData.required ? (
                                <CheckSquare className="w-5 h-5 text-primary" />
                            ) : (
                                <Square className="w-5 h-5 text-gray-600" />
                            )}
                        </button>
                        <span className="text-sm font-medium text-gray-300">Required Field</span>
                    </label>
                </div>

                {/* Order */}
                <div>
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                        Order
                    </label>
                    <input
                        type="number"
                        value={selectedBlock.order}
                        readOnly
                        className="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-500 cursor-not-allowed"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                        Automatically updated when dragging blocks
                    </p>
                </div>

                {/* Update Button */}
                <button
                    onClick={handleUpdate}
                    className="w-full px-4 py-3 bg-primary text-white rounded-lg font-bold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20 mt-6"
                >
                    Update Block
                </button>
            </div>
        </div>
    );
};
