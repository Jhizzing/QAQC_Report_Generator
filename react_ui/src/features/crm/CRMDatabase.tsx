import React, { useState, useMemo } from 'react';
import { Search, Database, X, Filter, Award, Beaker, Zap } from 'lucide-react';
import { CRM_DATABASE, type CRMValue } from '../../data/crmDatabase';
import { CRMCard } from './CRMCard';

type CategoryFilter = 'all' | 'gold' | 'multi-element' | 'pxrf';

interface CRMDatabaseProps {
  onClose?: () => void;
  onNavigateToEducation?: (topicId: string) => void;
}

const CATEGORY_TABS: { id: CategoryFilter; label: string; icon: React.ReactNode }[] = [
  { id: 'all', label: 'All Standards', icon: <Database className="w-4 h-4" /> },
  { id: 'gold', label: 'Gold', icon: <Award className="w-4 h-4" /> },
  { id: 'multi-element', label: 'Multi-Element', icon: <Beaker className="w-4 h-4" /> },
  { id: 'pxrf', label: 'pXRF', icon: <Zap className="w-4 h-4" /> },
];

export const CRMDatabase: React.FC<CRMDatabaseProps> = ({ onClose, onNavigateToEducation }) => {
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [elementFilter, setElementFilter] = useState<string>('');
  const [supplierFilter, setSupplierFilter] = useState<string>('');

  // Get unique suppliers for filter dropdown
  const suppliers = useMemo(() => {
    const uniqueSuppliers = [...new Set(CRM_DATABASE.map(crm => crm.supplier))];
    return uniqueSuppliers.sort();
  }, []);

  // Get unique elements for filter dropdown
  const allElements = useMemo(() => {
    const elements = new Set<string>();
    CRM_DATABASE.forEach(crm => {
      Object.keys(crm.elements).forEach(el => elements.add(el));
    });
    return [...elements].sort();
  }, []);

  // Filter CRMs (without category filter for tab counts)
  const filteredCRMsAllCategories = useMemo(() => {
    return CRM_DATABASE.filter(crm => {
      // Search filter
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchesName = crm.name.toLowerCase().includes(query);
        const matchesSupplier = crm.supplier.toLowerCase().includes(query);
        const matchesId = crm.id.toLowerCase().includes(query);
        const matchesNotes = crm.notes?.toLowerCase().includes(query);
        if (!matchesName && !matchesSupplier && !matchesId && !matchesNotes) {
          return false;
        }
      }

      // Element filter
      if (elementFilter && !crm.elements[elementFilter]) {
        return false;
      }

      // Supplier filter
      if (supplierFilter && crm.supplier !== supplierFilter) {
        return false;
      }

      return true;
    });
  }, [searchQuery, elementFilter, supplierFilter]);

  // Filter CRMs with category filter applied
  const filteredCRMs = useMemo(() => {
    if (categoryFilter === 'all') {
      return filteredCRMsAllCategories;
    }
    return filteredCRMsAllCategories.filter(crm => crm.category === categoryFilter);
  }, [categoryFilter, filteredCRMsAllCategories]);

  // Group by category for display
  const groupedCRMs = useMemo(() => {
    if (categoryFilter !== 'all') {
      return { [categoryFilter]: filteredCRMs };
    }
    
    const grouped: Record<string, CRMValue[]> = {
      gold: [],
      'multi-element': [],
      pxrf: [],
    };
    
    filteredCRMs.forEach(crm => {
      grouped[crm.category].push(crm);
    });
    
    return grouped;
  }, [filteredCRMs, categoryFilter]);

  const handleLearnMore = () => {
    onNavigateToEducation?.('standards-crms');
  };

  const clearFilters = () => {
    setSearchQuery('');
    setElementFilter('');
    setSupplierFilter('');
    setCategoryFilter('all');
  };

  const hasActiveFilters = searchQuery || elementFilter || supplierFilter || categoryFilter !== 'all';

  return (
    <div className="min-h-screen bg-background-dark">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-surface-dark/95 backdrop-blur-sm border-b border-secondary-dark">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-amber-500/20">
                <Database className="w-6 h-6 text-amber-400" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-50">CRM Database</h1>
                <p className="text-sm text-slate-400">
                  {CRM_DATABASE.length} Certified Reference Materials
                </p>
              </div>
            </div>
            {onClose && (
              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-surface-light text-slate-400 hover:text-slate-50 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          {/* Search and Filters */}
          <div className="flex flex-col md:flex-row gap-3">
            {/* Search */}
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
              <input
                type="text"
                placeholder="Search by name, ID, or supplier..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="
                  w-full pl-10 pr-4 py-2.5 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 placeholder-slate-500
                  focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                  transition-colors
                "
              />
              {searchQuery && (
                <button
                  onClick={() => setSearchQuery('')}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded hover:bg-surface-dark text-slate-500"
                >
                  <X className="w-4 h-4" />
                </button>
              )}
            </div>

            {/* Element Filter */}
            <div className="relative">
              <select
                value={elementFilter}
                onChange={(e) => setElementFilter(e.target.value)}
                className="
                  appearance-none px-4 py-2.5 pr-10 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 focus:outline-none focus:ring-2 focus:ring-primary/50
                  cursor-pointer min-w-[140px]
                "
              >
                <option value="">All Elements</option>
                {allElements.map(el => (
                  <option key={el} value={el}>{el}</option>
                ))}
              </select>
              <Filter className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
            </div>

            {/* Supplier Filter */}
            <div className="relative">
              <select
                value={supplierFilter}
                onChange={(e) => setSupplierFilter(e.target.value)}
                className="
                  appearance-none px-4 py-2.5 pr-10 rounded-lg
                  bg-surface-light border border-secondary-dark
                  text-slate-50 focus:outline-none focus:ring-2 focus:ring-primary/50
                  cursor-pointer min-w-[160px]
                "
              >
                <option value="">All Suppliers</option>
                {suppliers.map(supplier => (
                  <option key={supplier} value={supplier}>{supplier}</option>
                ))}
              </select>
              <Filter className="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none" />
            </div>

            {/* Clear Filters */}
            {hasActiveFilters && (
              <button
                onClick={clearFilters}
                className="px-4 py-2.5 rounded-lg bg-surface-light border border-secondary-dark text-slate-400 hover:text-slate-50 hover:bg-surface transition-colors"
              >
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Category Tabs */}
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex gap-1 border-b border-transparent overflow-x-auto">
            {CATEGORY_TABS.map((tab) => {
              // Calculate count from all filtered CRMs (not affected by category filter)
              const count = tab.id === 'all' 
                ? filteredCRMsAllCategories.length 
                : filteredCRMsAllCategories.filter(c => c.category === tab.id).length;
              
              return (
                <button
                  key={tab.id}
                  onClick={() => setCategoryFilter(tab.id)}
                  className={`
                    flex items-center gap-2 px-4 py-3 rounded-t-lg whitespace-nowrap
                    font-medium text-sm transition-all
                    ${categoryFilter === tab.id
                      ? 'bg-surface text-slate-50 border-t border-x border-secondary-dark -mb-px'
                      : 'text-slate-400 hover:text-slate-300 hover:bg-surface-light/50'
                    }
                  `}
                >
                  {tab.icon}
                  {tab.label}
                  <span className={`
                    px-2 py-0.5 rounded-full text-xs
                    ${categoryFilter === tab.id
                      ? 'bg-primary/20 text-primary'
                      : 'bg-surface-dark text-slate-500'
                    }
                  `}>
                    {count}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {filteredCRMs.length === 0 ? (
          <div className="text-center py-16">
            <Database className="w-12 h-12 text-slate-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-slate-400">No CRMs found</h3>
            <p className="text-sm text-slate-500 mt-1">
              Try adjusting your search or filters
            </p>
            <button
              onClick={clearFilters}
              className="mt-4 px-4 py-2 bg-primary text-slate-900 rounded-lg font-medium hover:bg-primary-light transition-colors"
            >
              Clear Filters
            </button>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(groupedCRMs).map(([category, crms]) => {
              if (crms.length === 0) return null;

              const categoryInfo = CATEGORY_TABS.find(t => t.id === category);

              return (
                <div key={category}>
                  {categoryFilter === 'all' && (
                    <div className="flex items-center gap-2 mb-4">
                      {categoryInfo?.icon}
                      <h2 className="text-lg font-semibold text-slate-300">
                        {categoryInfo?.label || category}
                      </h2>
                      <span className="px-2 py-0.5 rounded-full text-xs bg-surface-light text-slate-400">
                        {crms.length}
                      </span>
                    </div>
                  )}
                  <div className="grid gap-4 md:grid-cols-2">
                    {crms.map((crm) => (
                      <CRMCard
                        key={crm.id}
                        crm={crm}
                        onLearnMore={handleLearnMore}
                      />
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default CRMDatabase;
