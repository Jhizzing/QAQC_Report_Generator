/**
 * Mock QAQC Data Generator
 * 
 * Generates realistic QAQC datasets for testing and demonstration
 * Includes assays, standards (CRMs), blanks, and duplicates
 */

export interface MockQAQCDataset {
    combined: any[];  // All data combined for import
    assays: any[];
    standards: any[];
    blanks: any[];
    duplicates: any[];
    metadata: {
        project: string;
        campaign: string;
        elements: string[];
        category: 'gold' | 'pxrf' | 'multi';
    };
}

/**
 * Generate mock Gold QAQC dataset
 */
export function generateMockGoldData(): MockQAQCDataset {
    const assays: any[] = [];
    const standards: any[] = [];
    const blanks: any[] = [];
    const duplicates: any[] = [];

    let sampleNumber = 1;

    // Generate 10 batches of samples
    for (let batch = 1; batch <= 10; batch++) {
        // Standard at start of batch (OREAS-101, 102, or 103)
        const crmOptions = ['OREAS-101', 'OREAS-102', 'OREAS-103'];
        const crmId = crmOptions[Math.floor(Math.random() * 3)];
        const certifiedValues = { 'OREAS-101': 0.082, 'OREAS-102': 0.389, 'OREAS-103': 2.53 };
        const certifiedValue = certifiedValues[crmId as keyof typeof certifiedValues];

        standards.push({
            Sample_ID: `${crmId}-${batch}`,
            Sample_Type: 'Standard',
            Au_ppm: (certifiedValue + (Math.random() - 0.5) * certifiedValue * 0.15).toFixed(3),  // ±15% variance
            Cu_pct: (0.05 + (Math.random() - 0.5) * 0.01).toFixed(4),
            Batch: `BATCH-${batch.toString().padStart(2, '0')}`
        });

        // Blank every 2 batches
        if (batch % 2 === 0) {
            blanks.push({
                Sample_ID: `BLANK-${Math.floor(batch / 2)}`,
                Sample_Type: 'Blank',
                Au_ppm: (Math.random() * 0.01).toFixed(3),  // Very low values
                Cu_pct: (Math.random() * 0.001).toFixed(4),
                Batch: `BATCH-${batch.toString().padStart(2, '0')}`
            });
        }

        // 10 regular assay samples per batch
        for (let i = 1; i <= 10; i++) {
            const isDuplicate = i === 5;  // 5th sample will have a duplicate
            const auValue = Math.random() * 5;  // 0-5 g/t range
            const cuValue = Math.random() * 1.5;

            const sample = {
                Sample_ID: `RC${sampleNumber.toString().padStart(4, '0')}`,
                Sample_Type: 'Sample',
                Au_ppm: auValue.toFixed(3),
                Cu_pct: cuValue.toFixed(4),
                Batch: `BATCH-${batch.toString().padStart(2, '0')}`
            };

            assays.push(sample);

            // Add duplicate
            if (isDuplicate) {
                duplicates.push({
                    Sample_ID: `${sample.Sample_ID}-DUP`,
                    Sample_Type: 'Duplicate',
                    Au_ppm: (auValue * (1 + (Math.random() - 0.5) * 0.2)).toFixed(3),  // ±20% variance
                    Cu_pct: (cuValue * (1 + (Math.random() - 0.5) * 0.2)).toFixed(4),
                    Batch: `BATCH-${batch.toString().padStart(2, '0')}`
                });
            }

            sampleNumber++;
        }

        // Standard at end of batch
        standards.push({
            Sample_ID: `${crmId}-${batch}B`,
            Sample_Type: 'Standard',
            Au_ppm: (certifiedValue + (Math.random() - 0.5) * certifiedValue * 0.15).toFixed(3),
            Cu_pct: (0.05 + (Math.random() - 0.5) * 0.01).toFixed(4),
            Batch: `BATCH-${batch.toString().padStart(2, '0')}`
        });
    }

    // Combine all data in sequential order
    const combined = [...assays, ...standards, ...blanks, ...duplicates].sort((a, b) => {
        // Sort by batch, then by type priority (Standard, Sample, Blank, Duplicate)
        if (a.Batch !== b.Batch) return a.Batch.localeCompare(b.Batch);
        const priority = { Standard: 1, Sample: 2, Blank: 3, Duplicate: 4 };
        return priority[a.Sample_Type as keyof typeof priority] - priority[b.Sample_Type as keyof typeof priority];
    });

    return {
        combined,
        assays,
        standards,
        blanks,
        duplicates,
        metadata: {
            project: 'Demo Gold Project',
            campaign: '2025 Exploration Campaign',
            elements: ['Au', 'Cu'],
            category: 'gold'
        }
    };
}

/**
 * Generate mock pXRF dataset - Enhanced for base metals exploration
 * Includes Cu, Pb, Zn, Fe, As, Mn, Rb, Sr with proper QAQC distribution
 */
export function generateMockPXRFData(): MockQAQCDataset {
    const assays: any[] = [];
    const standards: any[] = [];
    const blanks: any[] = [];
    const duplicates: any[] = [];

    let sampleNumber = 1;

    // CRM options for pXRF (low, mid, high grade)
    const crmOptions = [
        { id: 'OREAS-101a', values: { Cu: 94, Pb: 21.2, Zn: 63, Fe: 1.71, As: 12.3, Mn: 448, Rb: 85, Sr: 180 } },
        { id: 'OREAS-100', values: { Cu: 189, Pb: 42.3, Zn: 127, Fe: 3.42, As: 24.6, Mn: 897, Rb: 112, Sr: 243 } },
        { id: 'OREAS-102a', values: { Cu: 312, Pb: 68.4, Zn: 194, Fe: 5.67, As: 38.7, Mn: 1342, Rb: 145, Sr: 320 } }
    ];

    // Generate 10 batches (~200 samples total)
    for (let batch = 1; batch <= 10; batch++) {
        // Standard at start of batch - rotate through CRMs
        const crm = crmOptions[(batch - 1) % crmOptions.length];
        const tolerance = 0.12; // 12% tolerance for pXRF

        standards.push({
            Sample_ID: `${crm.id}-${batch}`,
            Sample_Type: 'STD',
            Cu_ppm: (crm.values.Cu * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Pb_ppm: (crm.values.Pb * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Zn_ppm: (crm.values.Zn * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Fe_pct: (crm.values.Fe * (1 + (Math.random() - 0.5) * tolerance)).toFixed(2),
            As_ppm: (crm.values.As * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Mn_ppm: (crm.values.Mn * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Rb_ppm: (crm.values.Rb * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Sr_ppm: (crm.values.Sr * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Batch: `PXRF-BATCH-${batch.toString().padStart(2, '0')}`
        });

        // Blank every 2 batches (5% insertion rate)
        if (batch % 2 === 0) {
            blanks.push({
                Sample_ID: `BLANK-PX-${Math.floor(batch / 2)}`,
                Sample_Type: 'BLK',
                Cu_ppm: (Math.random() * 10).toFixed(1),  // Below 10 ppm DL
                Pb_ppm: (Math.random() * 10).toFixed(1),
                Zn_ppm: (Math.random() * 10).toFixed(1),
                Fe_pct: (Math.random() * 0.1).toFixed(2),
                As_ppm: (Math.random() * 10).toFixed(1),
                Mn_ppm: (Math.random() * 50).toFixed(0),
                Rb_ppm: (Math.random() * 20).toFixed(0),
                Sr_ppm: (Math.random() * 30).toFixed(0),
                Batch: `PXRF-BATCH-${batch.toString().padStart(2, '0')}`
            });
        }

        // 18 regular samples per batch
        for (let i = 1; i <= 18; i++) {
            const isDuplicate = i === 9; // Duplicate in middle of batch

            // Realistic concentration ranges for base metals exploration
            const cuValue = 50 + Math.random() * 4500; // 50-5000 ppm
            const pbValue = 20 + Math.random() * 1980; // 20-2000 ppm
            const znValue = 100 + Math.random() * 9900; // 100-10000 ppm
            const feValue = 1 + Math.random() * 14; // 1-15%
            const asValue = 10 + Math.random() * 490; // 10-500 ppm
            const mnValue = 200 + Math.random() * 1800; // 200-2000 ppm
            const rbValue = 50 + Math.random() * 250; // 50-300 ppm
            const srValue = 100 + Math.random() * 400; // 100-500 ppm

            const sample = {
                Sample_ID: `PX${sampleNumber.toString().padStart(4, '0')}`,
                Sample_Type: 'UNK',
                Cu_ppm: cuValue.toFixed(1),
                Pb_ppm: pbValue.toFixed(1),
                Zn_ppm: znValue.toFixed(1),
                Fe_pct: feValue.toFixed(2),
                As_ppm: asValue.toFixed(1),
                Mn_ppm: mnValue.toFixed(0),
                Rb_ppm: rbValue.toFixed(0),
                Sr_ppm: srValue.toFixed(0),
                Batch: `PXRF-BATCH-${batch.toString().padStart(2, '0')}`
            };

            assays.push(sample);

            // Add duplicate with realistic precision (15% HARD for pXRF)
            if (isDuplicate) {
                duplicates.push({
                    Sample_ID: `${sample.Sample_ID}-DUP`,
                    Sample_Type: 'DUP',
                    Cu_ppm: (parseFloat(sample.Cu_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Pb_ppm: (parseFloat(sample.Pb_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Zn_ppm: (parseFloat(sample.Zn_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Fe_pct: (parseFloat(sample.Fe_pct) * (1 + (Math.random() - 0.5) * 0.10)).toFixed(2),
                    As_ppm: (parseFloat(sample.As_ppm) * (1 + (Math.random() - 0.5) * 0.20)).toFixed(1),
                    Mn_ppm: (parseFloat(sample.Mn_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(0),
                    Rb_ppm: (parseFloat(sample.Rb_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(0),
                    Sr_ppm: (parseFloat(sample.Sr_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(0),
                    Batch: `PXRF-BATCH-${batch.toString().padStart(2, '0')}`
                });
            }

            sampleNumber++;
        }

        // Standard at end of batch
        standards.push({
            Sample_ID: `${crm.id}-${batch}B`,
            Sample_Type: 'STD',
            Cu_ppm: (crm.values.Cu * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Pb_ppm: (crm.values.Pb * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Zn_ppm: (crm.values.Zn * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Fe_pct: (crm.values.Fe * (1 + (Math.random() - 0.5) * tolerance)).toFixed(2),
            As_ppm: (crm.values.As * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1),
            Mn_ppm: (crm.values.Mn * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Rb_ppm: (crm.values.Rb * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Sr_ppm: (crm.values.Sr * (1 + (Math.random() - 0.5) * tolerance)).toFixed(0),
            Batch: `PXRF-BATCH-${batch.toString().padStart(2, '0')}`
        });
    }

    // Combine all data
    const combined = [...assays, ...standards, ...blanks, ...duplicates];

    return {
        combined,
        assays,
        standards,
        blanks,
        duplicates,
        metadata: {
            project: 'Demo pXRF Base Metals Project',
            campaign: '2025 pXRF Field Survey',
            elements: ['Cu', 'Pb', 'Zn', 'Fe', 'As', 'Mn', 'Rb', 'Sr'],
            category: 'pxrf'
        }
    };
}

/**
 * Generate mock Chrysos PhotonAssay dataset
 * Includes Au, Ag, Cu with error columns and high error flagging
 */
export function generateMockPhotonData(): MockQAQCDataset {
    const assays: any[] = [];
    const standards: any[] = [];
    const blanks: any[] = [];
    const duplicates: any[] = [];

    let sampleNumber = 1;

    // Generate 5 batches of samples
    for (let batch = 1; batch <= 5; batch++) {
        // Standard at start of batch (OREAS-230 or OREAS-230b)
        const crmOptions = ['OREAS-230', 'OREAS-230b', 'OREAS-231'];
        const crmId = crmOptions[Math.floor(Math.random() * 3)];
        const certifiedValues = {
            'OREAS-230': { Au: 0.329, Ag: 0.130 },
            'OREAS-230b': { Au: 0.374, Ag: 0.195 },
            'OREAS-231': { Au: 1.25, Ag: 0.45 }
        };
        const certified = certifiedValues[crmId as keyof typeof certifiedValues];

        const stdAu = certified.Au * (0.95 + Math.random() * 0.1); // ±5%
        standards.push({
            Sample_ID: `${crmId}-${batch}`,
            Sample_Type: 'Standard',
            Au_ppm: parseFloat(stdAu.toFixed(3)),
            Au_Error: parseFloat((stdAu * 0.02).toFixed(4)), // 2% error
            Ag_ppm: parseFloat((certified.Ag * (0.95 + Math.random() * 0.1)).toFixed(3)),
            Ag_Error: parseFloat((certified.Ag * 0.025).toFixed(4)),
            Cu_pct: parseFloat((0.01 + Math.random() * 0.02).toFixed(4)),
            Jar_Weight_g: 500,
            Batch: `PA-BATCH-${batch.toString().padStart(2, '0')}`
        });

        // Blank every batch
        blanks.push({
            Sample_ID: `BLANK-PA-${batch}`,
            Sample_Type: 'Blank',
            Au_ppm: parseFloat((Math.random() * 0.02).toFixed(4)), // Near detection limit (0.03 ppm)
            Au_Error: 0.001,
            Ag_ppm: parseFloat((Math.random() * 0.01).toFixed(4)),
            Ag_Error: 0.0005,
            Cu_pct: 0.0,
            Jar_Weight_g: 500,
            Batch: `PA-BATCH-${batch.toString().padStart(2, '0')}`
        });

        // 20 regular assay samples per batch
        for (let i = 1; i <= 20; i++) {
            const isDuplicate = i % 10 === 0; // Every 10th sample
            const auValue = Math.random() * 5 + 0.1; // 0.1-5.1 ppm
            const agValue = auValue * (0.3 + Math.random() * 0.4); // Ag correlates with Au
            const cuValue = Math.random() * 0.5; // 0-0.5% Cu

            // Calculate errors (2-5% typical, some high errors >10%)
            const isHighError = Math.random() < 0.05; // 5% chance of high error
            const auErrorPct = isHighError ? (0.10 + Math.random() * 0.05) : (0.02 + Math.random() * 0.03);
            const auError = auValue * auErrorPct;

            const sample = {
                Sample_ID: `PA-${String(batch).padStart(2, '0')}-${String(sampleNumber).padStart(3, '0')}`,
                Sample_Type: 'Assay',
                Au_ppm: parseFloat(auValue.toFixed(3)),
                Au_Error: parseFloat(auError.toFixed(4)),
                Ag_ppm: parseFloat(agValue.toFixed(3)),
                Ag_Error: parseFloat((agValue * 0.025).toFixed(4)),
                Cu_pct: parseFloat(cuValue.toFixed(3)),
                Jar_Weight_g: 500 + Math.random() * 50,
                Batch: `PA-BATCH-${batch.toString().padStart(2, '0')}`,
                High_Error: isHighError // Flag for high error samples
            };

            assays.push(sample);

            // Add duplicate
            if (isDuplicate) {
                const dupAu = auValue * (0.95 + Math.random() * 0.1); // ±5% variation
                duplicates.push({
                    Sample_ID: `${sample.Sample_ID}-DUP`,
                    Sample_Type: 'Duplicate',
                    Original_ID: sample.Sample_ID,
                    Au_ppm: parseFloat(dupAu.toFixed(3)),
                    Au_Error: parseFloat((dupAu * 0.025).toFixed(4)),
                    Ag_ppm: parseFloat((agValue * (0.95 + Math.random() * 0.1)).toFixed(3)),
                    Ag_Error: parseFloat((agValue * 0.03).toFixed(4)),
                    Cu_pct: parseFloat((cuValue * (0.95 + Math.random() * 0.1)).toFixed(3)),
                    Jar_Weight_g: 500,
                    Batch: `PA-BATCH-${batch.toString().padStart(2, '0')}`
                });
            }

            sampleNumber++;
        }

        // Standard at end of batch
        const stdAuEnd = certified.Au * (0.95 + Math.random() * 0.1);
        standards.push({
            Sample_ID: `${crmId}-${batch}B`,
            Sample_Type: 'Standard',
            Au_ppm: parseFloat(stdAuEnd.toFixed(3)),
            Au_Error: parseFloat((stdAuEnd * 0.02).toFixed(4)),
            Ag_ppm: parseFloat((certified.Ag * (0.95 + Math.random() * 0.1)).toFixed(3)),
            Ag_Error: parseFloat((certified.Ag * 0.025).toFixed(4)),
            Cu_pct: parseFloat((0.01 + Math.random() * 0.02).toFixed(4)),
            Jar_Weight_g: 500,
            Batch: `PA-BATCH-${batch.toString().padStart(2, '0')}`
        });
    }

    // Combine all data
    const combined = [...assays, ...standards, ...blanks, ...duplicates];

    return {
        combined,
        assays,
        standards,
        blanks,
        duplicates,
        metadata: {
            project: 'Demo PhotonAssay Project',
            campaign: '2025 Chrysos PhotonAssay Campaign',
            elements: ['Au', 'Ag', 'Cu'],
            category: 'gold'
        }
    };
}

/**
 * Generate mock Multi-Element ICP dataset
 * Includes major elements (Cu, Pb, Zn, Fe, S) and trace elements (Ni, Co, As, Mo, Ag, Au)
 */
export function generateMockMultiElementICPData(): MockQAQCDataset {
    const assays: any[] = [];
    const standards: any[] = [];
    const blanks: any[] = [];
    const duplicates: any[] = [];

    let sampleNumber = 1;

    // CRM options for multi-element (OREAS 201, 202, 203, 400 series)
    const crmOptions = [
        { 
            id: 'OREAS-201', 
            values: { 
                Cu: 0.393, Cu_unit: '%', 
                Pb: 37.2, Pb_unit: 'ppm',
                Zn: 113, Zn_unit: 'ppm',
                Fe: 4.12, Fe_unit: '%',
                S: 0.38, S_unit: '%',
                Au: 0.278, Au_unit: 'g/t',
                Ag: 1.56, Ag_unit: 'ppm',
                Ni: 45, Ni_unit: 'ppm',
                Co: 12, Co_unit: 'ppm',
                As: 8.5, As_unit: 'ppm',
                Mo: 15, Mo_unit: 'ppm'
            } 
        },
        { 
            id: 'OREAS-202', 
            values: { 
                Cu: 1.02, Cu_unit: '%',
                Pb: 22.4, Pb_unit: 'ppm',
                Zn: 67, Zn_unit: 'ppm',
                Fe: 4.5, Fe_unit: '%',
                S: 0.45, S_unit: '%',
                Au: 0.91, Au_unit: 'g/t',
                Ag: 3.21, Ag_unit: 'ppm',
                Ni: 52, Ni_unit: 'ppm',
                Co: 15, Co_unit: 'ppm',
                As: 12, As_unit: 'ppm',
                Mo: 142, Mo_unit: 'ppm'
            } 
        },
        { 
            id: 'OREAS-400', 
            values: { 
                Cu: 2.83, Cu_unit: '%',
                Pb: 1.62, Pb_unit: '%',
                Zn: 5.13, Zn_unit: '%',
                Fe: 12.4, Fe_unit: '%',
                S: 24.1, S_unit: '%',
                Au: 1.42, Au_unit: 'g/t',
                Ag: 47.2, Ag_unit: 'ppm',
                Ni: 125, Ni_unit: 'ppm',
                Co: 28, Co_unit: 'ppm',
                As: 185, As_unit: 'ppm',
                Mo: 45, Mo_unit: 'ppm'
            } 
        }
    ];

    // Generate 10 batches (~200 samples total)
    for (let batch = 1; batch <= 10; batch++) {
        // Standard at start of batch - rotate through CRMs
        const crm = crmOptions[(batch - 1) % crmOptions.length];
        
        // Different tolerances for major vs trace elements
        const majorTolerance = 0.08; // 8% for major elements
        const traceTolerance = 0.15; // 15% for trace elements

        const stdSample: any = {
            Sample_ID: `${crm.id}-${batch}`,
            Sample_Type: 'STD',
            Batch: `ICP-BATCH-${batch.toString().padStart(2, '0')}`
        };

        // Add element values with appropriate tolerances
        Object.keys(crm.values).forEach(key => {
            if (key.endsWith('_unit')) return;
            const value = crm.values[key as keyof typeof crm.values] as number;
            const unit = crm.values[`${key}_unit` as keyof typeof crm.values] as string;
            const tolerance = ['Cu', 'Pb', 'Zn', 'Fe', 'S'].includes(key) ? majorTolerance : traceTolerance;
            
            if (unit === '%') {
                stdSample[`${key}_pct`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(4);
            } else if (unit === 'g/t') {
                stdSample[`${key}_gpt`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(3);
            } else {
                stdSample[`${key}_ppm`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1);
            }
        });

        standards.push(stdSample);

        // Blank every 2 batches (5% insertion rate)
        if (batch % 2 === 0) {
            blanks.push({
                Sample_ID: `BLANK-ICP-${Math.floor(batch / 2)}`,
                Sample_Type: 'BLK',
                Cu_pct: (Math.random() * 0.0001).toFixed(4),  // Below 1 ppm DL
                Pb_ppm: (Math.random() * 0.5).toFixed(1),
                Zn_ppm: (Math.random() * 1).toFixed(1),
                Fe_pct: (Math.random() * 0.01).toFixed(2),
                S_pct: (Math.random() * 0.01).toFixed(2),
                Au_gpt: (Math.random() * 0.01).toFixed(3),
                Ag_ppm: (Math.random() * 0.1).toFixed(1),
                Ni_ppm: (Math.random() * 1).toFixed(1),
                Co_ppm: (Math.random() * 0.5).toFixed(1),
                As_ppm: (Math.random() * 2).toFixed(1),
                Mo_ppm: (Math.random() * 0.5).toFixed(1),
                Batch: `ICP-BATCH-${batch.toString().padStart(2, '0')}`
            });
        }

        // 18 regular samples per batch
        for (let i = 1; i <= 18; i++) {
            const isDuplicate = i === 9; // Duplicate in middle of batch

            // Realistic concentration ranges
            const cuValue = 0.1 + Math.random() * 4.9; // 0.1-5%
            const znValue = 0.1 + Math.random() * 9.9; // 0.1-10%
            const feValue = 2 + Math.random() * 18; // 2-20%
            const sValue = 0.5 + Math.random() * 24.5; // 0.5-25%
            const auValue = 0.1 + Math.random() * 4.9; // 0.1-5 g/t
            const agValue = 1 + Math.random() * 99; // 1-100 ppm
            const niValue = 10 + Math.random() * 490; // 10-500 ppm
            const coValue = 5 + Math.random() * 95; // 5-100 ppm
            const asValue = 10 + Math.random() * 990; // 10-1000 ppm
            const moValue = 5 + Math.random() * 195; // 5-200 ppm

            const sample: any = {
                Sample_ID: `ICP${sampleNumber.toString().padStart(4, '0')}`,
                Sample_Type: 'UNK',
                Cu_pct: cuValue.toFixed(4),
                Pb_ppm: (cuValue > 1 ? (cuValue * 1000 * 0.3) : (20 + Math.random() * 980)).toFixed(1), // Some Pb as %
                Zn_ppm: (znValue < 1 ? (znValue * 10000) : (100 + Math.random() * 9900)).toFixed(1),
                Fe_pct: feValue.toFixed(2),
                S_pct: sValue.toFixed(2),
                Au_gpt: auValue.toFixed(3),
                Ag_ppm: agValue.toFixed(1),
                Ni_ppm: niValue.toFixed(1),
                Co_ppm: coValue.toFixed(1),
                As_ppm: asValue.toFixed(1),
                Mo_ppm: moValue.toFixed(1),
                Batch: `ICP-BATCH-${batch.toString().padStart(2, '0')}`
            };

            // Fix Pb if it's major element level
            if (sample.Pb_ppm > 1000) {
                sample.Pb_pct = (parseFloat(sample.Pb_ppm) / 10000).toFixed(4);
                delete sample.Pb_ppm;
            }

            assays.push(sample);

            // Add duplicate with element-specific precision
            if (isDuplicate) {
                const dupSample: any = {
                    Sample_ID: `${sample.Sample_ID}-DUP`,
                    Sample_Type: 'DUP',
                    Batch: `ICP-BATCH-${batch.toString().padStart(2, '0')}`
                };

                // Major elements: 5-8% precision, Trace elements: 10-18% precision
                Object.keys(sample).forEach(key => {
                    if (key === 'Sample_ID' || key === 'Sample_Type' || key === 'Batch') return;
                    const value = parseFloat(sample[key]);
                    let precision;
                    
                    if (key.includes('Cu') || key.includes('Pb') || key.includes('Zn') || key.includes('Fe') || key.includes('S')) {
                        precision = 0.07; // 7% for major elements
                    } else {
                        precision = 0.15; // 15% for trace elements
                    }
                    
                    dupSample[key] = (value * (1 + (Math.random() - 0.5) * precision)).toFixed(
                        key.includes('_pct') ? 4 : key.includes('_gpt') ? 3 : 1
                    );
                });

                duplicates.push(dupSample);
            }

            sampleNumber++;
        }

        // Standard at end of batch
        const stdSampleEnd: any = {
            Sample_ID: `${crm.id}-${batch}B`,
            Sample_Type: 'STD',
            Batch: `ICP-BATCH-${batch.toString().padStart(2, '0')}`
        };

        Object.keys(crm.values).forEach(key => {
            if (key.endsWith('_unit')) return;
            const value = crm.values[key as keyof typeof crm.values] as number;
            const unit = crm.values[`${key}_unit` as keyof typeof crm.values] as string;
            const tolerance = ['Cu', 'Pb', 'Zn', 'Fe', 'S'].includes(key) ? majorTolerance : traceTolerance;
            
            if (unit === '%') {
                stdSampleEnd[`${key}_pct`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(4);
            } else if (unit === 'g/t') {
                stdSampleEnd[`${key}_gpt`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(3);
            } else {
                stdSampleEnd[`${key}_ppm`] = (value * (1 + (Math.random() - 0.5) * tolerance)).toFixed(1);
            }
        });

        standards.push(stdSampleEnd);
    }

    // Combine all data
    const combined = [...assays, ...standards, ...blanks, ...duplicates];

    return {
        combined,
        assays,
        standards,
        blanks,
        duplicates,
        metadata: {
            project: 'Demo Multi-Element ICP Project',
            campaign: '2025 ICP-MS/OES Analysis',
            elements: ['Cu', 'Pb', 'Zn', 'Fe', 'S', 'Au', 'Ag', 'Ni', 'Co', 'As', 'Mo'],
            category: 'multi'
        }
    };
}

/**
 * Get mock data by category
 */
export function getMockData(category: 'gold' | 'pxrf' | 'multi' | 'photon'): MockQAQCDataset {
    switch (category) {
        case 'gold':
            return generateMockGoldData();
        case 'pxrf':
            return generateMockPXRFData();
        case 'multi':
            return generateMockMultiElementICPData();
        case 'photon':
            return generateMockPhotonData();
        default:
            return generateMockGoldData();
    }
}
