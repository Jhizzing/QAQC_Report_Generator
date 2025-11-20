/**
 * Analysis Engine for QAQC Blanks Module
 * 
 * Analyzes blank samples to detect contamination
 * Flags blanks exceeding detection limits and contamination thresholds
 */

export interface BlankSample {
    sampleId: string;
    element: string;
    measuredValue: number;
    unit: string;
    sampleNumber: number;  // Sequence number for plotting
    batchId?: string;
}

export interface BlankResult extends BlankSample {
    detectionLimit: number;
    contaminationThreshold: number;
    pass: boolean;
    contaminated: boolean;
    status: 'pass' | 'warning' | 'fail';  // pass=below DL, warning=above DL but below contamination, fail=contaminated
}

export interface BlanksAnalysisConfig {
    detectionLimit: number;
    detectionLimitUnit: 'ppm' | 'ppb' | 'pct';
    contaminationMultiplier: number;  // e.g., 3x detection limit
}

export interface BlanksAnalysisResults {
    results: BlankResult[];
    flaggedBlanks: BlankResult[];
    statistics: {
        element: string;
        max: number;
        mean: number;
        median: number;
        contaminationRate: number;  // % of blanks exceeding contamination threshold
        count: number;
    }[];
}

/**
 * Analyze blanks data for contamination
 */
export function analyzeBlanks(
    samples: BlankSample[],
    config: BlanksAnalysisConfig
): BlanksAnalysisResults {
    const results: BlankResult[] = [];

    // Calculate contamination threshold
    const contaminationThreshold = config.detectionLimit * config.contaminationMultiplier;

    // Process each sample
    for (const sample of samples) {
        const measuredValue = sample.measuredValue;
        const detectionLimit = config.detectionLimit;

        // Determine status
        let status: 'pass' | 'warning' | 'fail';
        let pass: boolean;
        let contaminated: boolean;

        if (measuredValue <= detectionLimit) {
            status = 'pass';
            pass = true;
            contaminated = false;
        } else if (measuredValue <= contaminationThreshold) {
            status = 'warning';
            pass = false;
            contaminated = false;
        } else {
            status = 'fail';
            pass = false;
            contaminated = true;
        }

        results.push({
            ...sample,
            detectionLimit,
            contaminationThreshold,
            pass,
            contaminated,
            status
        });
    }

    // Calculate statistics for each element
    const statistics = calculateBlanksStatistics(results);

    // Flag contaminated blanks
    const flaggedBlanks = results.filter(r => r.contaminated);

    return {
        results,
        flaggedBlanks,
        statistics
    };
}

/**
 * Calculate statistics for each element
 */
function calculateBlanksStatistics(results: BlankResult[]): BlanksAnalysisResults['statistics'] {
    const groups = new Map<string, BlankResult[]>();

    // Group by element
    for (const result of results) {
        if (!groups.has(result.element)) {
            groups.set(result.element, []);
        }
        groups.get(result.element)!.push(result);
    }

    const statistics: BlanksAnalysisResults['statistics'] = [];

    for (const [element, groupResults] of groups) {
        const values = groupResults.map(r => r.measuredValue).sort((a, b) => a - b);
        const max = Math.max(...values);
        const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
        const median = values[Math.floor(values.length / 2)];
        const contaminatedCount = groupResults.filter(r => r.contaminated).length;
        const contaminationRate = (contaminatedCount / groupResults.length) * 100;

        statistics.push({
            element,
            max,
            mean,
            median,
            contaminationRate,
            count: groupResults.length
        });
    }

    return statistics;
}

/**
 * Helper: Extract blanks from imported data
 */
export function extractBlanksSamples(
    data: any[],
    sampleIdColumn: string,
    sampleTypeColumn: string,
    elementColumns: Record<string, string>  // Map of element name to column name
): BlankSample[] {
    const samples: BlankSample[] = [];
    let sampleNumber = 0;

    for (const row of data) {
        const sampleType = row[sampleTypeColumn];

        // Check if this is a blank
        if (!sampleType || !['BLK', 'Blank', 'BLANK', 'Field Blank', 'Method Blank'].some(type =>
            sampleType.toString().toUpperCase().includes(type.toUpperCase())
        )) {
            continue;
        }

        sampleNumber++;
        const sampleId = row[sampleIdColumn];

        // Extract measured values for each element
        for (const [element, columnName] of Object.entries(elementColumns)) {
            const measuredValue = parseFloat(row[columnName]);

            if (isNaN(measuredValue)) {
                continue;
            }

            // Determine unit from column name or defaults
            const unit = extractUnit(columnName, element);

            samples.push({
                sampleId,
                element,
                measuredValue,
                unit,
                sampleNumber
            });
        }
    }

    return samples;
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
 * Generate histogram bins for blank values
 */
export function generateBlankHistogram(values: number[], binCount: number = 10): { bin: string; count: number; range: [number, number] }[] {
    if (values.length === 0) return [];

    const min = Math.min(...values);
    const max = Math.max(...values);
    const binWidth = (max - min) / binCount;

    const bins: { bin: string; count: number; range: [number, number] }[] = [];

    for (let i = 0; i < binCount; i++) {
        const binStart = min + (i * binWidth);
        const binEnd = binStart + binWidth;
        const count = values.filter(v => v >= binStart && (i === binCount - 1 ? v <= binEnd : v < binEnd)).length;

        bins.push({
            bin: `${binStart.toFixed(3)}-${binEnd.toFixed(3)}`,
            count,
            range: [binStart, binEnd]
        });
    }

    return bins;
}
