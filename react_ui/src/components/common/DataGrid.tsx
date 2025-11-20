import React, { useMemo } from 'react';
import { AgGridReact } from 'ag-grid-react';
import { ModuleRegistry, AllCommunityModule } from 'ag-grid-community';
import type { ColDef } from 'ag-grid-community';

// Register all community modules
ModuleRegistry.registerModules([AllCommunityModule]);

interface DataGridProps {
    data: any[];
    headers: string[];
    height?: string;
}

export const DataGrid: React.FC<DataGridProps> = ({ data, headers, height = '500px' }) => {
    // Dynamic column definitions
    const columnDefs = useMemo<ColDef[]>(() => {
        return headers.map(header => ({
            field: header,
            headerName: header,
            sortable: true,
            filter: true,
            resizable: true,
            minWidth: 100,
            flex: 1,
        }));
    }, [headers]);

    const defaultColDef = useMemo<ColDef>(() => ({
        sortable: true,
        filter: true,
        resizable: true,
    }), []);

    return (
        <div className="w-full" style={{ height }}>
            <AgGridReact
                rowData={data}
                columnDefs={columnDefs}
                defaultColDef={defaultColDef}
                pagination={true}
                paginationPageSize={20}
                paginationPageSizeSelector={[20, 50, 100]}
                rowSelection="multiple"
                animateRows={true}
                theme="legacy" // Using legacy theme for now, will customize later
            />
        </div>
    );
};
