/**
 * Sample Test Data Generator
 * 
 * Generates diverse QAQC datasets with various column formats to test:
 * - Column mapping heuristics
 * - Different element naming conventions
 * - Various unit formats
 * - Multiple file structures
 */

interface SampleData {
    [key: string]: string | number;
}

/**
 * Generate Sample Dataset 1: Standard Assay File (Most Common Format)
 * Format: Sample_ID, Sample_Type, Au_ppm, Cu_pct, Pb_ppm, Zn_ppm
 */
export function generateStandardAssayData(): SampleData[] {
    const data: SampleData[] = [];
    let sampleNum = 1;

    // Regular samples
    for (let i = 0; i < 50; i++) {
        data.push({
            Sample_ID: `RC${sampleNum.toString().padStart(4, '0')}`,
            Sample_Type: 'Sample',
            Au_ppm: (Math.random() * 5).toFixed(3),
            Cu_pct: (Math.random() * 2).toFixed(4),
            Pb_ppm: (Math.random() * 500).toFixed(1),
            Zn_ppm: (Math.random() * 1000).toFixed(1)
        });
        sampleNum++;
    }

    // Insert standards every 10 samples
    for (let i = 10; i < 50; i += 10) {
        data.splice(i, 0, {
            Sample_ID: `OREAS-101-${Math.floor(i / 10)}`,
            Sample_Type: 'Standard',
            Au_ppm: (0.082 + (Math.random() - 0.5) * 0.01).toFixed(3),
            Cu_pct: (0.015 + (Math.random() - 0.5) * 0.002).toFixed(4),
            Pb_ppm: (37.2 + (Math.random() - 0.5) * 4).toFixed(1),
            Zn_ppm: (113 + (Math.random() - 0.5) * 10).toFixed(1)
        });
    }

    // Insert blanks
    data.splice(5, 0, {
        Sample_ID: 'BLANK-001',
        Sample_Type: 'Blank',
        Au_ppm: (Math.random() * 0.005).toFixed(3),
        Cu_pct: (Math.random() * 0.001).toFixed(4),
        Pb_ppm: (Math.random() * 2).toFixed(1),
        Zn_ppm: (Math.random() * 5).toFixed(1)
    });

    // Insert duplicates
    const dup1 = data[15];
    data.splice(16, 0, {
        Sample_ID: `${dup1.Sample_ID}-DUP`,
        Sample_Type: 'Duplicate',
        Au_ppm: (parseFloat(dup1.Au_ppm as string) * (1 + (Math.random() - 0.5) * 0.1)).toFixed(3),
        Cu_pct: (parseFloat(dup1.Cu_pct as string) * (1 + (Math.random() - 0.5) * 0.1)).toFixed(4),
        Pb_ppm: (parseFloat(dup1.Pb_ppm as string) * (1 + (Math.random() - 0.5) * 0.1)).toFixed(1),
        Zn_ppm: (parseFloat(dup1.Zn_ppm as string) * (1 + (Math.random() - 0.5) * 0.1)).toFixed(1)
    });

    return data;
}

/**
 * Generate Sample Dataset 2: Alternative Column Names
 * Format: SampleNo, Type, Gold_ppm, Copper_%, Lead, Zinc
 */
export function generateAlternativeNamesData(): SampleData[] {
    const data: SampleData[] = [];

    for (let i = 1; i <= 30; i++) {
        data.push({
            SampleNo: `DD${i.toString().padStart(3, '0')}`,
            Type: i % 12 === 0 ? 'STD' : i % 15 === 0 ? 'BLK' : i % 8 === 0 ? 'DUP' : 'SAMP',
            'Gold_ppm': (Math.random() * 3).toFixed(3),
            'Copper_%': (Math.random() * 1.5).toFixed(4),
            'Lead': (Math.random() * 300).toFixed(1),
            'Zinc': (Math.random() * 800).toFixed(1)
        });
    }

    return data;
}

/**
 * Generate Sample Dataset 3: Mixed Case & Special Characters
 * Format: Sample ID (with spaces), sAmPlE tYpE, au PPM, CU_PCT, pb-ppm
 */
export function generateMixedCaseData(): SampleData[] {
    const data: SampleData[] = [];

    for (let i = 1; i <= 25; i++) {
        data.push({
            'Sample ID': `HQ-${i}`,
            'sAmPlE tYpE': ['Sample', 'Standard', 'Blank', 'Duplicate'][Math.floor(Math.random() * 4)],
            'au PPM': (Math.random() * 4).toFixed(3),
            'CU_PCT': (Math.random() * 1.8).toFixed(4),
            'pb-ppm': (Math.random() * 400).toFixed(1)
        });
    }

    return data;
}

/**
 * Generate Sample Dataset 4: pXRF Multi-Element Format
 * Format: Sample_Name, QC_Type, As_ppm, Fe_pct, Mn_ppm, Sr_ppm, Rb_ppm
 */
export function generatePXRFData(): SampleData[] {
    const data: SampleData[] = [];

    for (let i = 1; i <= 40; i++) {
        const isCRM = i % 15 === 0;
        data.push({
            Sample_Name: isCRM ? 'OREAS-100' : `PX${i.toString().padStart(4, '0')}`,
            QC_Type: isCRM ? 'CRM' : 'Sample',
            As_ppm: isCRM ? (24.6 + (Math.random() - 0.5) * 3).toFixed(1) : (Math.random() * 100).toFixed(1),
            Fe_pct: isCRM ? (3.42 + (Math.random() - 0.5) * 0.2).toFixed(2) : (Math.random() * 8).toFixed(2),
            Mn_ppm: isCRM ? (897 + (Math.random() - 0.5) * 60).toFixed(0) : (Math.random() * 2000).toFixed(0),
            Sr_ppm: (Math.random() * 500).toFixed(0),
            Rb_ppm: (Math.random() * 200).toFixed(0)
        });
    }

    return data;
}

/**
 * Generate Sample Dataset 5: Gold with g/t Units (Fire Assay)
 * Format: SAMPLE_NO, SAMPLE_TYPE, AU_GT, AU_PPB (alternative unit)
 */
export function generateGoldGTData(): SampleData[] {
    const data: SampleData[] = [];
    let batchCount = 0;

    for (let batch = 0; batch < 3; batch++) {
        for (let i = 1; i <= 15; i++) {
            const sampleType = i === 1 ? 'Standard' : i === 8 ? 'Blank' : i % 7 === 0 ? 'Duplicate' : 'Sample';
            const auGT = sampleType === 'Standard' ?
                (0.389 + (Math.random() - 0.5) * 0.04) :
                sampleType === 'Blank' ?
                    (Math.random() * 0.01) :
                    (Math.random() * 10);

            data.push({
                SAMPLE_NO: sampleType === 'Standard' ? `OREAS102-${batch + 1}` :
                    sampleType === 'Blank' ? `BLK-${batch + 1}` :
                        `FA${(batchCount * 15 + i).toString().padStart(5, '0')}`,
                SAMPLE_TYPE: sampleType,
                AU_GT: auGT.toFixed(3),
                AU_PPB: (auGT * 1000).toFixed(1)  // Alternative unit: ppb = g/t * 1000
            });
        }
        batchCount++;
    }

    return data;
}

/**
 * Generate Sample Dataset 6: Inconsistent Delimiter File
 * Some columns use underscores, some use spaces, some use nothing
 */
export function generateInconsistentDelimiterData(): SampleData[] {
    const data: SampleData[] = [];

    for (let i = 1; i <= 20; i++) {
        data.push({
            'SampleID': `MX${i}`,
            'Sample Type': ['Sample', 'Std', 'Blk'][Math.floor(Math.random() * 3)],
            'Au ppm': (Math.random() * 5).toFixed(3),
            'Cu%': (Math.random() * 2).toFixed(4),
            'Pb_ppm': (Math.random() * 400).toFixed(1),
            'Zn (ppm)': (Math.random() * 900).toFixed(1)
        });
    }

    return data;
}

/**
 * Generate Sample Dataset 7: Thompson-Howarth Format (for coarse duplicates)
 * Includes both original and duplicate in same row
 */
export function generateThompsonHowarthData(): SampleData[] {
    const data: SampleData[] = [];

    for (let i = 1; i <= 20; i++) {
        const original = Math.random() * 8;
        const duplicate = original * (1 + (Math.random() - 0.5) * 0.25); // Add variability

        data.push({
            Sample_ID: `TH${i.toString().padStart(3, '0')}`,
            Au_Original_ppm: original.toFixed(3),
            Au_Duplicate_ppm: duplicate.toFixed(3),
            Cu_Original_pct: (Math.random() * 1.5).toFixed(4),
            Cu_Duplicate_pct: (Math.random() * 1.5).toFixed(4)
        });
    }

    return data;
}

/**
 * Export all datasets as downloadable files
 */
export const SAMPLE_DATASETS = {
    'standard_assay.csv': generateStandardAssayData(),
    'alternative_names.csv': generateAlternativeNamesData(),
    'mixed_case.csv': generateMixedCaseData(),
    'pxrf_data.csv': generatePXRFData(),
    'gold_gt_units.csv': generateGoldGTData(),
    'inconsistent_delimiters.csv': generateInconsistentDelimiterData(),
    'thompson_howarth.csv': generateThompsonHowarthData()
};

/**
 * Convert data array to CSV string
 */
export function dataToCSV(data: SampleData[]): string {
    if (data.length === 0) return '';

    const headers = Object.keys(data[0]);
    const rows = data.map(row =>
        headers.map(header => {
            const value = row[header];
            // Wrap in quotes if contains comma or quote
            return typeof value === 'string' && (value.includes(',') || value.includes('"'))
                ? `"${value.replace(/"/g, '""')}"`
                : value;
        }).join(',')
    );

    return [headers.join(','), ...rows].join('\n');
}

/**
 * Download a dataset as CSV file (for browser use)
 */
export function downloadDataset(filename: string): void {
    const data = SAMPLE_DATASETS[filename as keyof typeof SAMPLE_DATASETS];
    if (!data) {
        console.error(`Dataset ${filename} not found`);
        return;
    }

    const csv = dataToCSV(data);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
}
