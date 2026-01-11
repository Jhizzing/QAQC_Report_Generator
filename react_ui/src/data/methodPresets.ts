/**
 * Method-Specific Presets for QAQC Configuration
 * 
 * Provides preset configurations for different analytical methods
 * to simplify QAQC setup and ensure industry-standard defaults
 */

import { type AnalyticalMethod } from './elementDefaults';
import { type QAQCConfig } from '../features/analysis/QAQCRuleConfig';

export interface MethodPreset {
    id: AnalyticalMethod;
    name: string;
    description: string;
    category: 'gold' | 'pxrf' | 'multi';
    defaults: Partial<QAQCConfig>;
}

/**
 * Method-specific presets based on industry best practices
 */
export const METHOD_PRESETS: Record<AnalyticalMethod, MethodPreset> = {
    'Fire Assay': {
        id: 'Fire Assay',
        name: 'Fire Assay',
        description: 'Gold analysis using fire assay method',
        category: 'gold',
        defaults: {
            standards: {
                selectedCRMs: [],
                toleranceType: 'percentage',
                toleranceValue: 12,
                failureThreshold: 3
            },
            blanks: {
                detectionLimit: 0.01,
                detectionLimitUnit: 'g/t',
                contaminationMultiplier: 3
            },
            duplicates: {
                precisionTarget: 15,
                precisionMethod: 'hard',
                failureThreshold: 3
            },
            analyticalMethod: 'Fire Assay'
        }
    },
    'ICP-MS': {
        id: 'ICP-MS',
        name: 'ICP-MS',
        description: 'Inductively Coupled Plasma Mass Spectrometry - best for trace elements',
        category: 'multi',
        defaults: {
            standards: {
                selectedCRMs: [],
                toleranceType: 'percentage',
                toleranceValue: 10,  // Will be overridden by element-specific defaults
                failureThreshold: 3
            },
            blanks: {
                detectionLimit: 1,
                detectionLimitUnit: 'ppm',
                contaminationMultiplier: 3
            },
            duplicates: {
                precisionTarget: 12,  // Will be overridden by element-specific defaults
                precisionMethod: 'hard',
                failureThreshold: 3
            },
            analyticalMethod: 'ICP-MS'
        }
    },
    'ICP-OES': {
        id: 'ICP-OES',
        name: 'ICP-OES',
        description: 'Inductively Coupled Plasma Optical Emission Spectroscopy - best for major elements',
        category: 'multi',
        defaults: {
            standards: {
                selectedCRMs: [],
                toleranceType: 'percentage',
                toleranceValue: 7,  // Will be overridden by element-specific defaults
                failureThreshold: 3
            },
            blanks: {
                detectionLimit: 1,
                detectionLimitUnit: 'ppm',
                contaminationMultiplier: 3
            },
            duplicates: {
                precisionTarget: 7,  // Will be overridden by element-specific defaults
                precisionMethod: 'hard',
                failureThreshold: 3
            },
            analyticalMethod: 'ICP-OES'
        }
    },
    'pXRF': {
        id: 'pXRF',
        name: 'pXRF',
        description: 'Portable X-ray Fluorescence - field analysis with matrix effects',
        category: 'pxrf',
        defaults: {
            standards: {
                selectedCRMs: [],
                toleranceType: 'percentage',
                toleranceValue: 15,  // Will be overridden by element-specific defaults
                failureThreshold: 3
            },
            blanks: {
                detectionLimit: 10,
                detectionLimitUnit: 'ppm',
                contaminationMultiplier: 3
            },
            duplicates: {
                precisionTarget: 20,  // Will be overridden by element-specific defaults
                precisionMethod: 'hard',
                failureThreshold: 3
            },
            analyticalMethod: 'pXRF'
        }
    },
    'AAS': {
        id: 'AAS',
        name: 'AAS',
        description: 'Atomic Absorption Spectroscopy - traditional method for specific elements',
        category: 'multi',
        defaults: {
            standards: {
                selectedCRMs: [],
                toleranceType: 'percentage',
                toleranceValue: 12,
                failureThreshold: 3
            },
            blanks: {
                detectionLimit: 1,
                detectionLimitUnit: 'ppm',
                contaminationMultiplier: 3
            },
            duplicates: {
                precisionTarget: 12,
                precisionMethod: 'hard',
                failureThreshold: 3
            },
            analyticalMethod: 'AAS'
        }
    }
};

/**
 * Get preset for a given method
 */
export function getMethodPreset(method: AnalyticalMethod): MethodPreset {
    return METHOD_PRESETS[method];
}

/**
 * Get all presets for a given category
 */
export function getPresetsByCategory(category: 'gold' | 'pxrf' | 'multi'): MethodPreset[] {
    return Object.values(METHOD_PRESETS).filter(preset => preset.category === category);
}

/**
 * Apply method preset to QAQC config
 */
export function applyMethodPreset(
    config: QAQCConfig,
    method: AnalyticalMethod
): QAQCConfig {
    const preset = getMethodPreset(method);
    
    return {
        ...config,
        analyticalMethod: method,
        standards: {
            ...config.standards,
            ...preset.defaults.standards,
            selectedCRMs: config.standards.selectedCRMs  // Preserve selected CRMs
        },
        blanks: {
            ...config.blanks,
            ...preset.defaults.blanks
        },
        duplicates: {
            ...config.duplicates,
            ...preset.defaults.duplicates
        }
    };
}
