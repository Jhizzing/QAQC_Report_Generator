import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface ExportSettings {
  defaultFormat: 'pdf' | 'docx' | 'xlsx';
  figureResolution: 150 | 300 | 600;
  includeCoverPage: boolean;
  includeJORCTable: boolean;
}

export interface ReportSettings {
  defaultTitle: string;
  defaultColorScheme: 'default' | 'corporate' | 'minimal';
  defaultFontSize: 'small' | 'medium' | 'large';
  defaultPageLayout: 'portrait' | 'landscape';
  defaultLogoUrl?: string;
}

export interface AnalysisSettings {
  defaultTolerancePercent: number;
  defaultPrecisionTarget: number;
  defaultContaminationMultiplier: number;
  defaultFailureThreshold: number;
}

export interface APISettings {
  backendUrl: string;
  autoConnect: boolean;
  healthCheckInterval: number; // seconds
}

export interface AppSettings {
  export: ExportSettings;
  analysis: AnalysisSettings;
  api: APISettings;
  report: ReportSettings;
}

interface SettingsState {
  settings: AppSettings;
  updateExportSettings: (settings: Partial<ExportSettings>) => void;
  updateAnalysisSettings: (settings: Partial<AnalysisSettings>) => void;
  updateAPISettings: (settings: Partial<APISettings>) => void;
  updateReportSettings: (settings: Partial<ReportSettings>) => void;
  resetToDefaults: () => void;
}

const DEFAULT_SETTINGS: AppSettings = {
  export: {
    defaultFormat: 'pdf',
    figureResolution: 300,
    includeCoverPage: true,
    includeJORCTable: true,
  },
  analysis: {
    defaultTolerancePercent: 10,
    defaultPrecisionTarget: 20,
    defaultContaminationMultiplier: 3,
    defaultFailureThreshold: 3,
  },
  api: {
    backendUrl: 'http://localhost:8000',
    autoConnect: true,
    healthCheckInterval: 30,
  },
  report: {
    defaultTitle: 'QAQC Analysis Report',
    defaultColorScheme: 'default',
    defaultFontSize: 'medium',
    defaultPageLayout: 'portrait',
  },
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      settings: DEFAULT_SETTINGS,
      
      updateExportSettings: (newSettings) => set((state) => ({
        settings: {
          ...state.settings,
          export: { ...state.settings.export, ...newSettings },
        },
      })),
      
      updateAnalysisSettings: (newSettings) => set((state) => ({
        settings: {
          ...state.settings,
          analysis: { ...state.settings.analysis, ...newSettings },
        },
      })),
      
      updateAPISettings: (newSettings) => set((state) => ({
        settings: {
          ...state.settings,
          api: { ...state.settings.api, ...newSettings },
        },
      })),
      
      updateReportSettings: (newSettings) => set((state) => ({
        settings: {
          ...state.settings,
          report: { ...state.settings.report, ...newSettings },
        },
      })),
      
      resetToDefaults: () => set({ settings: DEFAULT_SETTINGS }),
    }),
    {
      name: 'qaqc-settings',
    }
  )
);
