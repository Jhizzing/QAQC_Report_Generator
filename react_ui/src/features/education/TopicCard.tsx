import React, { useState } from 'react';
import * as LucideIcons from 'lucide-react';
import { ChevronDown, ChevronUp, ExternalLink, HelpCircle, ListChecks, Lightbulb, FileText, Link } from 'lucide-react';
import { getTopicById } from '../../data/education/topics';
import type { EducationTopic } from '../../data/education/topics';

interface TopicCardProps {
  topic: EducationTopic;
  onNavigateToTopic?: (topicId: string) => void;
}

// Dynamic icon component - get icon by name from Lucide
const DynamicIcon: React.FC<{ name: string; className?: string }> = ({ name, className }) => {
  // Type-safe way to access Lucide icons
  const icons: Record<string, React.ComponentType<{ className?: string }>> = {
    LineChart: LucideIcons.LineChart,
    ScatterChart: LucideIcons.ScatterChart,
    TrendingUp: LucideIcons.TrendingUp,
    GitBranch: LucideIcons.GitBranch,
    BarChart3: LucideIcons.BarChart3,
    CircleDot: LucideIcons.CircleDot,
    Flame: LucideIcons.Flame,
    Zap: LucideIcons.Zap,
    Sun: LucideIcons.Sun,
    Sparkles: LucideIcons.Sparkles,
    Atom: LucideIcons.Atom,
    Gem: LucideIcons.Gem,
    CircleDollarSign: LucideIcons.CircleDollarSign,
    Star: LucideIcons.Star,
    Layers: LucideIcons.Layers,
    Hexagon: LucideIcons.Hexagon,
    Mountain: LucideIcons.Mountain,
    Battery: LucideIcons.Battery,
    Award: LucideIcons.Award,
    Square: LucideIcons.Square,
    Copy: LucideIcons.Copy,
    Percent: LucideIcons.Percent,
    ShieldCheck: LucideIcons.ShieldCheck,
    HelpCircle: LucideIcons.HelpCircle,
    Target: LucideIcons.Target,
  };
  
  const IconComponent = icons[name] || HelpCircle;
  return <IconComponent className={className} />;
};

export const TopicCard: React.FC<TopicCardProps> = ({ topic, onNavigateToTopic }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getCategoryColor = (category: string): string => {
    switch (category) {
      case 'graphs':
        return 'from-blue-500/20 to-blue-600/10 border-blue-500/30';
      case 'methods':
        return 'from-amber-500/20 to-amber-600/10 border-amber-500/30';
      case 'commodities':
        return 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30';
      case 'qaqc':
        return 'from-purple-500/20 to-purple-600/10 border-purple-500/30';
      default:
        return 'from-slate-500/20 to-slate-600/10 border-slate-500/30';
    }
  };

  const getIconColor = (category: string): string => {
    switch (category) {
      case 'graphs':
        return 'text-blue-400';
      case 'methods':
        return 'text-amber-400';
      case 'commodities':
        return 'text-emerald-400';
      case 'qaqc':
        return 'text-purple-400';
      default:
        return 'text-slate-400';
    }
  };

  return (
    <div
      className={`
        rounded-xl border bg-gradient-to-br ${getCategoryColor(topic.category)}
        transition-all duration-300 hover:shadow-lg hover:shadow-black/20
        ${isExpanded ? 'ring-1 ring-white/10' : ''}
      `}
    >
      {/* Card Header - Always visible */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-5 text-left focus:outline-none focus:ring-2 focus:ring-primary/50 rounded-xl"
      >
        <div className="flex items-start gap-4">
          {/* Icon */}
          <div className={`p-3 rounded-lg bg-surface-dark/50 ${getIconColor(topic.category)}`}>
            <DynamicIcon name={topic.icon} className="w-6 h-6" />
          </div>

          {/* Title and Summary */}
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-slate-50 mb-1">
              {topic.title}
            </h3>
            <p className="text-sm text-slate-400 line-clamp-2">
              {topic.summary}
            </p>
          </div>

          {/* Expand/Collapse Icon */}
          <div className="text-slate-500 mt-1">
            {isExpanded ? (
              <ChevronUp className="w-5 h-5" />
            ) : (
              <ChevronDown className="w-5 h-5" />
            )}
          </div>
        </div>
      </button>

      {/* Expanded Content */}
      {isExpanded && (
        <div className="px-5 pb-5 pt-0 border-t border-white/5 mt-0">
          {/* Key Points */}
          <div className="mt-4">
            <h4 className="text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
              <ListChecks className="w-4 h-4 text-slate-500" />
              Key Points
            </h4>
            <ul className="space-y-2">
              {topic.keyPoints.map((point, index) => (
                <li key={index} className="flex items-start gap-2 text-sm text-slate-400">
                  <span className="text-primary mt-1">•</span>
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* When to Use */}
          {topic.whenToUse && (
            <div className="mt-4 p-3 rounded-lg bg-surface-dark/30 border border-white/5">
              <h4 className="text-sm font-medium text-slate-300 mb-1 flex items-center gap-2">
                <Lightbulb className="w-4 h-4 text-amber-400" />
                When to Use
              </h4>
              <p className="text-sm text-slate-400">
                {topic.whenToUse}
              </p>
            </div>
          )}

          {/* Example */}
          {topic.example && (
            <div className="mt-4 p-3 rounded-lg bg-blue-500/10 border border-blue-500/20">
              <h4 className="text-sm font-medium text-blue-300 mb-1 flex items-center gap-2">
                <FileText className="w-4 h-4" />
                Example
              </h4>
              <p className="text-sm text-slate-400 italic">
                {topic.example}
              </p>
            </div>
          )}

          {/* Related Topics */}
          {topic.relatedTopics && topic.relatedTopics.length > 0 && (
            <div className="mt-4">
              <h4 className="text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
                <Link className="w-4 h-4 text-slate-500" />
                Related Topics
              </h4>
              <div className="flex flex-wrap gap-2">
                {topic.relatedTopics.map((relatedId) => {
                  const relatedTopic = getTopicById(relatedId);
                  if (!relatedTopic) return null;
                  return (
                    <button
                      key={relatedId}
                      onClick={(e) => {
                        e.stopPropagation();
                        onNavigateToTopic?.(relatedId);
                      }}
                      className="
                        inline-flex items-center gap-1 px-3 py-1.5 rounded-full
                        text-xs font-medium bg-surface-dark/50 text-slate-300
                        hover:bg-surface-light hover:text-slate-50
                        transition-colors border border-white/5
                      "
                    >
                      <DynamicIcon name={relatedTopic.icon} className="w-3 h-3" />
                      {relatedTopic.title}
                      <ExternalLink className="w-3 h-3 opacity-50" />
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TopicCard;
