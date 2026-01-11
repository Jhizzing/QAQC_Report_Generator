import { describe, it, expect, vi, beforeEach } from 'vitest';
import { exportFiguresOnly, exportJORCReport } from '../export';
import type { QAQCAnalysisOutput } from '../../features/analysis/qaqcAnalysis';
import type { FiguresConfig, JORCReportConfig } from '../../features/report/ReportConfig';
import { saveAs } from 'file-saver';

// Mock file-saver
vi.mock('file-saver', () => ({
    saveAs: vi.fn(),
}));

describe('export', () => {
    const mockResults: QAQCAnalysisOutput = {
        summary: {
            totalSamples: 100,
            totalStandards: 10,
            totalBlanks: 20,
            totalDuplicates: 15,
            overallPassRate: 95.5,
        },
        standards: {
            statistics: [
                {
                    element: 'Au',
                    passRate: 95.5,
                    rsd: 2.3,
                    count: 10,
                },
            ],
            results: [],
            flaggedBatches: [],
        },
        blanks: {
            statistics: [
                {
                    element: 'Au',
                    contaminationRate: 5.0,
                    max: 0.05,
                    count: 20,
                },
            ],
            results: [],
            flaggedBlanks: [],
        },
        duplicates: {
            statistics: [
                {
                    element: 'Au',
                    meanRPD: 8.5,
                    meanHARD: 6.2,
                    withinTarget: 90.0,
                    count: 15,
                },
            ],
            results: [],
            flaggedPairs: [],
        },
    };

    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('exportFiguresOnly', () => {
        it('should export figures with all options enabled', async () => {
            const config: FiguresConfig = {
                includeControlCharts: true,
                includeScatterPlots: true,
                includeHistograms: true,
                includeTables: true,
            };

            await exportFiguresOnly(mockResults, config, 'Test Project');

            // Verify saveAs was called
            expect(saveAs).toHaveBeenCalled();
        });

        it('should export figures with tables only', async () => {
            const config: FiguresConfig = {
                includeControlCharts: false,
                includeScatterPlots: false,
                includeHistograms: false,
                includeTables: true,
            };

            await exportFiguresOnly(mockResults, config);

            expect(saveAs).toHaveBeenCalled();
        });

        it('should handle empty results', async () => {
            const emptyResults: QAQCAnalysisOutput = {
                summary: {
                    totalSamples: 0,
                    totalStandards: 0,
                    totalBlanks: 0,
                    totalDuplicates: 0,
                    overallPassRate: 0,
                },
                standards: { statistics: [], results: [], flaggedBatches: [] },
                blanks: { statistics: [], results: [], flaggedBlanks: [] },
                duplicates: { statistics: [], results: [], flaggedPairs: [] },
            };

            const config: FiguresConfig = {
                includeControlCharts: true,
                includeScatterPlots: true,
                includeHistograms: true,
                includeTables: true,
            };

            await exportFiguresOnly(emptyResults, config);

            expect(saveAs).toHaveBeenCalled();
        });
    });

    describe('exportJORCReport', () => {
        it('should export a JORC report with all fields', async () => {
            const config: JORCReportConfig = {
                competentPerson: 'John Doe',
                companyName: 'Mining Corp',
                laboratory: 'ALS Geochemistry',
                drillingCompany: 'Drill Co',
                sampleType: 'RC Chips',
                comments: 'Test comments',
            };

            await exportJORCReport(mockResults, config, 'Test Project');

            expect(saveAs).toHaveBeenCalled();
        });

        it('should export a JORC report with minimal fields', async () => {
            const config: JORCReportConfig = {
                competentPerson: '',
                companyName: '',
                laboratory: '',
                drillingCompany: '',
                sampleType: '',
                comments: '',
            };

            await exportJORCReport(mockResults, config);

            expect(saveAs).toHaveBeenCalled();
        });

        it('should handle empty results in JORC report', async () => {
            const emptyResults: QAQCAnalysisOutput = {
                summary: {
                    totalSamples: 0,
                    totalStandards: 0,
                    totalBlanks: 0,
                    totalDuplicates: 0,
                    overallPassRate: 0,
                },
                standards: { statistics: [], results: [], flaggedBatches: [] },
                blanks: { statistics: [], results: [], flaggedBlanks: [] },
                duplicates: { statistics: [], results: [], flaggedPairs: [] },
            };

            const config: JORCReportConfig = {
                competentPerson: 'John Doe',
                companyName: 'Mining Corp',
                laboratory: 'ALS',
                drillingCompany: 'Drill Co',
                sampleType: 'RC',
                comments: '',
            };

            await exportJORCReport(emptyResults, config);

            expect(saveAs).toHaveBeenCalled();
        });
    });
});
