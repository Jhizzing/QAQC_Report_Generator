/**
 * Analysis Service
 * 
 * Unified interface for running QAQC analysis that routes to either:
 * - Server-side (FastAPI/Python) when backend is available
 * - Client-side (TypeScript) as fallback when offline
 */

import { apiClient, type AnalysisRequest, type AnalysisResult } from '../api/client';
import {
    runQAQCAnalysis as runClientAnalysis,
    autoDetectColumnMapping,
    type QAQCAnalysisInput,
    type QAQCAnalysisOutput
} from '../features/analysis/qaqcAnalysis';
import type { MethodologyConfig } from '../features/analysis/MethodologyWizard';
import type { QAQCConfig } from '../features/analysis/QAQCRuleConfig';
import { useCRMStore } from '../stores/crmStore';

export interface AnalysisServiceInput {
    /** Raw data array (for client-side analysis) */
    data: any[];
    /** File ID from upload (for server-side analysis) */
    fileId?: string;
    /** Methodology configuration */
    methodologyConfig: MethodologyConfig;
    /** QAQC rules configuration */
    qaqcConfig: QAQCConfig;
    /** Column mapping (auto-detected if not provided) */
    columnMapping?: QAQCAnalysisInput['columnMapping'];
}

export interface AnalysisServiceOutput {
    /** Analysis results in unified format */
    results: QAQCAnalysisOutput;
    /** Which mode was used */
    mode: 'server' | 'client';
    /** Analysis ID (server-side only) */
    analysisId?: string;
    /** Any warnings or info messages */
    messages: string[];
}

/**
 * Run QAQC analysis using the appropriate mode
 */
export async function runAnalysis(
    input: AnalysisServiceInput,
    useBackend: boolean
): Promise<AnalysisServiceOutput> {
    if (useBackend && input.fileId) {
        return runServerAnalysis(input);
    }
    return runLocalAnalysis(input);
}

/**
 * Run analysis on the server via FastAPI
 */
async function runServerAnalysis(input: AnalysisServiceInput): Promise<AnalysisServiceOutput> {
    const messages: string[] = [];

    try {
        // Build API request
        const columnMapping = input.columnMapping || autoDetectColumnMapping(input.data);

        const request: AnalysisRequest = {
            file_id: input.fileId!,
            column_mapping: {
                sample_id: columnMapping.sampleId,
                sample_type: columnMapping.sampleType,
                result: Object.values(columnMapping.elements)[0] || 'result',
                elements: columnMapping.elements,
            },
            methodology: {
                assay_method: input.methodologyConfig.assayMethod || 'fire_assay',
                duplicate_strategy: input.methodologyConfig.duplicateType || 'field_duplicate',
                insertion_rate: 5.0,
            },
            qaqc_rules: {
                standards_tolerance: input.qaqcConfig.standards.toleranceValue,
                blanks_threshold: input.qaqcConfig.blanks.detectionLimit,
                duplicates_rpd_limit: input.qaqcConfig.duplicates.precisionTarget,
                duplicates_hard_limit: input.qaqcConfig.duplicates.precisionTarget * 1.5,
            },
            crms: useCRMStore.getState().getAllCRMs(),
        };

        // Call API
        const apiResult = await apiClient.runAnalysis(request);

        // Map API response to UI format
        const results = mapApiResultToOutput(apiResult);

        messages.push('Analysis completed using Python backend');

        return {
            results,
            mode: 'server',
            analysisId: apiResult.analysis_id,
            messages,
        };
    } catch (error) {
        // Determine error type and provide appropriate message
        let errorMessage = 'Unknown error';
        let shouldFallback = true;

        if (error instanceof Error) {
            errorMessage = error.message;

            // Network errors - should fallback
            if (errorMessage.includes('Network error') ||
                errorMessage.includes('Failed to fetch') ||
                errorMessage.includes('timeout')) {
                messages.push(`Server unavailable: ${errorMessage}`);
                messages.push('Falling back to client-side analysis');
            }
            // 404 errors - file not found, don't fallback
            else if ((error as any).status === 404) {
                messages.push(`File not found on server: ${errorMessage}`);
                shouldFallback = false;
                throw new Error(`Server analysis failed: ${errorMessage}. Please re-upload your file.`);
            }
            // 400 errors - bad request, don't fallback
            else if ((error as any).status === 400) {
                messages.push(`Invalid request: ${errorMessage}`);
                shouldFallback = false;
                throw new Error(`Server analysis failed: ${errorMessage}. Please check your configuration.`);
            }
            // Other server errors - try fallback
            else {
                messages.push(`Server analysis error: ${errorMessage}`);
                messages.push('Falling back to client-side analysis');
            }
        } else {
            messages.push('Server analysis failed with unknown error');
            messages.push('Falling back to client-side analysis');
        }

        if (shouldFallback) {
            try {
                const fallback = await runLocalAnalysis(input);
                return {
                    ...fallback,
                    messages: [...messages, ...fallback.messages],
                };
            } catch (fallbackError) {
                throw new Error(
                    `Both server and client-side analysis failed. ` +
                    `Server error: ${errorMessage}. ` +
                    `Client error: ${fallbackError instanceof Error ? fallbackError.message : 'Unknown error'}`
                );
            }
        }

        throw error;
    }
}

/**
 * Run analysis locally using TypeScript engines
 */
async function runLocalAnalysis(input: AnalysisServiceInput): Promise<AnalysisServiceOutput> {
    const messages: string[] = [];

    try {
        const columnMapping = input.columnMapping || autoDetectColumnMapping(input.data);

        const analysisInput: QAQCAnalysisInput = {
            data: input.data,
            methodologyConfig: input.methodologyConfig,
            qaqcConfig: input.qaqcConfig,
            columnMapping,
        };

        const results = runClientAnalysis(analysisInput);

        messages.push('Analysis completed using client-side engine');

        return {
            results,
            mode: 'client',
            messages,
        };
    } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'Unknown error';

        // Provide more specific error messages
        if (errorMessage.includes('data') || errorMessage.includes('column')) {
            throw new Error(
                `Data processing failed: ${errorMessage}. ` +
                `Please check that your file contains the required columns (SampleID, Type, Result).`
            );
        }

        if (errorMessage.includes('mapping')) {
            throw new Error(
                `Column mapping failed: ${errorMessage}. ` +
                `Please verify your column mapping configuration.`
            );
        }

        throw new Error(`Client-side analysis failed: ${errorMessage}`);
    }
}

/**
 * Map API response format to UI component format
 */
function mapApiResultToOutput(apiResult: AnalysisResult): QAQCAnalysisOutput {
    return {
        standards: {
            results: apiResult.standards.data_points.map((dp, index) => ({
                sampleId: dp.crm_id || `STD-${index}`,
                crmId: dp.crm_id || 'Unknown',
                element: 'Au',
                measuredValue: dp.value,
                unit: 'ppm',
                sampleNumber: dp.sequence,
                certifiedValue: dp.certified_value || 0,
                uncertainty: 0,
                deviation: dp.certified_value ? dp.value - dp.certified_value : 0,
                percentDeviation: dp.certified_value ? ((dp.value - dp.certified_value) / dp.certified_value) * 100 : 0,
                pass: dp.status === 'PASS',
                upperLimit: 1.1, // TODO: calculate from certified value + tolerance
                lowerLimit: 0.9,
                toleranceUsed: 10, // Default tolerance for API results
            })),
            statistics: apiResult.standards.statistics.map(s => ({
                crm: s.crm || 'Unknown',
                element: s.element,
                mean: s.mean,
                sd: s.sd,
                rsd: s.rsd,
                passRate: s.pass_rate,
                count: s.count,
            })),
            flaggedBatches: apiResult.standards.flagged_batches,
        },
        blanks: {
            results: [],
            statistics: apiResult.blanks.statistics.map(s => ({
                element: s.element,
                count: s.count,
                max: s.max,
                mean: s.mean,
                median: s.median,
                contaminationRate: s.contamination_rate,
            })),
            flaggedBlanks: [],
        },
        duplicates: {
            results: apiResult.duplicates.pairs.map((p, index) => ({
                originalSampleId: p.sample_id,
                duplicateSampleId: `${p.sample_id}-DUP`,
                element: 'Au',
                originalValue: p.original,
                duplicateValue: p.duplicate,
                unit: 'ppm',
                pairNumber: index,
                rpd: p.rpd,
                hard: (Math.abs(p.original - p.duplicate) / Math.max(p.original, p.duplicate)) * 100,
                pass: p.rpd <= 20,
                targetPrecision: 20,
                precisionMethod: 'rpd' as const,
            })),
            statistics: apiResult.duplicates.statistics.map(s => ({
                element: s.element,
                count: s.count,
                meanRPD: s.mean_rpd,
                meanHARD: s.mean_hard,
                withinTarget: s.within_target,
            })),
            flaggedPairs: apiResult.duplicates.flagged_pairs.map((fp, index) => ({
                originalSampleId: fp.sample_id,
                duplicateSampleId: `${fp.sample_id}-DUP`,
                element: 'Au',
                originalValue: fp.original,
                duplicateValue: fp.duplicate,
                unit: 'ppm',
                pairNumber: index,
                rpd: fp.rpd,
                hard: (Math.abs(fp.original - fp.duplicate) / Math.max(fp.original, fp.duplicate)) * 100,
                pass: false,
                targetPrecision: 20,
                precisionMethod: 'rpd' as const,
            })),
            correlation: (apiResult.duplicates.correlation || []).map(c => ({
                element: c.element,
                coefficient: c.coefficient,
                pValue: c.pValue,
                strength: c.strength as 'strong' | 'moderate' | 'weak' | 'insufficient_data',
                meetsThreshold: c.meetsThreshold,
                statisticallySignificant: c.statisticallySignificant,
            })),
            nuggetRatio: (apiResult.duplicates.nuggetRatio || []).map(n => ({
                element: n.element,
                ratio: n.ratio,
                nugget: n.nugget,
                sill: n.sill,
                interpretation: n.interpretation as 'low' | 'moderate' | 'high' | 'insufficient_data',
                meetsThreshold: n.meetsThreshold,
            })),
        },
        summary: {
            totalSamples: apiResult.summary.total_samples,
            totalStandards: apiResult.summary.total_standards,
            totalBlanks: apiResult.summary.total_blanks,
            totalDuplicates: apiResult.summary.total_duplicates,
            overallPassRate: apiResult.summary.overall_pass_rate,
        },
    };
}

/**
 * Upload a file to the server for analysis
 */
export async function uploadFileForAnalysis(file: File): Promise<{
    fileId: string;
    columns: string[];
    rowCount: number;
    mappingSuggestions: Record<string, { column: string; confidence: number }>;
}> {
    const response = await apiClient.uploadFile(file);

    return {
        fileId: response.file_id,
        columns: response.columns,
        rowCount: response.row_count,
        mappingSuggestions: response.mapping_suggestions,
    };
}

/**
 * Export analysis results
 */
export async function exportResults(
    analysisId: string,
    format: 'excel' | 'pdf'
): Promise<void> {
    if (!analysisId) {
        throw new Error('Analysis ID is required for export');
    }

    try {
        const blob = format === 'excel'
            ? await apiClient.exportExcel(analysisId)
            : await apiClient.exportPDF(analysisId);

        if (!blob || blob.size === 0) {
            throw new Error(`Export generated an empty file. Please try again or contact support.`);
        }

        const filename = `qaqc_report_${new Date().toISOString().slice(0, 10)}.${format === 'excel' ? 'xlsx' : 'pdf'}`;
        apiClient.downloadBlob(blob, filename);
    } catch (error) {
        if (error instanceof Error) {
            if (error.message.includes('timeout')) {
                throw new Error(
                    `Export timeout: Report generation took too long. ` +
                    `This may happen with very large datasets. Please try again or contact support.`
                );
            }
            if (error.message.includes('Network error') || error.message.includes('Failed to fetch')) {
                throw new Error(
                    `Network error during export: Unable to connect to server. ` +
                    `Please check your connection and try again.`
                );
            }
            if ((error as any).status === 404) {
                throw new Error(
                    `Analysis not found: The analysis results may have expired. ` +
                    `Please run the analysis again.`
                );
            }
        }

        throw new Error(`Export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
}
