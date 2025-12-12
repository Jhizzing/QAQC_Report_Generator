import { useState, useCallback } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { Header } from './components/Header';
import { ImportWorkflow } from './features/import/ImportWorkflow';
import { DataCategorySelect } from './features/analysis/DataCategorySelect';
import { MethodologyWizard, type MethodologyConfig } from './features/analysis/MethodologyWizard';
import { QAQCRuleConfig, type QAQCConfig } from './features/analysis/QAQCRuleConfig';
import { ResultsDashboard } from './features/analysis/ResultsDashboard';
import { ReportWorkflow } from './features/report/ReportWorkflow';
import { TemplateEditor } from './features/templates/TemplateEditor';
import { ProjectEntry } from './features/projects/ProjectEntry';
import { WelcomeModal } from './components/onboarding/WelcomeModal';
import { OnboardingOverlay } from './components/onboarding/OnboardingOverlay';
import { useProjectStore } from './stores/projectStore';
import { runQAQCAnalysis, autoDetectColumnMapping, type QAQCAnalysisOutput } from './features/analysis/qaqcAnalysis';
import { exportFiguresOnly, exportJORCReport } from './utils/export';
import { generateMockGoldData, generateMockPhotonData } from './data/mockQAQCData';
import { saveProjectToFile, type QAQCProjectFile, type WorkflowStep as ProjectWorkflowStep } from './utils/projectFile';
import type { ProcessedData } from './utils/fileProcessor';
import type { JORCReportConfig, FiguresConfig } from './features/report/ReportConfig';

type WorkflowStep = 'entry' | 'import' | 'category' | 'methodology' | 'qaqcRules' | 'dashboard' | 'report' | 'template_editor';

function App() {
  const { currentProject } = useProjectStore();
  const [data, setData] = useState<ProcessedData | null>(null);
  const [workflowStep, setWorkflowStep] = useState<WorkflowStep>('import');
  const [selectedCategory, setSelectedCategory] = useState<'gold' | 'pxrf' | 'multi' | 'photon' | null>(null);
  const [methodologyConfig, setMethodologyConfig] = useState<MethodologyConfig | null>(null);
  const [qaqcConfig, setQaqcConfig] = useState<QAQCConfig | null>(null);
  const [analysisResults, setAnalysisResults] = useState<QAQCAnalysisOutput | null>(null);

  // Handle loading a project from file
  const handleProjectLoaded = useCallback((projectFile: QAQCProjectFile) => {
    // Restore all state from the loaded project
    setData(projectFile.data);
    setSelectedCategory(projectFile.category);
    setMethodologyConfig(projectFile.methodologyConfig);
    setQaqcConfig(projectFile.qaqcConfig);
    setAnalysisResults(projectFile.analysisResults);
    setWorkflowStep(projectFile.workflowStep as WorkflowStep);
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

  const handleImportComplete = (importedData: ProcessedData) => {
    setData(importedData);
    setWorkflowStep('category');
  };

  const handleLoadDemoData = (demoCategory?: 'gold' | 'photon') => {
    const categoryToUse = demoCategory || selectedCategory || 'gold';

    const mockData = categoryToUse === 'photon'
      ? generateMockPhotonData()
      : generateMockGoldData();

    const processedData: ProcessedData = {
      fileName: categoryToUse === 'photon'
        ? 'Demo_PhotonAssay_Data.csv'
        : 'Demo_Gold_QAQC_Data.csv',
      headers: Object.keys(mockData.combined[0]),
      data: mockData.combined.map(row => Object.values(row)),
      rowCount: mockData.combined.length
    };

    setData(processedData);
    setSelectedCategory(categoryToUse);

    if (categoryToUse === 'photon') {
      setWorkflowStep('methodology');
    } else {
      setWorkflowStep('category');
    }
  };

  const handleCategoryComplete = (category: 'gold' | 'pxrf' | 'multi' | 'photon') => {
    console.log('Selected category:', category);
    setSelectedCategory(category);
    setWorkflowStep('methodology');
  };

  const handleMethodologyComplete = (config: MethodologyConfig) => {
    console.log('Methodology config:', config);
    setMethodologyConfig(config);
    setWorkflowStep('qaqcRules');
  };

  const handleQAQCRulesComplete = (config: QAQCConfig) => {
    console.log('QAQC Rules config:', config);
    setQaqcConfig(config);

    if (data && selectedCategory) {
      runAnalysis(config);
    }
  };

  const runAnalysis = (config: QAQCConfig) => {
    if (!data || (!qaqcConfig && !config)) return;

    const rawData = data.data.map((row) => {
      const rowObj: any = {};
      data.headers.forEach((header, index) => {
        rowObj[header] = row[index];
      });
      return rowObj;
    });

    const columnMapping = autoDetectColumnMapping(rawData);

    const results = runQAQCAnalysis({
      data: rawData,
      methodologyConfig: methodologyConfig!,
      qaqcConfig: config || qaqcConfig!,
      columnMapping
    });

    setAnalysisResults(results);
    setWorkflowStep('dashboard');
  };

  const handleProceedToReport = () => {
    setWorkflowStep('report');
  };

  const handleGenerateReport = async (type: 'report' | 'figures', config: JORCReportConfig | FiguresConfig) => {
    if (!analysisResults || !currentProject) return;

    if (type === 'figures') {
      await exportFiguresOnly(analysisResults, config as FiguresConfig, currentProject.name);
    } else {
      await exportJORCReport(analysisResults, config as JORCReportConfig, currentProject.name);
    }
  };

  return (
    <MainLayout>
      <WelcomeModal />
      <OnboardingOverlay />
      <Header onSaveProject={handleSaveProject} />
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div data-tour="project-header">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {workflowStep === 'report' ? 'Report Generation' :
                workflowStep === 'dashboard' ? 'Analysis Dashboard' :
                  workflowStep === 'qaqcRules' ? 'QAQC Rules' :
                    workflowStep === 'methodology' ? 'Methodology Setup' :
                      workflowStep === 'category' ? 'Configuration' : 'Import Data'}
            </h2>
            <p className="text-sm text-gray-300 mt-1">
              {currentProject.name} • {currentProject.deposit} ({currentProject.commodity})
            </p>
          </div>

          {data && workflowStep === 'dashboard' && (
            <button
              onClick={() => {
                setData(null);
                setWorkflowStep('import');
              }}
              className="px-4 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
            >
              Reset Data
            </button>
          )}
        </div>

        {/* Demo Template Editor Button */}
        {workflowStep === 'import' && (
          <div className="flex justify-end">
            <button
              onClick={() => setWorkflowStep('template_editor')}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors"
            >
              🎨 Open Template Editor (Demo)
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
            />
          </div>
        )}

        {workflowStep === 'category' && (
          <DataCategorySelect onComplete={handleCategoryComplete} />
        )}

        {workflowStep === 'methodology' && selectedCategory && (
          <MethodologyWizard
            category={selectedCategory}
            onComplete={handleMethodologyComplete}
          />
        )}

        {workflowStep === 'qaqcRules' && selectedCategory && methodologyConfig && (
          <QAQCRuleConfig
            category={selectedCategory}
            methodologyConfig={methodologyConfig}
            onComplete={handleQAQCRulesComplete}
          />
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
          />
        )}
      </div>
    </MainLayout>
  );
}

export default App;
