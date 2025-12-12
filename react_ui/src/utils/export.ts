/**
 * Export utilities for QAQC Analysis Results
 * Supports CSV, PDF, and DOCX export formats
 */

import { Document, Packer, Paragraph, Table, TableCell, TableRow, TextRun, HeadingLevel, WidthType } from 'docx';
import { saveAs } from 'file-saver';
import type { QAQCAnalysisOutput } from '../features/analysis/qaqcAnalysis';
import type { JORCReportConfig, FiguresConfig } from '../features/report/ReportConfig';

/**
 * Export figures only based on user configuration
 */
export async function exportFiguresOnly(
    results: QAQCAnalysisOutput,
    config: FiguresConfig,
    projectName: string = 'QAQC Analysis'
): Promise<void> {
    const children: (Paragraph | Table)[] = [
        new Paragraph({
            text: `${projectName} - QAQC Figures`,
            heading: HeadingLevel.HEADING_1,
            spacing: { after: 400 }
        }),
        new Paragraph({
            text: `Generated on ${new Date().toLocaleDateString()}`,
            spacing: { after: 600 }
        })
    ];

    // Add tables based on configuration
    if (config.includeTables) {
        // Standards table
        children.push(
            new Paragraph({
                text: 'Standards Statistics',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 400, after: 200 }
            })
        );

        const standardsRows = [
            new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Pass Rate', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'RSD', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
                ]
            }),
            ...results.standards.statistics.map(stat => new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph(stat.element)] }),
                    new TableCell({ children: [new Paragraph(`${stat.passRate.toFixed(1)}%`)] }),
                    new TableCell({ children: [new Paragraph(`${stat.rsd.toFixed(2)}%`)] }),
                    new TableCell({ children: [new Paragraph(String(stat.count))] })
                ]
            }))
        ];

        children.push(
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: standardsRows
            })
        );

        // Blanks table
        children.push(
            new Paragraph({
                text: 'Blanks Statistics',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 400, after: 200 }
            })
        );

        const blanksRows = [
            new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Contamination Rate', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Max Value', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
                ]
            }),
            ...results.blanks.statistics.map(stat => new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph(stat.element)] }),
                    new TableCell({ children: [new Paragraph(`${stat.contaminationRate.toFixed(1)}%`)] }),
                    new TableCell({ children: [new Paragraph(stat.max.toFixed(4))] }),
                    new TableCell({ children: [new Paragraph(String(stat.count))] })
                ]
            }))
        ];

        children.push(
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: blanksRows
            })
        );

        // Duplicates table
        children.push(
            new Paragraph({
                text: 'Duplicates Statistics',
                heading: HeadingLevel.HEADING_2,
                spacing: { before: 400, after: 200 }
            })
        );

        const duplicatesRows = [
            new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Within Target', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Mean RPD', bold: true })] })] }),
                    new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
                ]
            }),
            ...results.duplicates.statistics.map(stat => new TableRow({
                children: [
                    new TableCell({ children: [new Paragraph(stat.element)] }),
                    new TableCell({ children: [new Paragraph(`${stat.withinTarget.toFixed(1)}%`)] }),
                    new TableCell({ children: [new Paragraph(`${stat.meanRPD.toFixed(2)}%`)] }),
                    new TableCell({ children: [new Paragraph(String(stat.count))] })
                ]
            }))
        ];

        children.push(
            new Table({
                width: { size: 100, type: WidthType.PERCENTAGE },
                rows: duplicatesRows
            })
        );
    }

    // Note about plot generation
    if (config.includeControlCharts || config.includeScatterPlots || config.includeHistograms) {
        children.push(
            new Paragraph({
                text: 'Note: Plot generation will be implemented in a future update. Currently exporting statistical tables only.',
                spacing: { before: 600 }
            })
        );
    }

    // Create document
    const doc = new Document({
        sections: [{
            children
        }]
    });

    // Generate and save
    const blob = await Packer.toBlob(doc);
    saveAs(blob, `QAQC_Figures_${new Date().toISOString().split('T')[0]}.docx`);
}

/**
 * Export complete JORC-compliant report
 */
export async function exportJORCReport(
    results: QAQCAnalysisOutput,
    config: JORCReportConfig,
    projectName: string = 'QAQC Analysis'
): Promise<void> {
    const children: any[] = [];

    // Title Page with JORC metadata
    children.push(
        new Paragraph({
            text: projectName,
            heading: HeadingLevel.HEADING_1,
            spacing: { after: 200 }
        }),
        new Paragraph({
            text: 'QAQC Analysis Report',
            heading: HeadingLevel.HEADING_2,
            spacing: { after: 400 }
        }),
        new Paragraph({
            text: `Report Date: ${new Date().toLocaleDateString()}`,
            spacing: { after: 200 }
        })
    );

    // JORC Metadata Section
    children.push(
        new Paragraph({
            text: 'Report Metadata',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
        }),
        new Paragraph({ text: `Competent Person: ${config.competentPerson || 'Not specified'}` }),
        new Paragraph({ text: `Company: ${config.companyName || 'Not specified'}` }),
        new Paragraph({ text: `Laboratory: ${config.laboratory || 'Not specified'}` }),
        new Paragraph({ text: `Drilling Company: ${config.drillingCompany || 'Not specified'}` }),
        new Paragraph({
            text: `Sample Type: ${config.sampleType || 'Not specified'}`,
            spacing: { after: 400 }
        })
    );

    if (config.comments) {
        children.push(
            new Paragraph({
                text: 'Comments',
                heading: HeadingLevel.HEADING_3,
                spacing: { before: 200, after: 200 }
            }),
            new Paragraph({
                text: config.comments,
                spacing: { after: 400 }
            })
        );
    }

    // Executive Summary
    children.push(
        new Paragraph({
            text: 'Executive Summary',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
        }),
        new Paragraph({ text: `Total Samples Analyzed: ${results.summary.totalSamples}` }),
        new Paragraph({ text: `Standards: ${results.summary.totalStandards}` }),
        new Paragraph({ text: `Blanks: ${results.summary.totalBlanks}` }),
        new Paragraph({ text: `Duplicates: ${results.summary.totalDuplicates}` }),
        new Paragraph({
            text: `Overall Pass Rate: ${results.summary.overallPassRate.toFixed(1)}%`,
            spacing: { after: 400 }
        })
    );

    // Standards Section
    children.push(
        new Paragraph({
            text: 'Standards Analysis',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
        })
    );

    const standardsRows = [
        new TableRow({
            children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Pass Rate', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'RSD', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
            ]
        }),
        ...results.standards.statistics.map(stat => new TableRow({
            children: [
                new TableCell({ children: [new Paragraph(stat.element)] }),
                new TableCell({ children: [new Paragraph(`${stat.passRate.toFixed(1)}%`)] }),
                new TableCell({ children: [new Paragraph(`${stat.rsd.toFixed(2)}%`)] }),
                new TableCell({ children: [new Paragraph(String(stat.count))] })
            ]
        }))
    ];

    children.push(
        new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: standardsRows
        })
    );

    // Blanks Section
    children.push(
        new Paragraph({
            text: 'Blanks Analysis',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
        })
    );

    const blanksRows = [
        new TableRow({
            children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Contamination Rate', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Max Value', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
            ]
        }),
        ...results.blanks.statistics.map(stat => new TableRow({
            children: [
                new TableCell({ children: [new Paragraph(stat.element)] }),
                new TableCell({ children: [new Paragraph(`${stat.contaminationRate.toFixed(1)}%`)] }),
                new TableCell({ children: [new Paragraph(stat.max.toFixed(4))] }),
                new TableCell({ children: [new Paragraph(String(stat.count))] })
            ]
        }))
    ];

    children.push(
        new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: blanksRows
        })
    );

    // Duplicates Section
    children.push(
        new Paragraph({
            text: 'Duplicates Analysis',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 400, after: 200 }
        })
    );

    const duplicatesRows = [
        new TableRow({
            children: [
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Element', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Within Target', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Mean RPD', bold: true })] })] }),
                new TableCell({ children: [new Paragraph({ children: [new TextRun({ text: 'Count', bold: true })] })] })
            ]
        }),
        ...results.duplicates.statistics.map(stat => new TableRow({
            children: [
                new TableCell({ children: [new Paragraph(stat.element)] }),
                new TableCell({ children: [new Paragraph(`${stat.withinTarget.toFixed(1)}%`)] }),
                new TableCell({ children: [new Paragraph(`${stat.meanRPD.toFixed(2)}%`)] }),
                new TableCell({ children: [new Paragraph(String(stat.count))] })
            ]
        }))
    ];

    children.push(
        new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            rows: duplicatesRows
        })
    );

    // Create document
    const doc = new Document({
        sections: [{
            children
        }]
    });

    // Generate and save
    const blob = await Packer.toBlob(doc);
    saveAs(blob, `QAQC_JORC_Report_${new Date().toISOString().split('T')[0]}.docx`);
}

/**
 * Export flagged samples to CSV
 */
export function exportFlaggedSamplesToCSV(results: QAQCAnalysisOutput): void {
    const { standards, blanks, duplicates } = results;

    const rows: string[] = [];
    rows.push('Category,Sample ID,Element,Issue,Details');

    // Flagged Standards (batches)
    for (const batchId of standards.flaggedBatches) {
        rows.push(`Standards,${batchId},-,Consecutive Failures,Batch flagged for consecutive standard failures`);
    }

    // Flagged Blanks
    for (const blank of blanks.flaggedBlanks) {
        rows.push(`Blanks,${blank.sampleId},${blank.element},Contamination,${blank.measuredValue.toFixed(4)} ${blank.unit} (threshold: ${blank.contaminationThreshold.toFixed(4)})`);
    }

    // Flagged Duplicates
    for (const dup of duplicates.flaggedPairs) {
        rows.push(`Duplicates,${dup.originalSampleId},${dup.element},Poor Precision,RPD: ${dup.rpd.toFixed(2)}% HARD: ${dup.hard.toFixed(2)}%`);
    }

    const csvContent = rows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `QAQC_Flagged_Samples_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export statistics to CSV
 */
export function exportStatisticsToCSV(results: QAQCAnalysisOutput): void {
    const rows: string[] = [];

    // Standards statistics
    rows.push('STANDARDS STATISTICS');
    rows.push('Element,Mean,SD,RSD,Pass Rate,Count');
    for (const stat of results.standards.statistics) {
        rows.push(`${stat.element},${stat.mean.toFixed(4)},${stat.sd.toFixed(4)},${stat.rsd.toFixed(2)}%,${stat.passRate.toFixed(1)}%,${stat.count}`);
    }
    rows.push('');

    // Blanks statistics
    rows.push('BLANKS STATISTICS');
    rows.push('Element,Max,Mean,Median,Contamination Rate,Count');
    for (const stat of results.blanks.statistics) {
        rows.push(`${stat.element},${stat.max.toFixed(4)},${stat.mean.toFixed(4)},${stat.median.toFixed(4)},${stat.contaminationRate.toFixed(1)}%,${stat.count}`);
    }
    rows.push('');

    // Duplicates statistics
    rows.push('DUPLICATES STATISTICS');
    rows.push('Element,Mean RPD,Mean HARD,Within Target,Count');
    for (const stat of results.duplicates.statistics) {
        rows.push(`${stat.element},${stat.meanRPD.toFixed(2)}%,${stat.meanHARD.toFixed(2)}%,${stat.withinTarget.toFixed(1)}%,${stat.count}`);
    }

    const csvContent = rows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `QAQC_Statistics_${new Date().toISOString().split('T')[0]}.csv`);
}

/**
 * Export all results in multiple formats (legacy function)
 */
export async function exportAll(results: QAQCAnalysisOutput, _projectName: string = 'QAQC Analysis'): Promise<void> {
    exportFlaggedSamplesToCSV(results);
    exportStatisticsToCSV(results);
}
