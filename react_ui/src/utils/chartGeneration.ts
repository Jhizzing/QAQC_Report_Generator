// TypeScript wrapper for Python chart generation
// Provides async functions to generate charts via child_process

import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import os from 'os';

const execAsync = promisify(exec);

interface ControlChartData {
    sequence: number;
    value: number;
    batch_id: string;
}

interface ScatterPlotData {
    original: number;
    duplicate: number;
    rpd: number;
}

/**
 * Generate a control chart for standards monitoring
 */
export async function generateControlChart(params: {
    data: ControlChartData[];
    certifiedValue: number;
    element: string;
    crmName: string;
}): Promise<string> {
    const outputPath = path.join(os.tmpdir(), `control_chart_${Date.now()}.png`);
    const pythonScript = path.join(__dirname, '../python/chart_generator.py');

    const inputData = JSON.stringify({
        data: params.data,
        certified_value: params.certifiedValue,
        element: params.element,
        crm_name: params.crmName,
        output_path: outputPath
    });

    const command = `python3 "${pythonScript}" control_chart '${inputData}'`;

    try {
        const { stdout } = await execAsync(command);
        const result = JSON.parse(stdout);

        if (result.error) {
            throw new Error(`Chart generation failed: ${result.error}`);
        }

        return result.path;
    } catch (error) {
        console.error('Control chart generation error:', error);
        throw error;
    }
}

/**
 * Generate a scatter plot for duplicate analysis
 */
export async function generateScatterPlot(params: {
    data: ScatterPlotData[];
    element: string;
}): Promise<string> {
    const outputPath = path.join(os.tmpdir(), `scatter_plot_${Date.now()}.png`);
    const pythonScript = path.join(__dirname, '../python/chart_generator.py');

    const inputData = JSON.stringify({
        data: params.data,
        element: params.element,
        output_path: outputPath
    });

    const command = `python3 "${pythonScript}" scatter_plot '${inputData}'`;

    try {
        const { stdout } = await execAsync(command);
        const result = JSON.parse(stdout);

        if (result.error) {
            throw new Error(`Chart generation failed: ${result.error}`);
        }

        return result.path;
    } catch (error) {
        console.error('Scatter plot generation error:', error);
        throw error;
    }
}

/**
 * Generate a histogram for distribution analysis
 */
export async function generateHistogram(params: {
    data: number[];
    threshold: number;
    title: string;
    xlabel: string;
}): Promise<string> {
    const outputPath = path.join(os.tmpdir(), `histogram_${Date.now()}.png`);
    const pythonScript = path.join(__dirname, '../python/chart_generator.py');

    const inputData = JSON.stringify({
        data: params.data,
        threshold: params.threshold,
        title: params.title,
        xlabel: params.xlabel,
        output_path: outputPath
    });

    const command = `python3 "${pythonScript}" histogram '${inputData}'`;

    try {
        const { stdout } = await execAsync(command);
        const result = JSON.parse(stdout);

        if (result.error) {
            throw new Error(`Chart generation failed: ${result.error}`);
        }

        return result.path;
    } catch (error) {
        console.error('Histogram generation error:', error);
        throw error;
    }
}
