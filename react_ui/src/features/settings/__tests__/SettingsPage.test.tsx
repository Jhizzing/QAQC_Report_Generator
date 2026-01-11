import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '../../../test/utils';
import { SettingsPage } from '../SettingsPage';

describe('SettingsPage', () => {
    const mockOnClose = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should render settings page', () => {
        render(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/settings/i)).toBeInTheDocument();
    });

    it('should render export settings section', () => {
        render(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/export defaults/i)).toBeInTheDocument();
    });

    it('should render analysis settings section', () => {
        render(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/analysis defaults/i)).toBeInTheDocument();
    });

    it('should render API settings section', () => {
        render(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/backend connection/i)).toBeInTheDocument();
    });

    it('should show backend connection status', () => {
        const { rerender } = render(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={true}
            />
        );

        expect(screen.getByText(/connected/i)).toBeInTheDocument();

        rerender(
            <SettingsPage
                onClose={mockOnClose}
                isBackendAvailable={false}
            />
        );

        expect(screen.getByText(/offline/i)).toBeInTheDocument();
    });
});
