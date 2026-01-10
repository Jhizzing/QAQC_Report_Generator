/**
 * Synchronized Data Table
 * 
 * A data table that syncs with chart selections:
 * - Highlighted rows match chart selection
 * - Click row to highlight point on chart
 * - Sortable columns
 * - Export selected rows as CSV
 */

import React, { useState, useMemo, useCallback } from 'react';
import { 
  ArrowUpDown, ArrowUp, ArrowDown, 
  Download, CheckCircle2, XCircle, 
  ChevronLeft, ChevronRight 
} from 'lucide-react';

export interface TableColumn<T> {
  key: keyof T;
  header: string;
  sortable?: boolean;
  width?: string;
  align?: 'left' | 'center' | 'right';
  render?: (value: T[keyof T], row: T, index: number) => React.ReactNode;
  format?: (value: T[keyof T]) => string;
}

interface SyncedDataTableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  selectedIndices: number[];
  onRowClick?: (index: number, row: T) => void;
  onRowHover?: (index: number | null) => void;
  pageSize?: number;
  showPagination?: boolean;
  showExport?: boolean;
  exportFilename?: string;
  emptyMessage?: string;
  className?: string;
  maxHeight?: string;
}

type SortDirection = 'asc' | 'desc' | null;

export function SyncedDataTable<T>({
  data,
  columns,
  selectedIndices,
  onRowClick,
  onRowHover,
  pageSize = 20,
  showPagination = true,
  showExport = true,
  exportFilename = 'data_export',
  emptyMessage = 'No data available',
  className = '',
  maxHeight = '400px',
}: SyncedDataTableProps<T>) {
  const [sortKey, setSortKey] = useState<keyof T | null>(null);
  const [sortDirection, setSortDirection] = useState<SortDirection>(null);
  const [currentPage, setCurrentPage] = useState(0);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortKey || !sortDirection) return data;

    return [...data].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];

      if (aVal === null || aVal === undefined) return 1;
      if (bVal === null || bVal === undefined) return -1;

      let comparison = 0;
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        comparison = aVal - bVal;
      } else {
        comparison = String(aVal).localeCompare(String(bVal));
      }

      return sortDirection === 'asc' ? comparison : -comparison;
    });
  }, [data, sortKey, sortDirection]);

  // Paginate data
  const paginatedData = useMemo(() => {
    if (!showPagination) return sortedData;
    const start = currentPage * pageSize;
    return sortedData.slice(start, start + pageSize);
  }, [sortedData, currentPage, pageSize, showPagination]);

  const totalPages = Math.ceil(data.length / pageSize);

  // Handle sort click
  const handleSort = useCallback((key: keyof T) => {
    if (sortKey === key) {
      // Cycle through: asc -> desc -> null
      if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else if (sortDirection === 'desc') {
        setSortDirection(null);
        setSortKey(null);
      }
    } else {
      setSortKey(key);
      setSortDirection('asc');
    }
  }, [sortKey, sortDirection]);

  // Get original index for a row (accounting for sorting and pagination)
  const getOriginalIndex = useCallback((displayIndex: number): number => {
    const rowData = paginatedData[displayIndex];
    return data.indexOf(rowData);
  }, [data, paginatedData]);

  // Export to CSV
  const exportCSV = useCallback(() => {
    const exportData = selectedIndices.length > 0
      ? selectedIndices.map(i => data[i])
      : data;

    const headers = columns.map(c => c.header).join(',');
    const rows = exportData.map(row => 
      columns.map(col => {
        const value = row[col.key];
        const formatted = col.format ? col.format(value) : String(value ?? '');
        // Escape quotes and wrap in quotes if contains comma
        if (formatted.includes(',') || formatted.includes('"')) {
          return `"${formatted.replace(/"/g, '""')}"`;
        }
        return formatted;
      }).join(',')
    );

    const csv = [headers, ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `${exportFilename}.csv`;
    a.click();
    
    URL.revokeObjectURL(url);
  }, [data, columns, selectedIndices, exportFilename]);

  // Render cell value
  const renderCell = (col: TableColumn<T>, row: T, index: number) => {
    const value = row[col.key];
    
    if (col.render) {
      return col.render(value, row, index);
    }
    
    if (col.format) {
      return col.format(value);
    }

    // Default rendering for common types
    if (typeof value === 'boolean') {
      return value ? (
        <CheckCircle2 className="w-4 h-4 text-status-success mx-auto" />
      ) : (
        <XCircle className="w-4 h-4 text-status-error mx-auto" />
      );
    }

    if (typeof value === 'number') {
      return value.toFixed(4);
    }

    return String(value ?? '-');
  };

  // Get sort icon
  const getSortIcon = (key: keyof T) => {
    if (sortKey !== key) {
      return <ArrowUpDown className="w-4 h-4 text-slate-500" />;
    }
    return sortDirection === 'asc' 
      ? <ArrowUp className="w-4 h-4 text-primary" />
      : <ArrowDown className="w-4 h-4 text-primary" />;
  };

  if (data.length === 0) {
    return (
      <div className={`bg-surface-dark rounded-lg border border-secondary-dark p-8 text-center ${className}`}>
        <p className="text-slate-400">{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className={`bg-surface-dark rounded-lg border border-secondary-dark overflow-hidden ${className}`}>
      {/* Header with export */}
      {showExport && (
        <div className="flex items-center justify-between px-4 py-3 border-b border-secondary-dark">
          <span className="text-sm text-slate-400">
            {selectedIndices.length > 0 
              ? `${selectedIndices.length} of ${data.length} selected`
              : `${data.length} rows`
            }
          </span>
          <button
            onClick={exportCSV}
            className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-300 bg-surface-light hover:bg-surface border border-secondary-dark rounded-lg transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            Export {selectedIndices.length > 0 ? 'Selected' : 'All'} CSV
          </button>
        </div>
      )}

      {/* Table */}
      <div className="overflow-auto" style={{ maxHeight }}>
        <table className="w-full text-sm">
          <thead className="sticky top-0 bg-surface-dark z-10">
            <tr className="border-b border-secondary-dark">
              {columns.map((col) => (
                <th
                  key={String(col.key)}
                  className={`
                    px-4 py-3 font-medium text-slate-300
                    ${col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left'}
                    ${col.sortable !== false ? 'cursor-pointer hover:bg-surface-light/50 select-none' : ''}
                  `}
                  style={{ width: col.width }}
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                >
                  <div className={`flex items-center gap-2 ${col.align === 'right' ? 'justify-end' : col.align === 'center' ? 'justify-center' : ''}`}>
                    <span>{col.header}</span>
                    {col.sortable !== false && getSortIcon(col.key)}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, displayIndex) => {
              const originalIndex = getOriginalIndex(displayIndex);
              const isSelected = selectedIndices.includes(originalIndex);

              return (
                <tr
                  key={displayIndex}
                  className={`
                    border-b border-secondary-dark/50 transition-colors cursor-pointer
                    ${isSelected 
                      ? 'bg-primary/20 hover:bg-primary/30' 
                      : 'hover:bg-surface-light/30'
                    }
                  `}
                  onClick={() => onRowClick?.(originalIndex, row)}
                  onMouseEnter={() => onRowHover?.(originalIndex)}
                  onMouseLeave={() => onRowHover?.(null)}
                >
                  {columns.map((col) => (
                    <td
                      key={String(col.key)}
                      className={`
                        px-4 py-2.5 text-slate-200
                        ${col.align === 'right' ? 'text-right' : col.align === 'center' ? 'text-center' : 'text-left'}
                      `}
                    >
                      {renderCell(col, row, originalIndex)}
                    </td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {showPagination && totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 border-t border-secondary-dark">
          <span className="text-sm text-slate-400">
            Page {currentPage + 1} of {totalPages}
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setCurrentPage(p => Math.max(0, p - 1))}
              disabled={currentPage === 0}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-surface-light disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button
              onClick={() => setCurrentPage(p => Math.min(totalPages - 1, p + 1))}
              disabled={currentPage >= totalPages - 1}
              className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-surface-light disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default SyncedDataTable;
