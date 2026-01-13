/**
 * Plotly Scatter Plot
 * 
 * Duplicates analysis scatter plot with:
 * - Original vs Duplicate values
 * - 1:1 reference line
 * - Pass/Fail color coding
 * - Lasso and box selection
 * - Zoom, pan, and export
 */

import React, { useMemo, useRef, useCallback } from 'react';
import type { PlotMouseEvent, Data, PlotSelectionEvent } from 'plotly.js';
import {
  PlotlyWrapper,
  ExportButtons,
  PLOTLY_COLORS,
  getBaseLayout,
  getMarkerColors,
  getMarkerSizes,
  type PlotlyChartProps,
  type ChartSelection,
} from './PlotlyBase';

export interface ScatterDataPoint {
  pairNumber: number;
  originalSampleId: string;
  duplicateSampleId: string;
  originalValue: number;
  duplicateValue: number;
  rpd: number;
  hard?: number;
  pass: boolean;
  element?: string;
}

interface PlotlyScatterPlotProps extends PlotlyChartProps {
  data: ScatterDataPoint[];
  title?: string;
  element?: string;
  showOneToOneLine?: boolean;
  showToleranceBands?: boolean;
  tolerancePercent?: number;
}

export const PlotlyScatterPlot: React.FC<PlotlyScatterPlotProps> = ({
  data,
  title,
  element,
  showOneToOneLine = true,
  showToleranceBands = false,
  tolerancePercent = 20,
  onSelectionChange,
  onPointClick,
  selectedIndices = [],
  height = 450,
  className,
}) => {
  const plotRef = useRef<{ el: HTMLElement } | null>(null);

  // Early return if no data
  if (!data || data.length === 0) {
    return (
      <div className={`flex items-center justify-center bg-surface-dark rounded-lg border border-secondary-dark p-8 ${className || ''}`} style={{ height }}>
        <p className="text-slate-400">No duplicate pairs data available</p>
      </div>
    );
  }

  // Calculate axis range
  const axisRange = useMemo(() => {
    const allValues = data.flatMap(d => [d.originalValue, d.duplicateValue]);
    const minVal = Math.min(...allValues, 0);
    const maxVal = Math.max(...allValues);
    const padding = (maxVal - minVal) * 0.1;
    return [Math.max(0, minVal - padding), maxVal + padding];
  }, [data]);

  // Prepare trace data
  const traceData = useMemo(() => {
    const x = data.map(d => d.originalValue);
    const y = data.map(d => d.duplicateValue);
    const colors = getMarkerColors(data.map(d => d.pass), selectedIndices, PLOTLY_COLORS.highlight);
    const sizes = getMarkerSizes(data.length, selectedIndices, 10, 16);

    // Custom hover text
    const hoverText = data.map(d => 
      `<b>Pair #${d.pairNumber}</b><br>` +
      `Original: ${d.originalSampleId} (${d.originalValue.toFixed(4)})<br>` +
      `Duplicate: ${d.duplicateSampleId} (${d.duplicateValue.toFixed(4)})<br>` +
      `RPD: ${d.rpd.toFixed(2)}%<br>` +
      `Status: <b>${d.pass ? 'PASS' : 'FAIL'}</b>`
    );

    const traces: Data[] = [
      {
        type: 'scatter',
        mode: 'markers',
        x,
        y,
        name: 'Duplicate Pairs',
        marker: {
          color: colors,
          size: sizes,
          line: { 
            color: selectedIndices.length > 0 
              ? data.map((_, i) => selectedIndices.includes(i) ? '#ffffff' : PLOTLY_COLORS.paper)
              : PLOTLY_COLORS.paper, 
            width: selectedIndices.length > 0
              ? data.map((_, i) => selectedIndices.includes(i) ? 2 : 1)
              : 1
          },
          opacity: 0.85,
        },
        hovertemplate: '%{customdata}<extra></extra>',
        customdata: hoverText,
      },
    ];

    // Add 1:1 reference line
    if (showOneToOneLine) {
      traces.push({
        type: 'scatter',
        mode: 'lines',
        x: axisRange,
        y: axisRange,
        name: '1:1 Line',
        line: {
          color: PLOTLY_COLORS.primary,
          width: 2,
          dash: 'solid',
        },
        hoverinfo: 'skip',
      });
    }

    // Add tolerance bands
    if (showToleranceBands) {
      const factor = 1 + tolerancePercent / 100;
      traces.push(
        {
          type: 'scatter',
          mode: 'lines',
          x: axisRange,
          y: axisRange.map(v => v * factor),
          name: `+${tolerancePercent}%`,
          line: { color: PLOTLY_COLORS.warning, width: 1.5, dash: 'dash' },
          hoverinfo: 'skip',
        },
        {
          type: 'scatter',
          mode: 'lines',
          x: axisRange,
          y: axisRange.map(v => v / factor),
          name: `-${tolerancePercent}%`,
          line: { color: PLOTLY_COLORS.warning, width: 1.5, dash: 'dash' },
          hoverinfo: 'skip',
        }
      );
    }

    return traces;
  }, [data, selectedIndices, axisRange, showOneToOneLine, showToleranceBands, tolerancePercent]);

  // Chart title
  const chartTitle = title || (element 
    ? `Original vs Duplicate - ${element}` 
    : 'Duplicate Pairs Scatter Plot');

  // Layout
  const layout = useMemo(() => getBaseLayout({
    title: {
      text: chartTitle,
      font: { size: 16, color: PLOTLY_COLORS.text },
    },
    xaxis: {
      title: { text: 'Original Value' },
      range: axisRange,
      gridcolor: PLOTLY_COLORS.grid,
      scaleanchor: 'y',
      scaleratio: 1,
    },
    yaxis: {
      title: { text: 'Duplicate Value' },
      range: axisRange,
      gridcolor: PLOTLY_COLORS.grid,
    },
    dragmode: 'lasso',
    hovermode: 'closest',
    margin: { t: 60, r: 30, b: 60, l: 70 },
    showlegend: true,
    legend: {
      x: 0.02,
      y: 0.98,
      bgcolor: 'rgba(26, 26, 46, 0.8)',
      bordercolor: PLOTLY_COLORS.grid,
      borderwidth: 1,
    },
  }), [chartTitle, axisRange]);

  // Handle point click
  const handleClick = useCallback((event: Readonly<PlotMouseEvent>) => {
    if (!event.points.length || !onPointClick) return;
    
    const point = event.points[0];
    // Only handle clicks on data points (curveNumber 0)
    if (point.curveNumber !== 0) return;
    
    const pointIndex = point.pointIndex;
    const pointData = data[pointIndex];
    
    onPointClick(pointIndex, pointData as unknown as Record<string, unknown>);
  }, [data, onPointClick]);

  // Handle selection (box/lasso)
  const handleSelection = useCallback((event: Readonly<PlotSelectionEvent>) => {
    if (!onSelectionChange) return;
    
    // Filter to only data points (curveNumber 0)
    const dataPoints = event.points.filter((p) => p.curveNumber === 0);
    
    const selection: ChartSelection = {
      indices: dataPoints.map((p) => p.pointIndex),
      points: dataPoints.map((p) => ({
        x: (p.x ?? 0) as number,
        y: (p.y ?? 0) as number,
        pointIndex: p.pointIndex,
        curveNumber: p.curveNumber,
        data: data[p.pointIndex] as unknown as Record<string, unknown>,
      })),
    };
    
    onSelectionChange(selection);
  }, [data, onSelectionChange]);

  return (
    <div className={`space-y-3 ${className || ''}`}>
      {/* Export buttons */}
      <div className="flex justify-end">
        <ExportButtons plotRef={plotRef} filename={`scatter_${element || 'duplicates'}`} />
      </div>

      {/* Chart */}
      <PlotlyWrapper
        plotRef={plotRef}
        data={traceData}
        layout={layout}
        config={{
          modeBarButtonsToAdd: ['select2d', 'lasso2d'],
        }}
        onClick={handleClick}
        onSelected={handleSelection}
        height={height}
      />

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 text-xs text-slate-400">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-status-success" />
          <span>Within Target</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-status-error" />
          <span>Exceeds Target</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-primary" />
          <span>1:1 Line</span>
        </div>
      </div>
    </div>
  );
};

export default PlotlyScatterPlot;
