import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { CRM_DATABASE, type CRMValue } from '../data/crmDatabase';

interface CRMState {
    customCRMs: CRMValue[];
    defaultCRMs: CRMValue[];

    // Actions
    addCustomCRM: (crm: CRMValue) => void;
    removeCustomCRM: (id: string) => void;
    updateCustomCRM: (id: string, updates: Partial<CRMValue>) => void;
    resetCustomCRMs: () => void;

    // Getters that combine both lists
    getAllCRMs: () => CRMValue[];
    getCRMsByCategory: (category: 'gold' | 'multi-element' | 'pxrf') => CRMValue[];
    getCRMById: (id: string) => CRMValue | undefined;
}

export const useCRMStore = create<CRMState>()(
    persist(
        (set, get) => ({
            customCRMs: [],
            defaultCRMs: CRM_DATABASE,

            addCustomCRM: (crm) => set((state) => ({
                customCRMs: [...state.customCRMs, crm]
            })),

            removeCustomCRM: (id) => set((state) => ({
                customCRMs: state.customCRMs.filter((c) => c.id !== id)
            })),

            updateCustomCRM: (id, updates) => set((state) => ({
                customCRMs: state.customCRMs.map((c) =>
                    c.id === id ? { ...c, ...updates } : c
                )
            })),

            resetCustomCRMs: () => set({ customCRMs: [] }),

            getAllCRMs: () => {
                const { customCRMs, defaultCRMs } = get();
                return [...defaultCRMs, ...customCRMs];
            },

            getCRMsByCategory: (category) => {
                const { customCRMs, defaultCRMs } = get();
                const all = [...defaultCRMs, ...customCRMs];
                return all.filter((c) => c.category === category);
            },

            getCRMById: (id) => {
                const { customCRMs, defaultCRMs } = get();
                return [...defaultCRMs, ...customCRMs].find((c) => c.id === id);
            }
        }),
        {
            name: 'qaqc-crm-storage',
            partialize: (state) => ({ customCRMs: state.customCRMs }), // Only persist custom CRMs
        }
    )
);
