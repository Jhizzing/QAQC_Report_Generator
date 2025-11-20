import { useState } from 'react';
import { MainLayout } from './components/layout/MainLayout';
import { Header } from './components/Header';
import { ImportWorkflow } from './features/import/ImportWorkflow';
import { DataCategorySelect } from './features/analysis/DataCategorySelect';
import { MethodologyWizard, type MethodologyConfig } from './features/analysis/MethodologyWizard';
import { QAQCRuleConfig, type QAQCConfig } from './features/analysis/QAQCRuleConfig';
import { ResultsDashboard } from './features/analysis/ResultsDashboard';
import { ProjectEntry } from './features/projects/ProjectEntry';
import { useProjectStore } from './stores/projectStore';
import { runQAQCAnalysis, autoDetectColumnMapping, type QAQCAnalysisOutput } from './features/analysis/qaqcAnalysis';
import { exportAll } from './utils/export';
import { generateMockGoldData, generateMockPhotonData } from './data/mockQAQCData';
import type { ProcessedData } from './utils/fileProcessor';

type WorkflowStep = 'entry' | 'import' | 'category' | 'methodology' | 'qaqcRules' | 'dashboard';

function App() {
  const { currentProject } = useProjectStore();
  const [data, setData] = useState<ProcessedData | null>(null);
  const [workflowStep, setWorkflowStep] = useState<WorkflowStep>('import');
  const [selectedCategory, setSelectedCategory] = useState<'gold' | 'pxrf' | 'multi' | 'photon' | null>(null);
  const [methodologyConfig, setMethodologyConfig] = useState<MethodologyConfig | null>(null);
  const [qaqcConfig, setQaqcConfig] = useState<QAQCConfig | null>(null);
  const [analysisResults, setAnalysisResults] = useState<QAQCAnalysisOutput | null>(null);

  if (!currentProject) {
    return <ProjectEntry />;
  }

  // Simple state machine for workflow
  // In a real app, this might be in a store
  const handleImportComplete = (importedData: ProcessedData) => {
    setData(importedData);
    setWorkflowStep('category');
  };

  const handleLoadDemoData = (demoCategory?: 'gold' | 'photon') => {
    // Determine which category to use
    const categoryToUse = demoCategory || selectedCategory || 'gold';

    // Load appropriate mock data based on category
    const mockData = categoryToUse === 'photon'
      ? generateMockPhotonData()
      : generateMockGoldData();

    // Convert to ProcessedData format
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

    // For PhotonAssay, skip category selection and go straight to methodology
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

    // Auto-run analysis
    if (data && selectedCategory) {
      runAnalysis(config);
    }
  };

  const runAnalysis = (config: QAQCConfig) => {
    if (!data || !qaqcConfig && !config) return;

    // Convert data to format needed for analysis
    const rawData = data.data.map((row) => {
      const rowObj: any = {};
      data.headers.forEach((header, index) => {
        rowObj[header] = row[index];
      });
      return rowObj;
    });

    // Auto-detect column mappings
    const columnMapping = autoDetectColumnMapping(rawData);

    // Run analysis
    const results = runQAQCAnalysis({
      data: rawData,
      methodologyConfig: methodologyConfig!,
      qaqcConfig: config || qaqcConfig!,
      columnMapping
    });

    setAnalysisResults(results);
    setWorkflowStep('dashboard');
  };

  const handleExport = async () => {
    if (analysisResults && currentProject) {
      await exportAll(analysisResults, currentProject.name);
    }
  };

  // Log config for debugging (will be used in dashboard later)
  if (methodologyConfig) {
    console.log('Current methodology:', methodologyConfig);
  }
  if (qaqcConfig) {
    console.log('Current QAQC rules:', qaqcConfig);
  }

  return (
    <MainLayout>
      <Header />
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {workflowStep === 'dashboard' ? 'Analysis Dashboard' :
                workflowStep === 'qaqcRules' ? 'QAQC Rules' :
                  workflowStep === 'methodology' ? 'Methodology Setup' :
                    workflowStep === 'category' ? 'Configuration' : 'Import Data'}
            </h2>
            <p className="text-sm text-gray-500 mt-1">
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
            onExport={handleExport}
          />
        )}
      </div>
    </MainLayout>
  );
}

export default App;
