import { read, utils } from 'xlsx';

export interface ProcessedData {
    fileName: string;
    headers: string[];
    data: any[];
    rowCount: number;
}

// Maximum file size: 50MB
const MAX_FILE_SIZE = 50 * 1024 * 1024;

// Maximum rows to process in memory (to prevent memory issues)
const MAX_ROWS = 100000;

export const processFile = async (file: File): Promise<ProcessedData> => {
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        throw new Error(
            `File size (${(file.size / 1024 / 1024).toFixed(2)}MB) exceeds maximum allowed size of 50MB. ` +
            `Please use a smaller file or split your data into multiple files.`
        );
    }

    // Validate file type
    const validTypes = [
        'text/csv',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ];
    const validExtensions = ['.csv', '.xlsx', '.xls'];
    const hasValidType = validTypes.includes(file.type);
    const hasValidExtension = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!hasValidType && !hasValidExtension) {
        throw new Error(
            `Invalid file type. Expected CSV or Excel file (.csv, .xlsx, .xls), ` +
            `but received: ${file.type || 'unknown type'}`
        );
    }

    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        // Set timeout for file reading (30 seconds)
        const timeout = setTimeout(() => {
            reader.abort();
            reject(new Error('File reading timeout. The file may be corrupted or too large.'));
        }, 30000);

        reader.onload = (e) => {
            clearTimeout(timeout);
            try {
                const bstr = e.target?.result;
                
                if (!bstr || (typeof bstr === 'string' && bstr.length === 0)) {
                    reject(new Error('File appears to be empty or corrupted'));
                    return;
                }

                const wb = read(bstr, { type: 'binary' });

                if (!wb.SheetNames || wb.SheetNames.length === 0) {
                    reject(new Error('File does not contain any worksheets'));
                    return;
                }

                // Get first worksheet
                const wsname = wb.SheetNames[0];
                const ws = wb.Sheets[wsname];

                if (!ws) {
                    reject(new Error('Unable to read worksheet data'));
                    return;
                }

                // Convert to JSON
                const data = utils.sheet_to_json(ws, { header: 1 });

                if (data.length === 0) {
                    reject(new Error('File is empty - no data rows found'));
                    return;
                }

                // Check row count
                if (data.length > MAX_ROWS) {
                    reject(new Error(
                        `File contains too many rows (${data.length}). ` +
                        `Maximum allowed is ${MAX_ROWS.toLocaleString()} rows. ` +
                        `Please split your data into smaller files.`
                    ));
                    return;
                }

                const headers = data[0] as string[];
                
                if (!headers || headers.length === 0) {
                    reject(new Error('File does not contain column headers'));
                    return;
                }

                const rows = data.slice(1);

                resolve({
                    fileName: file.name,
                    headers,
                    data: rows,
                    rowCount: rows.length
                });
            } catch (error) {
                if (error instanceof Error) {
                    reject(new Error(`Failed to process file: ${error.message}`));
                } else {
                    reject(new Error('Failed to process file: Unknown error occurred'));
                }
            }
        };

        reader.onerror = (error) => {
            clearTimeout(timeout);
            reject(new Error(`File read error: ${error.type || 'Unknown error'}`));
        };

        try {
            reader.readAsBinaryString(file);
        } catch (error) {
            clearTimeout(timeout);
            reject(new Error(`Failed to read file: ${error instanceof Error ? error.message : 'Unknown error'}`));
        }
    });
};
