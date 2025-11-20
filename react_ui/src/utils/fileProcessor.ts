import { read, utils } from 'xlsx';

export interface ProcessedData {
    fileName: string;
    headers: string[];
    data: any[];
    rowCount: number;
}

export const processFile = async (file: File): Promise<ProcessedData> => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();

        reader.onload = (e) => {
            try {
                const bstr = e.target?.result;
                const wb = read(bstr, { type: 'binary' });

                // Get first worksheet
                const wsname = wb.SheetNames[0];
                const ws = wb.Sheets[wsname];

                // Convert to JSON
                const data = utils.sheet_to_json(ws, { header: 1 });

                if (data.length === 0) {
                    reject(new Error('File is empty'));
                    return;
                }

                const headers = data[0] as string[];
                const rows = data.slice(1);

                resolve({
                    fileName: file.name,
                    headers,
                    data: rows,
                    rowCount: rows.length
                });
            } catch (error) {
                reject(error);
            }
        };

        reader.onerror = (error) => reject(error);
        reader.readAsBinaryString(file);
    });
};
