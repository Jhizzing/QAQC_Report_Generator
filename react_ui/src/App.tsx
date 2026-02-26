import React, { useState, useCallback, useMemo } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { Header } from './components/Header';
import { ImportWorkflow } from './features/import/ImportWorkflow';
import { AnalysisSetup } from './features/analysis/AnalysisSetup';
import { type MethodologyConfig } from './features/analysis/MethodologyWizard';
import { type QAQCConfig } from './features/analysis/QAQCRuleConfig';
import { ResultsDashboard } from './features/analysis/ResultsDashboard';
import { ReportWorkflow } from './features/report/ReportWorkflow';
import { TemplateEditor } from './features/templates/TemplateEditor';
import { ProjectEntry } from './features/projects/ProjectEntry';
import { EducationCenter } from './features/education/EducationCenter';
import { CRMDatabase } from './features/crm/CRMDatabase';
import { SettingsPage } from './features/settings/SettingsPage';
import { WelcomeModal } from './components/onboarding/WelcomeModal';
import { OnboardingOverlay } from './components/onboarding/OnboardingOverlay';
import { WorkflowStepper, type WorkflowStep as StepperWorkflowStep } from './components/common/WorkflowStepper';
import { Breadcrumbs } from './components/common/Breadcrumbs';
import { useProjectStore } from './stores/projectStore';
import { autoDetectColumnMapping, type QAQCAnalysisOutput } from './features/analysis/qaqcAnalysis';
import { exportFiguresOnly, exportJORCReport } from './utils/export';
import { generateMockGoldData, generateMockPhotonData, generateMockPXRFData, generateMockMultiElementICPData } from './data/mockQAQCData';
import { saveProjectToFile, type QAQCProjectFile, type WorkflowStep as ProjectWorkflowStep } from './utils/projectFile';
import { useBackendService, setGlobalBackendStatus } from './hooks/useBackendService';
import { runAnalysis } from './services/analysisService';
import { BackendStatus } from './components/common/BackendStatus';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { useNotificationStore } from './stores/notificationStore';
import type { ProcessedData } from './utils/fileProcessor';
import type { JORCReportConfig, FiguresConfig } from './features/report/ReportConfig';

// Use the shared WorkflowStep type from WorkflowStepper
type WorkflowStep = StepperWorkflowStep;

function App() {
  const { currentProject } = useProjectStore();
  const { addNotification } = useNotificationStore();
  const [data, setData] = useState<ProcessedData | null>(null);
  const [fileId, setFileId] = useState<string | null>(null); // Server file ID for backend analysis
  const [workflowStep, setWorkflowStep] = useState<WorkflowStep>('import');
  const [selectedCategory, setSelectedCategory] = useState<'gold' | 'pxrf' | 'multi' | 'photon' | null>(null);
  const [methodologyConfig, setMethodologyConfig] = useState<MethodologyConfig | null>(null);
  const [qaqcConfig, setQaqcConfig] = useState<QAQCConfig | null>(null);
  const [analysisResults, setAnalysisResults] = useState<QAQCAnalysisOutput | null>(null);
  const [analysisId, setAnalysisId] = useState<string | null>(null); // Server analysis ID for exports
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  // Backend service hook
  const backendService = useBackendService();

  // Notify on backend status changes and update global status
  const prevBackendAvailable = React.useRef(backendService.isAvailable);
  React.useEffect(() => {
    // Update global backend status for non-React contexts (moved from render body to avoid hook ordering issues)
    setGlobalBackendStatus(backendService.isAvailable);

    if (backendService.isAvailable && !prevBackendAvailable.current) {
      addNotification({
        type: 'success',
        title: 'Backend Connected',
        message: 'Python backend is now available. Server-side analysis enabled.',
      });
    }
    prevBackendAvailable.current = backendService.isAvailable;
  }, [backendService.isAvailable, addNotification]);

  // Handle loading a project from file
  const handleProjectLoaded = useCallback((projectFile: QAQCProjectFile) => {
    // Restore all state from the loaded project
    setData(projectFile.data);
    setSelectedCategory(projectFile.category);
    setMethodologyConfig(projectFile.methodologyConfig);
    setQaqcConfig(projectFile.qaqcConfig);
    setAnalysisResults(projectFile.analysisResults);
    // Map old workflow steps to new simplified steps
    const oldStep = projectFile.workflowStep;
    let newStep: WorkflowStep = 'import';
    if (oldStep === 'dashboard') newStep = 'dashboard';
    else if (oldStep === 'report') newStep = 'report';
    else if (oldStep === 'category' || oldStep === 'methodology' || oldStep === 'qaqcRules') newStep = 'setup';
    else if (oldStep === 'template_editor') newStep = 'template_editor';
    else newStep = oldStep as WorkflowStep;
    setWorkflowStep(newStep);
  }, []);

  // Handle saving the current project to file
  const handleSaveProject = useCallback(() => {
    if (!currentProject) return;

    saveProjectToFile(currentProject, {
      data,
      category: selectedCategory,
      methodologyConfig,
      qaqcConfig,
      analysisResults,
      workflowStep: workflowStep as ProjectWorkflowStep,
    });
  }, [currentProject, data, selectedCategory, methodologyConfig, qaqcConfig, analysisResults, workflowStep]);

  if (!currentProject) {
    return <ProjectEntry onProjectLoaded={handleProjectLoaded} />;
  }

  const handleImportComplete = (importedData: ProcessedData, serverFileId?: string) => {
    setData(importedData);
    if (serverFileId) {
      setFileId(serverFileId);
    }
    setWorkflowStep('setup');
  };

  const handleLoadDemoData = (demoCategory?: 'gold' | 'photon' | 'pxrf' | 'multielement') => {
    const categoryToUse = demoCategory || selectedCategory || 'gold';

    let mockData;
    let fileName: string;
    let appCategory: 'gold' | 'pxrf' | 'photon';

    switch (categoryToUse) {
      case 'photon':
        mockData = generateMockPhotonData();
        fileName = 'Demo_PhotonAssay_Data.csv';
        appCategory = 'photon';
        break;
      case 'pxrf':
        mockData = generateMockPXRFData();
        fileName = 'Demo_pXRF_BaseMetals_Data.csv';
        appCategory = 'pxrf';
        break;
      case 'multielement':
        mockData = generateMockMultiElementICPData();
        fileName = 'Demo_MultiElement_ICP_Data.csv';
        appCategory = 'pxrf'; // Use pxrf category for multi-element (handles both pXRF and multi-element)
        break;
      default:
        mockData = generateMockGoldData();
        fileName = 'Demo_Gold_QAQC_Data.csv';
        appCategory = 'gold';
    }

    const processedData: ProcessedData = {
      fileName,
      headers: Object.keys(mockData.combined[0]),
      data: mockData.combined.map(row => Object.values(row)),
      rowCount: mockData.combined.length
    };

    setData(processedData);
    setSelectedCategory(appCategory);
    setWorkflowStep('setup');

    // Notify user that sample data skips preview/mapping
    addNotification({
      type: 'info',
      title: 'Sample Data Loaded',
      message: `Loaded ${fileName} — preview and column mapping steps skipped.`,
    });
  };

  // New unified handler for the AnalysisSetup component
  const handleAnalysisSetupComplete = async (result: {
    category: 'gold' | 'pxrf' | 'photon';
    methodologyConfig: MethodologyConfig;
    qaqcConfig: QAQCConfig;
  }) => {
    console.log('Analysis setup complete:', result);
    setSelectedCategory(result.category);
    setMethodologyConfig(result.methodologyConfig);
    setQaqcConfig(result.qaqcConfig);
    setAnalysisError(null);

    // Run analysis immediately
    if (data) {
      setIsAnalyzing(true);

      try {
        const rawData = data.data.map((row) => {
          const rowObj: Record<string, unknown> = {};
          data.headers.forEach((header, index) => {
            rowObj[header] = row[index];
          });
          return rowObj;
        });

        const columnMapping = autoDetectColumnMapping(rawData);

        // Use the analysis service which routes to server or client
        const analysisOutput = await runAnalysis(
          {
            data: rawData,
            fileId: fileId || undefined,
            methodologyConfig: result.methodologyConfig,
            qaqcConfig: result.qaqcConfig,
            columnMapping,
          },
          backendService.isAvailable
        );

        console.log(`Analysis completed using ${analysisOutput.mode} mode:`, analysisOutput.messages);

        setAnalysisResults(analysisOutput.results);
        if (analysisOutput.analysisId) {
          setAnalysisId(analysisOutput.analysisId);
        }
        setWorkflowStep('dashboard');

        // Notification for successful analysis
        const passRate = analysisOutput.results.summary.overallPassRate;
        addNotification({
          type: passRate >= 95 ? 'success' : passRate >= 85 ? 'warning' : 'error',
          title: 'Analysis Complete',
          message: `QAQC analysis completed. Pass rate: ${passRate.toFixed(1)}%`,
          action: {
            label: 'View Results',
            onClick: () => setWorkflowStep('dashboard'),
          },
        });
      } catch (error) {
        console.error('Analysis failed:', error);
        const errorMessage = error instanceof Error ? error.message : 'Analysis failed';
        setAnalysisError(errorMessage);

        // Notification for analysis failure
        addNotification({
          type: 'error',
          title: 'Analysis Failed',
          message: errorMessage,
        });
      } finally {
        setIsAnalyzing(false);
      }
    }
  };

  const handleProceedToReport = () => {
    setWorkflowStep('report');
  };

  const handleGenerateReport = async (type: 'report' | 'figures', config: JORCReportConfig | FiguresConfig): Promise<void> => {
    if (!analysisResults || !currentProject) return;

    try {
      if (type === 'figures') {
        await exportFiguresOnly(analysisResults, config as FiguresConfig, currentProject.name);
        addNotification({
          type: 'success',
          title: 'Figures Exported',
          message: 'Figures have been exported successfully.',
        });
      } else {
        await exportJORCReport(analysisResults, config as JORCReportConfig, currentProject.name);
        addNotification({
          type: 'success',
          title: 'Report Exported',
          message: 'JORC report has been exported successfully.',
        });
      }
    } catch (error) {
      addNotification({
        type: 'error',
        title: 'Export Failed',
        message: error instanceof Error ? error.message : 'Failed to export report',
      });
      throw error; // Re-throw so ReportWorkflow can show local feedback
    }
  };

  // Get title for current workflow step
  const getStepTitle = () => {
    switch (workflowStep) {
      case 'report': return 'Report Generation';
      case 'dashboard': return 'Analysis Dashboard';
      case 'setup': return 'Analysis Setup';
      case 'template_editor': return 'Template Editor';
      case 'education': return 'Education Center';
      case 'crm': return 'CRM Database';
      case 'settings': return 'Settings';
      default: return 'Import Data';
    }
  };

  // Calculate completed steps based on current state
  const completedSteps = useMemo(() => {
    const completed: string[] = [];
    if (data) completed.push('import');
    if (selectedCategory && methodologyConfig) completed.push('setup');
    if (analysisResults) completed.push('dashboard');
    return completed;
  }, [data, selectedCategory, methodologyConfig, analysisResults]);

  // Check if navigation to a step is allowed
  const canNavigateTo = useCallback((step: WorkflowStep): boolean => {
    switch (step) {
      case 'import':
        return true; // Always can go to import
      case 'setup':
        return !!data; // Need data to go to setup
      case 'dashboard':
        return !!analysisResults; // Need analysis results
      case 'report':
        return !!analysisResults; // Need analysis results
      case 'education':
        return true; // Always accessible
      case 'template_editor':
        return true; // Always accessible
      case 'crm':
        return true; // Always accessible
      case 'settings':
        return true; // Always accessible
      default:
        return false;
    }
  }, [data, analysisResults]);

  // Unified navigation handler
  const navigateTo = useCallback((step: WorkflowStep | 'home') => {
    if (step === 'home') {
      setWorkflowStep('import');
      return;
    }
    if (canNavigateTo(step)) {
      setWorkflowStep(step);
    }
  }, [canNavigateTo]);

  // Handle navigation from sidebar
  const handleSidebarNavigate = (section: string) => {
    const stepMap: Record<string, WorkflowStep> = {
      'dashboard': 'dashboard',
      'import': 'import',
      'setup': 'setup',
      'education': 'education',
      'crm': 'crm',
      'settings': 'settings',
    };
    const step = stepMap[section];
    if (step) {
      navigateTo(step);
    }
  };

  // Navigate to education topic from help tooltip
  const handleNavigateToEducation = (topicId?: string) => {
    setWorkflowStep('education');
    // Topic ID can be used later to scroll to specific topic
    console.log('Navigate to education topic:', topicId);
  };

  // Get active section for sidebar
  const getActiveSection = () => {
    switch (workflowStep) {
      case 'import': return 'import';
      case 'setup': return 'setup';
      case 'dashboard': return 'dashboard';
      case 'report': return 'dashboard'; // Report is part of dashboard flow
      case 'education': return 'education';
      case 'crm': return 'crm';
      case 'settings': return 'settings';
      default: return 'import';
    }
  };

  return (
    <ErrorBoundary>
      <MainLayout
        onSidebarNavigate={handleSidebarNavigate}
        activeSection={getActiveSection()}
        hasData={!!data}
        hasAnalysis={!!analysisResults}
        completedSteps={completedSteps}
      >
        <WelcomeModal onNavigate={navigateTo} />
        <OnboardingOverlay />
        <Header onSaveProject={handleSaveProject} />

        {/* Workflow Stepper - shows progress through main workflow */}
        <WorkflowStepper
          currentStep={workflowStep}
          onNavigate={navigateTo}
          canNavigateTo={canNavigateTo}
          completedSteps={completedSteps as WorkflowStep[]}
        />

        <div className="space-y-6 mt-4">
          {/* Breadcrumbs */}
          <Breadcrumbs
            currentStep={workflowStep}
            projectName={currentProject.name}
            onNavigate={navigateTo}
            canNavigateTo={canNavigateTo}
          />

          <div className="flex items-center justify-between">
            <div data-tour="project-header">
              <h2 className="text-2xl font-bold text-slate-50">
                {getStepTitle()}
              </h2>
              <p className="text-sm text-slate-400 mt-1">
                {currentProject.deposit} ({currentProject.commodity})
              </p>
            </div>

            <div className="flex items-center gap-4">
              <BackendStatus
                isAvailable={backendService.isAvailable}
                isChecking={backendService.isChecking}
                onRetry={backendService.retry}
              />
              {data && workflowStep === 'dashboard' && (
                <button
                  onClick={() => {
                    setData(null);
                    setFileId(null);
                    setAnalysisId(null);
                    setSelectedCategory(null);
                    setMethodologyConfig(null);
                    setQaqcConfig(null);
                    setAnalysisResults(null);
                    setAnalysisError(null);
                    setWorkflowStep('import');
                  }}
                  className="px-4 py-2 text-sm text-status-error hover:bg-status-error/10 rounded-lg transition-colors"
                >
                  Reset Data
                </button>
              )}
            </div>
          </div>

          {/* Demo Template Editor Button */}
          {workflowStep === 'import' && (
            <div className="flex justify-end">
              <button
                onClick={() => setWorkflowStep('template_editor')}
                className="px-4 py-2 bg-purple-600 text-slate-50 rounded-lg font-medium hover:bg-purple-700 transition-colors"
              >
                Open Template Editor (Demo)
              </button>
            </div>
          )}

          {workflowStep === 'template_editor' && (
            <TemplateEditor onBack={() => setWorkflowStep('import')} />
          )}

          {workflowStep === 'import' && (
            <div className="mt-8">
              <ImportWorkflow
                onComplete={handleImportComplete}
                onLoadDemoData={handleLoadDemoData}
                isBackendAvailable={backendService.isAvailable}
              />
            </div>
          )}

          {workflowStep === 'setup' && (
            <div className="relative">
              {isAnalyzing && (
                <div className="absolute inset-0 bg-background-dark/80 z-10 flex items-center justify-center rounded-lg">
                  <div className="text-center">
                    <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
                    <p className="text-slate-300">
                      Running analysis{backendService.isAvailable ? ' on server...' : '...'}
                    </p>
                  </div>
                </div>
              )}
              {analysisError && (
                <div className="mb-4 p-4 bg-status-error/10 border border-status-error rounded-lg">
                  <p className="text-status-error font-medium">Analysis Error</p>
                  <p className="text-slate-400 text-sm mt-1">{analysisError}</p>
                </div>
              )}
              <AnalysisSetup
                initialCategory={selectedCategory as 'gold' | 'pxrf' | 'photon' | null}
                onComplete={handleAnalysisSetupComplete}
                onNavigateToEducation={handleNavigateToEducation}
              />
            </div>
          )}

          {workflowStep === 'dashboard' && analysisResults && (
            <ResultsDashboard
              results={analysisResults}
              onProceed={handleProceedToReport}
            />
          )}

          {workflowStep === 'report' && analysisResults && (
            <ReportWorkflow
              results={analysisResults}
              onBack={() => setWorkflowStep('dashboard')}
              onGenerate={handleGenerateReport}
              isBackendAvailable={backendService.isAvailable}
              analysisId={analysisId}
            />
          )}

          {workflowStep === 'education' && (
            <EducationCenter onClose={() => setWorkflowStep('import')} />
          )}

          {workflowStep === 'crm' && (
            <CRMDatabase
              onClose={() => setWorkflowStep('import')}
              onNavigateToEducation={handleNavigateToEducation}
            />
          )}

          {workflowStep === 'settings' && (
            <SettingsPage
              onClose={() => setWorkflowStep('import')}
              isBackendAvailable={backendService.isAvailable}
            />
          )}
        </div>
      </MainLayout>
    </ErrorBoundary>
  );
}

export default App;
