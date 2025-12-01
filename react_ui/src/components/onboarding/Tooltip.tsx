import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, X } from 'lucide-react';
import type { TooltipConfig } from '../../types/onboarding';
import { useOnboardingStore } from '../../stores/onboardingStore';

interface TooltipProps {
    config: TooltipConfig;
}

export const Tooltip: React.FC<TooltipProps> = ({ config }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [position, setPosition] = useState<{ top: number; left: number } | null>(null);
    const tooltipRef = useRef<HTMLDivElement>(null);
    const triggerRef = useRef<HTMLButtonElement>(null);

    const { progress, dismissTooltip, settings } = useOnboardingStore();

    // Don't show if dismissed or tooltips disabled
    if (!settings.showTooltips || progress.dismissedTooltips.includes(config.id)) {
        return null;
    }

    const trigger = config.trigger || 'hover';
    const placement = config.placement || 'top';

    useEffect(() => {
        if (isVisible && triggerRef.current && tooltipRef.current) {
            const triggerRect = triggerRef.current.getBoundingClientRect();
            const tooltipRect = tooltipRef.current.getBoundingClientRect();

            let top = 0;
            let left = 0;

            switch (placement) {
                case 'top':
                    top = triggerRect.top - tooltipRect.height - 8;
                    left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
                    break;
                case 'bottom':
                    top = triggerRect.bottom + 8;
                    left = triggerRect.left + (triggerRect.width / 2) - (tooltipRect.width / 2);
                    break;
                case 'left':
                    top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
                    left = triggerRect.left - tooltipRect.width - 8;
                    break;
                case 'right':
                    top = triggerRect.top + (triggerRect.height / 2) - (tooltipRect.height / 2);
                    left = triggerRect.right + 8;
                    break;
            }

            setPosition({ top, left });
        }
    }, [isVisible, placement]);

    const handleTrigger = () => {
        if (trigger === 'click') {
            setIsVisible(!isVisible);
        }
    };

    const handleMouseEnter = () => {
        if (trigger === 'hover') {
            setIsVisible(true);
        }
    };

    const handleMouseLeave = () => {
        if (trigger === 'hover') {
            setIsVisible(false);
        }
    };

    const handleDismiss = () => {
        dismissTooltip(config.id);
        setIsVisible(false);
    };

    return (
        <>
            <button
                ref={triggerRef}
                onClick={handleTrigger}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                onFocus={handleMouseEnter}
                onBlur={handleMouseLeave}
                className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-primary/20 hover:bg-primary/30 text-primary transition-colors cursor-help"
                aria-label="Help"
            >
                <HelpCircle className="w-3.5 h-3.5" />
            </button>

            {isVisible && (
                <div
                    ref={tooltipRef}
                    style={position ? { position: 'fixed', ...position } : { position: 'absolute', opacity: 0 }}
                    className="z-50 animate-tooltip-in"
                    onMouseEnter={trigger === 'hover' ? () => setIsVisible(true) : undefined}
                    onMouseLeave={trigger === 'hover' ? () => setIsVisible(false) : undefined}
                >
                    <div className="bg-gray-900 border border-gray-700 rounded-lg shadow-xl p-4 max-w-xs">
                        {config.title && (
                            <div className="flex items-start justify-between mb-2">
                                <h4 className="text-sm font-semibold text-white">{config.title}</h4>
                                {config.dismissible && (
                                    <button
                                        onClick={handleDismiss}
                                        className="p-0.5 hover:bg-gray-800 rounded transition-colors ml-2"
                                    >
                                        <X className="w-3.5 h-3.5 text-gray-400" />
                                    </button>
                                )}
                            </div>
                        )}
                        <p className="text-sm text-gray-300 leading-relaxed">{config.content}</p>

                        {/* Arrow */}
                        <div
                            className={`absolute w-2 h-2 bg-gray-900 border-gray-700 transform rotate-45 ${placement === 'top' ? 'bottom-[-5px] left-1/2 -translate-x-1/2 border-b border-r' :
                                    placement === 'bottom' ? 'top-[-5px] left-1/2 -translate-x-1/2 border-t border-l' :
                                        placement === 'left' ? 'right-[-5px] top-1/2 -translate-y-1/2 border-t border-r' :
                                            'left-[-5px] top-1/2 -translate-y-1/2 border-b border-l'
                                }`}
                        />
                    </div>
                </div>
            )}

            <style>{`
        @keyframes tooltip-in {
          from {
            opacity: 0;
            transform: translateY(-4px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-tooltip-in {
          animation: tooltip-in 0.2s ease-out;
        }
      `}</style>
        </>
    );
};
