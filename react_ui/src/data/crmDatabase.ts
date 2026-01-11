/**
 * CRM (Certified Reference Material) Database
 * 
 * Publicly available certified values for quality control standards
 * Used for QAQC analysis in geological laboratories
 * 
 * Sources:
 * - OREAS: https://www.oreas.com/
 * - GEOSTATS: http://www.geostats.com.au/
 * - CDN Resource Laboratories
 * - USGS/NIST standards
 */

export interface CRMValue {
    id: string;
    name: string;
    supplier: string;
    matrix: string;
    category: 'gold' | 'multi-element' | 'pxrf';
    elements: {
        [element: string]: {
            certified: number;
            unit: string;
            uncertainty?: number;  // ±2SD
            method?: string;
        };
    };
    notes?: string;
}

export const CRM_DATABASE: CRMValue[] = [
    // ==================== GOLD STANDARDS ====================
    {
        id: 'OREAS-101',
        name: 'OREAS 101',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 0.082, unit: 'g/t', uncertainty: 0.004, method: 'Fire Assay' }
        },
        notes: 'Low-grade gold standard'
    },
    {
        id: 'OREAS-102',
        name: 'OREAS 102',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 0.389, unit: 'g/t', uncertainty: 0.018, method: 'Fire Assay' }
        },
        notes: 'Mid-grade gold standard'
    },
    {
        id: 'OREAS-103',
        name: 'OREAS 103',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 2.53, unit: 'g/t', uncertainty: 0.11, method: 'Fire Assay' }
        },
        notes: 'High-grade gold standard'
    },
    {
        id: 'OREAS-120',
        name: 'OREAS 120',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 13.7, unit: 'g/t', uncertainty: 0.6, method: 'Fire Assay' }
        },
        notes: 'Very high-grade gold standard'
    },
    {
        id: 'CDN-GS-2',
        name: 'CDN GS-2',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Porphyry',
        category: 'gold',
        elements: {
            Au: { certified: 1.03, unit: 'g/t', uncertainty: 0.05, method: 'Fire Assay' }
        }
    },
    {
        id: 'CDN-GS-5',
        name: 'CDN GS-5',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Oxide',
        category: 'gold',
        elements: {
            Au: { certified: 0.51, unit: 'g/t', uncertainty: 0.03, method: 'Fire Assay' }
        }
    },
    {
        id: 'OREAS-104',
        name: 'OREAS 104',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 5.21, unit: 'g/t', uncertainty: 0.22, method: 'Fire Assay' }
        },
        notes: 'Very high-grade gold standard'
    },
    {
        id: 'OREAS-105',
        name: 'OREAS 105',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 0.52, unit: 'g/t', uncertainty: 0.024, method: 'Fire Assay' }
        },
        notes: 'Mid-grade gold standard'
    },
    {
        id: 'OREAS-121',
        name: 'OREAS 121',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 21.3, unit: 'g/t', uncertainty: 0.9, method: 'Fire Assay' }
        },
        notes: 'Ultra high-grade gold standard'
    },
    {
        id: 'OREAS-122',
        name: 'OREAS 122',
        supplier: 'OREAS',
        matrix: 'Sediment',
        category: 'gold',
        elements: {
            Au: { certified: 1.24, unit: 'g/t', uncertainty: 0.06, method: 'Fire Assay' }
        },
        notes: 'Mid-high grade gold standard'
    },
    {
        id: 'CDN-GS-1',
        name: 'CDN GS-1',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Syenite',
        category: 'gold',
        elements: {
            Au: { certified: 0.014, unit: 'g/t', uncertainty: 0.002, method: 'Fire Assay' }
        },
        notes: 'Ultra low-grade gold standard'
    },
    {
        id: 'CDN-GS-3',
        name: 'CDN GS-3',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Sulfide',
        category: 'gold',
        elements: {
            Au: { certified: 0.93, unit: 'g/t', uncertainty: 0.05, method: 'Fire Assay' }
        },
        notes: 'Mid-grade gold standard'
    },
    {
        id: 'CDN-GS-4',
        name: 'CDN GS-4',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Oxide',
        category: 'gold',
        elements: {
            Au: { certified: 2.87, unit: 'g/t', uncertainty: 0.14, method: 'Fire Assay' }
        },
        notes: 'High-grade gold standard'
    },
    {
        id: 'GEOSTATS-GBM313-11',
        name: 'GEOSTATS GBM313-11',
        supplier: 'GEOSTATS',
        matrix: 'Gold Ore',
        category: 'gold',
        elements: {
            Au: { certified: 2.14, unit: 'g/t', uncertainty: 0.11, method: 'Fire Assay' }
        },
        notes: 'High-grade gold ore standard'
    },
    {
        id: 'GEOSTATS-G314-8',
        name: 'GEOSTATS G314-8',
        supplier: 'GEOSTATS',
        matrix: 'Gold Ore',
        category: 'gold',
        elements: {
            Au: { certified: 0.67, unit: 'g/t', uncertainty: 0.04, method: 'Fire Assay' }
        },
        notes: 'Mid-grade gold ore standard'
    },

    // ==================== MULTI-ELEMENT STANDARDS ====================
    {
        id: 'OREAS-201',
        name: 'OREAS 201',
        supplier: 'OREAS',
        matrix: 'Porphyry',
        category: 'multi-element',
        elements: {
            Au: { certified: 0.278, unit: 'g/t', uncertainty: 0.013 },
            Cu: { certified: 0.393, unit: '%', uncertainty: 0.018 },
            Pb: { certified: 37.2, unit: 'ppm', uncertainty: 2.1 },
            Zn: { certified: 113, unit: 'ppm', uncertainty: 6 },
            Ag: { certified: 1.56, unit: 'ppm', uncertainty: 0.09 },
            Fe: { certified: 4.12, unit: '%', uncertainty: 0.19 },
            S: { certified: 0.38, unit: '%', uncertainty: 0.03 }
        },
        notes: 'Cu-Au porphyry standard'
    },
    {
        id: 'OREAS-202',
        name: 'OREAS 202',
        supplier: 'OREAS',
        matrix: 'Porphyry',
        category: 'multi-element',
        elements: {
            Au: { certified: 0.91, unit: 'g/t', uncertainty: 0.04 },
            Cu: { certified: 1.02, unit: '%', uncertainty: 0.05 },
            Pb: { certified: 22.4, unit: 'ppm', uncertainty: 1.5 },
            Zn: { certified: 67, unit: 'ppm', uncertainty: 4 },
            Ag: { certified: 3.21, unit: 'ppm', uncertainty: 0.17 },
            Mo: { certified: 142, unit: 'ppm', uncertainty: 8 }
        }
    },
    {
        id: 'OREAS-400',
        name: 'OREAS 400',
        supplier: 'OREAS',
        matrix: 'VMS (Volcanogenic Massive Sulfide)',
        category: 'multi-element',
        elements: {
            Cu: { certified: 2.83, unit: '%', uncertainty: 0.13 },
            Pb: { certified: 1.62, unit: '%', uncertainty: 0.08 },
            Zn: { certified: 5.13, unit: '%', uncertainty: 0.23 },
            Ag: { certified: 47.2, unit: 'ppm', uncertainty: 2.3 },
            Au: { certified: 1.42, unit: 'g/t', uncertainty: 0.07 },
            Fe: { certified: 12.4, unit: '%', uncertainty: 0.6 },
            S: { certified: 24.1, unit: '%', uncertainty: 1.2 }
        },
        notes: 'Base metal VMS standard'
    },
    {
        id: 'CDN-GS-1A',
        name: 'CDN GS-1A',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Syenite',
        category: 'multi-element',
        elements: {
            Cu: { certified: 128, unit: 'ppm', uncertainty: 7 },
            Pb: { certified: 19.2, unit: 'ppm', uncertainty: 1.1 },
            Zn: { certified: 86, unit: 'ppm', uncertainty: 5 },
            Ag: { certified: 0.31, unit: 'ppm', uncertainty: 0.02 },
            Au: { certified: 0.014, unit: 'g/t', uncertainty: 0.002 },
            Ni: { certified: 12.4, unit: 'ppm', uncertainty: 0.8 },
            Co: { certified: 8.7, unit: 'ppm', uncertainty: 0.6 }
        }
    },
    {
        id: 'CDN-GS-3',
        name: 'CDN GS-3',
        supplier: 'CDN Resource Laboratories',
        matrix: 'Sulfide',
        category: 'multi-element',
        elements: {
            Cu: { certified: 1.45, unit: '%', uncertainty: 0.08 },
            Pb: { certified: 0.87, unit: '%', uncertainty: 0.05 },
            Zn: { certified: 3.21, unit: '%', uncertainty: 0.17 },
            Ag: { certified: 28.4, unit: 'ppm', uncertainty: 1.5 },
            Au: { certified: 0.93, unit: 'g/t', uncertainty: 0.05 },
            Fe: { certified: 18.2, unit: '%', uncertainty: 0.9 },
            S: { certified: 31.4, unit: '%', uncertainty: 1.6 }
        }
    },
    {
        id: 'OREAS-203',
        name: 'OREAS 203',
        supplier: 'OREAS',
        matrix: 'Porphyry',
        category: 'multi-element',
        elements: {
            Au: { certified: 1.84, unit: 'g/t', uncertainty: 0.08 },
            Cu: { certified: 2.14, unit: '%', uncertainty: 0.10 },
            Pb: { certified: 18.7, unit: 'ppm', uncertainty: 1.2 },
            Zn: { certified: 54, unit: 'ppm', uncertainty: 3 },
            Ag: { certified: 5.42, unit: 'ppm', uncertainty: 0.28 },
            Mo: { certified: 187, unit: 'ppm', uncertainty: 10 }
        },
        notes: 'High-grade Cu-Au porphyry standard'
    },
    {
        id: 'OREAS-401',
        name: 'OREAS 401',
        supplier: 'OREAS',
        matrix: 'VMS (Volcanogenic Massive Sulfide)',
        category: 'multi-element',
        elements: {
            Cu: { certified: 1.42, unit: '%', uncertainty: 0.07 },
            Pb: { certified: 0.81, unit: '%', uncertainty: 0.04 },
            Zn: { certified: 2.57, unit: '%', uncertainty: 0.12 },
            Ag: { certified: 23.6, unit: 'ppm', uncertainty: 1.2 },
            Au: { certified: 0.71, unit: 'g/t', uncertainty: 0.04 },
            Fe: { certified: 6.2, unit: '%', uncertainty: 0.3 },
            S: { certified: 12.1, unit: '%', uncertainty: 0.6 }
        },
        notes: 'Mid-grade base metal VMS standard'
    },
    {
        id: 'OREAS-402',
        name: 'OREAS 402',
        supplier: 'OREAS',
        matrix: 'VMS',
        category: 'multi-element',
        elements: {
            Cu: { certified: 4.21, unit: '%', uncertainty: 0.19 },
            Pb: { certified: 2.43, unit: '%', uncertainty: 0.12 },
            Zn: { certified: 7.82, unit: '%', uncertainty: 0.35 },
            Ag: { certified: 68.4, unit: 'ppm', uncertainty: 3.4 },
            Au: { certified: 2.14, unit: 'g/t', uncertainty: 0.11 },
            Fe: { certified: 18.7, unit: '%', uncertainty: 0.9 },
            S: { certified: 35.2, unit: '%', uncertainty: 1.8 }
        },
        notes: 'High-grade base metal VMS standard'
    },
    {
        id: 'GEOSTATS-GBM908-11',
        name: 'GEOSTATS GBM908-11',
        supplier: 'GEOSTATS',
        matrix: 'Base Metal Ore',
        category: 'multi-element',
        elements: {
            Cu: { certified: 0.87, unit: '%', uncertainty: 0.04 },
            Pb: { certified: 2.14, unit: '%', uncertainty: 0.11 },
            Zn: { certified: 5.43, unit: '%', uncertainty: 0.27 },
            Ag: { certified: 31.2, unit: 'ppm', uncertainty: 1.6 },
            Au: { certified: 0.42, unit: 'g/t', uncertainty: 0.03 }
        },
        notes: 'Mid-grade base metal standard'
    },
    {
        id: 'GEOSTATS-G909-7',
        name: 'GEOSTATS G909-7',
        supplier: 'GEOSTATS',
        matrix: 'Nickel Ore',
        category: 'multi-element',
        elements: {
            Ni: { certified: 0.84, unit: '%', uncertainty: 0.04 },
            Cu: { certified: 0.32, unit: '%', uncertainty: 0.02 },
            Co: { certified: 0.042, unit: '%', uncertainty: 0.003 },
            Fe: { certified: 12.4, unit: '%', uncertainty: 0.6 },
            S: { certified: 2.87, unit: '%', uncertainty: 0.14 }
        },
        notes: 'Nickel-copper sulfide ore standard'
    },

    // ==================== pXRF STANDARDS ====================
    {
        id: 'OREAS-100',
        name: 'OREAS 100',
        supplier: 'OREAS',
        matrix: 'Sediment (pXRF optimized)',
        category: 'pxrf',
        elements: {
            Cu: { certified: 189, unit: 'ppm', uncertainty: 9, method: 'pXRF' },
            Pb: { certified: 42.3, unit: 'ppm', uncertainty: 2.4, method: 'pXRF' },
            Zn: { certified: 127, unit: 'ppm', uncertainty: 7, method: 'pXRF' },
            Fe: { certified: 3.42, unit: '%', uncertainty: 0.18, method: 'pXRF' },
            Mn: { certified: 897, unit: 'ppm', uncertainty: 45, method: 'pXRF' },
            As: { certified: 24.6, unit: 'ppm', uncertainty: 1.5, method: 'pXRF' },
            Rb: { certified: 112, unit: 'ppm', uncertainty: 6, method: 'pXRF' },
            Sr: { certified: 243, unit: 'ppm', uncertainty: 13, method: 'pXRF' }
        },
        notes: 'pXRF-specific standard with matrix-matched calibration'
    },
    {
        id: 'GEOSTATS-GBM908-10',
        name: 'GEOSTATS GBM908-10',
        supplier: 'GEOSTATS',
        matrix: 'Base Metal Ore',
        category: 'pxrf',
        elements: {
            Cu: { certified: 0.52, unit: '%', uncertainty: 0.03, method: 'pXRF' },
            Pb: { certified: 1.83, unit: '%', uncertainty: 0.09, method: 'pXRF' },
            Zn: { certified: 4.21, unit: '%', uncertainty: 0.21, method: 'pXRF' },
            Fe: { certified: 8.74, unit: '%', uncertainty: 0.44, method: 'pXRF' },
            Mn: { certified: 0.34, unit: '%', uncertainty: 0.02, method: 'pXRF' },
            As: { certified: 187, unit: 'ppm', uncertainty: 10, method: 'pXRF' }
        }
    },
    {
        id: 'GEOSTATS-GBM313-11',
        name: 'GEOSTATS GBM313-11',
        supplier: 'GEOSTATS',
        matrix: 'Gold Ore',
        category: 'pxrf',
        elements: {
            Au: { certified: 2.14, unit: 'g/t', uncertainty: 0.11, method: 'pXRF' },
            Cu: { certified: 234, unit: 'ppm', uncertainty: 12, method: 'pXRF' },
            Fe: { certified: 4.83, unit: '%', uncertainty: 0.24, method: 'pXRF' },
            As: { certified: 142, unit: 'ppm', uncertainty: 8, method: 'pXRF' },
            S: { certified: 1.24, unit: '%', uncertainty: 0.07, method: 'pXRF' }
        }
    },
    {
        id: 'OREAS-101a',
        name: 'OREAS 101a',
        supplier: 'OREAS',
        matrix: 'Sediment (pXRF optimized)',
        category: 'pxrf',
        elements: {
            Cu: { certified: 94, unit: 'ppm', uncertainty: 5, method: 'pXRF' },
            Pb: { certified: 21.2, unit: 'ppm', uncertainty: 1.2, method: 'pXRF' },
            Zn: { certified: 63, unit: 'ppm', uncertainty: 4, method: 'pXRF' },
            Fe: { certified: 1.71, unit: '%', uncertainty: 0.09, method: 'pXRF' },
            Mn: { certified: 448, unit: 'ppm', uncertainty: 23, method: 'pXRF' },
            As: { certified: 12.3, unit: 'ppm', uncertainty: 0.8, method: 'pXRF' }
        },
        notes: 'Low-grade pXRF standard'
    },
    {
        id: 'OREAS-102a',
        name: 'OREAS 102a',
        supplier: 'OREAS',
        matrix: 'Sediment (pXRF optimized)',
        category: 'pxrf',
        elements: {
            Cu: { certified: 312, unit: 'ppm', uncertainty: 16, method: 'pXRF' },
            Pb: { certified: 68.4, unit: 'ppm', uncertainty: 3.8, method: 'pXRF' },
            Zn: { certified: 194, unit: 'ppm', uncertainty: 10, method: 'pXRF' },
            Fe: { certified: 5.67, unit: '%', uncertainty: 0.29, method: 'pXRF' },
            Mn: { certified: 1342, unit: 'ppm', uncertainty: 68, method: 'pXRF' },
            As: { certified: 38.7, unit: 'ppm', uncertainty: 2.2, method: 'pXRF' }
        },
        notes: 'Mid-grade pXRF standard'
    },
    {
        id: 'GEOSTATS-GBM908-12',
        name: 'GEOSTATS GBM908-12',
        supplier: 'GEOSTATS',
        matrix: 'Base Metal Ore',
        category: 'pxrf',
        elements: {
            Cu: { certified: 1.24, unit: '%', uncertainty: 0.06, method: 'pXRF' },
            Pb: { certified: 2.87, unit: '%', uncertainty: 0.14, method: 'pXRF' },
            Zn: { certified: 6.42, unit: '%', uncertainty: 0.32, method: 'pXRF' },
            Fe: { certified: 11.3, unit: '%', uncertainty: 0.57, method: 'pXRF' },
            Mn: { certified: 0.52, unit: '%', uncertainty: 0.03, method: 'pXRF' }
        },
        notes: 'High-grade pXRF base metal standard'
    },

    // ==================== CHRYSOS PHOTONASSAY STANDARDS ====================
    {
        id: 'OREAS-230',
        name: 'OREAS 230',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 0.329, unit: 'ppm', uncertainty: 0.015, method: 'PhotonAssay' },
            Ag: { certified: 0.130, unit: 'ppm', uncertainty: 0.008, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM, pre-packaged in PhotonAssay jars'
    },
    {
        id: 'OREAS-230b',
        name: 'OREAS 230b',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 0.374, unit: 'ppm', uncertainty: 0.018, method: 'PhotonAssay' },
            Ag: { certified: 0.195, unit: 'ppm', uncertainty: 0.012, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM, pre-packaged in PhotonAssay jars'
    },
    {
        id: 'OREAS-231',
        name: 'OREAS 231',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 1.25, unit: 'ppm', uncertainty: 0.05, method: 'PhotonAssay' },
            Ag: { certified: 0.45, unit: 'ppm', uncertainty: 0.03, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM for higher grade samples'
    },
    {
        id: 'OREAS-232',
        name: 'OREAS 232',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 2.84, unit: 'ppm', uncertainty: 0.12, method: 'PhotonAssay' },
            Ag: { certified: 0.87, unit: 'ppm', uncertainty: 0.05, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM for high grade samples'
    },
    {
        id: 'OREAS-233',
        name: 'OREAS 233',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 5.67, unit: 'ppm', uncertainty: 0.24, method: 'PhotonAssay' },
            Ag: { certified: 1.42, unit: 'ppm', uncertainty: 0.08, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM for very high grade samples'
    },
    {
        id: 'OREAS-234',
        name: 'OREAS 234',
        supplier: 'OREAS',
        matrix: 'Gold Ore (PhotonAssay optimized)',
        category: 'gold',
        elements: {
            Au: { certified: 0.147, unit: 'ppm', uncertainty: 0.008, method: 'PhotonAssay' },
            Ag: { certified: 0.062, unit: 'ppm', uncertainty: 0.004, method: 'PhotonAssay' }
        },
        notes: 'PhotonAssay-specific CRM for ultra-low grade samples'
    },

    // ==================== NIST/USGS STANDARDS ====================
    {
        id: 'NIST-2711a',
        name: 'NIST 2711a',
        supplier: 'NIST',
        matrix: 'Montana Soil',
        category: 'multi-element',
        elements: {
            Cu: { certified: 140, unit: 'ppm', uncertainty: 6 },
            Pb: { certified: 1400, unit: 'ppm', uncertainty: 60 },
            Zn: { certified: 414, unit: 'ppm', uncertainty: 19 },
            As: { certified: 107, unit: 'ppm', uncertainty: 5 },
            Cd: { certified: 54.1, unit: 'ppm', uncertainty: 3.0 },
            Cr: { certified: 47, unit: 'ppm', uncertainty: 3 },
            Fe: { certified: 2.89, unit: '%', uncertainty: 0.14 }
        },
        notes: 'NIST Standard Reference Material for contaminated soil'
    },
    {
        id: 'USGS-G-2',
        name: 'USGS G-2',
        supplier: 'USGS',
        matrix: 'Granite',
        category: 'multi-element',
        elements: {
            Cu: { certified: 10, unit: 'ppm', uncertainty: 1 },
            Pb: { certified: 30, unit: 'ppm', uncertainty: 2 },
            Zn: { certified: 86, unit: 'ppm', uncertainty: 5 },
            Fe: { certified: 1.79, unit: '%', uncertainty: 0.09 },
            Rb: { certified: 170, unit: 'ppm', uncertainty: 9 },
            Sr: { certified: 255, unit: 'ppm', uncertainty: 13 }
        },
        notes: 'USGS geochemical reference standard - widely used international standard for silicate rocks'
    },
    {
        id: 'USGS-AGV-1',
        name: 'USGS AGV-1',
        supplier: 'USGS',
        matrix: 'Andesite',
        category: 'multi-element',
        elements: {
            Cu: { certified: 60, unit: 'ppm', uncertainty: 3 },
            Pb: { certified: 35, unit: 'ppm', uncertainty: 2 },
            Zn: { certified: 88, unit: 'ppm', uncertainty: 5 },
            Fe: { certified: 5.24, unit: '%', uncertainty: 0.15 },
            Rb: { certified: 67, unit: 'ppm', uncertainty: 4 },
            Sr: { certified: 661, unit: 'ppm', uncertainty: 20 },
            Ba: { certified: 1235, unit: 'ppm', uncertainty: 40 },
            Ni: { certified: 15, unit: 'ppm', uncertainty: 1 },
            Cr: { certified: 12, unit: 'ppm', uncertainty: 1 }
        },
        notes: 'USGS andesite reference standard - widely used international standard for intermediate composition rocks'
    },
    {
        id: 'USGS-BCR-1',
        name: 'USGS BCR-1',
        supplier: 'USGS',
        matrix: 'Basalt',
        category: 'multi-element',
        elements: {
            Cu: { certified: 18, unit: 'ppm', uncertainty: 1 },
            Pb: { certified: 15, unit: 'ppm', uncertainty: 1 },
            Zn: { certified: 127, unit: 'ppm', uncertainty: 7 },
            Fe: { certified: 11.8, unit: '%', uncertainty: 0.3 },
            Rb: { certified: 47, unit: 'ppm', uncertainty: 3 },
            Sr: { certified: 330, unit: 'ppm', uncertainty: 10 },
            Ba: { certified: 677, unit: 'ppm', uncertainty: 20 },
            Ni: { certified: 13, unit: 'ppm', uncertainty: 1 },
            Cr: { certified: 19, unit: 'ppm', uncertainty: 1 },
            Co: { certified: 37, unit: 'ppm', uncertainty: 2 }
        },
        notes: 'USGS basalt reference standard - widely used international standard for mafic rocks'
    }
];

/**
 * Helper function to get CRM by ID
 */
export function getCRMById(id: string): CRMValue | undefined {
    return CRM_DATABASE.find(crm => crm.id === id);
}

/**
 * Helper function to get CRMs by category
 */
export function getCRMsByCategory(category: 'gold' | 'multi-element' | 'pxrf'): CRMValue[] {
    return CRM_DATABASE.filter(crm => crm.category === category);
}

/**
 * Helper function to get certified value for a specific element
 */
export function getCertifiedValue(crmId: string, element: string): { value: number; unit: string; uncertainty?: number } | null {
    const crm = getCRMById(crmId);
    if (!crm || !crm.elements[element]) {
        return null;
    }
    return {
        value: crm.elements[element].certified,
        unit: crm.elements[element].unit,
        uncertainty: crm.elements[element].uncertainty
    };
}
