/**
 * QAQC API Client
 * 
 * Client for communicating with the FastAPI backend.
 * Provides typed methods for all API endpoints.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ColumnMapping {
    sample_id: string;
    sample_type: string;
    result: string;
    batch_id?: string;
    elements?: Record<string, string>;
}

export interface MethodologyConfig {
    assay_method: string;
    duplicate_strategy: string;
    insertion_rate: number;
}

export interface QAQCRulesConfig {
    standards_tolerance: number;
    blanks_threshold: number;
    duplicates_rpd_limit: number;
    duplicates_hard_limit: number;
}

export interface AnalysisRequest {
    file_id: string;
    column_mapping: ColumnMapping;
    methodology: MethodologyConfig;
    qaqc_rules: QAQCRulesConfig;
}

export interface UploadResponse {
    file_id: string;
    filename: string;
    row_count: number;
    columns: string[];
    mapping_suggestions: Record<string, { column: string; confidence: number }>;
}

export interface PreviewResponse {
    file_id: string;
    total_rows: number;
    offset: number;
    limit: number;
    columns: string[];
    data: Record<string, any>[];
}

export interface AnalysisResult {
    analysis_id: string;
    file_id: string;
    timestamp: string;
    summary: {
        total_samples: number;
        total_standards: number;
        total_blanks: number;
        total_duplicates: number;
        overall_pass_rate: number;
    };
    standards: {
        statistics: Array<{
            element: string;
            mean: number;
            sd: number;
            rsd: number;
            pass_rate: number;
            count: number;
        }>;
        data_points: Array<{
            sequence: number;
            value: number;
            status: string;
        }>;
        flagged_batches: string[];
    };
    blanks: {
        statistics: Array<{
            element: string;
            max: number;
            mean: number;
            median: number;
            contamination_rate: number;
            count: number;
        }>;
        flagged_blanks: any[];
    };
    duplicates: {
        statistics: Array<{
            element: string;
            mean_rpd: number;
            mean_hard: number;
            within_target: number;
            count: number;
        }>;
        pairs: Array<{
            sample_id: string;
            original: number;
            duplicate: number;
            rpd: number;
        }>;
        flagged_pairs: any[];
    };
}

class QAQCApiClient {
    private baseUrl: string;

    constructor(baseUrl: string = API_BASE_URL) {
        this.baseUrl = baseUrl;
    }

    private async request<T>(
        endpoint: string,
        options: RequestInit = {}
    ): Promise<T> {
        const url = `${this.baseUrl}${endpoint}`;
        
        const response = await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(error.detail || `HTTP ${response.status}`);
        }

        return response.json();
    }

    // ============== Health ==============

    async healthCheck(): Promise<{ status: string; timestamp: string }> {
        return this.request('/health');
    }

    // ============== Projects ==============

    async createProject(name: string, deposit: string, commodity: string = 'Gold') {
        return this.request('/api/projects', {
            method: 'POST',
            body: JSON.stringify({ name, deposit, commodity }),
        });
    }

    async listProjects() {
        return this.request<{ projects: any[] }>('/api/projects');
    }

    async getProject(projectId: string) {
        return this.request(`/api/projects/${projectId}`);
    }

    // ============== File Upload ==============

    async uploadFile(file: File): Promise<UploadResponse> {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.baseUrl}/api/upload`, {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
            throw new Error(error.detail);
        }

        return response.json();
    }

    async previewFile(fileId: string, offset = 0, limit = 50): Promise<PreviewResponse> {
        return this.request(`/api/preview/${fileId}?offset=${offset}&limit=${limit}`);
    }

    // ============== CRM Database ==============

    async listCRMs(element?: string, search?: string) {
        const params = new URLSearchParams();
        if (element) params.append('element', element);
        if (search) params.append('search', search);
        
        const query = params.toString();
        return this.request<{ crms: any[]; total: number }>(
            `/api/crms${query ? `?${query}` : ''}`
        );
    }

    async getCRM(crmName: string) {
        return this.request(`/api/crms/${encodeURIComponent(crmName)}`);
    }

    // ============== Analysis ==============

    async runAnalysis(request: AnalysisRequest): Promise<AnalysisResult> {
        return this.request('/api/analyze', {
            method: 'POST',
            body: JSON.stringify(request),
        });
    }

    async getResults(analysisId: string): Promise<AnalysisResult> {
        return this.request(`/api/results/${analysisId}`);
    }

    // ============== Export ==============

    async exportExcel(analysisId: string): Promise<Blob> {
        const response = await fetch(
            `${this.baseUrl}/api/export/excel?analysis_id=${analysisId}`,
            { method: 'POST' }
        );

        if (!response.ok) {
            throw new Error('Failed to export Excel report');
        }

        return response.blob();
    }

    async exportPDF(analysisId: string): Promise<Blob> {
        const response = await fetch(
            `${this.baseUrl}/api/export/pdf?analysis_id=${analysisId}`,
            { method: 'POST' }
        );

        if (!response.ok) {
            throw new Error('Failed to export PDF report');
        }

        return response.blob();
    }

    // ============== Helper: Download Blob ==============

    downloadBlob(blob: Blob, filename: string) {
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Export singleton instance
export const apiClient = new QAQCApiClient();

// Export class for custom instances
export { QAQCApiClient };

