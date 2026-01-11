/**
 * Element Classification and Default QAQC Values
 * 
 * Defines element categories (major vs trace) and default tolerances,
 * precision targets, and detection limits by element and method.
 */

export type ElementCategory = 'major' | 'trace';
export type AnalyticalMethod = 'ICP-MS' | 'ICP-OES' | 'pXRF' | 'Fire Assay' | 'AAS';

export interface ElementClassification {
    element: string;
    category: ElementCategory;
    defaultUnit: string;
    typicalConcentrationRange: {
        min: number;
        max: number;
        unit: string;
    };
}

export interface ElementQAQCDefaults {
    // Standards tolerance (%)
    tolerancePercent: number;
    // Blanks detection limit
    detectionLimit: number;
    detectionLimitUnit: 'ppm' | 'ppb' | 'pct' | 'g/t';
    // Duplicates precision target (%)
    precisionTargetRPD: number;
    precisionTargetHARD: number;
}

/**
 * Element classifications: Major (>1% typical) vs Trace (<0.1% typical)
 */
export const ELEMENT_CLASSIFICATIONS: Record<string, ElementClassification> = {
    // Major elements
    Fe: {
        element: 'Fe',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 1, max: 50, unit: '%' }
    },
    S: {
        element: 'S',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.1, max: 50, unit: '%' }
    },
    Cu: {
        element: 'Cu',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.1, max: 10, unit: '%' }
    },
    Pb: {
        element: 'Pb',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.1, max: 10, unit: '%' }
    },
    Zn: {
        element: 'Zn',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.1, max: 20, unit: '%' }
    },
    Al: {
        element: 'Al',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 1, max: 30, unit: '%' }
    },
    Ca: {
        element: 'Ca',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 1, max: 50, unit: '%' }
    },
    Mg: {
        element: 'Mg',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 1, max: 30, unit: '%' }
    },
    K: {
        element: 'K',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.5, max: 10, unit: '%' }
    },
    Na: {
        element: 'Na',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.5, max: 10, unit: '%' }
    },
    Ti: {
        element: 'Ti',
        category: 'major',
        defaultUnit: '%',
        typicalConcentrationRange: { min: 0.1, max: 5, unit: '%' }
    },
    
    // Trace elements
    Au: {
        element: 'Au',
        category: 'trace',
        defaultUnit: 'g/t',
        typicalConcentrationRange: { min: 0.01, max: 100, unit: 'g/t' }
    },
    Ag: {
        element: 'Ag',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 1000, unit: 'ppm' }
    },
    As: {
        element: 'As',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 1, max: 10000, unit: 'ppm' }
    },
    Ni: {
        element: 'Ni',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 10, max: 50000, unit: 'ppm' }
    },
    Co: {
        element: 'Co',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 1, max: 10000, unit: 'ppm' }
    },
    Mo: {
        element: 'Mo',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 1, max: 10000, unit: 'ppm' }
    },
    W: {
        element: 'W',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 1, max: 10000, unit: 'ppm' }
    },
    Sb: {
        element: 'Sb',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 1, max: 10000, unit: 'ppm' }
    },
    Bi: {
        element: 'Bi',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 1000, unit: 'ppm' }
    },
    Te: {
        element: 'Te',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 1000, unit: 'ppm' }
    },
    Se: {
        element: 'Se',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 1000, unit: 'ppm' }
    },
    Mn: {
        element: 'Mn',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 100, max: 100000, unit: 'ppm' }
    },
    Rb: {
        element: 'Rb',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 10, max: 10000, unit: 'ppm' }
    },
    Sr: {
        element: 'Sr',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 10, max: 10000, unit: 'ppm' }
    },
    Ba: {
        element: 'Ba',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 10, max: 100000, unit: 'ppm' }
    },
    Cr: {
        element: 'Cr',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 10, max: 50000, unit: 'ppm' }
    },
    Cd: {
        element: 'Cd',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 1000, unit: 'ppm' }
    },
    U: {
        element: 'U',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 10000, unit: 'ppm' }
    },
    Th: {
        element: 'Th',
        category: 'trace',
        defaultUnit: 'ppm',
        typicalConcentrationRange: { min: 0.1, max: 10000, unit: 'ppm' }
    }
};

/**
 * Get element classification
 */
export function getElementClassification(element: string): ElementClassification | undefined {
    return ELEMENT_CLASSIFICATIONS[element];
}

/**
 * Check if element is major (>1% typical) or trace (<0.1% typical)
 */
export function isMajorElement(element: string): boolean {
    const classification = getElementClassification(element);
    return classification?.category === 'major';
}

/**
 * Element-specific QAQC defaults by method
 * Based on industry best practices from research
 */
export const ELEMENT_QAQC_DEFAULTS: Record<string, Partial<Record<AnalyticalMethod, ElementQAQCDefaults>>> = {
    // Gold
    Au: {
        'Fire Assay': {
            tolerancePercent: 12,
            detectionLimit: 0.01,
            detectionLimitUnit: 'g/t',
            precisionTargetRPD: 15,
            precisionTargetHARD: 12
        },
        'pXRF': {
            tolerancePercent: 20,
            detectionLimit: 1,
            detectionLimitUnit: 'g/t',
            precisionTargetRPD: 25,
            precisionTargetHARD: 20
        }
    },
    
    // Copper
    Cu: {
        'ICP-MS': {
            tolerancePercent: 8,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 8,
            precisionTargetHARD: 6
        },
        'ICP-OES': {
            tolerancePercent: 7,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 7,
            precisionTargetHARD: 5
        },
        'pXRF': {
            tolerancePercent: 12,
            detectionLimit: 10,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 15,
            precisionTargetHARD: 12
        }
    },
    
    // Lead
    Pb: {
        'ICP-MS': {
            tolerancePercent: 8,
            detectionLimit: 0.5,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 8,
            precisionTargetHARD: 6
        },
        'ICP-OES': {
            tolerancePercent: 7,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 7,
            precisionTargetHARD: 5
        },
        'pXRF': {
            tolerancePercent: 12,
            detectionLimit: 10,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 15,
            precisionTargetHARD: 12
        }
    },
    
    // Zinc
    Zn: {
        'ICP-MS': {
            tolerancePercent: 8,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 8,
            precisionTargetHARD: 6
        },
        'ICP-OES': {
            tolerancePercent: 7,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 7,
            precisionTargetHARD: 5
        },
        'pXRF': {
            tolerancePercent: 12,
            detectionLimit: 10,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 15,
            precisionTargetHARD: 12
        }
    },
    
    // Iron
    Fe: {
        'ICP-OES': {
            tolerancePercent: 4,
            detectionLimit: 0.01,
            detectionLimitUnit: 'pct',
            precisionTargetRPD: 4,
            precisionTargetHARD: 3
        },
        'pXRF': {
            tolerancePercent: 8,
            detectionLimit: 0.1,
            detectionLimitUnit: 'pct',
            precisionTargetRPD: 10,
            precisionTargetHARD: 8
        }
    },
    
    // Sulfur
    S: {
        'ICP-OES': {
            tolerancePercent: 8,
            detectionLimit: 0.01,
            detectionLimitUnit: 'pct',
            precisionTargetRPD: 8,
            precisionTargetHARD: 6
        },
        'pXRF': {
            tolerancePercent: 12,
            detectionLimit: 0.1,
            detectionLimitUnit: 'pct',
            precisionTargetRPD: 15,
            precisionTargetHARD: 12
        }
    },
    
    // Silver
    Ag: {
        'ICP-MS': {
            tolerancePercent: 12,
            detectionLimit: 0.1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 12,
            precisionTargetHARD: 10
        },
        'pXRF': {
            tolerancePercent: 15,
            detectionLimit: 5,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 20,
            precisionTargetHARD: 15
        }
    },
    
    // Arsenic
    As: {
        'ICP-MS': {
            tolerancePercent: 18,
            detectionLimit: 2,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 18,
            precisionTargetHARD: 15
        },
        'pXRF': {
            tolerancePercent: 20,
            detectionLimit: 10,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 25,
            precisionTargetHARD: 20
        }
    },
    
    // Nickel
    Ni: {
        'ICP-MS': {
            tolerancePercent: 12,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 12,
            precisionTargetHARD: 10
        },
        'ICP-OES': {
            tolerancePercent: 10,
            detectionLimit: 1,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 10,
            precisionTargetHARD: 8
        },
        'pXRF': {
            tolerancePercent: 15,
            detectionLimit: 20,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 20,
            precisionTargetHARD: 15
        }
    },
    
    // Cobalt
    Co: {
        'ICP-MS': {
            tolerancePercent: 18,
            detectionLimit: 0.5,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 18,
            precisionTargetHARD: 15
        },
        'pXRF': {
            tolerancePercent: 20,
            detectionLimit: 10,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 25,
            precisionTargetHARD: 20
        }
    },
    
    // Molybdenum
    Mo: {
        'ICP-MS': {
            tolerancePercent: 12,
            detectionLimit: 0.5,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 12,
            precisionTargetHARD: 10
        },
        'pXRF': {
            tolerancePercent: 15,
            detectionLimit: 5,
            detectionLimitUnit: 'ppm',
            precisionTargetRPD: 20,
            precisionTargetHARD: 15
        }
    }
};

/**
 * Get element-specific QAQC defaults for a given element and method
 */
export function getElementQAQCDefaults(
    element: string,
    method: AnalyticalMethod = 'ICP-MS'
): ElementQAQCDefaults | null {
    const elementDefaults = ELEMENT_QAQC_DEFAULTS[element];
    if (!elementDefaults) {
        return null;
    }
    
    // Try method-specific defaults first
    if (elementDefaults[method]) {
        return elementDefaults[method]!;
    }
    
    // Fall back to any available method
    const availableMethod = Object.keys(elementDefaults)[0] as AnalyticalMethod;
    if (availableMethod && elementDefaults[availableMethod]) {
        return elementDefaults[availableMethod]!;
    }
    
    return null;
}

/**
 * Get default tolerance for element and method
 */
export function getDefaultTolerance(element: string, method: AnalyticalMethod = 'ICP-MS'): number {
    const defaults = getElementQAQCDefaults(element, method);
    if (defaults) {
        return defaults.tolerancePercent;
    }
    
    // Fall back to category-based defaults
    const classification = getElementClassification(element);
    if (classification?.category === 'major') {
        return method === 'ICP-OES' ? 7 : 8;
    } else {
        return method === 'pXRF' ? 20 : 15;
    }
}

/**
 * Get default detection limit for element and method
 */
export function getDefaultDetectionLimit(
    element: string,
    method: AnalyticalMethod = 'ICP-MS'
): { value: number; unit: 'ppm' | 'ppb' | 'pct' | 'g/t' } {
    const defaults = getElementQAQCDefaults(element, method);
    if (defaults) {
        return {
            value: defaults.detectionLimit,
            unit: defaults.detectionLimitUnit
        };
    }
    
    // Fall back to category-based defaults
    const classification = getElementClassification(element);
    if (classification?.category === 'major') {
        return { value: 0.01, unit: 'pct' as const };
    } else {
        if (element === 'Au') {
            return { value: 0.01, unit: 'g/t' as const };
        }
        return { value: method === 'pXRF' ? 10 : 1, unit: 'ppm' as const };
    }
}

/**
 * Get default precision target for element and method
 */
export function getDefaultPrecisionTarget(
    element: string,
    method: AnalyticalMethod = 'ICP-MS',
    precisionMethod: 'rpd' | 'hard' = 'hard'
): number {
    const defaults = getElementQAQCDefaults(element, method);
    if (defaults) {
        return precisionMethod === 'rpd' 
            ? defaults.precisionTargetRPD 
            : defaults.precisionTargetHARD;
    }
    
    // Fall back to category-based defaults
    const classification = getElementClassification(element);
    if (classification?.category === 'major') {
        return method === 'ICP-OES' ? 5 : 7;
    } else {
        return method === 'pXRF' ? 20 : 15;
    }
}
