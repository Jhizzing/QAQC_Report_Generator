/**
 * Plotly Base Configuration
 * 
 * Shared configuration, theme, types, and utilities for all Plotly charts.
 * Provides consistent dark theme styling and export functionality.
 */

import React, { Suspense, useCallback } from 'react';
import type { Layout, Config, PlotMouseEvent, Data, Shape, Annotations, PlotSelectionEvent } from 'plotly.js';
import { Download, Image, FileCode } from 'lucide-react';

// Lazy load Plotly to reduce initial bundle size
const Plot = React.lazy(() => import('react-plotly.js'));

// ============== Theme Colors ==============

export const PLOTLY_COLORS = {
  // Background colors
  paper: '#1a1a2e',
  plot: '#16162a',
  
  // Text colors
  text: '#e2e8f0',
  textMuted: '#94a3b8',
  
  // Grid and lines
  grid: '#2d2d4a',
  axis: '#475569',
  
  // Accent colors
  primary: '#4a90d9',
  primaryLight: '#6ba3e0',
  success: '#22c55e',
  warning: '#f59e0b',
  danger: '#ef4444',
  
  // Chart-specific colors
  pass: '#22c55e',
  fail: '#ef4444',
  neutral: '#64748b',
  highlight: '#fbbf24', // Bright yellow/amber for selected points
  
  // Reference lines
  certified: '#4a90d9',
  upperLimit: '#f59e0b',
  lowerLimit: '#f59e0b',
  target: '#a855f7',
};

// ============== Base Layout ==============

export const getBaseLayout = (overrides: Partial<Layout> = {}): Partial<Layout> => ({
  paper_bgcolor: PLOTLY_COLORS.paper,
  plot_bgcolor: PLOTLY_COLORS.plot,
  font: {
    family: 'Inter, system-ui, sans-serif',
    color: PLOTLY_COLORS.text,
    size: 12,
  },
  margin: { t: 50, r: 30, b: 60, l: 60 },
  xaxis: {
    gridcolor: PLOTLY_COLORS.grid,
    linecolor: PLOTLY_COLORS.axis,
    zerolinecolor: PLOTLY_COLORS.grid,
    tickfont: { color: PLOTLY_COLORS.textMuted },
    title: { font: { color: PLOTLY_COLORS.text } },
  },
  yaxis: {
    gridcolor: PLOTLY_COLORS.grid,
    linecolor: PLOTLY_COLORS.axis,
    zerolinecolor: PLOTLY_COLORS.grid,
    tickfont: { color: PLOTLY_COLORS.textMuted },
    title: { font: { color: PLOTLY_COLORS.text } },
  },
  hoverlabel: {
    bgcolor: '#1e293b',
    bordercolor: '#475569',
    font: { color: PLOTLY_COLORS.text, size: 12 },
  },
  legend: {
    font: { color: PLOTLY_COLORS.text },
    bgcolor: 'rgba(0,0,0,0)',
  },
  ...overrides,
});

// ============== Base Config ==============

export const getBaseConfig = (overrides: Partial<Config> = {}): Partial<Config> => ({
  responsive: true,
  displaylogo: false,
  modeBarButtonsToRemove: [
    'sendDataToCloud',
    'autoScale2d',
    'hoverClosestCartesian',
    'hoverCompareCartesian',
    'toggleSpikelines',
  ],
  modeBarButtonsToAdd: [],
  toImageButtonOptions: {
    format: 'png',
    filename: 'qaqc_chart',
    height: 800,
    width: 1200,
    scale: 2, // 2x for high DPI
  },
  ...overrides,
});

// ============== Types ==============

export interface ChartSelection {
  indices: number[];
  points: Array<{
    x: number | string;
    y: number;
    pointIndex: number;
    curveNumber: number;
    data: Record<string, unknown>;
  }>;
}

export interface PlotlyChartProps {
  onSelectionChange?: (selection: ChartSelection) => void;
  onPointClick?: (pointIndex: number, data: Record<string, unknown>) => void;
  selectedIndices?: number[];
  height?: number | string;
  className?: string;
}

// ============== Loading Fallback ==============

export const ChartLoadingFallback: React.FC<{ height?: number | string }> = ({ height = 400 }) => (
  <div 
    className="flex items-center justify-center bg-surface-dark rounded-lg border border-secondary-dark animate-pulse"
    style={{ height }}
  >
    <div className="text-center">
      <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-3" />
      <p className="text-slate-400 text-sm">Loading chart...</p>
    </div>
  </div>
);

// ============== Export Buttons Component ==============

interface ExportButtonsProps {
  plotRef: React.RefObject<{ el: HTMLElement } | null>;
  filename?: string;
}

export const ExportButtons: React.FC<ExportButtonsProps> = ({ plotRef, filename = 'chart' }) => {
  const exportChart = useCallback(async (format: 'png' | 'svg' | 'jpeg') => {
    if (!plotRef.current?.el) return;
    
    const Plotly = await import('plotly.js');
    const graphDiv = plotRef.current.el;
    
    const options = {
      format,
      filename,
      height: 800,
      width: 1200,
      scale: format === 'svg' ? 1 : 2,
    };
    
    await Plotly.downloadImage(graphDiv, options);
  }, [plotRef, filename]);

  return (
    <div className="flex items-center gap-2">
      <button
        onClick={() => exportChart('png')}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-light hover:bg-surface border border-secondary-dark rounded-lg transition-colors"
        title="Export as PNG (300 DPI)"
      >
        <Image className="w-3.5 h-3.5" />
        PNG
      </button>
      <button
        onClick={() => exportChart('svg')}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-light hover:bg-surface border border-secondary-dark rounded-lg transition-colors"
        title="Export as SVG (Vector)"
      >
        <FileCode className="w-3.5 h-3.5" />
        SVG
      </button>
      <button
        onClick={() => exportChart('jpeg')}
        className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-light hover:bg-surface border border-secondary-dark rounded-lg transition-colors"
        title="Export as JPEG"
      >
        <Download className="w-3.5 h-3.5" />
        JPEG
      </button>
    </div>
  );
};

// ============== Chart Wrapper ==============

interface PlotlyWrapperProps {
  data: Data[];
  layout: Partial<Layout>;
  config?: Partial<Config>;
  onSelected?: (event: Readonly<PlotSelectionEvent>) => void;
  onClick?: (event: Readonly<PlotMouseEvent>) => void;
  onHover?: (event: Readonly<PlotMouseEvent>) => void;
  height?: number | string;
  className?: string;
  plotRef?: React.MutableRefObject<unknown>;
}

export const PlotlyWrapper: React.FC<PlotlyWrapperProps> = ({
  data,
  layout,
  config,
  onSelected,
  onClick,
  onHover,
  height = 400,
  className = '',
  plotRef,
}) => {
  const mergedLayout = getBaseLayout({
    ...layout,
    height: typeof height === 'number' ? height : undefined,
  });
  
  const mergedConfig = getBaseConfig(config);

  return (
    <Suspense fallback={<ChartLoadingFallback height={height} />}>
      <div className={`rounded-lg overflow-hidden ${className}`} style={{ height }}>
        <Plot
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          ref={plotRef as any}
          data={data}
          layout={mergedLayout}
          config={mergedConfig}
          onSelected={onSelected}
          onClick={onClick}
          onHover={onHover}
          useResizeHandler
          style={{ width: '100%', height: '100%' }}
        />
      </div>
    </Suspense>
  );
};

// ============== Utility Functions ==============

/**
 * Generate marker colors based on pass/fail status
 */
export const getStatusColors = (passArray: boolean[]): string[] => {
  return passArray.map(pass => pass ? PLOTLY_COLORS.pass : PLOTLY_COLORS.fail);
};

/**
 * Generate marker colors with highlights for selected points
 * Selected points get a bright highlight color (yellow/cyan) while maintaining pass/fail indication
 */
export const getMarkerColors = (
  passArray: boolean[],
  selectedIndices: number[] = [],
  highlightColor: string = '#fbbf24' // Bright yellow/amber for selection
): string[] => {
  const baseColors = getStatusColors(passArray);
  return baseColors.map((color, i) => 
    selectedIndices.includes(i) ? highlightColor : color
  );
};

/**
 * Generate marker sizes with highlights for selected points
 */
export const getMarkerSizes = (
  dataLength: number, 
  selectedIndices: number[] = [], 
  baseSize = 8, 
  selectedSize = 12
): number[] => {
  return Array.from({ length: dataLength }, (_, i) => 
    selectedIndices.includes(i) ? selectedSize : baseSize
  );
};

/**
 * Create a horizontal reference line shape
 */
export const createHorizontalLine = (
  y: number, 
  color: string, 
  dash: 'solid' | 'dash' | 'dot' = 'solid',
  _label?: string
): Partial<Shape> => ({
  type: 'line',
  xref: 'paper',
  x0: 0,
  x1: 1,
  yref: 'y',
  y0: y,
  y1: y,
  line: { color, width: 2, dash },
});

/**
 * Create annotation for reference lines
 */
export const createLineAnnotation = (
  y: number,
  text: string,
  color: string
): Partial<Annotations> => ({
  xref: 'paper',
  x: 1.02,
  yref: 'y',
  y,
  text,
  showarrow: false,
  font: { color, size: 10 },
  xanchor: 'left',
});

export default PlotlyWrapper;
