/**
 * Analysis Engine for QAQC Duplicates Module
 * 
 * Analyzes duplicate pairs to assess precision
 * Calculates RPD (Relative Percent Difference) and HARD (Half Absolute Relative Difference)
 */

import { getDefaultPrecisionTarget, type AnalyticalMethod } from '../../data/elementDefaults';

export interface DuplicatePair {
    originalSampleId: string;
    duplicateSampleId: string;
    element: string;
    originalValue: number;
    duplicateValue: number;
    unit: string;
    pairNumber: number;  // Sequence number for plotting
    batchId?: string;
}

export interface DuplicateResult extends DuplicatePair {
    rpd: number;  // Relative Percent Difference
    hard: number;  // Half Absolute Relative Difference
    pass: boolean;
    targetPrecision: number;  // The precision target actually used for this element
    precisionMethod: 'rpd' | 'hard';
}

export interface DuplicatesAnalysisConfig {
    precisionTarget: number;      // Default precision target (e.g., 20%)
    elementSpecificPrecision?: Record<string, number>;  // Element-specific precision overrides
    analyticalMethod?: AnalyticalMethod;  // Method for determining defaults
    precisionMethod: 'rpd' | 'hard';
    failureThreshold: number;  // Consecutive failures to review
}

export interface DuplicatesAnalysisResults {
    results: DuplicateResult[];
    flaggedPairs: DuplicateResult[];
    statistics: {
        element: string;
        meanRPD: number;
        meanHARD: number;
        withinTarget: number;  // % of pairs within target precision
        count: number;
    }[];
}

/**
 * Analyze duplicate pairs for precision
 */
export function analyzeDuplicates(
    pairs: DuplicatePair[],
    config: DuplicatesAnalysisConfig
): DuplicatesAnalysisResults {
    const results: DuplicateResult[] = [];

    // Process each pair
    for (const pair of pairs) {
        const { originalValue, duplicateValue, element } = pair;

        // Calculate RPD: |A - B| / ((A + B) / 2) × 100
        const average = (originalValue + duplicateValue) / 2;
        const rpd = average !== 0 ? (Math.abs(originalValue - duplicateValue) / average) * 100 : 0;

        // Calculate HARD: |A - B| / MAX(A, B) × 100
        const max = Math.max(originalValue, duplicateValue);
        const hard = max !== 0 ? (Math.abs(originalValue - duplicateValue) / max) * 100 : 0;

        // Get element-specific precision target if available, otherwise use default
        let precisionTarget = config.precisionTarget;
        if (config.elementSpecificPrecision && config.elementSpecificPrecision[element]) {
            precisionTarget = config.elementSpecificPrecision[element];
        } else if (config.analyticalMethod) {
            // Use element-specific default based on method
            precisionTarget = getDefaultPrecisionTarget(element, config.analyticalMethod, config.precisionMethod);
        }

        // Determine if within target
        const precision = config.precisionMethod === 'rpd' ? rpd : hard;
        const pass = precision <= precisionTarget;

        results.push({
            ...pair,
            rpd,
            hard,
            pass,
            targetPrecision: precisionTarget,
            precisionMethod: config.precisionMethod
        });
    }

    // Calculate statistics for each element
    const statistics = calculateDuplicatesStatistics(results);

    // Flag poor precision pairs
    const flaggedPairs = results.filter(r => !r.pass);

    return {
        results,
        flaggedPairs,
        statistics
    };
}

/**
 * Calculate statistics for each element
 */
function calculateDuplicatesStatistics(results: DuplicateResult[]): DuplicatesAnalysisResults['statistics'] {
    const groups = new Map<string, DuplicateResult[]>();

    // Group by element
    for (const result of results) {
        if (!groups.has(result.element)) {
            groups.set(result.element, []);
        }
        groups.get(result.element)!.push(result);
    }

    const statistics: DuplicatesAnalysisResults['statistics'] = [];

    for (const [element, groupResults] of groups) {
        const rpdValues = groupResults.map(r => r.rpd);
        const hardValues = groupResults.map(r => r.hard);
        const meanRPD = rpdValues.reduce((sum, v) => sum + v, 0) / rpdValues.length;
        const meanHARD = hardValues.reduce((sum, v) => sum + v, 0) / hardValues.length;
        const passCount = groupResults.filter(r => r.pass).length;
        const withinTarget = (passCount / groupResults.length) * 100;

        statistics.push({
            element,
            meanRPD,
            meanHARD,
            withinTarget,
            count: groupResults.length
        });
    }

    return statistics;
}

/**
 * Helper: Extract duplicate pairs from imported data
 */
export function extractDuplicatePairs(
    data: any[],
    sampleIdColumn: string,
    sampleTypeColumn: string,
    elementColumns: Record<string, string>  // Map of element name to column name
): DuplicatePair[] {
    const pairs: DuplicatePair[] = [];
    let pairNumber = 0;

    // Find duplicates (samples that have "-DUP", "DUP", or similar suffix)
    const duplicateSamples = data.filter(row => {
        const sampleType = row[sampleTypeColumn];
        const sampleId = row[sampleIdColumn];
        return sampleType && (
            ['DUP', 'Duplicate', 'DUPLICATE'].some(type =>
                sampleType.toString().toUpperCase().includes(type.toUpperCase())
            ) ||
            sampleId && sampleId.toString().toUpperCase().includes('DUP')
        );
    });

    // Match each duplicate with its original
    for (const dupRow of duplicateSamples) {
        const dupSampleId = dupRow[sampleIdColumn];

        // Try to find original sample (remove -DUP suffix or similar)
        const originalId = dupSampleId.toString().replace(/[-_]?DUP[-_]?\d*/i, '');
        const originalRow = data.find(row => row[sampleIdColumn] === originalId);

        if (!originalRow) {
            console.warn(`Could not find original for duplicate: ${dupSampleId}`);
            continue;
        }

        pairNumber++;

        // Extract values for each element
        for (const [element, columnName] of Object.entries(elementColumns)) {
            const originalValue = parseFloat(originalRow[columnName]);
            const duplicateValue = parseFloat(dupRow[columnName]);

            if (isNaN(originalValue) || isNaN(duplicateValue)) {
                continue;
            }

            // Determine unit from column name
            const unit = extractUnit(columnName, element);

            pairs.push({
                originalSampleId: originalId,
                duplicateSampleId: dupSampleId,
                element,
                originalValue,
                duplicateValue,
                unit,
                pairNumber
            });
        }
    }

    return pairs;
}

/**
 * Extract unit from column name
 */
function extractUnit(columnName: string, element: string): string {
    const lower = columnName.toLowerCase();

    if (lower.includes('ppm')) return 'ppm';
    if (lower.includes('ppb')) return 'ppb';
    if (lower.includes('%') || lower.includes('pct')) return '%';
    if (lower.includes('g/t') || lower.includes('gt')) return 'g/t';

    // Default units by element
    if (element === 'Au') return 'g/t';
    if (['Cu', 'Fe', 'S'].includes(element)) return '%';
    return 'ppm';
}

/**
 * Generate histogram bins for RPD/HARD values
 */
export function generatePrecisionHistogram(values: number[], binCount: number = 10): { bin: string; count: number; range: [number, number] }[] {
    if (values.length === 0) return [];

    const min = 0; // Precision starts at 0%
    const max = Math.max(...values, 50); // Cap at reasonable max or highest value
    const binWidth = (max - min) / binCount;

    const bins: { bin: string; count: number; range: [number, number] }[] = [];

    for (let i = 0; i < binCount; i++) {
        const binStart = min + (i * binWidth);
        const binEnd = binStart + binWidth;
        const count = values.filter(v => v >= binStart && (i === binCount - 1 ? v <= binEnd : v < binEnd)).length;

        bins.push({
            bin: `${binStart.toFixed(1)}-${binEnd.toFixed(1)}%`,
            count,
            range: [binStart, binEnd]
        });
    }

    return bins;
}
