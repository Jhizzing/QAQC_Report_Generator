import type { Tour } from '../../types/onboarding';

export const APP_WORKFLOW_TOUR: Tour = {
    id: 'app-workflow',
    name: 'Application Workflow',
    description: 'Complete walkthrough of the LogiQore Reporter workflow',
    requiredForFirstTime: true,
    steps: [
        {
            id: 'welcome',
            type: 'modal',
            title: 'Welcome to LogiQore Reporter! ⛏️',
            content: `A powerful tool for geological QAQC analysis and reporting, aligned with JORC Code 2012 guidelines.

Let's walk through the complete workflow together!`,
            placement: 'center',
        },
        {
            id: 'project-info',
            type: 'spotlight',
            target: '[data-tour="project-header"]',
            title: 'Your Active Project',
            content: `Every analysis starts with a project. Your current project details are shown here.

You can switch projects or create new ones from the project menu.`,
            placement: 'bottom',
        },
        {
            id: 'import-data',
            type: 'spotlight',
            target: '[data-tour="upload-area"]',
            title: 'Import Your Data',
            content: `Drag & drop your CSV or Excel files here, or click to browse.

💡 Tip: You can import multiple files for different data types (assays, standards, blanks, duplicates).`,
            placement: 'top',
        },
        {
            id: 'demo-data',
            type: 'spotlight',
            target: '[data-tour="demo-gold-btn"]',
            title: 'Try Sample Data',
            content: `Click this button to load a complete Gold Fire Assay dataset and see the analysis in action!`,
            placement: 'right',
            nextOnClick: true,
        },
        {
            id: 'analysis-setup',
            type: 'spotlight',
            target: '[data-tour="category-gold"]',
            title: 'One-Step Analysis Setup',
            content: `Configure your entire analysis on a single page:

🎯 Select analysis type (Gold, pXRF, PhotonAssay)
⚙️ Quick settings appear inline
📋 Select your CRMs
🚀 Click "Run Analysis"

No more multi-step wizards - just pick your options and go!`,
            placement: 'right',
            nextOnClick: true,
        },
        {
            id: 'results-dashboard',
            type: 'modal',
            title: 'Analysis Results',
            content: `Review your QAQC analysis results in an interactive dashboard:

📊 Summary metrics and pass/fail stats
📈 Interactive visualizations
🔬 Detailed breakdown by sample type
⚠️ Flagged issues and recommendations

From here, you can proceed to generate your report!`,
            placement: 'center',
        },
        {
            id: 'report-generation',
            type: 'modal',
            title: 'Generate Reports',
            content: `Create professional QAQC reports:

📑 Complete JORC Report - Full analysis with narratives
📊 Figures Only - Charts and tables for presentations

Choose a template, configure options, and export as DOCX.

You can also create custom templates in the Template Editor!`,
            placement: 'center',
        },
    ],
};
