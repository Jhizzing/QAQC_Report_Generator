/**
 * Plotly Control Chart
 * 
 * Standards analysis control chart with:
 * - Measured values plotted over sequence
 * - Certified value reference line
 * - Upper/Lower control limits (±2SD or ±tolerance)
 * - Pass/Fail color coding
 * - Zoom, pan, and selection
 * - High-quality export
 */

import React, { useMemo, useRef, useCallback } from 'react';
import type { PlotMouseEvent, Data, Shape, Annotations, PlotSelectionEvent } from 'plotly.js';
import {
  PlotlyWrapper,
  ExportButtons,
  PLOTLY_COLORS,
  getBaseLayout,
  getStatusColors,
  getMarkerColors,
  getMarkerSizes,
  createHorizontalLine,
  createLineAnnotation,
  type PlotlyChartProps,
  type ChartSelection,
} from './PlotlyBase';

export interface ControlChartDataPoint {
  sampleNumber: number;
  sampleId: string;
  measuredValue: number;
  certifiedValue: number;
  upperLimit: number;
  lowerLimit: number;
  pass: boolean;
  zScore?: number;
  batchId?: string;
}

interface PlotlyControlChartProps extends PlotlyChartProps {
  data: ControlChartDataPoint[];
  title?: string;
  crmName?: string;
  element?: string;
  showLimits?: boolean;
}

export const PlotlyControlChart: React.FC<PlotlyControlChartProps> = ({
  data,
  title,
  crmName,
  element,
  showLimits = true,
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
        <p className="text-slate-400">No standards data available</p>
      </div>
    );
  }

  // Prepare trace data
  const traceData = useMemo(() => {
    const x = data.map(d => d.sampleNumber);
    const y = data.map(d => d.measuredValue);
    const colors = getMarkerColors(data.map(d => d.pass), selectedIndices, PLOTLY_COLORS.highlight);
    const sizes = getMarkerSizes(data.length, selectedIndices, 10, 16);

    // Custom hover text
    const hoverText = data.map(d => 
      `<b>${d.sampleId}</b><br>` +
      `Value: ${d.measuredValue.toFixed(4)}<br>` +
      `Certified: ${d.certifiedValue.toFixed(4)}<br>` +
      (d.zScore !== undefined ? `Z-Score: ${d.zScore.toFixed(2)}<br>` : '') +
      `Status: <b>${d.pass ? 'PASS' : 'FAIL'}</b>`
    );

    const mainTrace: Data = {
      type: 'scatter',
      mode: 'lines+markers',
      x,
      y,
      name: 'Measured',
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
      },
      line: {
        color: PLOTLY_COLORS.primary,
        width: 1.5,
      },
      hovertemplate: '%{customdata}<extra></extra>',
      customdata: hoverText,
    };

    return [mainTrace];
  }, [data, selectedIndices]);

  // Create reference lines and annotations
  const shapes = useMemo(() => {
    if (!data.length || !showLimits) return [];
    
    const certified = data[0].certifiedValue;
    const upper = data[0].upperLimit;
    const lower = data[0].lowerLimit;

    return [
      createHorizontalLine(certified, PLOTLY_COLORS.certified, 'solid'),
      createHorizontalLine(upper, PLOTLY_COLORS.upperLimit, 'dash'),
      createHorizontalLine(lower, PLOTLY_COLORS.lowerLimit, 'dash'),
    ];
  }, [data, showLimits]);

  const annotations = useMemo(() => {
    if (!data.length || !showLimits) return [];
    
    const certified = data[0].certifiedValue;
    const upper = data[0].upperLimit;
    const lower = data[0].lowerLimit;

    return [
      createLineAnnotation(certified, 'Certified', PLOTLY_COLORS.certified),
      createLineAnnotation(upper, '+2SD', PLOTLY_COLORS.upperLimit),
      createLineAnnotation(lower, '-2SD', PLOTLY_COLORS.lowerLimit),
    ];
  }, [data, showLimits]);

  // Chart title
  const chartTitle = title || (crmName && element 
    ? `Control Chart - ${crmName} (${element})` 
    : 'Standards Control Chart');

  // Layout with dynamic range
  const layout = useMemo(() => {
    const yValues = data.map(d => d.measuredValue);
    const minY = Math.min(...yValues, ...data.map(d => d.lowerLimit));
    const maxY = Math.max(...yValues, ...data.map(d => d.upperLimit));
    const padding = (maxY - minY) * 0.1;

    return getBaseLayout({
      title: {
        text: chartTitle,
        font: { size: 16, color: PLOTLY_COLORS.text },
      },
      xaxis: {
        title: { text: 'Sample Sequence' },
        gridcolor: PLOTLY_COLORS.grid,
      },
      yaxis: {
        title: { text: 'Measured Value' },
        range: [minY - padding, maxY + padding],
        gridcolor: PLOTLY_COLORS.grid,
      },
      shapes: shapes as Shape[],
      annotations: annotations as Annotations[],
      dragmode: 'zoom',
      selectdirection: 'h',
      margin: { t: 60, r: 80, b: 60, l: 70 },
    });
  }, [data, chartTitle, shapes, annotations]);

  // Handle point click
  const handleClick = useCallback((event: Readonly<PlotMouseEvent>) => {
    if (!event.points.length || !onPointClick) return;
    
    const point = event.points[0];
    const pointIndex = point.pointIndex;
    const pointData = data[pointIndex];
    
    onPointClick(pointIndex, pointData as unknown as Record<string, unknown>);
  }, [data, onPointClick]);

  // Handle selection (box/lasso)
  const handleSelection = useCallback((event: Readonly<PlotSelectionEvent>) => {
    if (!onSelectionChange) return;
    
    const selection: ChartSelection = {
      indices: event.points.map((p) => p.pointIndex),
      points: event.points.map((p) => ({
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
        <ExportButtons plotRef={plotRef} filename={`control_chart_${crmName || 'standards'}`} />
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
          <span>Pass</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-status-error" />
          <span>Fail</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 bg-primary" />
          <span>Certified Value</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-0.5 border-t-2 border-dashed border-amber-500" />
          <span>±2SD Limits</span>
        </div>
      </div>
    </div>
  );
};

export default PlotlyControlChart;
