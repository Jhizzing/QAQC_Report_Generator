import React from 'react';
import {
  Settings,
  FileOutput,
  FileText,
  Beaker,
  Server,
  Info,
  RotateCcw,
  Check,
  X,
  ExternalLink
} from 'lucide-react';
import { useSettingsStore } from '../../stores/settingsStore';

interface SettingsPageProps {
  onClose?: () => void;
  isBackendAvailable?: boolean;
}

export const SettingsPage: React.FC<SettingsPageProps> = ({ onClose, isBackendAvailable }) => {
  const { settings, updateExportSettings, updateAnalysisSettings, updateAPISettings, updateReportSettings, resetToDefaults } = useSettingsStore();

  return (
    <div className="min-h-screen bg-background-dark">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-surface-dark/95 backdrop-blur-sm border-b border-secondary-dark">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-slate-500/20">
                <Settings className="w-6 h-6 text-slate-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-50">Settings</h1>
                <p className="text-sm text-slate-400">Configure application preferences</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={resetToDefaults}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-slate-400 hover:text-slate-50 hover:bg-surface-light transition-colors"
              >
                <RotateCcw className="w-4 h-4" />
                Reset to Defaults
              </button>
              {onClose && (
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-surface-light text-slate-400 hover:text-slate-50 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-8 space-y-8">

        {/* Export Settings */}
        <section className="bg-surface rounded-xl border border-secondary-dark overflow-hidden">
          <div className="px-6 py-4 border-b border-secondary-dark flex items-center gap-3">
            <FileOutput className="w-5 h-5 text-blue-400" />
            <h2 className="text-lg font-semibold text-slate-50">Export Defaults</h2>
          </div>
          <div className="p-6 space-y-6">
            {/* Default Format */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Default Report Format
              </label>
              <div className="flex gap-3">
                {(['pdf', 'docx', 'xlsx'] as const).map((format) => (
                  <button
                    key={format}
                    onClick={() => updateExportSettings({ defaultFormat: format })}
                    className={`
                      px-4 py-2 rounded-lg border font-medium uppercase text-sm
                      transition-all
                      ${settings.export.defaultFormat === format
                        ? 'bg-primary/20 border-primary text-primary'
                        : 'bg-surface-light border-secondary-light text-slate-400 hover:border-primary/50'
                      }
                    `}
                  >
                    {format}
                  </button>
                ))}
              </div>
            </div>

            {/* Figure Resolution */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Figure Resolution (DPI)
              </label>
              <div className="flex gap-3">
                {([150, 300, 600] as const).map((dpi) => (
                  <button
                    key={dpi}
                    onClick={() => updateExportSettings({ figureResolution: dpi })}
                    className={`
                      px-4 py-2 rounded-lg border font-medium text-sm
                      transition-all
                      ${settings.export.figureResolution === dpi
                        ? 'bg-primary/20 border-primary text-primary'
                        : 'bg-surface-light border-secondary-light text-slate-400 hover:border-primary/50'
                      }
                    `}
                  >
                    {dpi} DPI
                    {dpi === 150 && <span className="text-xs ml-1 opacity-60">(Fast)</span>}
                    {dpi === 600 && <span className="text-xs ml-1 opacity-60">(Print)</span>}
                  </button>
                ))}
              </div>
            </div>

            {/* Toggles */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <ToggleSetting
                label="Include Cover Page"
                description="Add a professional cover page to reports"
                value={settings.export.includeCoverPage}
                onChange={(value) => updateExportSettings({ includeCoverPage: value })}
              />
              <ToggleSetting
                label="Include JORC Table 1"
                description="Add editable JORC Table 1 section"
                value={settings.export.includeJORCTable}
                onChange={(value) => updateExportSettings({ includeJORCTable: value })}
              />
            </div>
          </div>
        </section>

        {/* Analysis Settings */}
        <section className="bg-surface rounded-xl border border-secondary-dark overflow-hidden">
          <div className="px-6 py-4 border-b border-secondary-dark flex items-center gap-3">
            <Beaker className="w-5 h-5 text-amber-400" />
            <h2 className="text-lg font-semibold text-slate-50">Analysis Defaults</h2>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <NumberSetting
                label="Standards Tolerance (%)"
                description="Default ± percentage for CRM pass/fail"
                value={settings.analysis.defaultTolerancePercent}
                onChange={(value) => updateAnalysisSettings({ defaultTolerancePercent: value })}
                min={1}
                max={50}
                step={1}
              />
              <NumberSetting
                label="Precision Target (%)"
                description="Default RPD/HARD limit for duplicates"
                value={settings.analysis.defaultPrecisionTarget}
                onChange={(value) => updateAnalysisSettings({ defaultPrecisionTarget: value })}
                min={5}
                max={50}
                step={1}
              />
              <NumberSetting
                label="Contamination Multiplier"
                description="Blank failure = X × detection limit"
                value={settings.analysis.defaultContaminationMultiplier}
                onChange={(value) => updateAnalysisSettings({ defaultContaminationMultiplier: value })}
                min={1}
                max={10}
                step={0.5}
              />
              <NumberSetting
                label="Failure Threshold"
                description="Consecutive failures before flagging"
                value={settings.analysis.defaultFailureThreshold}
                onChange={(value) => updateAnalysisSettings({ defaultFailureThreshold: value })}
                min={1}
                max={10}
                step={1}
              />
            </div>
          </div>
        </section>

        {/* API Settings */}
        <section className="bg-surface rounded-xl border border-secondary-dark overflow-hidden">
          <div className="px-6 py-4 border-b border-secondary-dark flex items-center gap-3">
            <Server className="w-5 h-5 text-emerald-400" />
            <h2 className="text-lg font-semibold text-slate-50">Server Status</h2>
            <div className={`
              ml-auto flex items-center gap-2 px-3 py-1 rounded-full text-xs font-medium
              ${isBackendAvailable
                ? 'bg-status-success/20 text-status-success'
                : 'bg-slate-600/20 text-slate-400'
              }
            `}>
              <div className={`w-2 h-2 rounded-full ${isBackendAvailable ? 'bg-status-success' : 'bg-slate-500'}`} />
              {isBackendAvailable ? 'Server Connected' : 'Offline Mode'}
            </div>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Backend URL
              </label>
              <input
                type="text"
                value={settings.api.backendUrl}
                onChange={(e) => updateAPISettings({ backendUrl: e.target.value })}
                className="
                  w-full px-4 py-2.5 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 placeholder-slate-500
                  focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                "
                placeholder="http://localhost:8000"
              />
              <p className="mt-1 text-xs text-slate-500">
                FastAPI backend for server-side analysis and exports
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <ToggleSetting
                label="Auto-connect on Startup"
                description="Automatically check for backend availability"
                value={settings.api.autoConnect}
                onChange={(value) => updateAPISettings({ autoConnect: value })}
              />
              <NumberSetting
                label="Health Check Interval (sec)"
                description="How often to check backend status"
                value={settings.api.healthCheckInterval}
                onChange={(value) => updateAPISettings({ healthCheckInterval: value })}
                min={10}
                max={120}
                step={10}
              />
            </div>
          </div>
        </section>

        {/* Report Settings */}
        <section className="bg-surface rounded-xl border border-secondary-dark overflow-hidden">
          <div className="px-6 py-4 border-b border-secondary-dark flex items-center gap-3">
            <FileText className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold text-slate-50">Report Defaults</h2>
          </div>
          <div className="p-6 space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Default Report Title
              </label>
              <input
                type="text"
                value={settings.report.defaultTitle}
                onChange={(e) => updateReportSettings({ defaultTitle: e.target.value })}
                className="
                  w-full px-4 py-2.5 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 placeholder-slate-500
                  focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                "
                placeholder="LogiQore Reporter Analysis Report"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Color Scheme
                </label>
                <select
                  value={settings.report.defaultColorScheme}
                  onChange={(e) => updateReportSettings({ defaultColorScheme: e.target.value as 'default' | 'corporate' | 'minimal' })}
                  className="
                    w-full px-4 py-2.5 rounded-lg
                    bg-surface-light border border-secondary-dark
                    text-slate-50
                    focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                  "
                >
                  <option value="default">Default</option>
                  <option value="corporate">Corporate</option>
                  <option value="minimal">Minimal</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Font Size
                </label>
                <select
                  value={settings.report.defaultFontSize}
                  onChange={(e) => updateReportSettings({ defaultFontSize: e.target.value as 'small' | 'medium' | 'large' })}
                  className="
                    w-full px-4 py-2.5 rounded-lg
                    bg-surface-light border border-secondary-dark
                    text-slate-50
                    focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                  "
                >
                  <option value="small">Small</option>
                  <option value="medium">Medium</option>
                  <option value="large">Large</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-2">
                  Page Layout
                </label>
                <select
                  value={settings.report.defaultPageLayout}
                  onChange={(e) => updateReportSettings({ defaultPageLayout: e.target.value as 'portrait' | 'landscape' })}
                  className="
                    w-full px-4 py-2.5 rounded-lg
                    bg-surface-light border border-secondary-dark
                    text-slate-50
                    focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                  "
                >
                  <option value="portrait">Portrait</option>
                  <option value="landscape">Landscape</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Default Logo URL (optional)
              </label>
              <input
                type="text"
                value={settings.report.defaultLogoUrl || ''}
                onChange={(e) => updateReportSettings({ defaultLogoUrl: e.target.value || undefined })}
                className="
                  w-full px-4 py-2.5 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 placeholder-slate-500
                  focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                "
                placeholder="https://example.com/logo.png"
              />
              <p className="mt-1 text-xs text-slate-500">
                URL or path to company logo for report headers
              </p>
            </div>
          </div>
        </section>

        {/* About Section */}
        <section className="bg-surface rounded-xl border border-secondary-dark overflow-hidden">
          <div className="px-6 py-4 border-b border-secondary-dark flex items-center gap-3">
            <Info className="w-5 h-5 text-purple-400" />
            <h2 className="text-lg font-semibold text-slate-50">About</h2>
          </div>
          <div className="p-6">
            <div className="flex items-start gap-4">
              <div className="w-16 h-16 bg-primary/20 rounded-xl flex items-center justify-center">
                <span className="text-2xl font-bold text-primary">LR</span>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold text-slate-50">LogiQore Reporter</h3>
                <p className="text-sm text-slate-400 mt-1">
                  Professional QAQC analysis and reporting tool for geological assay data.
                  Supports JORC/NI 43-101 compliant workflows.
                </p>
                <div className="flex items-center gap-4 mt-3">
                  <span className="text-xs text-slate-500">Version 1.0.0</span>
                  <a
                    href="#"
                    className="flex items-center gap-1 text-xs text-primary hover:text-primary-light transition-colors"
                  >
                    <ExternalLink className="w-3 h-3" />
                    Documentation
                  </a>
                  <a
                    href="#"
                    className="flex items-center gap-1 text-xs text-primary hover:text-primary-light transition-colors"
                  >
                    <ExternalLink className="w-3 h-3" />
                    GitHub
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  );
};

// Toggle Setting Component
interface ToggleSettingProps {
  label: string;
  description: string;
  value: boolean;
  onChange: (value: boolean) => void;
}

const ToggleSetting: React.FC<ToggleSettingProps> = ({ label, description, value, onChange }) => (
  <div
    className="flex items-center justify-between p-4 bg-surface-light/30 rounded-lg border border-white/5 cursor-pointer hover:bg-surface-light/50 transition-colors"
    onClick={() => onChange(!value)}
  >
    <div>
      <p className="text-sm font-medium text-slate-200">{label}</p>
      <p className="text-xs text-slate-500">{description}</p>
    </div>
    <div className={`
      w-11 h-6 rounded-full transition-colors relative
      ${value ? 'bg-primary' : 'bg-slate-600'}
    `}>
      <div className={`
        absolute top-0.5 w-5 h-5 bg-white rounded-full transition-transform shadow
        ${value ? 'left-5.5 translate-x-0.5' : 'left-0.5'}
      `}>
        {value ? (
          <Check className="w-3 h-3 text-primary absolute top-1 left-1" />
        ) : null}
      </div>
    </div>
  </div>
);

// Number Setting Component
interface NumberSettingProps {
  label: string;
  description: string;
  value: number;
  onChange: (value: number) => void;
  min: number;
  max: number;
  step: number;
}

const NumberSetting: React.FC<NumberSettingProps> = ({
  label, description, value, onChange, min, max, step
}) => (
  <div className="p-4 bg-surface-light/30 rounded-lg border border-white/5">
    <div className="flex items-center justify-between mb-2">
      <p className="text-sm font-medium text-slate-200">{label}</p>
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        min={min}
        max={max}
        step={step}
        className="
          w-20 px-2 py-1 rounded text-right
          bg-surface-dark border border-secondary-dark
          text-slate-50 text-sm
          focus:outline-none focus:ring-1 focus:ring-primary/50
        "
      />
    </div>
    <p className="text-xs text-slate-500">{description}</p>
  </div>
);

export default SettingsPage;
