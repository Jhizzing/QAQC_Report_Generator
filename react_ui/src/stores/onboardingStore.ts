import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Tour, TourStep, OnboardingProgress, OnboardingSettings } from '../types/onboarding';

interface OnboardingState {
    // Active tour state
    isActive: boolean;
    currentTour: Tour | null;
    currentStepIndex: number;

    // User progress
    progress: OnboardingProgress;
    settings: OnboardingSettings;

    // Actions
    startTour: (tour: Tour) => void;
    nextStep: () => void;
    previousStep: () => void;
    skipTour: () => void;
    completeTour: () => void;
    endTour: () => void;

    // Settings
    updateSettings: (settings: Partial<OnboardingSettings>) => void;
    dismissTooltip: (tooltipId: string) => void;
    resetOnboarding: () => void;

    // Helpers
    getCurrentStep: () => TourStep | null;
    isStepCompleted: (stepId: string) => boolean;
    isTourCompleted: (tourId: string) => boolean;
    getTourProgress: () => number; // Percentage
}

const DEFAULT_SETTINGS: OnboardingSettings = {
    showTooltips: true,
    showHints: true,
    hasSeenWelcome: false,
    autoStartTours: true,
};

const DEFAULT_PROGRESS: OnboardingProgress = {
    completedTours: [],
    skippedTours: [],
    dismissedTooltips: [],
};

export const useOnboardingStore = create<OnboardingState>()(
    persist(
        (set, get) => ({
            // Initial state
            isActive: false,
            currentTour: null,
            currentStepIndex: 0,
            progress: DEFAULT_PROGRESS,
            settings: DEFAULT_SETTINGS,

            // Start a tour
            startTour: (tour: Tour) => {
                set({
                    isActive: true,
                    currentTour: tour,
                    currentStepIndex: 0,
                });
            },

            // Navigate to next step
            nextStep: () => {
                const { currentTour, currentStepIndex } = get();
                if (!currentTour) return;

                if (currentStepIndex < currentTour.steps.length - 1) {
                    set({ currentStepIndex: currentStepIndex + 1 });
                } else {
                    get().completeTour();
                }
            },

            // Navigate to previous step
            previousStep: () => {
                const { currentStepIndex } = get();
                if (currentStepIndex > 0) {
                    set({ currentStepIndex: currentStepIndex - 1 });
                }
            },

            // Skip current tour
            skipTour: () => {
                const { currentTour, progress } = get();
                if (!currentTour) return;

                set({
                    isActive: false,
                    currentTour: null,
                    currentStepIndex: 0,
                    progress: {
                        ...progress,
                        skippedTours: [...progress.skippedTours, currentTour.id],
                    },
                });
            },

            // Complete current tour
            completeTour: () => {
                const { currentTour, progress } = get();
                if (!currentTour) return;

                set({
                    isActive: false,
                    currentTour: null,
                    currentStepIndex: 0,
                    progress: {
                        ...progress,
                        completedTours: [...progress.completedTours, currentTour.id],
                        lastCompletedAt: Date.now(),
                    },
                });
            },

            // End tour without marking as complete or skipped
            endTour: () => {
                set({
                    isActive: false,
                    currentTour: null,
                    currentStepIndex: 0,
                });
            },

            // Update settings
            updateSettings: (newSettings: Partial<OnboardingSettings>) => {
                const { settings } = get();
                set({
                    settings: { ...settings, ...newSettings },
                });
            },

            // Dismiss a tooltip permanently
            dismissTooltip: (tooltipId: string) => {
                const { progress } = get();
                set({
                    progress: {
                        ...progress,
                        dismissedTooltips: [...progress.dismissedTooltips, tooltipId],
                    },
                });
            },

            // Reset all onboarding data
            resetOnboarding: () => {
                set({
                    isActive: false,
                    currentTour: null,
                    currentStepIndex: 0,
                    progress: DEFAULT_PROGRESS,
                    settings: { ...DEFAULT_SETTINGS, hasSeenWelcome: false },
                });
            },

            // Get current step
            getCurrentStep: () => {
                const { currentTour, currentStepIndex } = get();
                if (!currentTour) return null;
                return currentTour.steps[currentStepIndex] || null;
            },

            // Check if a specific step is completed
            isStepCompleted: (stepId: string) => {
                const { currentTour, currentStepIndex } = get();
                if (!currentTour) return false;
                const stepIndex = currentTour.steps.findIndex(s => s.id === stepId);
                return stepIndex !== -1 && stepIndex < currentStepIndex;
            },

            // Check if a tour is completed
            isTourCompleted: (tourId: string) => {
                const { progress } = get();
                return progress.completedTours.includes(tourId);
            },

            // Get tour progress percentage
            getTourProgress: () => {
                const { currentTour, currentStepIndex } = get();
                if (!currentTour || currentTour.steps.length === 0) return 0;
                return Math.round(((currentStepIndex + 1) / currentTour.steps.length) * 100);
            },
        }),
        {
            name: 'onboarding-storage',
            partialize: (state) => ({
                progress: state.progress,
                settings: state.settings,
            }),
        }
    )
);
