import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileSpreadsheet, X, ChevronDown, ChevronUp, CheckCircle2, AlertCircle, ArrowRight, Server } from 'lucide-react';
import { useImportStore } from '../../stores/importStore';
import { processFile } from '../../utils/fileProcessor';
import { guessMapping } from '../../utils/smartMapper';
import { uploadFileForAnalysis } from '../../services/analysisService';

interface ImportWorkflowProps {
    onComplete?: (data: any, serverFileId?: string) => void;
    onLoadDemoData?: (category?: 'gold' | 'photon') => void;
    isBackendAvailable?: boolean;
}

export const ImportWorkflow: React.FC<ImportWorkflowProps> = ({ onComplete, onLoadDemoData, isBackendAvailable }) => {
    const { files, addFile, removeFile, updateFileStatus, updateMapping } = useImportStore();
    const [expandedFileId, setExpandedFileId] = useState<string | null>(null);
    const [serverFileIds, setServerFileIds] = useState<Record<string, string>>({});
    const [uploadingToServer, setUploadingToServer] = useState<string | null>(null);

    const handleDrop = async (acceptedFiles: File[]) => {
        for (const file of acceptedFiles) {
            addFile(file, 'assays');

            try {
                // Always do client-side processing first for immediate feedback
                const data = await processFile(file);
                const rawMapping = guessMapping(data.headers);

                const mapping = {
                    sampleId: rawMapping['sampleId'] || '',
                    sampleType: rawMapping['sampleType'] || '',
                    elementMap: Object.fromEntries(
                        Object.entries(rawMapping).filter(([k]) => k !== 'sampleId' && k !== 'sampleType')
                    )
                };

                const fileInStore = useImportStore.getState().files.find(f => f.file.name === file.name && f.status === 'pending');

                if (fileInStore) {
                    updateFileStatus(fileInStore.id, 'mapped', {
                        headers: data.headers,
                        data: data.data
                    });
                    updateMapping(fileInStore.id, mapping);
                    // Auto-expand the first uploaded file
                    if (files.length === 0) {
                        setExpandedFileId(fileInStore.id);
                    }

                    // If backend is available, also upload to server in background
                    if (isBackendAvailable) {
                        setUploadingToServer(fileInStore.id);
                        try {
                            const serverResponse = await uploadFileForAnalysis(file);
                            setServerFileIds(prev => ({ ...prev, [fileInStore.id]: serverResponse.fileId }));
                            console.log(`File uploaded to server: ${serverResponse.fileId}`);
                        } catch (serverError) {
                            console.warn('Server upload failed, will use client-side analysis:', serverError);
                        } finally {
                            setUploadingToServer(null);
                        }
                    }
                }
            } catch (error) {
                console.error("Error processing file:", error);
                const fileInStore = useImportStore.getState().files.find(f => f.file.name === file.name);
                if (fileInStore) {
                    updateFileStatus(fileInStore.id, 'error');
                }
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

    const handleProceed = () => {
        const firstFile = files[0];
        if (firstFile && (firstFile as any).data && onComplete) {
            // Pass server file ID if available for server-side analysis
            const serverFileId = serverFileIds[firstFile.id];
            onComplete({
                fileName: firstFile.file.name,
                headers: firstFile.headers || [],
                data: (firstFile as any).data,
                rowCount: (firstFile as any).data.length
            }, serverFileId);
        }
    };

    // Calculate mapping percentage
    const getMappingPercentage = (file: typeof files[0]) => {
        if (!file.mapping) return 0;
        const hasSampleId = !!file.mapping.sampleId;
        const hasSampleType = !!file.mapping.sampleType;
        const elementCount = Object.keys(file.mapping.elementMap || {}).length;
        
        if (!hasSampleId && !hasSampleType && elementCount === 0) return 0;
        
        // Required fields weight: 40%, elements: 60%
        const requiredScore = (hasSampleId ? 20 : 0) + (hasSampleType ? 20 : 0);
        const elementScore = elementCount > 0 ? 60 : 0;
        return requiredScore + elementScore;
    };

    const allFilesMapped = files.length > 0 && files.every(f => f.status === 'mapped' && getMappingPercentage(f) >= 40);

    return (
        <div className="max-w-4xl mx-auto">
            {/* Upload Zone */}
            <div
                {...getRootProps()}
                data-tour="upload-area"
                className={`
                    border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-300
                    ${isDragActive
                        ? 'border-primary bg-primary/10 scale-[1.01] shadow-[0_0_20px_rgba(245,158,11,0.2)]'
                        : 'border-secondary-light hover:border-primary/50 hover:bg-surface-light'
                    }
                `}
            >
                <input {...getInputProps()} />
                <div className={`w-14 h-14 rounded-2xl flex items-center justify-center mx-auto mb-3 transition-colors ${
                    isDragActive ? 'bg-primary/20 text-primary' : 'bg-surface-light text-slate-400'
                }`}>
                    <Upload className={`w-7 h-7 ${isDragActive ? 'animate-bounce' : ''}`} />
                </div>
                <h3 className="text-lg font-bold text-slate-50 mb-1">
                    {isDragActive ? 'Drop files now' : 'Upload Data Files'}
                </h3>
                <p className="text-sm text-slate-400">Drag & drop CSV or Excel files here, or click to browse</p>
            </div>

            {/* Demo Data Section */}
            <div className="mt-6 pt-6 border-t border-secondary-dark">
                <p className="text-sm font-semibold text-slate-300 mb-3 text-center">
                    Or try with sample data
                </p>
                <div className="grid grid-cols-2 gap-3" data-tour="demo-gold-btn">
                    <button
                        onClick={() => onLoadDemoData?.('gold')}
                        className="px-4 py-3 bg-gradient-to-r from-primary to-primary-dark text-slate-900 rounded-xl font-semibold hover:shadow-lg hover:shadow-primary/20 transition-all flex items-center justify-center gap-2"
                    >
                        <FileSpreadsheet className="w-4 h-4" />
                        Gold Fire Assay
                    </button>
                    <button
                        onClick={() => onLoadDemoData?.('photon')}
                        className="px-4 py-3 bg-gradient-to-r from-purple-500 to-purple-700 text-slate-50 rounded-xl font-semibold hover:shadow-lg transition-all flex items-center justify-center gap-2"
                    >
                        <FileSpreadsheet className="w-4 h-4" />
                        PhotonAssay
                    </button>
                </div>
            </div>

            {/* Uploaded Files with Inline Mapping */}
            {files.length > 0 && (
                <div className="mt-8 space-y-4">
                    <h4 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
                        Uploaded Files ({files.length})
                    </h4>
                    
                    {files.map((file) => {
                        const mappingPct = getMappingPercentage(file);
                        const isExpanded = expandedFileId === file.id;
                        const isError = file.status === 'error';
                        
                        return (
                            <div 
                                key={file.id} 
                                className={`bg-surface rounded-xl border overflow-hidden transition-all ${
                                    isError ? 'border-status-error/50' : 'border-secondary-dark'
                                }`}
                            >
                                {/* File Header */}
                                <div className="p-4 flex items-center justify-between">
                                    <div className="flex items-center gap-4">
                                        <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                                            isError ? 'bg-status-error/20' : 'bg-accent/20'
                                        }`}>
                                            {isError ? (
                                                <AlertCircle className="w-5 h-5 text-status-error" />
                                            ) : (
                                                <FileSpreadsheet className="w-5 h-5 text-accent" />
                                            )}
                                        </div>
                                        <div>
                                            <p className="font-medium text-slate-50">{file.file.name}</p>
                                            <p className="text-xs text-slate-500">
                                                {(file.file.size / 1024).toFixed(1)} KB
                                                {file.headers && ` • ${file.headers.length} columns`}
                                            </p>
                                        </div>
                                    </div>
                                    
                                    <div className="flex items-center gap-3">
                                        {!isError && (
                                            <>
                                                {/* Server Upload Status */}
                                                {isBackendAvailable && (
                                                    <div className="flex items-center gap-1">
                                                        {uploadingToServer === file.id ? (
                                                            <div className="flex items-center gap-1 text-xs text-yellow-400">
                                                                <Server className="w-3 h-3 animate-pulse" />
                                                                <span>Uploading...</span>
                                                            </div>
                                                        ) : serverFileIds[file.id] ? (
                                                            <div className="flex items-center gap-1 text-xs text-green-400">
                                                                <Server className="w-3 h-3" />
                                                                <span>Server</span>
                                                            </div>
                                                        ) : null}
                                                    </div>
                                                )}
                                                
                                                {/* Mapping Status */}
                                                <div className="flex items-center gap-2">
                                                    {mappingPct >= 40 ? (
                                                        <CheckCircle2 className="w-4 h-4 text-status-success" />
                                                    ) : null}
                                                    <span className={`text-sm font-medium ${
                                                        mappingPct >= 40 ? 'text-status-success' : 'text-slate-400'
                                                    }`}>
                                                        {mappingPct}% mapped
                                                    </span>
                                                </div>
                                                
                                                {/* Expand Toggle */}
                                                <button
                                                    onClick={() => setExpandedFileId(isExpanded ? null : file.id)}
                                                    className="p-2 hover:bg-surface-light rounded-lg transition-colors text-slate-400 hover:text-slate-200"
                                                >
                                                    {isExpanded ? (
                                                        <ChevronUp className="w-4 h-4" />
                                                    ) : (
                                                        <ChevronDown className="w-4 h-4" />
                                                    )}
                                                </button>
                                            </>
                                        )}
                                        
                                        {/* Remove Button */}
                                        <button
                                            onClick={() => removeFile(file.id)}
                                            className="p-2 hover:bg-status-error/20 text-slate-400 hover:text-status-error rounded-lg transition-colors"
                                        >
                                            <X className="w-4 h-4" />
                                        </button>
                                    </div>
                                </div>

                                {/* Expanded Mapping Panel */}
                                {isExpanded && !isError && (
                                    <div className="px-4 pb-4 border-t border-secondary-dark pt-4 animate-fade-in">
                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                            {/* Required Columns */}
                                            <div>
                                                <h5 className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                                                    Required Columns
                                                </h5>
                                                <div className="space-y-3">
                                                    {['Sample ID', 'Sample Type'].map((field) => (
                                                        <div key={field} className="flex items-center justify-between gap-4">
                                                            <label className="text-sm text-slate-300 font-medium">{field}</label>
                                                            <select
                                                                className="text-sm bg-surface-light border border-secondary-light rounded-lg px-3 py-2 w-40 focus:ring-2 focus:ring-primary/50 outline-none text-slate-200"
                                                                value={file.mapping?.[field === 'Sample ID' ? 'sampleId' : 'sampleType'] || ''}
                                                                onChange={(e) => {
                                                                    const newMapping = { ...file.mapping } as any;
                                                                    if (field === 'Sample ID') newMapping.sampleId = e.target.value;
                                                                    else newMapping.sampleType = e.target.value;
                                                                    updateMapping(file.id, newMapping);
                                                                }}
                                                            >
                                                                <option value="">Select...</option>
                                                                {file.headers?.map(h => (
                                                                    <option key={h} value={h}>{h}</option>
                                                                ))}
                                                            </select>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>

                                            {/* Element Columns (auto-detected) */}
                                            <div>
                                                <h5 className="text-xs font-semibold text-slate-400 mb-3 uppercase tracking-wider">
                                                    Detected Elements ({Object.keys(file.mapping?.elementMap || {}).length})
                                                </h5>
                                                <div className="bg-surface-light rounded-lg p-3 max-h-32 overflow-y-auto space-y-1">
                                                    {Object.entries(file.mapping?.elementMap || {}).map(([key, value]) => (
                                                        <div key={key} className="flex items-center justify-between text-sm">
                                                            <span className="text-slate-300">{key}</span>
                                                            <span className="text-xs text-slate-500 font-mono">{value}</span>
                                                        </div>
                                                    ))}
                                                    {(!file.mapping?.elementMap || Object.keys(file.mapping.elementMap).length === 0) && (
                                                        <p className="text-sm text-slate-500 text-center py-2">No elements detected</p>
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                )}
                            </div>
                        );
                    })}

                    {/* Proceed Button */}
                    <div className="pt-4">
                        <button
                            onClick={handleProceed}
                            disabled={!allFilesMapped}
                            className="w-full flex items-center justify-center gap-2 px-6 py-4 bg-gradient-to-r from-primary to-primary-dark text-slate-900 rounded-xl font-bold text-lg hover:shadow-lg hover:shadow-primary/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                        >
                            Proceed to Analysis Setup
                            <ArrowRight className="w-5 h-5" />
                        </button>
                        {!allFilesMapped && files.length > 0 && (
                            <p className="text-center text-sm text-slate-500 mt-2">
                                Ensure all files have Sample ID and Sample Type mapped
                            </p>
                        )}
                    </div>
                </div>
            )}

            <style>{`
                @keyframes fade-in {
                    from { opacity: 0; transform: translateY(-8px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in {
                    animation: fade-in 0.2s ease-out;
                }
            `}</style>
        </div>
    );
};
