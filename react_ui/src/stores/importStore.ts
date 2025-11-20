import { create } from 'zustand';

export interface ColumnMapping {
    sampleId: string;
    sampleType?: string;
    labId?: string;
    batchId?: string;
    elementMap: Record<string, string>; // e.g. 'Au' -> 'Au_ppm'
}

export interface FileUploadState {
    id: string;
    file: File;
    type: 'assays' | 'standards' | 'blanks' | 'duplicates' | 'pxrf';
    status: 'pending' | 'processing' | 'mapped' | 'error';
    data?: any[];
    headers?: string[];
    mapping?: ColumnMapping;
}

interface ImportState {
    files: FileUploadState[];
    activeStep: 'upload' | 'mapping' | 'review';

    addFile: (file: File, type: FileUploadState['type']) => void;
    removeFile: (id: string) => void;
    updateFileStatus: (id: string, status: FileUploadState['status'], data?: any) => void;
    updateMapping: (id: string, mapping: ColumnMapping) => void;
    setStep: (step: ImportState['activeStep']) => void;
    reset: () => void;
}

export const useImportStore = create<ImportState>((set) => ({
    files: [],
    activeStep: 'upload',

    addFile: (file, type) => set((state) => ({
        files: [...state.files, {
            id: crypto.randomUUID(),
            file,
            type,
            status: 'pending'
        }]
    })),

    removeFile: (id) => set((state) => ({
        files: state.files.filter(f => f.id !== id)
    })),

    updateFileStatus: (id, status, data) => set((state) => ({
        files: state.files.map(f => f.id === id ? { ...f, status, ...data } : f)
    })),

    updateMapping: (id, mapping) => set((state) => ({
        files: state.files.map(f => f.id === id ? { ...f, mapping } : f)
    })),

    setStep: (step) => set({ activeStep: step }),

    reset: () => set({ files: [], activeStep: 'upload' })
}));
