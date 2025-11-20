/**
 * QAQC Analysis Orchestrator
 * 
 * Coordinates all QAQC analyses (Standards, Blanks, Duplicates)
 * Processes imported data and returns combined results
 */

import type { MethodologyConfig } from '../analysis/MethodologyWizard';
import type { QAQCConfig } from '../analysis/QAQCRuleConfig';
import {
    analyzeStandards,
    extractStandardsSamples,
    type StandardsAnalysisResults
} from './standardsEngine';
import {
    analyzeBlanks,
    extractBlanksSamples,
    type BlanksAnalysisResults
} from './blanksEngine';
import {
    analyzeDuplicates,
    extractDuplicatePairs,
    type DuplicatesAnalysisResults
} from './duplicatesEngine';

export interface QAQCAnalysisInput {
    data: any[];
    methodologyConfig: MethodologyConfig;
    qaqcConfig: QAQCConfig;
    columnMapping: {
        sampleId: string;
        sampleType: string;
        elements: Record<string, string>;  // Map of element name to column name
    };
}

export interface QAQCAnalysisOutput {
    standards: StandardsAnalysisResults;
    blanks: BlanksAnalysisResults;
    duplicates: DuplicatesAnalysisResults;
    summary: {
        totalSamples: number;
        totalStandards: number;
        totalBlanks: number;
        totalDuplicates: number;
        overallPassRate: number;
    };
}

/**
 * Run complete QAQC analysis on imported data
 */
export function runQAQCAnalysis(input: QAQCAnalysisInput): QAQCAnalysisOutput {
    const { data, qaqcConfig, columnMapping } = input;

    // Extract Standards samples
    const standardsSamples = extractStandardsSamples(
        data,
        columnMapping.sampleId,
        columnMapping.sampleType,
        columnMapping.elements
    );

    // Analyze Standards
    const standardsResults = analyzeStandards(standardsSamples, {
        toleranceType: qaqcConfig.standards.toleranceType,
        toleranceValue: qaqcConfig.standards.toleranceValue,
        failureThreshold: qaqcConfig.standards.failureThreshold
    });

    // Extract Blanks samples
    const blanksSamples = extractBlanksSamples(
        data,
        columnMapping.sampleId,
        columnMapping.sampleType,
        columnMapping.elements
    );

    // Analyze Blanks
    const blanksResults = analyzeBlanks(blanksSamples, {
        detectionLimit: qaqcConfig.blanks.detectionLimit,
        detectionLimitUnit: qaqcConfig.blanks.detectionLimitUnit,
        contaminationMultiplier: qaqcConfig.blanks.contaminationMultiplier
    });

    // Extract Duplicate pairs
    const duplicatePairs = extractDuplicatePairs(
        data,
        columnMapping.sampleId,
        columnMapping.sampleType,
        columnMapping.elements
    );

    // Analyze Duplicates
    const duplicatesResults = analyzeDuplicates(duplicatePairs, {
        precisionTarget: qaqcConfig.duplicates.precisionTarget,
        precisionMethod: qaqcConfig.duplicates.precisionMethod,
        failureThreshold: qaqcConfig.duplicates.failureThreshold
    });

    // Calculate overall summary
    const totalSamples = data.length;
    const totalStandards = standardsSamples.length;
    const totalBlanks = blanksSamples.length;
    const totalDuplicates = duplicatePairs.length;

    const standardsPassRate = standardsResults.statistics.length > 0
        ? standardsResults.statistics.reduce((sum, s) => sum + s.passRate, 0) / standardsResults.statistics.length
        : 0;

    const blanksPassRate = blanksResults.statistics.length > 0
        ? 100 - (blanksResults.statistics.reduce((sum, s) => sum + s.contaminationRate, 0) / blanksResults.statistics.length)
        : 0;

    const duplicatesPassRate = duplicatesResults.statistics.length > 0
        ? duplicatesResults.statistics.reduce((sum, s) => sum + s.withinTarget, 0) / duplicatesResults.statistics.length
        : 0;

    const overallPassRate = (standardsPassRate + blanksPassRate + duplicatesPassRate) / 3;

    return {
        standards: standardsResults,
        blanks: blanksResults,
        duplicates: duplicatesResults,
        summary: {
            totalSamples,
            totalStandards,
            totalBlanks,
            totalDuplicates,
            overallPassRate
        }
    };
}

/**
 * Auto-detect column mappings from data
 * Helper function for demo data
 */
export function autoDetectColumnMapping(data: any[]): QAQCAnalysisInput['columnMapping'] {
    if (data.length === 0) {
        throw new Error('No data to analyze');
    }

    const headers = Object.keys(data[0]);

    // Detect sample ID column
    const sampleIdPatterns = /sample.*id|sample.*no|sampleid|sample_id|sample.*name/i;
    const sampleIdColumn = headers.find(h => sampleIdPatterns.test(h)) || headers[0];

    // Detect sample type column
    const sampleTypePatterns = /sample.*type|type|qc.*type/i;
    const sampleTypeColumn = headers.find(h => sampleTypePatterns.test(h)) || 'Sample_Type';

    // Detect element columns
    const elementPatterns: Record<string, RegExp> = {
        Au: /au[_-]?ppm|gold/i,
        Cu: /cu[_-]?(ppm|pct|%)|copper/i,
        Pb: /pb[_-]?ppm|lead/i,
        Zn: /zn[_-]?ppm|zinc/i,
        As: /as[_-]?ppm|arsenic/i,
        Fe: /fe[_-]?(pct|%)|iron/i
    };

    const elements: Record<string, string> = {};

    for (const [element, pattern] of Object.entries(elementPatterns)) {
        const column = headers.find(h => pattern.test(h));
        if (column) {
            elements[element] = column;
        }
    }

    return {
        sampleId: sampleIdColumn,
        sampleType: sampleTypeColumn,
        elements
    };
}
