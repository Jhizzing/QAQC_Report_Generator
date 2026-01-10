import React, { useState, useRef, useEffect } from 'react';
import { HelpCircle, ExternalLink, X } from 'lucide-react';
import { getTopicById } from '../../data/education/topics';

interface HelpTooltipProps {
  /** The education topic ID to display */
  topicId: string;
  /** Optional custom summary to override the topic's summary */
  customSummary?: string;
  /** Size of the help icon */
  size?: 'sm' | 'md' | 'lg';
  /** Callback when "Learn more" is clicked */
  onLearnMore?: (topicId: string) => void;
}

export const HelpTooltip: React.FC<HelpTooltipProps> = ({
  topicId,
  customSummary,
  size = 'sm',
  onLearnMore
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [position, setPosition] = useState<'top' | 'bottom'>('bottom');
  const triggerRef = useRef<HTMLButtonElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);

  const topic = getTopicById(topicId);

  // Calculate position based on viewport
  useEffect(() => {
    if (isOpen && triggerRef.current) {
      const rect = triggerRef.current.getBoundingClientRect();
      const spaceBelow = window.innerHeight - rect.bottom;
      const spaceAbove = rect.top;
      
      // Prefer bottom, but use top if not enough space below
      setPosition(spaceBelow < 200 && spaceAbove > spaceBelow ? 'top' : 'bottom');
    }
  }, [isOpen]);

  // Close on click outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        tooltipRef.current &&
        !tooltipRef.current.contains(event.target as Node) &&
        triggerRef.current &&
        !triggerRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen]);

  if (!topic) {
    console.warn(`HelpTooltip: Topic "${topicId}" not found`);
    return null;
  }

  const iconSizes = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6'
  };

  const summary = customSummary || topic.summary;

  return (
    <div className="relative inline-flex">
      {/* Trigger Button */}
      <button
        ref={triggerRef}
        onClick={() => setIsOpen(!isOpen)}
        onMouseEnter={() => setIsOpen(true)}
        className={`
          p-1 rounded-full transition-colors
          text-slate-500 hover:text-primary hover:bg-primary/10
          focus:outline-none focus:ring-2 focus:ring-primary/50
        `}
        aria-label={`Help: ${topic.title}`}
        aria-expanded={isOpen}
      >
        <HelpCircle className={iconSizes[size]} />
      </button>

      {/* Tooltip Popover */}
      {isOpen && (
        <div
          ref={tooltipRef}
          onMouseLeave={() => setIsOpen(false)}
          className={`
            absolute z-50 w-80
            ${position === 'bottom' ? 'top-full mt-2' : 'bottom-full mb-2'}
            left-1/2 -translate-x-1/2
          `}
        >
          {/* Arrow */}
          <div
            className={`
              absolute left-1/2 -translate-x-1/2 w-3 h-3
              bg-surface rotate-45 border-secondary-dark
              ${position === 'bottom'
                ? '-top-1.5 border-l border-t'
                : '-bottom-1.5 border-r border-b'
              }
            `}
          />

          {/* Content */}
          <div className="relative bg-surface border border-secondary-dark rounded-lg shadow-xl shadow-black/30 overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 bg-surface-light border-b border-secondary-dark">
              <h4 className="font-medium text-slate-50 text-sm">
                {topic.title}
              </h4>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded hover:bg-surface-dark text-slate-500 hover:text-slate-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Summary */}
            <div className="px-4 py-3">
              <p className="text-sm text-slate-400 leading-relaxed">
                {summary}
              </p>

              {/* Key Points Preview (first 2) */}
              {topic.keyPoints.length > 0 && (
                <ul className="mt-3 space-y-1">
                  {topic.keyPoints.slice(0, 2).map((point, index) => (
                    <li key={index} className="flex items-start gap-2 text-xs text-slate-500">
                      <span className="text-primary mt-0.5">•</span>
                      <span className="line-clamp-1">{point}</span>
                    </li>
                  ))}
                  {topic.keyPoints.length > 2 && (
                    <li className="text-xs text-slate-600 italic pl-4">
                      +{topic.keyPoints.length - 2} more points...
                    </li>
                  )}
                </ul>
              )}
            </div>

            {/* Footer - Learn More */}
            <div className="px-4 py-2 bg-surface-dark/50 border-t border-secondary-dark">
              <button
                onClick={() => {
                  setIsOpen(false);
                  onLearnMore?.(topicId);
                }}
                className="
                  flex items-center gap-2 text-xs font-medium
                  text-primary hover:text-primary-light
                  transition-colors
                "
              >
                <ExternalLink className="w-3 h-3" />
                Learn more in Education Center
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default HelpTooltip;
