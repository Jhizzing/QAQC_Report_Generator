// Onboarding type definitions

export type TourStepType = 'modal' | 'spotlight' | 'tooltip';
export type PlacementType = 'top' | 'bottom' | 'left' | 'right' | 'center';

export interface TourStep {
    id: string;
    type: TourStepType;
    title: string;
    content: string;
    target?: string; // CSS selector or data-tour attribute
    placement?: PlacementType;
    image?: string;
    actions?: string[]; // Required user actions
    interactionRequired?: boolean;
    nextOnClick?: boolean; // Auto-advance when target clicked
}

export interface Tour {
    id: string;
    name: string;
    description: string;
    steps: TourStep[];
    requiredForFirstTime?: boolean;
}

export interface TooltipConfig {
    id: string;
    target: string;
    title?: string;
    content: string;
    placement?: PlacementType;
    trigger?: 'hover' | 'click' | 'focus';
    persistent?: boolean;
    dismissible?: boolean;
}

export interface OnboardingProgress {
    completedTours: string[];
    skippedTours: string[];
    dismissedTooltips: string[];
    lastCompletedAt?: number;
}

export interface OnboardingSettings {
    showTooltips: boolean;
    showHints: boolean;
    hasSeenWelcome: boolean;
    autoStartTours: boolean;
}
