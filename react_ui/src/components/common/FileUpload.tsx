import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, AlertCircle, Shield, Loader2 } from 'lucide-react';
import { processFile } from '../../utils/fileProcessor';
import type { ProcessedData } from '../../utils/fileProcessor';

interface FileUploadProps {
    onDataLoaded: (data: ProcessedData) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onDataLoaded }) => {
    const [isProcessing, setIsProcessing] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        if (!file) return;

        setIsProcessing(true);
        setError(null);

        try {
            const data = await processFile(file);
            onDataLoaded(data);
        } catch (err) {
            setError('Failed to process file. Please ensure it is a valid Excel or CSV file.');
            console.error(err);
        } finally {
            setIsProcessing(false);
        }
    }, [onDataLoaded]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/vnd.ms-excel': ['.xls'],
            'text/csv': ['.csv']
        },
        multiple: false
    });

    return (
        <div className="w-full max-w-2xl mx-auto">
            <div
                {...getRootProps()}
                className={`
          relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 cursor-pointer
          ${isDragActive
                        ? 'border-primary bg-primary/5'
                        : 'border-secondary-light hover:border-primary hover:bg-surface-light'
                    }
        `}
            >
                <input {...getInputProps()} />

                <div className="flex flex-col items-center gap-4">
                    <div className={`
            w-16 h-16 rounded-full flex items-center justify-center
            ${isProcessing ? 'bg-primary/10' : 'bg-surface-light'}
          `}>
                        {isProcessing ? (
                            <Loader2 className="w-8 h-8 text-primary animate-spin" />
                        ) : (
                            <Upload className={`w-8 h-8 ${isDragActive ? 'text-primary' : 'text-slate-400'}`} />
                        )}
                    </div>

                    <div className="space-y-2">
                        <h3 className="text-lg font-semibold text-slate-50">
                            {isDragActive ? 'Drop your file here' : 'Upload Assay Data'}
                        </h3>
                        <p className="text-sm text-slate-400 max-w-sm mx-auto">
                            Drag and drop your Excel or CSV file here, or click to browse.
                            <br />
                            <span className="text-xs opacity-75">Supports .xlsx, .xls, .csv</span>
                        </p>
                    </div>
                </div>

                {/* Security Badge */}
                <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-1.5 text-xs text-status-success bg-status-success/10 px-3 py-1 rounded-full">
                    <Shield className="w-3 h-3" />
                    <span>Local Processing • Data never leaves your device</span>
                </div>
            </div>

            {error && (
                <div className="mt-4 p-4 bg-status-error/10 text-status-error rounded-lg flex items-center gap-3 text-sm">
                    <AlertCircle className="w-5 h-5 shrink-0" />
                    {error}
                </div>
            )}
        </div>
    );
};
