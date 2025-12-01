import React, { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { useOnboardingStore } from '../../stores/onboardingStore';

export const OnboardingOverlay: React.FC = () => {
    const {
        isActive,
        currentStepIndex,
        getCurrentStep,
        nextStep,
        previousStep,
        skipTour,
        getTourProgress,
        currentTour,
    } = useOnboardingStore();

    const overlayRef = useRef<HTMLDivElement>(null);
    const currentStep = getCurrentStep();

    useEffect(() => {
        if (isActive) {
            // Disable body scroll when overlay is active
            document.body.style.overflow = 'hidden';

            // Handle keyboard navigation
            const handleKeyDown = (e: KeyboardEvent) => {
                if (e.key === 'Escape') {
                    skipTour();
                } else if (e.key === 'ArrowRight') {
                    nextStep();
                } else if (e.key === 'ArrowLeft') {
                    previousStep();
                }
            };

            window.addEventListener('keydown', handleKeyDown);
            return () => {
                document.body.style.overflow = '';
                window.removeEventListener('keydown', handleKeyDown);
            };
        }
    }, [isActive, skipTour, nextStep, previousStep]);

    useEffect(() => {
        if (isActive && currentStep?.target) {
            // Scroll target element into view
            const targetElement = document.querySelector(currentStep.target);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                });
            }
        }
    }, [isActive, currentStep]);

    if (!isActive || !currentStep || !currentTour) return null;

    const progress = getTourProgress();
    const isFirstStep = currentStepIndex === 0;
    const isLastStep = currentStepIndex === currentTour.steps.length - 1;

    // Calculate popover position for spotlight tours
    const getPopoverStyle = (): React.CSSProperties => {
        if (currentStep.type === 'modal' || currentStep.type === 'tooltip') {
            return {
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                zIndex: 10002,
            };
        }

        // For spotlight, position based on target element
        const targetElement = currentStep.target ? document.querySelector(currentStep.target) : null;
        if (!targetElement) {
            return {
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                zIndex: 10002,
            };
        }

        const rect = targetElement.getBoundingClientRect();
        const placement = currentStep.placement || 'right';

        const styles: React.CSSProperties = {
            position: 'fixed',
            zIndex: 10002,
        };

        switch (placement) {
            case 'right':
                styles.top = `${rect.top + rect.height / 2}px`;
                styles.left = `${rect.right + 20}px`;
                styles.transform = 'translateY(-50%)';
                break;
            case 'left':
                styles.top = `${rect.top + rect.height / 2}px`;
                styles.right = `${window.innerWidth - rect.left + 20}px`;
                styles.transform = 'translateY(-50%)';
                break;
            case 'bottom':
                styles.top = `${rect.bottom + 20}px`;
                styles.left = `${rect.left + rect.width / 2}px`;
                styles.transform = 'translateX(-50%)';
                break;
            case 'top':
                styles.bottom = `${window.innerHeight - rect.top + 20}px`;
                styles.left = `${rect.left + rect.width / 2}px`;
                styles.transform = 'translateX(-50%)';
                break;
            default:
                styles.top = '50%';
                styles.left = '50%';
                styles.transform = 'translate(-50%, -50%)';
        }

        return styles;
    };

    // Get spotlight highlight style
    const getSpotlightStyle = (): React.CSSProperties | null => {
        if (currentStep.type !== 'spotlight' || !currentStep.target) return null;

        const targetElement = document.querySelector(currentStep.target);
        if (!targetElement) return null;

        const rect = targetElement.getBoundingClientRect();

        return {
            position: 'fixed',
            top: `${rect.top - 8}px`,
            left: `${rect.left - 8}px`,
            width: `${rect.width + 16}px`,
            height: `${rect.height + 16}px`,
            border: '3px solid rgb(251, 191, 36)', // primary gold
            borderRadius: '12px',
            boxShadow: '0 0 0 4px rgba(251, 191, 36, 0.2), 0 0 40px rgba(251, 191, 36, 0.4)',
            pointerEvents: 'none',
            zIndex: 10001,
            animation: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        };
    };

    const spotlightStyle = getSpotlightStyle();

    return (
        <>
            {/* Overlay backdrop */}
            <div
                ref={overlayRef}
                className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[10000] transition-opacity duration-300"
                onClick={(e) => {
                    if (e.target === overlayRef.current && currentStep.type === 'modal') {
                        skipTour();
                    }
                }}
            />

            {/* Spotlight highlight */}
            {spotlightStyle && (
                <div
                    style={spotlightStyle}
                    className="spotlight-highlight"
                />
            )}

            {/* Popover content */}
            <div
                style={getPopoverStyle()}
                className="bg-gray-900 border border-gray-700 rounded-xl shadow-2xl max-w-md w-full mx-4 animate-fade-in"
            >
                {/* Header */}
                <div className="p-6 border-b border-gray-800">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                                <span className="text-xs font-semibold text-primary">
                                    Step {currentStepIndex + 1} of {currentTour.steps.length}
                                </span>
                                <div className="flex-1 h-1.5 bg-gray-800 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-primary transition-all duration-300"
                                        style={{ width: `${progress}%` }}
                                    />
                                </div>
                            </div>
                            <h3 className="text-xl font-bold text-white">{currentStep.title}</h3>
                        </div>
                        <button
                            onClick={skipTour}
                            className="p-2 hover:bg-gray-800 rounded-lg transition-colors"
                            title="Skip tour"
                        >
                            <X className="w-5 h-5 text-gray-400" />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="p-6">
                    {currentStep.image && (
                        <img
                            src={currentStep.image}
                            alt={currentStep.title}
                            className="w-full rounded-lg mb-4"
                        />
                    )}
                    <p className="text-gray-300 whitespace-pre-line leading-relaxed">
                        {currentStep.content}
                    </p>

                    {currentStep.actions && currentStep.actions.length > 0 && (
                        <div className="mt-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                            <p className="text-sm font-medium text-blue-300 mb-2">Required Action:</p>
                            <ul className="text-sm text-blue-200 space-y-1">
                                {currentStep.actions.map((action, index) => (
                                    <li key={index} className="flex items-start gap-2">
                                        <span className="text-primary">•</span>
                                        <span>{action}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-gray-800 flex items-center justify-between">
                    <button
                        onClick={skipTour}
                        className="text-sm text-gray-400 hover:text-white transition-colors"
                    >
                        Skip Tour
                    </button>

                    <div className="flex items-center gap-3">
                        {!isFirstStep && (
                            <button
                                onClick={previousStep}
                                className="px-4 py-2 text-sm font-medium text-gray-300 hover:text-white rounded-lg hover:bg-gray-800 transition-colors"
                            >
                                Back
                            </button>
                        )}
                        <button
                            onClick={nextStep}
                            className="px-6 py-2 text-sm font-bold bg-primary text-gray-900 rounded-lg hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20"
                        >
                            {isLastStep ? 'Finish' : 'Next →'}
                        </button>
                    </div>
                </div>
            </div>

            {/* CSS animations */}
            <style>{`
        @keyframes pulse {
          0%, 100% {
            opacity: 1;
          }
          50% {
            opacity: 0.7;
          }
        }

        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.3s ease-out;
        }
      `}</style>
        </>
    );
};
