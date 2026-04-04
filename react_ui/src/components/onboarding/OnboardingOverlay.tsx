import React, { useEffect, useRef, useState, useCallback } from 'react';
import { X, ChevronLeft, ChevronRight } from 'lucide-react';
import { useOnboardingStore } from '../../stores/onboardingStore';

interface SpotlightRect {
    x: number;
    y: number;
    width: number;
    height: number;
}

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

    const [spotlightRect, setSpotlightRect] = useState<SpotlightRect | null>(null);
    const [isTransitioning, setIsTransitioning] = useState(false);
    const popoverRef = useRef<HTMLDivElement>(null);
    const currentStep = getCurrentStep();

    // Padding around the spotlight target
    const SPOTLIGHT_PADDING = 12;
    const SPOTLIGHT_BORDER_RADIUS = 12;

    // Calculate spotlight rectangle from target element
    const updateSpotlightRect = useCallback(() => {
        if (!currentStep?.target || currentStep.type !== 'spotlight') {
            setSpotlightRect(null);
            return;
        }

        const targetElement = document.querySelector(currentStep.target);
        if (!targetElement) {
            setSpotlightRect(null);
            return;
        }

        const rect = targetElement.getBoundingClientRect();
        setSpotlightRect({
            x: rect.left - SPOTLIGHT_PADDING,
            y: rect.top - SPOTLIGHT_PADDING,
            width: rect.width + SPOTLIGHT_PADDING * 2,
            height: rect.height + SPOTLIGHT_PADDING * 2,
        });
    }, [currentStep]);

    // Update spotlight on step change with transition
    useEffect(() => {
        if (isActive && currentStep) {
            setIsTransitioning(true);
            const timer = setTimeout(() => {
                updateSpotlightRect();
                setIsTransitioning(false);
            }, 50);
            return () => clearTimeout(timer);
        }
    }, [isActive, currentStep, updateSpotlightRect]);

    // Scroll target into view and update spotlight
    useEffect(() => {
        if (isActive && currentStep?.target) {
            const targetElement = document.querySelector(currentStep.target);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                });
                // Update spotlight after scroll
                const timer = setTimeout(updateSpotlightRect, 400);
                return () => clearTimeout(timer);
            }
        }
    }, [isActive, currentStep, updateSpotlightRect]);

    // Handle window resize
    useEffect(() => {
        if (isActive) {
            const handleResize = () => updateSpotlightRect();
            window.addEventListener('resize', handleResize);
            return () => window.removeEventListener('resize', handleResize);
        }
    }, [isActive, updateSpotlightRect]);

    // Keyboard navigation and body scroll lock
    useEffect(() => {
        if (isActive) {
            document.body.style.overflow = 'hidden';

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

    // Handle click on spotlight target for nextOnClick steps
    useEffect(() => {
        if (!isActive || !currentStep?.nextOnClick || !currentStep.target) return;

        const targetElement = document.querySelector(currentStep.target);
        if (!targetElement) return;

        const handleTargetClick = (e: Event) => {
            e.stopPropagation();
            nextStep();
        };

        targetElement.addEventListener('click', handleTargetClick);
        return () => targetElement.removeEventListener('click', handleTargetClick);
    }, [isActive, currentStep, nextStep]);

    if (!isActive || !currentStep || !currentTour) return null;

    const progress = getTourProgress();
    const isFirstStep = currentStepIndex === 0;
    const isLastStep = currentStepIndex === currentTour.steps.length - 1;
    const isSpotlight = currentStep.type === 'spotlight' && spotlightRect;

    // Generate SVG path for the overlay with cutout
    const generateOverlayPath = (): string => {
        const vw = window.innerWidth;
        const vh = window.innerHeight;

        if (!spotlightRect) {
            // Full overlay, no cutout
            return `M 0 0 L ${vw} 0 L ${vw} ${vh} L 0 ${vh} Z`;
        }

        const { x, y, width, height } = spotlightRect;
        const r = SPOTLIGHT_BORDER_RADIUS;

        // Outer rectangle (clockwise)
        // Inner rounded rectangle cutout (counter-clockwise for hole)
        return `
            M 0 0 
            L ${vw} 0 
            L ${vw} ${vh} 
            L 0 ${vh} 
            Z
            M ${x + r} ${y}
            L ${x + width - r} ${y}
            Q ${x + width} ${y} ${x + width} ${y + r}
            L ${x + width} ${y + height - r}
            Q ${x + width} ${y + height} ${x + width - r} ${y + height}
            L ${x + r} ${y + height}
            Q ${x} ${y + height} ${x} ${y + height - r}
            L ${x} ${y + r}
            Q ${x} ${y} ${x + r} ${y}
            Z
        `;
    };

    // Calculate effective placement with basic collision detection
    const getEffectivePlacement = (): 'top' | 'bottom' | 'left' | 'right' => {
        const defaultPlacement = currentStep.placement || 'right';
        if (currentStep.type === 'modal' || !spotlightRect) return defaultPlacement;
        
        const POPOVER_MAX_WIDTH = 400;
        const POPOVER_GAP = 24;
        const vw = window.innerWidth;

        let placement = defaultPlacement;
        
        if (placement === 'right' && spotlightRect.x + spotlightRect.width + POPOVER_GAP + POPOVER_MAX_WIDTH > vw) {
            placement = 'left';
            if (spotlightRect.x - POPOVER_GAP - POPOVER_MAX_WIDTH < 0) {
                placement = 'bottom';
            }
        }
        
        if (placement === 'left' && spotlightRect.x - POPOVER_GAP - POPOVER_MAX_WIDTH < 0) {
            placement = 'right';
        }

        return placement;
    };

    const effectivePlacement = getEffectivePlacement();

    // Calculate popover position
    const getPopoverStyle = (): React.CSSProperties => {
        if (currentStep.type === 'modal' || !spotlightRect) {
            return {
                position: 'fixed',
                top: '50%',
                left: '50%',
                transform: 'translate(-50%, -50%)',
                zIndex: 10002,
                maxWidth: '500px',
                width: 'calc(100% - 32px)',
            };
        }

        const placement = effectivePlacement;
        const popoverGap = 24;
        const styles: React.CSSProperties = {
            position: 'fixed',
            zIndex: 10002,
            maxWidth: '400px',
        };

        switch (placement) {
            case 'right':
                styles.top = `${spotlightRect.y + spotlightRect.height / 2}px`;
                styles.left = `${spotlightRect.x + spotlightRect.width + popoverGap}px`;
                styles.transform = 'translateY(-50%)';
                break;
            case 'left':
                styles.top = `${spotlightRect.y + spotlightRect.height / 2}px`;
                styles.right = `${window.innerWidth - spotlightRect.x + popoverGap}px`;
                styles.transform = 'translateY(-50%)';
                break;
            case 'bottom':
                styles.top = `${spotlightRect.y + spotlightRect.height + popoverGap}px`;
                styles.left = `${spotlightRect.x + spotlightRect.width / 2}px`;
                styles.transform = 'translateX(-50%)';
                break;
            case 'top':
                styles.bottom = `${window.innerHeight - spotlightRect.y + popoverGap}px`;
                styles.left = `${spotlightRect.x + spotlightRect.width / 2}px`;
                styles.transform = 'translateX(-50%)';
                break;
            default:
                styles.top = '50%';
                styles.left = '50%';
                styles.transform = 'translate(-50%, -50%)';
        }

        return styles;
    };

    // Calculate arrow position and path
    const getArrowPath = (): { path: string; visible: boolean } => {
        if (!isSpotlight || !spotlightRect || !popoverRef.current) {
            return { path: '', visible: false };
        }

        const placement = effectivePlacement;
        const popoverRect = popoverRef.current.getBoundingClientRect();

        let startX: number, startY: number, endX: number, endY: number;
        let ctrlX1: number, ctrlY1: number, ctrlX2: number, ctrlY2: number;

        switch (placement) {
            case 'right':
                startX = spotlightRect.x + spotlightRect.width;
                startY = spotlightRect.y + spotlightRect.height / 2;
                endX = popoverRect.left;
                endY = popoverRect.top + popoverRect.height / 2;
                ctrlX1 = startX + 12;
                ctrlY1 = startY;
                ctrlX2 = endX - 12;
                ctrlY2 = endY;
                break;
            case 'left':
                startX = spotlightRect.x;
                startY = spotlightRect.y + spotlightRect.height / 2;
                endX = popoverRect.right;
                endY = popoverRect.top + popoverRect.height / 2;
                ctrlX1 = startX - 12;
                ctrlY1 = startY;
                ctrlX2 = endX + 12;
                ctrlY2 = endY;
                break;
            case 'bottom':
                startX = spotlightRect.x + spotlightRect.width / 2;
                startY = spotlightRect.y + spotlightRect.height;
                endX = popoverRect.left + popoverRect.width / 2;
                endY = popoverRect.top;
                ctrlX1 = startX;
                ctrlY1 = startY + 12;
                ctrlX2 = endX;
                ctrlY2 = endY - 12;
                break;
            case 'top':
                startX = spotlightRect.x + spotlightRect.width / 2;
                startY = spotlightRect.y;
                endX = popoverRect.left + popoverRect.width / 2;
                endY = popoverRect.bottom;
                ctrlX1 = startX;
                ctrlY1 = startY - 12;
                ctrlX2 = endX;
                ctrlY2 = endY + 12;
                break;
            default:
                return { path: '', visible: false };
        }

        return {
            path: `M ${startX} ${startY} C ${ctrlX1} ${ctrlY1}, ${ctrlX2} ${ctrlY2}, ${endX} ${endY}`,
            visible: true,
        };
    };

    const arrowData = getArrowPath();

    return (
        <>
            {/* SVG Overlay with cutout */}
            <svg
                className="fixed inset-0 z-[10000] pointer-events-none"
                style={{ width: '100vw', height: '100vh' }}
            >
                <defs>
                    {/* Glow filter for spotlight border */}
                    <filter id="spotlight-glow" x="-50%" y="-50%" width="200%" height="200%">
                        <feGaussianBlur stdDeviation="4" result="blur" />
                        <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                    {/* Animated gradient for arrow */}
                    <linearGradient id="arrow-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stopColor="rgb(251, 191, 36)" stopOpacity="0.3" />
                        <stop offset="50%" stopColor="rgb(251, 191, 36)" stopOpacity="1" />
                        <stop offset="100%" stopColor="rgb(251, 191, 36)" stopOpacity="0.3" />
                    </linearGradient>
                </defs>

                {/* Dark overlay with cutout */}
                <path
                    d={generateOverlayPath()}
                    fill="rgba(0, 0, 0, 0.75)"
                    fillRule="evenodd"
                    className="transition-all duration-300 ease-out"
                    style={{ pointerEvents: 'auto' }}
                    onClick={() => currentStep.type === 'modal' && skipTour()}
                />

                {/* Spotlight border glow */}
                {isSpotlight && spotlightRect && (
                    <rect
                        x={spotlightRect.x}
                        y={spotlightRect.y}
                        width={spotlightRect.width}
                        height={spotlightRect.height}
                        rx={SPOTLIGHT_BORDER_RADIUS}
                        ry={SPOTLIGHT_BORDER_RADIUS}
                        fill="none"
                        stroke="rgb(251, 191, 36)"
                        strokeWidth="3"
                        filter="url(#spotlight-glow)"
                        className="animate-spotlight-pulse transition-all duration-300 ease-out"
                    />
                )}

                {/* Connecting arrow */}
                {arrowData.visible && (
                    <path
                        d={arrowData.path}
                        fill="none"
                        stroke="url(#arrow-gradient)"
                        strokeWidth="2"
                        strokeDasharray="6 4"
                        className="animate-arrow-dash"
                    />
                )}
            </svg>

            {/* Clickable spotlight zone for nextOnClick steps */}
            {isSpotlight && spotlightRect && currentStep.nextOnClick && (
                <div
                    className="fixed z-[10001] cursor-pointer"
                    style={{
                        left: spotlightRect.x,
                        top: spotlightRect.y,
                        width: spotlightRect.width,
                        height: spotlightRect.height,
                        borderRadius: SPOTLIGHT_BORDER_RADIUS,
                    }}
                    onClick={nextStep}
                >
                    {/* Pulsing click hint */}
                    <div className="absolute inset-0 rounded-xl animate-click-hint pointer-events-none" />
                </div>
            )}

            {/* Popover content */}
            <div
                ref={popoverRef}
                style={getPopoverStyle()}
                className={`bg-gradient-to-br from-gray-900 via-gray-900 to-gray-850 border border-gray-700/80 rounded-2xl shadow-2xl w-full mx-4 
                    ${isTransitioning ? 'opacity-0 scale-95' : 'opacity-100 scale-100'}
                    transition-all duration-300 ease-out`}
            >
                {/* Decorative top accent */}
                <div className="absolute -top-px left-6 right-6 h-px bg-gradient-to-r from-transparent via-primary/50 to-transparent" />

                {/* Header */}
                <div className="p-5 pb-4">
                    <div className="flex items-start justify-between gap-4">
                        <div className="flex-1 min-w-0">
                            <h3 className="text-lg font-bold text-white leading-tight mb-1">
                                {currentStep.title}
                            </h3>
                            <div className="flex items-center gap-2 text-xs text-gray-400">
                                <span>Step {currentStepIndex + 1} of {currentTour.steps.length}</span>
                                {isFirstStep && (
                                    <span className="text-gray-500">• Use arrow keys to navigate</span>
                                )}
                            </div>
                        </div>
                        <button
                            onClick={skipTour}
                            className="p-1.5 hover:bg-gray-800 rounded-lg transition-colors flex-shrink-0"
                            title="Skip tour (Esc)"
                        >
                            <X className="w-4 h-4 text-gray-500 hover:text-gray-300" />
                        </button>
                    </div>
                </div>

                {/* Content */}
                <div className="px-5 pb-4">
                    {currentStep.image && (
                        <img
                            src={currentStep.image}
                            alt={currentStep.title}
                            className="w-full rounded-lg mb-4 border border-gray-800"
                        />
                    )}
                    <p className="text-gray-300 text-sm whitespace-pre-line leading-relaxed">
                        {currentStep.content}
                    </p>

                    {/* Action hint for interactive steps */}
                    {currentStep.nextOnClick && (
                        <div className="mt-4 p-3 bg-primary/10 border border-primary/30 rounded-lg">
                            <p className="text-sm font-medium text-primary flex items-center gap-2">
                                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                                Click the highlighted element to continue
                            </p>
                        </div>
                    )}

                    {currentStep.actions && currentStep.actions.length > 0 && !currentStep.nextOnClick && (
                        <div className="mt-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg">
                            <p className="text-sm font-medium text-blue-300 mb-2">Try this:</p>
                            <ul className="text-sm text-blue-200/80 space-y-1">
                                {currentStep.actions.map((action, index) => (
                                    <li key={index} className="flex items-start gap-2">
                                        <span className="text-primary mt-0.5">→</span>
                                        <span>{action}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Footer with navigation */}
                <div className="px-5 pb-5 pt-2 flex items-center justify-between gap-4">
                    {/* Step indicators */}
                    <div className="flex items-center gap-1.5">
                        {currentTour.steps.map((_, index) => (
                            <div
                                key={index}
                                className={`w-2 h-2 rounded-full transition-all duration-300 ${
                                    index === currentStepIndex
                                        ? 'bg-primary w-6'
                                        : index < currentStepIndex
                                        ? 'bg-primary/40'
                                        : 'bg-gray-700'
                                }`}
                            />
                        ))}
                    </div>

                    {/* Navigation buttons */}
                    <div className="flex items-center gap-2">
                        <button
                            onClick={previousStep}
                            disabled={isFirstStep}
                            className={`p-2 rounded-lg transition-colors ${
                                isFirstStep
                                    ? 'text-gray-600 cursor-not-allowed'
                                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                            }`}
                            title="Previous (←)"
                        >
                            <ChevronLeft className="w-5 h-5" />
                        </button>

                        {!currentStep.nextOnClick ? (
                            <button
                                onClick={nextStep}
                                className="px-5 py-2 text-sm font-bold bg-primary text-gray-900 rounded-lg hover:bg-primary/90 transition-all shadow-lg shadow-primary/20 flex items-center gap-1.5"
                            >
                                {isLastStep ? 'Finish' : 'Next'}
                                {!isLastStep && <ChevronRight className="w-4 h-4" />}
                            </button>
                        ) : (
                            <button
                                onClick={skipTour}
                                className="px-4 py-2 text-sm font-medium text-gray-400 hover:text-white rounded-lg hover:bg-gray-800 transition-colors"
                            >
                                Skip
                            </button>
                        )}
                    </div>
                </div>

                {/* Progress bar */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-gray-800 rounded-b-2xl overflow-hidden">
                    <div
                        className="h-full bg-gradient-to-r from-primary to-primary-light transition-all duration-500 ease-out"
                        style={{ width: `${progress}%` }}
                    />
                </div>
            </div>

            {/* CSS animations */}
            <style>{`
                @keyframes spotlight-pulse {
                    0%, 100% {
                        opacity: 1;
                        stroke-width: 3;
                    }
                    50% {
                        opacity: 0.7;
                        stroke-width: 4;
                    }
                }

                @keyframes arrow-dash {
                    0% {
                        stroke-dashoffset: 20;
                    }
                    100% {
                        stroke-dashoffset: 0;
                    }
                }

                @keyframes click-hint {
                    0%, 100% {
                        box-shadow: inset 0 0 0 2px rgba(251, 191, 36, 0.3);
                    }
                    50% {
                        box-shadow: inset 0 0 0 4px rgba(251, 191, 36, 0.5);
                    }
                }

                .animate-spotlight-pulse {
                    animation: spotlight-pulse 2s ease-in-out infinite;
                }

                .animate-arrow-dash {
                    animation: arrow-dash 1s linear infinite;
                }

                .animate-click-hint {
                    animation: click-hint 1.5s ease-in-out infinite;
                }
            `}</style>
        </>
    );
};
