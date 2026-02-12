import ExcelJS from 'exceljs';
import Papa from 'papaparse';

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

const VALID_MIME_TYPES = [
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
];

const LEGACY_XLS_MIME_TYPES = [
    'application/vnd.ms-excel',
];

const VALID_EXTENSIONS = ['.csv', '.xlsx'];

const getFileExtension = (fileName: string): string => {
    const lower = fileName.toLowerCase();
    if (lower.endsWith('.xlsx')) return '.xlsx';
    if (lower.endsWith('.xls')) return '.xls';
    if (lower.endsWith('.csv')) return '.csv';
    return '';
};

const normalizeHeaders = (headers: unknown[]): string[] => {
    return headers.map((header, index) => {
        const normalized = String(header ?? '').trim();
        return normalized.length > 0 ? normalized : `Column ${index + 1}`;
    });
};

const readFileAsText = async (file: File): Promise<string> => {
    if (typeof file.text === 'function') {
        return file.text();
    }

    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => resolve(String(event.target?.result ?? ''));
        reader.onerror = () => reject(new Error('Unable to read file as text'));
        reader.readAsText(file);
    });
};

const readFileAsArrayBuffer = async (file: File): Promise<ArrayBuffer> => {
    if (typeof file.arrayBuffer === 'function') {
        return file.arrayBuffer();
    }

    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (event) => {
            const result = event.target?.result;
            if (result instanceof ArrayBuffer) {
                resolve(result);
                return;
            }
            reject(new Error('Unable to read file as binary data'));
        };
        reader.onerror = () => reject(new Error('Unable to read file as binary data'));
        reader.readAsArrayBuffer(file);
    });
};

const normalizeCellValue = (value: ExcelJS.CellValue): unknown => {
    if (value === null || value === undefined) return '';
    if (typeof value !== 'object') return value;

    if ('result' in value && value.result !== undefined) return value.result;
    if ('text' in value && typeof value.text === 'string') return value.text;
    if ('richText' in value && Array.isArray(value.richText)) {
        return value.richText.map((part) => part.text).join('');
    }

    return String(value);
};

const parseCsvRows = async (file: File): Promise<unknown[][]> => {
    const text = await readFileAsText(file);
    if (text.trim().length === 0) {
        throw new Error('File appears to be empty or corrupted');
    }

    const parsed = Papa.parse<unknown[]>(text, {
        skipEmptyLines: false,
    });

    if (parsed.errors.length > 0) {
        throw new Error(`CSV parsing failed: ${parsed.errors[0]?.message ?? 'unknown error'}`);
    }

    return parsed.data.filter((row) => Array.isArray(row));
};

const parseXlsxRows = async (file: File): Promise<unknown[][]> => {
    const fileBuffer = await readFileAsArrayBuffer(file);
    if (fileBuffer.byteLength === 0) {
        throw new Error('File appears to be empty or corrupted');
    }

    const workbook = new ExcelJS.Workbook();
    await workbook.xlsx.load(fileBuffer);

    const worksheet = workbook.worksheets[0];
    if (!worksheet) {
        throw new Error('File does not contain any worksheets');
    }

    const rows: unknown[][] = [];
    worksheet.eachRow({ includeEmpty: false }, (row) => {
        const rowValues: unknown[] = [];
        for (let colIndex = 1; colIndex <= row.cellCount; colIndex += 1) {
            rowValues.push(normalizeCellValue(row.getCell(colIndex).value));
        }
        rows.push(rowValues);
    });

    return rows;
};

export const processFile = async (file: File): Promise<ProcessedData> => {
    if (file.size > MAX_FILE_SIZE) {
        throw new Error(
            `File size (${(file.size / 1024 / 1024).toFixed(2)}MB) exceeds maximum allowed size of 50MB. ` +
            `Please use a smaller file or split your data into multiple files.`
        );
    }

    const extension = getFileExtension(file.name);
    const hasValidExtension = VALID_EXTENSIONS.includes(extension);
    const hasValidMimeType = VALID_MIME_TYPES.includes(file.type);

    if (extension === '.xls' || LEGACY_XLS_MIME_TYPES.includes(file.type)) {
        throw new Error(
            'Legacy .xls files are no longer supported for local processing. ' +
            'Please convert to .xlsx or .csv and try again.'
        );
    }

    if (!hasValidExtension && !hasValidMimeType) {
        throw new Error(
            `Invalid file type. Expected CSV or Excel (.csv, .xlsx), ` +
            `but received: ${file.type || 'unknown type'}`
        );
    }

    try {
        const rows = extension === '.csv' ? await parseCsvRows(file) : await parseXlsxRows(file);

        if (rows.length === 0) {
            throw new Error('File is empty - no data rows found');
        }

        if (rows.length > MAX_ROWS) {
            throw new Error(
                `File contains too many rows (${rows.length}). ` +
                `Maximum allowed is ${MAX_ROWS.toLocaleString()} rows. ` +
                `Please split your data into smaller files.`
            );
        }

        const headerRow = rows[0];
        if (!Array.isArray(headerRow) || headerRow.length === 0) {
            throw new Error('File does not contain column headers');
        }

        const headers = normalizeHeaders(headerRow);
        const data = rows.slice(1);

        return {
            fileName: file.name,
            headers,
            data,
            rowCount: data.length,
        };
    } catch (error) {
        if (error instanceof Error) {
            throw new Error(`Failed to process file: ${error.message}`);
        }
        throw new Error('Failed to process file: Unknown error occurred');
    }
};
