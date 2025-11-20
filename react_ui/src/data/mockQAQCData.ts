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
 * Generate mock pXRF dataset
 */
export function generateMockPXRFData(): MockQAQCDataset {
    const assays: any[] = [];
    const standards: any[] = [];
    const blanks: any[] = [];
    const duplicates: any[] = [];

    let sampleNumber = 1;

    // Generate 5 batches
    for (let batch = 1; batch <= 5; batch++) {
        // Standard (OREAS-100 for pXRF)
        standards.push({
            Sample_Name: `OREAS-100-${batch}`,
            QC_Type: 'CRM',
            Cu_ppm: (189 + (Math.random() - 0.5) * 20).toFixed(1),
            Pb_ppm: (42.3 + (Math.random() - 0.5) * 5).toFixed(1),
            Zn_ppm: (127 + (Math.random() - 0.5) * 15).toFixed(1),
            As_ppm: (24.6 + (Math.random() - 0.5) * 3).toFixed(1),
            Fe_pct: (3.42 + (Math.random() - 0.5) * 0.3).toFixed(2),
            Batch: `PXRF-${batch}`
        });

        // Blank
        if (batch % 2 === 1) {
            blanks.push({
                Sample_Name: `BLANK-PX-${batch}`,
                QC_Type: 'Blank',
                Cu_ppm: (Math.random() * 5).toFixed(1),
                Pb_ppm: (Math.random() * 3).toFixed(1),
                Zn_ppm: (Math.random() * 8).toFixed(1),
                As_ppm: (Math.random() * 2).toFixed(1),
                Fe_pct: (Math.random() * 0.1).toFixed(2),
                Batch: `PXRF-${batch}`
            });
        }

        // 15 samples per batch
        for (let i = 1; i <= 15; i++) {
            const isDuplicate = i === 8;

            const sample = {
                Sample_Name: `PX${sampleNumber.toString().padStart(4, '0')}`,
                QC_Type: 'Sample',
                Cu_ppm: (Math.random() * 500).toFixed(1),
                Pb_ppm: (Math.random() * 200).toFixed(1),
                Zn_ppm: (Math.random() * 300).toFixed(1),
                As_ppm: (Math.random() * 100).toFixed(1),
                Fe_pct: (Math.random() * 8).toFixed(2),
                Batch: `PXRF-${batch}`
            };

            assays.push(sample);

            if (isDuplicate) {
                duplicates.push({
                    Sample_Name: `${sample.Sample_Name}-DUP`,
                    QC_Type: 'Duplicate',
                    Cu_ppm: (parseFloat(sample.Cu_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Pb_ppm: (parseFloat(sample.Pb_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Zn_ppm: (parseFloat(sample.Zn_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    As_ppm: (parseFloat(sample.As_ppm) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(1),
                    Fe_pct: (parseFloat(sample.Fe_pct) * (1 + (Math.random() - 0.5) * 0.15)).toFixed(2),
                    Batch: `PXRF-${batch}`
                });
            }

            sampleNumber++;
        }
    }

    const combined = [...assays, ...standards, ...blanks, ...duplicates];

    return {
        combined,
        assays,
        standards,
        blanks,
        duplicates,
        metadata: {
            project: 'Demo pXRF Project',
            campaign: '2025 pXRF Survey',
            elements: ['Cu', 'Pb', 'Zn', 'As', 'Fe'],
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
 * Get mock data by category
 */
export function getMockData(category: 'gold' | 'pxrf' | 'multi' | 'photon'): MockQAQCDataset {
    switch (category) {
        case 'gold':
            return generateMockGoldData();
        case 'pxrf':
            return generateMockPXRFData();
        case 'photon':
            return generateMockPhotonData();
        default:
            return generateMockGoldData();
    }
}
