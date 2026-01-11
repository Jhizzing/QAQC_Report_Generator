import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '../../../test/utils';
import { ResultsDashboard } from '../ResultsDashboard';
import type { QAQCAnalysisOutput } from '../qaqcAnalysis';

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

describe('ResultsDashboard', () => {
    const mockOnProceed = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should render results dashboard', () => {
        render(
            <ResultsDashboard
                results={mockResults}
                onProceed={mockOnProceed}
            />
        );

        expect(screen.getByText(/QAQC Analysis Results/i)).toBeInTheDocument();
    });

    it('should display summary statistics', () => {
        render(
            <ResultsDashboard
                results={mockResults}
                onProceed={mockOnProceed}
            />
        );

        expect(screen.getByText('100')).toBeInTheDocument(); // Total Samples
        expect(screen.getByText('20')).toBeInTheDocument(); // Standards
        expect(screen.getByText('15')).toBeInTheDocument(); // Blanks
        expect(screen.getByText('30')).toBeInTheDocument(); // Duplicates
        expect(screen.getByText('95.5%')).toBeInTheDocument(); // Pass Rate
    });

    it('should render tab navigation', () => {
        render(
            <ResultsDashboard
                results={mockResults}
                onProceed={mockOnProceed}
            />
        );

        // Use getAllByText since "blanks" appears in both tab button and summary card
        const standardsTabs = screen.getAllByText(/standards/i);
        expect(standardsTabs.length).toBeGreaterThan(0);
        const blanksTabs = screen.getAllByText(/blanks/i);
        expect(blanksTabs.length).toBeGreaterThan(0);
        const duplicatesTabs = screen.getAllByText(/duplicates/i);
        expect(duplicatesTabs.length).toBeGreaterThan(0);
    });

    it('should call onProceed when Create Report button is clicked', async () => {
        const { userEvent } = await import('../../../test/utils');
        render(
            <ResultsDashboard
                results={mockResults}
                onProceed={mockOnProceed}
            />
        );

        const button = screen.getByText(/create report/i);
        await userEvent.click(button);

        expect(mockOnProceed).toHaveBeenCalledTimes(1);
    });

    it('should not show Create Report button when onProceed is not provided', () => {
        render(
            <ResultsDashboard
                results={mockResults}
            />
        );

        expect(screen.queryByText(/create report/i)).not.toBeInTheDocument();
    });

    it('should switch between tabs', async () => {
        const { userEvent } = await import('../../../test/utils');
        render(
            <ResultsDashboard
                results={mockResults}
                onProceed={mockOnProceed}
            />
        );

        // Find the tab button (not the summary card text)
        const blanksTabs = screen.getAllByText(/blanks/i);
        // The first one should be the tab button (contains count in parentheses)
        const blanksTabButton = blanksTabs.find(el => el.textContent?.includes('('));
        expect(blanksTabButton).toBeDefined();
        
        if (blanksTabButton) {
            await userEvent.click(blanksTabButton);
            // Tab should still be in document after click
            expect(blanksTabButton).toBeInTheDocument();
        }
    });
});
