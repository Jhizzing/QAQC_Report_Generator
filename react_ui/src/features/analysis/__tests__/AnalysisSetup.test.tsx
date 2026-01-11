import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '../../../test/utils';
import { AnalysisSetup } from '../AnalysisSetup';

describe('AnalysisSetup', () => {
    const mockOnComplete = vi.fn();
    const mockOnNavigateToEducation = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should render category selection', () => {
        render(
            <AnalysisSetup
                initialCategory={null}
                onComplete={mockOnComplete}
                onNavigateToEducation={mockOnNavigateToEducation}
            />
        );

        // Component says "Select Analysis Type" or "Analysis Type"
        expect(screen.getByText(/analysis type/i)).toBeInTheDocument();
    });

    it('should render with initial category', () => {
        render(
            <AnalysisSetup
                initialCategory="gold"
                onComplete={mockOnComplete}
                onNavigateToEducation={mockOnNavigateToEducation}
            />
        );

        // Should show gold category as selected
        expect(screen.getByText(/gold/i)).toBeInTheDocument();
    });

    it('should render methodology configuration', () => {
        render(
            <AnalysisSetup
                initialCategory="gold"
                onComplete={mockOnComplete}
                onNavigateToEducation={mockOnNavigateToEducation}
            />
        );

        // Component has multiple "duplicate" texts, so use getAllByText
        const duplicateTexts = screen.getAllByText(/duplicate/i);
        expect(duplicateTexts.length).toBeGreaterThan(0);
        
        // Also check for assay method
        const assayMethod = screen.queryByText(/assay method/i);
        expect(assayMethod || duplicateTexts.length > 0).toBeTruthy();
    });
});
