/**
 * Analysis Engine for QAQC Standards Module
 * 
 * Analyzes CRM (Certified Reference Material) results against certified values
 * Flags outliers and consecutive failures
 */

import { getCertifiedValue } from '../../data/crmDatabase';

export interface StandardSample {
    sampleId: string;
    crmId: string;  // e.g., 'OREAS-101'
    element: string;
    measuredValue: number;
    unit: string;
    sampleNumber: number;  // Sequence number for plotting
    batchId?: string;
}

export interface StandardResult extends StandardSample {
    certifiedValue: number;
    uncertainty?: number;
    deviation: number;  // Measured - Certified
    percentDeviation: number;  // (Measured - Certified) / Certified * 100
    pass: boolean;
    upperLimit: number;
    lowerLimit: number;
}

export interface StandardsAnalysisConfig {
    toleranceType: 'percentage' | 'absolute' | 'sd';
    toleranceValue: number;
    failureThreshold: number;  // Consecutive failures to flag batch
}

export interface StandardsAnalysisResults {
    results: StandardResult[];
    flaggedBatches: string[];
    statistics: {
        crm: string;
        element: string;
        mean: number;
        sd: number;
        rsd: number;  // Relative Standard Deviation (%)
        passRate: number;  // % of samples passing
        count: number;
    }[];
}

/**
 * Analyze standards data against certified values
  */
export function analyzeStandards(
    samples: StandardSample[],
    config: StandardsAnalysisConfig
): StandardsAnalysisResults {
    const results: StandardResult[] = [];

    // Process each sample
    for (const sample of samples) {
        const certifiedData = getCertifiedValue(sample.crmId, sample.element);

        if (!certifiedData) {
            console.warn(`No certified value found for ${sample.crmId} - ${sample.element}`);
            continue;
        }

        const certifiedValue = certifiedData.value;
        const uncertainty = certifiedData.uncertainty;

        // Calculate limits based on tolerance type
        let upperLimit: number;
        let lowerLimit: number;

        switch (config.toleranceType) {
            case 'percentage':
                const tolerance = certifiedValue * (config.toleranceValue / 100);
                upperLimit = certifiedValue + tolerance;
                lowerLimit = certifiedValue - tolerance;
                break;

            case 'absolute':
                upperLimit = certifiedValue + config.toleranceValue;
                lowerLimit = certifiedValue - config.toleranceValue;
                break;

            case 'sd':
                if (!uncertainty) {
                    // Fall back to percentage if no uncertainty available
                    const fallbackTolerance = certifiedValue * 0.1; // 10%
                    upperLimit = certifiedValue + fallbackTolerance;
                    lowerLimit = certifiedValue - fallbackTolerance;
                } else {
                    upperLimit = certifiedValue + (uncertainty * config.toleranceValue);
                    lowerLimit = certifiedValue - (uncertainty * config.toleranceValue);
                }
                break;

            default:
                upperLimit = certifiedValue * 1.1;
                lowerLimit = certifiedValue * 0.9;
        }

        const deviation = sample.measuredValue - certifiedValue;
        const percentDeviation = (deviation / certifiedValue) * 100;
        const pass = sample.measuredValue >= lowerLimit && sample.measuredValue <= upperLimit;

        results.push({
            ...sample,
            certifiedValue,
            uncertainty,
            deviation,
            percentDeviation,
            pass,
            upperLimit,
            lowerLimit
        });
    }

    // Calculate statistics for each CRM/element combination
    const statistics = calculateStandardsStatistics(results);

    // Flag batches with consecutive failures
    const flaggedBatches = findConsecutiveFailures(results, config.failureThreshold);

    return {
        results,
        flaggedBatches,
        statistics
    };
}

/**
 * Calculate statistics for each CRM/element combination
 */
function calculateStandardsStatistics(results: StandardResult[]): StandardsAnalysisResults['statistics'] {
    const groups = new Map<string, StandardResult[]>();

    // Group by CRM + element
    for (const result of results) {
        const key = `${result.crmId}|${result.element}`;
        if (!groups.has(key)) {
            groups.set(key, []);
        }
        groups.get(key)!.push(result);
    }

    const statistics: StandardsAnalysisResults['statistics'] = [];

    for (const [key, groupResults] of groups) {
        const [crm, element] = key.split('|');
        const values = groupResults.map(r => r.measuredValue);
        const mean = values.reduce((sum, v) => sum + v, 0) / values.length;
        const variance = values.reduce((sum, v) => sum + Math.pow(v - mean, 2), 0) / values.length;
        const sd = Math.sqrt(variance);
        const rsd = (sd / mean) * 100;
        const passCount = groupResults.filter(r => r.pass).length;
        const passRate = (passCount / groupResults.length) * 100;

        statistics.push({
            crm,
            element,
            mean,
            sd,
            rsd,
            passRate,
            count: groupResults.length
        });
    }

    return statistics;
}

/**
 * Find batches with consecutive failures
 */
function findConsecutiveFailures(results: StandardResult[], threshold: number): string[] {
    const flaggedBatches = new Set<string>();
    let consecutiveFailures = 0;
    let currentBatch: string | undefined;

    // Sort by sample number to check sequence
    const sorted = [...results].sort((a, b) => a.sampleNumber - b.sampleNumber);

    for (const result of sorted) {
        if (!result.pass) {
            consecutiveFailures++;
            if (result.batchId) {
                currentBatch = result.batchId;
            }

            if (consecutiveFailures >= threshold && currentBatch) {
                flaggedBatches.add(currentBatch);
            }
        } else {
            consecutiveFailures = 0;
            currentBatch = undefined;
        }
    }

    return Array.from(flaggedBatches);
}

/**
 * Helper: Extract standards from imported data
 */
export function extractStandardsSamples(
    data: any[],
    sampleIdColumn: string,
    sampleTypeColumn: string,
    elementColumns: Record<string, string>  // Map of element name to column name
): StandardSample[] {
    const samples: StandardSample[] = [];
    let sampleNumber = 0;

    for (const row of data) {
        const sampleType = row[sampleTypeColumn];

        // Check if this is a standard/CRM
        if (!sampleType || !['STD', 'Standard', 'CRM', 'QC'].some(type =>
            sampleType.toString().toUpperCase().includes(type.toUpperCase())
        )) {
            continue;
        }

        sampleNumber++;
        const sampleId = row[sampleIdColumn];

        // Try to identify CRM ID from sample name
        const crmId = extractCRMId(sampleId);
        if (!crmId) {
            console.warn(`Could not extract CRM ID from sample: ${sampleId}`);
            continue;
        }

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
                crmId,
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
 * Extract CRM ID from sample name (e.g., "OREAS-101" from "OREAS-101-01")
 */
function extractCRMId(sampleName: string): string | null {
    // Common CRM patterns
    const patterns = [
        /OREAS[-_]?\d+/i,
        /CDN[-_]?GS[-_]?\d+[A-Z]?/i,
        /GEOSTATS[-_]?[A-Z]+\d+[-_]?\d*/i,
        /NIST[-_]?\d+[A-Z]?/i,
        /USGS[-_]?[A-Z][-_]?\d+/i
    ];

    for (const pattern of patterns) {
        const match = sampleName.match(pattern);
        if (match) {
            return match[0].toUpperCase().replace('_', '-');
        }
    }

    return null;
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
