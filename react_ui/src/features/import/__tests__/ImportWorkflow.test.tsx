import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '../../../test/utils';
import { ImportWorkflow } from '../ImportWorkflow';
import { createMockFile } from '../../../test/utils';

// Mock the file processor
vi.mock('../../../utils/fileProcessor', () => ({
    processFile: vi.fn(),
}));

describe('ImportWorkflow', () => {
    const mockOnComplete = vi.fn();
    const mockOnLoadDemoData = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should render file upload interface', () => {
        render(
            <ImportWorkflow
                onComplete={mockOnComplete}
                onLoadDemoData={mockOnLoadDemoData}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/upload/i)).toBeInTheDocument();
    });

    it('should handle file upload', async () => {
        const { processFile } = await import('../../../utils/fileProcessor');
        const mockProcessedData = {
            fileName: 'test.csv',
            headers: ['SampleID', 'Type', 'Result'],
            data: [['STD-001', 'STD', '10.5']],
            rowCount: 1,
        };

        vi.mocked(processFile).mockResolvedValue(mockProcessedData);

        render(
            <ImportWorkflow
                onComplete={mockOnComplete}
                onLoadDemoData={mockOnLoadDemoData}
                isBackendAvailable={false}
            />
        );

        // File upload would be tested with user interaction
        // This is a basic structure test
        expect(screen.getByText(/upload/i)).toBeInTheDocument();
    });

    it('should show demo data option', () => {
        render(
            <ImportWorkflow
                onComplete={mockOnComplete}
                onLoadDemoData={mockOnLoadDemoData}
                isBackendAvailable={false}
            />
        );

        // Component says "Or try with sample data" or "sample data"
        expect(screen.getByText(/sample data/i)).toBeInTheDocument();
    });

    it('should handle backend availability status', () => {
        const { rerender } = render(
            <ImportWorkflow
                onComplete={mockOnComplete}
                onLoadDemoData={mockOnLoadDemoData}
                isBackendAvailable={true}
            />
        );

        // Component should render differently based on backend status
        expect(screen.getByText(/upload/i)).toBeInTheDocument();

        rerender(
            <ImportWorkflow
                onComplete={mockOnComplete}
                onLoadDemoData={mockOnLoadDemoData}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/upload/i)).toBeInTheDocument();
    });
});
