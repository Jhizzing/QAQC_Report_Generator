import React from 'react';
import { Check, Upload, Settings, BarChart3, FileText, Lock } from 'lucide-react';

export type WorkflowStep = 'entry' | 'import' | 'setup' | 'dashboard' | 'report' | 'education' | 'template_editor' | 'crm' | 'settings';

interface StepConfig {
  id: WorkflowStep;
  label: string;
  shortLabel: string;
  icon: React.ReactNode;
}

const WORKFLOW_STEPS: StepConfig[] = [
  { id: 'import', label: 'Import Data', shortLabel: 'Import', icon: <Upload className="w-4 h-4" /> },
  { id: 'setup', label: 'Analysis Setup', shortLabel: 'Setup', icon: <Settings className="w-4 h-4" /> },
  { id: 'dashboard', label: 'Results Dashboard', shortLabel: 'Results', icon: <BarChart3 className="w-4 h-4" /> },
  { id: 'report', label: 'Generate Report', shortLabel: 'Report', icon: <FileText className="w-4 h-4" /> },
];

interface WorkflowStepperProps {
  currentStep: WorkflowStep;
  onNavigate: (step: WorkflowStep) => void;
  canNavigateTo: (step: WorkflowStep) => boolean;
  completedSteps: WorkflowStep[];
}

export const WorkflowStepper: React.FC<WorkflowStepperProps> = ({
  currentStep,
  onNavigate,
  canNavigateTo,
  completedSteps,
}) => {
  // Don't show stepper on education or template_editor
  if (currentStep === 'education' || currentStep === 'template_editor') {
    return null;
  }

  const currentIndex = WORKFLOW_STEPS.findIndex(s => s.id === currentStep);

  return (
    <div className="w-full py-4 px-6 bg-surface border-b border-secondary-dark">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center relative">
          {WORKFLOW_STEPS.map((step, index) => {
            const isCompleted = completedSteps.includes(step.id);
            const isCurrent = currentStep === step.id;
            const isNavigable = canNavigateTo(step.id);
            const isPast = index < currentIndex;
            const isFuture = index > currentIndex;

            return (
              <React.Fragment key={step.id}>
                <button
                  onClick={() => isNavigable && onNavigate(step.id)}
                  disabled={!isNavigable}
                  className={`
                    relative z-10 flex flex-col items-center gap-2 group
                    transition-all duration-200 flex-shrink-0
                    ${isNavigable ? 'cursor-pointer' : 'cursor-not-allowed'}
                  `}
                  title={!isNavigable ? 'Complete previous steps first' : step.label}
                >
                {/* Step circle - z-10 ensures it's above the line */}
                <div
                  className={`
                    relative z-10 w-10 h-10 rounded-full flex items-center justify-center
                    border-2 transition-all duration-300
                    ${isCurrent
                      ? 'bg-primary border-primary text-slate-900 scale-110 shadow-lg shadow-primary/30'
                      : isCompleted || isPast
                        ? 'bg-primary/20 border-primary text-primary'
                        : isNavigable
                          ? 'bg-surface border-secondary-light text-slate-400 hover:border-primary/50 hover:text-slate-300'
                          : 'bg-surface border-secondary-dark text-slate-600'
                    }
                  `}
                >
                  {isCompleted && !isCurrent ? (
                    <Check className="w-5 h-5" />
                  ) : !isNavigable && isFuture ? (
                    <Lock className="w-4 h-4" />
                  ) : (
                    step.icon
                  )}
                </div>

                {/* Step label */}
                <span
                  className={`
                    text-xs font-medium transition-colors whitespace-nowrap
                    ${isCurrent
                      ? 'text-primary'
                      : isCompleted || isPast
                        ? 'text-slate-300'
                        : isNavigable
                          ? 'text-slate-400 group-hover:text-slate-300'
                          : 'text-slate-600'
                    }
                  `}
                >
                  {step.shortLabel}
                </span>
                </button>
                
                {/* Line segment between steps */}
                {index < WORKFLOW_STEPS.length - 1 && (
                  <div className="flex-1 h-0.5 mx-2 relative">
                    {/* Background line */}
                    <div className="absolute top-0 left-0 right-0 h-full bg-secondary-dark" />
                    {/* Filled line if step is completed */}
                    {(isCompleted || isPast) && (
                      <div className="absolute top-0 left-0 right-0 h-full bg-primary transition-all duration-500" />
                    )}
                  </div>
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default WorkflowStepper;
