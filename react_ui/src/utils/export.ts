/**
 * Export utilities for QAQC Analysis Results
 * Supports CSV, PDF, and DOCX export formats
 */

import { jsPDF } from 'jspdf';
import { Document, Packer, Paragraph, Table, TableCell, TableRow, TextRun, HeadingLevel, WidthType } from 'docx';
import { saveAs } from 'file-saver';
import type { QAQCAnalysisOutput } from '../features/analysis/qaqcAnalysis';

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
 * Export complete report to PDF
 */
export function exportToPDF(results: QAQCAnalysisOutput, projectName: string = 'QAQC Analysis'): void {
    const doc = new jsPDF();
    let yPos = 20;

    // Title
    doc.setFontSize(20);
    doc.text(projectName, 20, yPos);
    yPos += 10;

    doc.setFontSize(12);
    doc.text(`QAQC Analysis Report - ${new Date().toLocaleDateString()}`, 20, yPos);
    yPos += 15;

    // Summary Section
    doc.setFontSize(16);
    doc.text('Summary', 20, yPos);
    yPos += 10;

    doc.setFontSize(10);
    doc.text(`Total Samples: ${results.summary.totalSamples}`, 30, yPos);
    yPos += 6;
    doc.text(`Standards: ${results.summary.totalStandards}`, 30, yPos);
    yPos += 6;
    doc.text(`Blanks: ${results.summary.totalBlanks}`, 30, yPos);
    yPos += 6;
    doc.text(`Duplicates: ${results.summary.totalDuplicates}`, 30, yPos);
    yPos += 6;
    doc.text(`Overall Pass Rate: ${results.summary.overallPassRate.toFixed(1)}%`, 30, yPos);
    yPos += 15;

    // Standards Section
    doc.setFontSize(14);
    doc.text('Standards Analysis', 20, yPos);
    yPos += 8;

    doc.setFontSize(10);
    for (const stat of results.standards.statistics) {
        if (yPos > 270) {
            doc.addPage();
            yPos = 20;
        }
        doc.text(`${stat.element}: Pass Rate ${stat.passRate.toFixed(1)}%, RSD ${stat.rsd.toFixed(2)}%, Count ${stat.count}`, 30, yPos);
        yPos += 6;
    }

    if (results.standards.flaggedBatches.length > 0) {
        yPos += 5;
        doc.setFontSize(12);
        doc.text('Flagged Batches:', 30, yPos);
        yPos += 6;
        doc.setFontSize(10);
        for (const batchId of results.standards.flaggedBatches) {
            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
            doc.text(`- ${batchId}: Consecutive failures detected`, 40, yPos);
            yPos += 6;
        }
    }
    yPos += 10;

    // Blanks Section
    if (yPos > 250) {
        doc.addPage();
        yPos = 20;
    }

    doc.setFontSize(14);
    doc.text('Blanks Analysis', 20, yPos);
    yPos += 8;

    doc.setFontSize(10);
    for (const stat of results.blanks.statistics) {
        if (yPos > 270) {
            doc.addPage();
            yPos = 20;
        }
        doc.text(`${stat.element}: Contamination Rate ${stat.contaminationRate.toFixed(1)}%, Max ${stat.max.toFixed(4)}, Count ${stat.count}`, 30, yPos);
        yPos += 6;
    }

    if (results.blanks.flaggedBlanks.length > 0) {
        yPos += 5;
        doc.setFontSize(12);
        doc.text(`Contaminated Blanks (${results.blanks.flaggedBlanks.length}):`, 30, yPos);
        yPos += 6;
        doc.setFontSize(10);
        for (const blank of results.blanks.flaggedBlanks.slice(0, 10)) {
            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
            doc.text(`- ${blank.sampleId}: ${blank.measuredValue.toFixed(4)} ${blank.unit}`, 40, yPos);
            yPos += 6;
        }
    }
    yPos += 10;

    // Duplicates Section
    if (yPos > 250) {
        doc.addPage();
        yPos = 20;
    }

    doc.setFontSize(14);
    doc.text('Duplicates Analysis', 20, yPos);
    yPos += 8;

    doc.setFontSize(10);
    for (const stat of results.duplicates.statistics) {
        if (yPos > 270) {
            doc.addPage();
            yPos = 20;
        }
        doc.text(`${stat.element}: Within Target ${stat.withinTarget.toFixed(1)}%, Mean RPD ${stat.meanRPD.toFixed(2)}%, Count ${stat.count}`, 30, yPos);
        yPos += 6;
    }

    if (results.duplicates.flaggedPairs.length > 0) {
        yPos += 5;
        doc.setFontSize(12);
        doc.text(`Poor Precision Pairs (${results.duplicates.flaggedPairs.length}):`, 30, yPos);
        yPos += 6;
        doc.setFontSize(10);
        for (const dup of results.duplicates.flaggedPairs.slice(0, 10)) {
            if (yPos > 270) {
                doc.addPage();
                yPos = 20;
            }
            doc.text(`- ${dup.originalSampleId}: RPD ${dup.rpd.toFixed(2)}%, HARD ${dup.hard.toFixed(2)}%`, 40, yPos);
            yPos += 6;
        }
    }

    // Save PDF
    doc.save(`QAQC_Report_${new Date().toISOString().split('T')[0]}.pdf`);
}

/**
 * Export complete report to DOCX
 */
export async function exportToDOCX(results: QAQCAnalysisOutput, projectName: string = 'QAQC Analysis'): Promise<void> {
    const children: any[] = [];

    // Title
    children.push(
        new Paragraph({
            text: projectName,
            heading: HeadingLevel.HEADING_1,
            spacing: { after: 200 }
        })
    );

    children.push(
        new Paragraph({
            text: `QAQC Analysis Report - ${new Date().toLocaleDateString()}`,
            spacing: { after: 400 }
        })
    );

    // Summary Section
    children.push(
        new Paragraph({
            text: 'Summary',
            heading: HeadingLevel.HEADING_2,
            spacing: { before: 200, after: 200 }
        })
    );

    children.push(
        new Paragraph({ text: `Total Samples: ${results.summary.totalSamples}` }),
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
            spacing: { before: 200, after: 200 }
        })
    );

    // Standards table
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
    saveAs(blob, `QAQC_Report_${new Date().toISOString().split('T')[0]}.docx`);
}

/**
 * Export all results in multiple formats
 */
export async function exportAll(results: QAQCAnalysisOutput, projectName: string = 'QAQC Analysis'): Promise<void> {
    exportFlaggedSamplesToCSV(results);
    exportStatisticsToCSV(results);
    exportToPDF(results, projectName);
    await exportToDOCX(results, projectName);
}
