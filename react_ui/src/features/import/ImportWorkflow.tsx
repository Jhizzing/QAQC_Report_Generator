import React from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileSpreadsheet, X, ArrowRight } from 'lucide-react';
import { useImportStore } from '../../stores/importStore';
import { processFile } from '../../utils/fileProcessor';
import { guessMapping } from '../../utils/smartMapper';

interface ImportWorkflowProps {
    onComplete?: (data: any) => void;
    onLoadDemoData?: () => void;
}

export const ImportWorkflow: React.FC<ImportWorkflowProps> = ({ onComplete, onLoadDemoData }) => {
    const { files, addFile, removeFile, updateFileStatus, updateMapping, activeStep, setStep } = useImportStore();

    const handleDrop = async (acceptedFiles: File[]) => {
        for (const file of acceptedFiles) {
            addFile(file, 'assays');

            // Process immediately
            try {
                const data = await processFile(file);
                const rawMapping = guessMapping(data.headers);

                // Transform raw mapping to ColumnMapping
                const mapping = {
                    sampleId: rawMapping['sampleId'] || '',
                    sampleType: rawMapping['sampleType'] || '',
                    elementMap: Object.fromEntries(
                        Object.entries(rawMapping).filter(([k]) => k !== 'sampleId' && k !== 'sampleType')
                    )
                };

                // Find the file in the store to update it.
                // Since addFile is sync, the file should be in the store now.
                // We'll find it by name and 'pending' status.
                const fileInStore = useImportStore.getState().files.find(f => f.file.name === file.name && f.status === 'pending');

                if (fileInStore) {
                    updateFileStatus(fileInStore.id, 'mapped', { headers: data.headers });
                    updateMapping(fileInStore.id, mapping);
                }
            } catch (error) {
                console.error("Error processing file:", error);
                // update status to error
            }
        }
    };

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop: handleDrop,
        accept: {
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'text/csv': ['.csv']
        }
    });

    return (
        <div className="max-w-5xl mx-auto p-6">
            {/* Stepper */}
            <div className="flex items-center justify-center mb-12">
                {['Upload Data', 'Map Columns', 'Review'].map((step, i) => (
                    <div key={step} className="flex items-center">
                        <div className={`
              w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm
              ${i === 0 && activeStep === 'upload' ? 'bg-primary text-white' :
                                i === 1 && activeStep === 'mapping' ? 'bg-primary text-white' :
                                    i === 2 && activeStep === 'review' ? 'bg-primary text-white' :
                                        'bg-gray-100 dark:bg-gray-800 text-gray-400'}
            `}>
                            {i + 1}
                        </div>
                        <span className={`ml-3 text-sm font-medium ${(i === 0 && activeStep === 'upload') || (i === 1 && activeStep === 'mapping') || (i === 2 && activeStep === 'review')
                            ? 'text-gray-900 dark:text-white' : 'text-gray-400'
                            }`}>
                            {step}
                        </span>
                        {i < 2 && <div className="w-16 h-0.5 bg-gray-200 dark:bg-gray-800 mx-4" />}
                    </div>
                ))}
            </div>

            {activeStep === 'upload' && (
                <div className="space-y-8">
                    <div
                        {...getRootProps()}
                        className={`
              border-2 border-dashed rounded-2xl p-12 text-center transition-all cursor-pointer
              ${isDragActive
                                ? 'border-primary bg-primary/5'
                                : 'border-gray-300 dark:border-gray-700 hover:border-primary hover:bg-gray-50 dark:hover:bg-gray-800/50'
                            }
            `}
                    >
                        <input {...getInputProps()} />
                        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                            <Upload className="w-8 h-8 text-primary" />
                        </div>
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">Upload Files</h3>
                        <p className="text-gray-500 mt-2">Drag & drop assays, standards, or blank files here</p>
                        <p className="text-sm text-gray-400 mt-1">Supported: .xlsx, .csv</p>
                    </div>

                    {/* Demo Data Button */}
                    <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
                        <button
                            onClick={() => {
                                if (onLoadDemoData) onLoadDemoData();
                            }}
                            className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold hover:from-blue-600 hover:to-purple-700 transition-all shadow-lg hover:shadow-xl flex items-center justify-center gap-2"
                        >
                            <FileSpreadsheet className="w-5 h-5" />
                            📊 Load Demo Data (Gold QAQC Sample)
                        </button>
                        <p className="text-xs text-center text-gray-400 mt-2">
                            Try the workflow with pre-loaded sample data
                        </p>
                    </div>

                    {files.length > 0 && (
                        <div className="bg-surface dark:bg-surface-dark rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
                            <div className="p-4 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800">
                                <h4 className="font-semibold text-gray-900 dark:text-white">Uploaded Files ({files.length})</h4>
                            </div>
                            <div className="divide-y divide-gray-200 dark:divide-gray-800">
                                {files.map((file) => (
                                    <div key={file.id} className="p-4 flex items-center justify-between">
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 bg-blue-50 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
                                                <FileSpreadsheet className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900 dark:text-white">{file.file.name}</p>
                                                <p className="text-xs text-gray-500">{(file.file.size / 1024).toFixed(1)} KB</p>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <select
                                                className="text-sm bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg px-3 py-1.5 outline-none focus:ring-2 focus:ring-primary/50"
                                                value={file.type}
                                                onChange={() => { /* Update type placeholder */ }}
                                            >
                                                <option value="assays">Assays</option>
                                                <option value="standards">Standards</option>
                                                <option value="blanks">Blanks</option>
                                                <option value="duplicates">Duplicates</option>
                                            </select>
                                            <button
                                                onClick={() => removeFile(file.id)}
                                                className="p-2 hover:bg-red-50 dark:hover:bg-red-900/20 text-gray-400 hover:text-red-600 rounded-lg transition-colors"
                                            >
                                                <X className="w-4 h-4" />
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="flex justify-end">
                        <button
                            disabled={files.length === 0}
                            onClick={() => setStep('mapping')}
                            className="flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            Next: Map Columns
                            <ArrowRight className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            )}

            {activeStep === 'mapping' && (
                <div className="space-y-8">
                    <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-xl flex items-start gap-3">
                        <div className="p-2 bg-blue-100 dark:bg-blue-800 rounded-lg">
                            <FileSpreadsheet className="w-5 h-5 text-blue-600 dark:text-blue-300" />
                        </div>
                        <div>
                            <h4 className="font-semibold text-blue-900 dark:text-blue-100">Smart Mapping Active</h4>
                            <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">
                                We've automatically detected column headers based on common geological formats. Please review and adjust the mappings below.
                            </p>
                        </div>
                    </div>

                    <div className="space-y-6">
                        {files.map((file) => (
                            <div key={file.id} className="bg-surface dark:bg-surface-dark border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden">
                                <div className="p-4 bg-gray-50 dark:bg-gray-800/50 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
                                    <div className="flex items-center gap-3">
                                        <span className="px-2 py-1 text-xs font-medium uppercase tracking-wider bg-gray-200 dark:bg-gray-700 rounded text-gray-600 dark:text-gray-300">
                                            {file.type}
                                        </span>
                                        <h4 className="font-semibold text-gray-900 dark:text-white">{file.file.name}</h4>
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        Mapped: <span className="font-medium text-green-600">85%</span>
                                    </div>
                                </div>

                                <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-8">
                                    {/* Required Fields */}
                                    <div>
                                        <h5 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 uppercase tracking-wider">Required Columns</h5>
                                        <div className="space-y-4">
                                            {['Sample ID', 'Sample Type'].map((field) => (
                                                <div key={field} className="flex items-center justify-between group">
                                                    <label className="text-sm text-gray-600 dark:text-gray-400">{field}</label>
                                                    <select
                                                        className="text-sm bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg px-3 py-2 w-48 focus:ring-2 focus:ring-primary/50 outline-none"
                                                        value={file.mapping?.[field === 'Sample ID' ? 'sampleId' : 'sampleType'] || ''}
                                                        onChange={(e) => {
                                                            const newMapping = { ...file.mapping } as any;
                                                            if (field === 'Sample ID') newMapping.sampleId = e.target.value;
                                                            else newMapping.sampleType = e.target.value;
                                                            updateMapping(file.id, newMapping);
                                                        }}
                                                    >
                                                        <option value="">Select Column...</option>
                                                        {file.headers?.map(h => (
                                                            <option key={h} value={h}>{h}</option>
                                                        ))}
                                                    </select>                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    {/* Element Mapping */}
                                    <div>
                                        <h5 className="text-sm font-semibold text-gray-900 dark:text-white mb-4 uppercase tracking-wider">Element Columns</h5>
                                        <div className="bg-gray-50 dark:bg-gray-900/50 rounded-lg p-4 h-64 overflow-y-auto space-y-2 custom-scrollbar">
                                            {Object.entries(file.mapping?.elementMap || {}).map(([key, value]) => (
                                                <div key={key} className="flex items-center gap-3 p-2 hover:bg-white dark:hover:bg-gray-800 rounded-lg transition-colors cursor-pointer border border-transparent hover:border-gray-200 dark:hover:border-gray-700">
                                                    <div className="w-4 h-4 rounded border border-gray-300 dark:border-gray-600 bg-primary text-white flex items-center justify-center text-[10px]">
                                                        ✓
                                                    </div>
                                                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{key}</span>
                                                    <ArrowRight className="w-3 h-3 text-gray-400 ml-auto" />
                                                    <span className="text-xs font-mono text-gray-500 bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
                                                        {value}
                                                    </span>
                                                </div>
                                            ))}
                                            {(!file.mapping?.elementMap || Object.keys(file.mapping.elementMap).length === 0) && (
                                                <p className="text-sm text-gray-500 text-center py-4">No elements mapped yet.</p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="flex justify-between pt-6 border-t border-gray-200 dark:border-gray-800">
                        <button
                            onClick={() => setStep('upload')}
                            className="px-6 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white font-medium"
                        >
                            Back
                        </button>
                        <button
                            onClick={() => setStep('review')}
                            className="flex items-center gap-2 px-6 py-3 bg-primary text-white rounded-xl font-semibold hover:bg-primary-dark transition-all"
                        >
                            Review & Import
                            <ArrowRight className="w-4 h-4" />
                        </button>
                    </div>
                </div>
            )}

            {activeStep === 'review' && (
                <div className="text-center py-12">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Ready to Import</h3>
                    <p className="text-gray-500 mt-2 mb-8">You are about to import {files.length} files into the project.</p>
                    <button
                        onClick={() => {
                            // In a real app, we would aggregate all data here
                            // For this demo, we just pass the first file's data to the parent
                            const firstFile = files[0];
                            if (firstFile && (firstFile as any).data && onComplete) {
                                // Construct ProcessedData object
                                onComplete({
                                    fileName: firstFile.file.name,
                                    headers: firstFile.headers || [],
                                    data: (firstFile as any).data,
                                    rowCount: (firstFile as any).data.length
                                });
                            }
                        }}
                        className="px-8 py-3 bg-green-600 text-white rounded-xl font-bold hover:bg-green-700 transition-all shadow-lg shadow-green-600/20"
                    >
                        Confirm Import
                    </button>
                </div>
            )}
        </div>
    );
};
