import React, { useState } from 'react';
import { Save, Download, Upload, ArrowLeft } from 'lucide-react';
import { SectionList } from './SectionList';
import { BlockEditor } from './BlockEditor';
import { PropertiesPanel } from './PropertiesPanel';
import { useTemplateStore } from '../../stores/templateStore';

interface TemplateEditorProps {
    onBack?: () => void;
}

export const TemplateEditor: React.FC<TemplateEditorProps> = ({ onBack }) => {
    const { activeTemplate, saveTemplate, validateTemplate, exportTemplate, importTemplate } = useTemplateStore();
    const [previewMode, setPreviewMode] = useState(false);

    const handleSave = () => {
        if (!activeTemplate) return;

        const validation = validateTemplate(activeTemplate);

        if (!validation.valid) {
            alert(`Template has errors:\n${validation.errors.join('\n')}`);
            return;
        }

        if (validation.warnings.length > 0) {
            const proceed = window.confirm(
                `Template has warnings:\n${validation.warnings.join('\n')}\n\nSave anyway?`
            );
            if (!proceed) return;
        }

        saveTemplate(activeTemplate);
        alert('Template saved successfully!');
    };

    const handleExport = () => {
        if (!activeTemplate) return;

        try {
            const json = exportTemplate(activeTemplate.template_id);
            const blob = new Blob([json], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${activeTemplate.template_id}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (error) {
            alert(`Export failed: ${error}`);
        }
    };

    const handleImport = () => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.json';
        input.onchange = async (e) => {
            const file = (e.target as HTMLInputElement).files?.[0];
            if (!file) return;

            try {
                const text = await file.text();
                importTemplate(text);
                alert('Template imported successfully!');
            } catch (error) {
                alert(`Import failed: ${error}`);
            }
        };
        input.click();
    };

    if (!activeTemplate) {
        return (
            <div className="min-h-screen bg-gray-950 flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-2xl font-bold text-white mb-4">No Template Selected</h2>
                    <p className="text-gray-400 mb-6">Please select or create a template to edit</p>
                    {onBack && (
                        <button
                            onClick={onBack}
                            className="px-6 py-3 bg-primary text-white rounded-xl font-bold hover:bg-primary/90 transition-colors"
                        >
                            Go Back
                        </button>
                    )}
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-950">
            {/* Top Toolbar */}
            <div className="bg-gray-900 border-b border-gray-800 px-6 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        {onBack && (
                            <button
                                onClick={onBack}
                                className="p-2 rounded-lg hover:bg-gray-800 transition-colors"
                            >
                                <ArrowLeft className="w-5 h-5 text-gray-300" />
                            </button>
                        )}
                        <div>
                            <h1 className="text-xl font-bold text-white">{activeTemplate.title}</h1>
                            <p className="text-sm text-gray-400">{activeTemplate.description}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-3" data-tour="editor-toolbar">
                        <button
                            onClick={() => setPreviewMode(!previewMode)}
                            data-tour="preview-toggle"
                            className={`px-4 py-2 rounded-lg font-medium transition-colors ${previewMode
                                ? 'bg-gray-700 text-white'
                                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                                }`}
                        >
                            {previewMode ? 'Edit Mode' : 'Preview Mode'}
                        </button>

                        <button
                            onClick={handleImport}
                            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg font-medium hover:bg-gray-700 transition-colors flex items-center gap-2"
                        >
                            <Upload className="w-4 h-4" />
                            Import
                        </button>

                        <button
                            onClick={handleExport}
                            className="px-4 py-2 bg-gray-800 text-gray-300 rounded-lg font-medium hover:bg-gray-700 transition-colors flex items-center gap-2"
                        >
                            <Download className="w-4 h-4" />
                            Export
                        </button>

                        <button
                            onClick={handleSave}
                            data-tour="save-button"
                            className="px-6 py-2 bg-primary text-white rounded-lg font-bold hover:bg-primary/90 transition-colors flex items-center gap-2 shadow-lg shadow-primary/20"
                        >
                            <Save className="w-4 h-4" />
                            Save
                        </button>
                    </div>
                </div>
            </div>

            {/* Three-Panel Layout */}
            <div className="flex h-[calc(100vh-80px)]">
                {/* Left Panel: Section List */}
                <div className="w-80 bg-gray-900 border-r border-gray-800 overflow-y-auto" data-tour="sections-panel">
                    <SectionList previewMode={previewMode} />
                </div>

                {/* Center Panel: Block Editor */}
                <div className="flex-1 bg-gray-950 overflow-y-auto" data-tour="blocks-panel">
                    <BlockEditor previewMode={previewMode} />
                </div>

                {/* Right Panel: Properties */}
                <div className="w-96 bg-gray-900 border-l border-gray-800 overflow-y-auto" data-tour="properties-panel">
                    <PropertiesPanel />
                </div>
            </div>
        </div>
    );
};
