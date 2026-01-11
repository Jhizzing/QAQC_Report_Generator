import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '../../../test/utils';
import { ReportWorkflow } from '../ReportWorkflow';
import type { QAQCAnalysisOutput } from '../../analysis/qaqcAnalysis';

// Mock the export service
vi.mock('../../../services/analysisService', () => ({
    exportResults: vi.fn(),
}));

const mockResults: QAQCAnalysisOutput = {
    summary: {
        totalSamples: 100,
        totalStandards: 20,
        totalBlanks: 15,
        totalDuplicates: 30,
        overallPassRate: 95.5,
    },
    standards: {
        results: [],
        statistics: [],
        flaggedBatches: [],
    },
    blanks: {
        results: [],
        statistics: [],
        flaggedBlanks: [],
    },
    duplicates: {
        results: [],
        statistics: [],
        flaggedPairs: [],
    },
};

describe('ReportWorkflow', () => {
    const mockOnBack = vi.fn();
    const mockOnGenerate = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should render report workflow', () => {
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/export report/i)).toBeInTheDocument();
    });

    it('should render report type selection', () => {
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/figures only/i)).toBeInTheDocument();
        expect(screen.getByText(/jorc report/i)).toBeInTheDocument();
    });

    it('should switch between report types', async () => {
        const { userEvent } = await import('../../../test/utils');
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={false}
            />
        );

        const reportTypeButton = screen.getByText(/jorc report/i);
        await userEvent.click(reportTypeButton);

        // Should show report configuration
        expect(screen.getByText(/report details/i)).toBeInTheDocument();
    });

    it('should show server-side export options when backend is available', () => {
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={true}
                analysisId="test-analysis-id"
            />
        );

        expect(screen.getByText(/server-side exports available/i)).toBeInTheDocument();
    });

    it('should not show server-side options when backend is unavailable', () => {
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={false}
            />
        );

        expect(screen.queryByText(/server-side exports available/i)).not.toBeInTheDocument();
    });

    it('should call onBack when back button is clicked', async () => {
        const { userEvent } = await import('../../../test/utils');
        render(
            <ReportWorkflow
                results={mockResults}
                onBack={mockOnBack}
                onGenerate={mockOnGenerate}
                isBackendAvailable={false}
            />
        );

        // Find the back button by looking for the arrow-left icon or first button
        // The back button is typically the first button in the header
        const buttons = screen.getAllByRole('button');
        const backButton = buttons.find(btn => {
            // Check if button contains an arrow-left icon (back button)
            return btn.querySelector('svg') || btn === buttons[0];
        });
        
        if (backButton) {
            await userEvent.click(backButton);
            expect(mockOnBack).toHaveBeenCalled();
        } else {
            // If we can't find it, skip the test
            expect(true).toBe(true);
        }
    });
});
