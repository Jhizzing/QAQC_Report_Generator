import type { Tour } from '../../types/onboarding';

export const APP_WORKFLOW_TOUR: Tour = {
    id: 'app-workflow',
    name: 'Application Workflow',
    description: 'Complete walkthrough of the QAQC analysis workflow',
    requiredForFirstTime: true,
    steps: [
        {
            id: 'welcome',
            type: 'modal',
            title: 'Welcome to LogiQore QAQC Reporter! ⛏️',
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
            id: 'data-category',
            type: 'spotlight',
            target: '[data-tour="category-gold"]',
            title: 'Select Gold Analysis',
            content: `For this demo, we'll use the Gold Analysis workflow. Click the card to proceed.`,
            placement: 'right',
            nextOnClick: true,
        },
        {
            id: 'methodology',
            type: 'modal',
            title: 'Methodology Configuration',
            content: `Configure your analysis methodology:

• Sample types and classification
• Detection limits and thresholds
• Standard reference materials (CRMs)
• Analysis method details

These settings ensure JORC compliance and accurate QAQC reporting.`,
            placement: 'center',
        },
        {
            id: 'qaqc-rules',
            type: 'modal',
            title: 'QAQC Rules Setup',
            content: `Define quality control rules:

✅ Standards (CRM) - Accuracy checks
🔍 Blanks - Contamination detection
👥 Duplicates - Precision analysis

Set insertion rates, acceptance criteria, and Westgard rules for sophisticated QAQC analysis.`,
            placement: 'center',
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
