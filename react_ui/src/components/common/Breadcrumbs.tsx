import React from 'react';
import { ChevronRight, Home } from 'lucide-react';
import type { WorkflowStep } from './WorkflowStepper';

interface BreadcrumbItem {
  id: WorkflowStep | 'home';
  label: string;
  navigable: boolean;
}

const STEP_LABELS: Record<WorkflowStep | 'home', string> = {
  home: 'Home',
  entry: 'Home',
  import: 'Import Data',
  setup: 'Analysis Setup',
  dashboard: 'Results Dashboard',
  report: 'Generate Report',
  education: 'Education Center',
  template_editor: 'Template Editor',
  crm: 'CRM Database',
  settings: 'Settings',
};

interface BreadcrumbsProps {
  currentStep: WorkflowStep;
  projectName?: string;
  onNavigate: (step: WorkflowStep | 'home') => void;
  canNavigateTo: (step: WorkflowStep) => boolean;
}

export const Breadcrumbs: React.FC<BreadcrumbsProps> = ({
  currentStep,
  projectName,
  onNavigate,
  canNavigateTo,
}) => {
  // Build breadcrumb trail based on current step
  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const items: BreadcrumbItem[] = [];

    // Always start with project/home
    if (projectName) {
      items.push({ id: 'home', label: projectName, navigable: true });
    }

    // Add workflow-specific breadcrumbs
    switch (currentStep) {
      case 'import':
        items.push({ id: 'import', label: STEP_LABELS.import, navigable: false });
        break;
      case 'setup':
        items.push({ id: 'import', label: STEP_LABELS.import, navigable: canNavigateTo('import') });
        items.push({ id: 'setup', label: STEP_LABELS.setup, navigable: false });
        break;
      case 'dashboard':
        items.push({ id: 'import', label: STEP_LABELS.import, navigable: canNavigateTo('import') });
        items.push({ id: 'setup', label: STEP_LABELS.setup, navigable: canNavigateTo('setup') });
        items.push({ id: 'dashboard', label: STEP_LABELS.dashboard, navigable: false });
        break;
      case 'report':
        items.push({ id: 'import', label: STEP_LABELS.import, navigable: canNavigateTo('import') });
        items.push({ id: 'setup', label: STEP_LABELS.setup, navigable: canNavigateTo('setup') });
        items.push({ id: 'dashboard', label: STEP_LABELS.dashboard, navigable: canNavigateTo('dashboard') });
        items.push({ id: 'report', label: STEP_LABELS.report, navigable: false });
        break;
      case 'education':
        items.push({ id: 'education', label: STEP_LABELS.education, navigable: false });
        break;
      case 'template_editor':
        items.push({ id: 'template_editor', label: STEP_LABELS.template_editor, navigable: false });
        break;
    }

    return items;
  };

  const breadcrumbs = getBreadcrumbs();

  return (
    <nav className="flex items-center text-sm" aria-label="Breadcrumb">
      <ol className="flex items-center gap-1">
        {breadcrumbs.map((item, index) => {
          const isLast = index === breadcrumbs.length - 1;
          const showHomeIcon = index === 0 && item.id === 'home';

          return (
            <li key={item.id} className="flex items-center">
              {index > 0 && (
                <ChevronRight className="w-4 h-4 text-slate-600 mx-1" />
              )}
              
              {item.navigable && !isLast ? (
                <button
                  onClick={() => onNavigate(item.id as WorkflowStep | 'home')}
                  className="flex items-center gap-1.5 text-slate-400 hover:text-primary transition-colors"
                >
                  {showHomeIcon && <Home className="w-3.5 h-3.5" />}
                  <span className="hover:underline">{item.label}</span>
                </button>
              ) : (
                <span 
                  className={`flex items-center gap-1.5 ${
                    isLast ? 'text-slate-200 font-medium' : 'text-slate-500'
                  }`}
                >
                  {showHomeIcon && <Home className="w-3.5 h-3.5" />}
                  <span>{item.label}</span>
                </span>
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
};

export default Breadcrumbs;
