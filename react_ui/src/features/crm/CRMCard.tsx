import React, { useState } from 'react';
import { ChevronDown, ChevronUp, Award, ExternalLink } from 'lucide-react';
import type { CRMValue } from '../../data/crmDatabase';

interface CRMCardProps {
  crm: CRMValue;
  onLearnMore?: () => void;
}

export const CRMCard: React.FC<CRMCardProps> = ({ crm, onLearnMore }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const getCategoryColor = (category: string): string => {
    switch (category) {
      case 'gold':
        return 'from-amber-500/20 to-amber-600/10 border-amber-500/30';
      case 'multi-element':
        return 'from-blue-500/20 to-blue-600/10 border-blue-500/30';
      case 'pxrf':
        return 'from-emerald-500/20 to-emerald-600/10 border-emerald-500/30';
      default:
        return 'from-slate-500/20 to-slate-600/10 border-slate-500/30';
    }
  };

  const getCategoryLabel = (category: string): string => {
    switch (category) {
      case 'gold': return 'Gold';
      case 'multi-element': return 'Multi-Element';
      case 'pxrf': return 'pXRF';
      default: return category;
    }
  };

  const getCategoryBadgeColor = (category: string): string => {
    switch (category) {
      case 'gold': return 'bg-amber-500/20 text-amber-400';
      case 'multi-element': return 'bg-blue-500/20 text-blue-400';
      case 'pxrf': return 'bg-emerald-500/20 text-emerald-400';
      default: return 'bg-slate-500/20 text-slate-400';
    }
  };

  // Get primary element for display
  const primaryElement = Object.entries(crm.elements)[0];
  const elementCount = Object.keys(crm.elements).length;

  return (
    <div
      className={`
        rounded-xl border bg-gradient-to-br ${getCategoryColor(crm.category)}
        transition-all duration-300 hover:shadow-lg hover:shadow-black/20
        ${isExpanded ? 'ring-1 ring-white/10' : ''}
      `}
    >
      {/* Card Header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-4 text-left focus:outline-none focus:ring-2 focus:ring-primary/50 rounded-xl"
      >
        <div className="flex items-start gap-3">
          {/* Icon */}
          <div className="p-2 rounded-lg bg-surface-dark/50 text-amber-400">
            <Award className="w-5 h-5" />
          </div>

          {/* Title and Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <h3 className="text-base font-semibold text-slate-50">
                {crm.name}
              </h3>
              <span className={`px-2 py-0.5 text-xs rounded-full ${getCategoryBadgeColor(crm.category)}`}>
                {getCategoryLabel(crm.category)}
              </span>
            </div>
            <p className="text-sm text-slate-400">
              {crm.supplier} • {crm.matrix}
            </p>
            {/* Quick preview of primary element */}
            {primaryElement && (
              <p className="text-sm text-slate-300 mt-1">
                <span className="font-medium">{primaryElement[0]}:</span>{' '}
                {primaryElement[1].certified} {primaryElement[1].unit}
                {primaryElement[1].uncertainty && (
                  <span className="text-slate-500"> ±{primaryElement[1].uncertainty}</span>
                )}
                {elementCount > 1 && (
                  <span className="text-slate-500 ml-2">+{elementCount - 1} more</span>
                )}
              </p>
            )}
          </div>

          {/* Expand Icon */}
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
        <div className="px-4 pb-4 pt-0 border-t border-white/5">
          {/* All Elements Table */}
          <div className="mt-4">
            <h4 className="text-sm font-medium text-slate-300 mb-2">Certified Values</h4>
            <div className="bg-surface-dark/30 rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-white/5">
                    <th className="text-left px-3 py-2 text-slate-400 font-medium">Element</th>
                    <th className="text-right px-3 py-2 text-slate-400 font-medium">Value</th>
                    <th className="text-right px-3 py-2 text-slate-400 font-medium">±2SD</th>
                    <th className="text-left px-3 py-2 text-slate-400 font-medium">Method</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(crm.elements).map(([element, data]) => (
                    <tr key={element} className="border-b border-white/5 last:border-0">
                      <td className="px-3 py-2 text-slate-200 font-medium">{element}</td>
                      <td className="px-3 py-2 text-right text-slate-300">
                        {data.certified} {data.unit}
                      </td>
                      <td className="px-3 py-2 text-right text-slate-500">
                        {data.uncertainty ? `±${data.uncertainty}` : '-'}
                      </td>
                      <td className="px-3 py-2 text-slate-500">
                        {data.method || '-'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Notes */}
          {crm.notes && (
            <div className="mt-3 p-3 rounded-lg bg-surface-dark/30 border border-white/5">
              <p className="text-sm text-slate-400 italic">{crm.notes}</p>
            </div>
          )}

          {/* Learn More Link */}
          {onLearnMore && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onLearnMore();
              }}
              className="mt-3 flex items-center gap-1.5 text-xs text-primary hover:text-primary-light transition-colors"
            >
              <ExternalLink className="w-3 h-3" />
              Learn more about CRMs
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default CRMCard;
