/**
 * Plotly Histogram
 * 
 * Distribution chart for:
 * - Blank values (contamination analysis)
 * - RPD/HARD values (precision distribution)
 * - Any numeric distribution with threshold
 * 
 * Features:
 * - Threshold reference line
 * - Color coding for values exceeding threshold
 * - Zoom, pan, and export
 */

import React, { useMemo, useRef, useCallback } from 'react';
import type { PlotMouseEvent, Data, Shape, Annotations } from 'plotly.js';
import {
  PlotlyWrapper,
  ExportButtons,
  PLOTLY_COLORS,
  getBaseLayout,
  type PlotlyChartProps,
} from './PlotlyBase';

export interface HistogramDataPoint {
  index: number;
  value: number;
  sampleId?: string;
  pass?: boolean;
}

interface PlotlyHistogramProps extends PlotlyChartProps {
  data: HistogramDataPoint[];
  title?: string;
  xAxisLabel?: string;
  yAxisLabel?: string;
  threshold?: number;
  thresholdLabel?: string;
  binCount?: number;
  showKDE?: boolean;
  colorByThreshold?: boolean;
}

export const PlotlyHistogram: React.FC<PlotlyHistogramProps> = ({
  data,
  title = 'Distribution',
  xAxisLabel = 'Value',
  yAxisLabel = 'Count',
  threshold,
  thresholdLabel = 'Threshold',
  binCount = 20,
  colorByThreshold = true,
  onPointClick,
  height = 400,
  className,
}) => {
  const plotRef = useRef<{ el: HTMLElement } | null>(null);

  // Early return if no data
  if (!data || data.length === 0) {
    return (
      <div className={`flex items-center justify-center bg-surface-dark rounded-lg border border-secondary-dark p-8 ${className || ''}`} style={{ height }}>
        <p className="text-slate-400">No data available for histogram</p>
      </div>
    );
  }

  // Split data by threshold if color coding enabled
  const traceData = useMemo(() => {
    const traces: Data[] = [];
    const values = data.map(d => d.value);

    if (colorByThreshold && threshold !== undefined) {
      const passingValues = data.filter(d => d.value <= threshold).map(d => d.value);
      const failingValues = data.filter(d => d.value > threshold).map(d => d.value);

      if (passingValues.length > 0) {
        traces.push({
          type: 'histogram',
          x: passingValues,
          name: 'Within Limit',
          marker: {
            color: PLOTLY_COLORS.pass,
            line: { color: PLOTLY_COLORS.paper, width: 1 },
          },
          opacity: 0.8,
          autobinx: false,
          xbins: { size: Math.max((Math.max(...values) - Math.min(...values)) / binCount, 0.001) },
          hovertemplate: 'Value: %{x}<br>Count: %{y}<extra></extra>',
        } as Data);
      }

      if (failingValues.length > 0) {
        traces.push({
          type: 'histogram',
          x: failingValues,
          name: 'Exceeds Limit',
          marker: {
            color: PLOTLY_COLORS.fail,
            line: { color: PLOTLY_COLORS.paper, width: 1 },
          },
          opacity: 0.8,
          autobinx: false,
          xbins: { size: Math.max((Math.max(...values) - Math.min(...values)) / binCount, 0.001) },
          hovertemplate: 'Value: %{x}<br>Count: %{y}<extra></extra>',
        } as Data);
      }
    } else {
      // Single color histogram
      traces.push({
        type: 'histogram',
        x: values,
        name: 'Distribution',
        marker: {
          color: PLOTLY_COLORS.primary,
          line: { color: PLOTLY_COLORS.paper, width: 1 },
        },
        opacity: 0.8,
        autobinx: false,
        xbins: { size: (Math.max(...values) - Math.min(...values)) / binCount },
        hovertemplate: 'Value: %{x}<br>Count: %{y}<extra></extra>',
      } as Data);
    }

    return traces;
  }, [data, threshold, colorByThreshold, binCount]);

  // Create threshold line shape
  const shapes = useMemo(() => {
    if (threshold === undefined) return [];

    return [{
      type: 'line' as const,
      xref: 'x' as const,
      x0: threshold,
      x1: threshold,
      yref: 'paper' as const,
      y0: 0,
      y1: 1,
      line: {
        color: PLOTLY_COLORS.warning,
        width: 2,
        dash: 'dash' as const,
      },
    }];
  }, [threshold]);

  // Create threshold annotation
  const annotations = useMemo(() => {
    if (threshold === undefined) return [];

    return [{
      x: threshold,
      y: 1.05,
      xref: 'x' as const,
      yref: 'paper' as const,
      text: `${thresholdLabel}: ${threshold}`,
      showarrow: false,
      font: { color: PLOTLY_COLORS.warning, size: 11 },
      xanchor: 'left' as const,
    }];
  }, [threshold, thresholdLabel]);

  // Layout
  const layout = useMemo(() => getBaseLayout({
    title: {
      text: title,
      font: { size: 16, color: PLOTLY_COLORS.text },
    },
    xaxis: {
      title: { text: xAxisLabel },
      gridcolor: PLOTLY_COLORS.grid,
    },
    yaxis: {
      title: { text: yAxisLabel },
      gridcolor: PLOTLY_COLORS.grid,
    },
    barmode: 'stack',
    bargap: 0.05,
    shapes: shapes as Shape[],
    annotations: annotations as Annotations[],
    hovermode: 'x unified',
    margin: { t: 60, r: 30, b: 60, l: 60 },
    showlegend: colorByThreshold && threshold !== undefined,
    legend: {
      x: 0.98,
      y: 0.98,
      xanchor: 'right',
      bgcolor: 'rgba(26, 26, 46, 0.8)',
      bordercolor: PLOTLY_COLORS.grid,
      borderwidth: 1,
    },
  }), [title, xAxisLabel, yAxisLabel, shapes, annotations, colorByThreshold, threshold]);

  // Handle click (returns bin info)
  const handleClick = useCallback((event: Readonly<PlotMouseEvent>) => {
    if (!event.points.length || !onPointClick) return;
    
    const point = event.points[0];
    onPointClick(point.pointIndex, { 
      binStart: point.x,
      count: point.y,
    });
  }, [onPointClick]);

  // Calculate summary statistics
  const stats = useMemo(() => {
    const values = data.map(d => d.value);
    const n = values.length;
    if (n === 0) return null;

    const mean = values.reduce((a, b) => a + b, 0) / n;
    const sorted = [...values].sort((a, b) => a - b);
    const median = n % 2 === 0 
      ? (sorted[n/2 - 1] + sorted[n/2]) / 2 
      : sorted[Math.floor(n/2)];
    const max = Math.max(...values);
    const min = Math.min(...values);
    
    const exceedsThreshold = threshold !== undefined 
      ? values.filter(v => v > threshold).length 
      : 0;

    return { n, mean, median, max, min, exceedsThreshold };
  }, [data, threshold]);

  return (
    <div className={`space-y-3 ${className || ''}`}>
      {/* Export buttons */}
      <div className="flex justify-end">
        <ExportButtons plotRef={plotRef} filename={`histogram_${title.toLowerCase().replace(/\s+/g, '_')}`} />
      </div>

      {/* Chart */}
      <PlotlyWrapper
        plotRef={plotRef}
        data={traceData}
        layout={layout}
        onClick={handleClick}
        height={height}
      />

      {/* Statistics summary */}
      {stats && (
        <div className="flex items-center justify-center gap-6 text-xs text-slate-400 bg-surface-dark/50 rounded-lg py-2 px-4">
          <span>n = <b className="text-slate-200">{stats.n}</b></span>
          <span>Mean = <b className="text-slate-200">{stats.mean.toFixed(4)}</b></span>
          <span>Median = <b className="text-slate-200">{stats.median.toFixed(4)}</b></span>
          <span>Range = <b className="text-slate-200">{stats.min.toFixed(4)} – {stats.max.toFixed(4)}</b></span>
          {threshold !== undefined && (
            <span>
              Exceeds Limit = <b className={stats.exceedsThreshold > 0 ? 'text-status-error' : 'text-status-success'}>
                {stats.exceedsThreshold} ({((stats.exceedsThreshold / stats.n) * 100).toFixed(1)}%)
              </b>
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default PlotlyHistogram;
