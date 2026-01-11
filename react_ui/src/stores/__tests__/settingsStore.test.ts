import { describe, it, expect, beforeEach } from 'vitest';
import { useSettingsStore } from '../settingsStore';

describe('settingsStore', () => {
    beforeEach(() => {
        // Reset to defaults
        useSettingsStore.getState().resetToDefaults();
    });

    it('should have default settings', () => {
        const { settings } = useSettingsStore.getState();

        expect(settings.export.defaultFormat).toBe('pdf');
        expect(settings.export.figureResolution).toBe(300);
        expect(settings.analysis.defaultTolerancePercent).toBe(10);
        expect(settings.api.backendUrl).toBe('http://localhost:8000');
    });

    it('should update export settings', () => {
        const { updateExportSettings } = useSettingsStore.getState();

        updateExportSettings({ defaultFormat: 'docx' });

        const { settings } = useSettingsStore.getState();
        expect(settings.export.defaultFormat).toBe('docx');
        expect(settings.export.figureResolution).toBe(300); // Unchanged
    });

    it('should update analysis settings', () => {
        const { updateAnalysisSettings } = useSettingsStore.getState();

        updateAnalysisSettings({ defaultTolerancePercent: 15 });

        const { settings } = useSettingsStore.getState();
        expect(settings.analysis.defaultTolerancePercent).toBe(15);
        expect(settings.analysis.defaultPrecisionTarget).toBe(20); // Unchanged
    });

    it('should update API settings', () => {
        const { updateAPISettings } = useSettingsStore.getState();

        updateAPISettings({ backendUrl: 'http://example.com:8000' });

        const { settings } = useSettingsStore.getState();
        expect(settings.api.backendUrl).toBe('http://example.com:8000');
    });

    it('should update report settings', () => {
        const { updateReportSettings } = useSettingsStore.getState();

        updateReportSettings({ defaultTitle: 'Custom Report' });

        const { settings } = useSettingsStore.getState();
        expect(settings.report.defaultTitle).toBe('Custom Report');
    });

    it('should reset to defaults', () => {
        const { updateExportSettings, updateAnalysisSettings, resetToDefaults } = useSettingsStore.getState();

        updateExportSettings({ defaultFormat: 'docx' });
        updateAnalysisSettings({ defaultTolerancePercent: 15 });

        resetToDefaults();

        const { settings } = useSettingsStore.getState();
        expect(settings.export.defaultFormat).toBe('pdf');
        expect(settings.analysis.defaultTolerancePercent).toBe(10);
    });
});
