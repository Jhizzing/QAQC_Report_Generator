import type { Tour } from '../../types/onboarding';

export const TEMPLATE_EDITOR_TOUR: Tour = {
    id: 'template-editor',
    name: 'Template Editor',
    description: 'Learn to create and customize report templates',
    requiredForFirstTime: false,
    steps: [
        {
            id: 'welcome',
            type: 'modal',
            title: 'Welcome to the Template Editor! 🎨',
            content: `Templates define your report structure and content.

Think of them as blueprints: create once, reuse for every project.

The editor has 3 main panels that work together:
📂 Sections (left) - Report chapters
📝 Blocks (center) - Content elements  
⚙️ Properties (right) - Configuration`,
            placement: 'center',
        },
        {
            id: 'sections-panel',
            type: 'spotlight',
            target: '[data-tour="sections-panel"]',
            title: 'Sections Panel',
            content: `Sections are top-level report divisions (like chapters).

✨ Drag to reorder
➕ Click + to add new  
🗑️ Click trash to delete
🎯 Click to select and view blocks

Try selecting "1. Executive Summary" now!`,
            placement: 'right',
            actions: ['Click on any section to proceed'],
            nextOnClick: true,
        },
        {
            id: 'blocks-panel',
            type: 'spotlight',
            target: '[data-tour="blocks-panel"]',
            title: 'Content Blocks',
            content: `Blocks are the building blocks of your report. Each type serves a purpose:

📝 text_auto - Auto-generated narratives from analysis  
✍️ text_user - Your custom commentary
📊 table_auto - Data tables (CRM summary, etc.)
📈 figure_auto - Charts and plots
🏷️ meta - Metadata fields (project name, date)

Drag blocks to reorder them within a section!`,
            placement: 'right',
        },
        {
            id: 'add-block',
            type: 'spotlight',
            target: '[data-tour="add-block"]',
            title: 'Adding Blocks',
            content: `Click "+ Add Block" to insert new content.

Blocks are grouped by type for easy browsing.

Each block type has different properties and behaviors - we'll configure those next!`,
            placement: 'left',
        },
        {
            id: 'block-actions',
            type: 'spotlight',
            target: '[data-tour="blocks-panel"]',
            title: 'Block Actions',
            content: `Each block has action buttons:

✏️ Edit - Configure properties (opens right panel)
🗑️ Delete - Remove from section

Try clicking Edit on any block to see its properties!`,
            placement: 'right',
            actions: ['Click Edit on any block'],
        },
        {
            id: 'properties-panel',
            type: 'spotlight',
            target: '[data-tour="properties-panel"]',
            title: 'Block Properties',
            content: `Configure every aspect of a block:

🏷️ Type - What kind of content
📝 Label - How it appears in report
📋 Description - Help text for users
🔗 Data Key - Bind to analysis results  
✔️ Required - Must be filled

The magic happens with Data Keys!`,
            placement: 'left',
        },
        {
            id: 'data-binding',
            type: 'spotlight',
            target: '[data-tour="data-key-select"]',
            title: 'Data Binding Keys',
            content: `This dropdown contains 50+ predefined data points!

Examples:
• report_purpose → Project purpose text
• table_crm_summary → CRM results table
• chart_blanks_timeseries → Blanks chart

When you select a key, the block automatically populates from your analysis results during report generation.

No manual copy-paste needed! 🎉`,
            placement: 'left',
        },
        {
            id: 'drag-drop',
            type: 'modal',
            title: 'Drag & Drop Reordering',
            content: `Both sections and blocks support drag-and-drop!

🖱️ Click and hold the grip icon
📍 Drag to new position
✨ Release to drop

The order numbers update automatically. Your changes are saved instantly!`,
            placement: 'center',
        },
        {
            id: 'toolbar',
            type: 'spotlight',
            target: '[data-tour="editor-toolbar"]',
            title: 'Editor Toolbar',
            content: `Control your template from the toolbar:

💾 Save - Store current state
📤 Export - Download as JSON
📥 Import - Load saved templates
👁️ Preview Mode - See readonly view

Templates auto-save to your browser, but export lets you share with your team!`,
            placement: 'bottom',
        },
        {
            id: 'preview-mode',
            type: 'spotlight',
            target: '[data-tour="preview-toggle"]',
            title: 'Preview Mode',
            content: `Toggle Preview Mode to see how your template looks without edit controls.

Perfect for:
• Reviewing structure
• Taking screenshots
• Presenting to stakeholders

Click the toggle to try it!`,
            placement: 'bottom',
        },
        {
            id: 'completion',
            type: 'modal',
            title: 'You\'re All Set! 🎉',
            content: `You now know how to:

✅ Organize sections
✅ Add and configure blocks  
✅ Bind data to analysis results
✅ Drag-and-drop reordering
✅ Save and export templates

Templates make your reporting workflow repeatable and professional.

Create custom templates for different commodities, project types, or client requirements!`,
            placement: 'center',
        },
    ],
};
