import React, { useState, useMemo, useRef, useEffect } from 'react';
import { 
  Search, 
  GraduationCap, 
  LineChart, 
  FlaskConical, 
  Gem, 
  ShieldCheck,
  X
} from 'lucide-react';
import { 
  CATEGORY_INFO, 
  EDUCATION_TOPICS, 
  getTopicsByCategory,
  searchTopics,
} from '../../data/education/topics';
import type { TopicCategory, EducationTopic } from '../../data/education/topics';
import TopicCard from './TopicCard';

interface EducationCenterProps {
  onClose?: () => void;
}

const CATEGORY_ICONS: Record<TopicCategory, React.ReactNode> = {
  graphs: <LineChart className="w-5 h-5" />,
  methods: <FlaskConical className="w-5 h-5" />,
  commodities: <Gem className="w-5 h-5" />,
  qaqc: <ShieldCheck className="w-5 h-5" />
};

export const EducationCenter: React.FC<EducationCenterProps> = ({ onClose }) => {
  const [activeCategory, setActiveCategory] = useState<TopicCategory>('qaqc');
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedTopicId, setHighlightedTopicId] = useState<string | null>(null);
  const topicRefs = useRef<Record<string, HTMLDivElement | null>>({});

  // Get topics based on search or category
  const displayedTopics = useMemo(() => {
    if (searchQuery.trim()) {
      return searchTopics(searchQuery);
    }
    return getTopicsByCategory(activeCategory);
  }, [searchQuery, activeCategory]);

  // Group search results by category
  const groupedSearchResults = useMemo(() => {
    if (!searchQuery.trim()) return null;
    
    const grouped: Record<TopicCategory, EducationTopic[]> = {
      graphs: [],
      methods: [],
      commodities: [],
      qaqc: []
    };
    
    displayedTopics.forEach(topic => {
      grouped[topic.category].push(topic);
    });
    
    return grouped;
  }, [searchQuery, displayedTopics]);

  // Navigate to a related topic
  const handleNavigateToTopic = (topicId: string) => {
    const topic = EDUCATION_TOPICS.find(t => t.id === topicId);
    if (topic) {
      setSearchQuery('');
      setActiveCategory(topic.category);
      setHighlightedTopicId(topicId);
      
      // Scroll to the topic after a short delay for state to update
      setTimeout(() => {
        const element = topicRefs.current[topicId];
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }, 100);
    }
  };

  // Clear highlight after animation
  useEffect(() => {
    if (highlightedTopicId) {
      const timer = setTimeout(() => setHighlightedTopicId(null), 2000);
      return () => clearTimeout(timer);
    }
  }, [highlightedTopicId]);

  return (
    <div className="min-h-screen bg-background-dark">
      {/* Header */}
      <div className="sticky top-0 z-10 bg-surface-dark/95 backdrop-blur-sm border-b border-secondary-dark">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-primary/20">
                <GraduationCap className="w-6 h-6 text-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-slate-50">Education Center</h1>
                <p className="text-sm text-slate-400">Learn about QAQC concepts, methods, and best practices</p>
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

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500" />
            <input
              type="text"
              placeholder="Search topics..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="
                w-full pl-10 pr-4 py-3 rounded-lg
                bg-surface-light border border-secondary-dark
                text-slate-50 placeholder-slate-500
                focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary
                transition-colors
              "
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-3 top-1/2 -translate-y-1/2 p-1 rounded hover:bg-surface-dark text-slate-500 hover:text-slate-300"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Category Tabs - Only show when not searching */}
        {!searchQuery && (
          <div className="max-w-6xl mx-auto px-6">
            <div className="flex gap-1 border-b border-transparent">
              {(Object.keys(CATEGORY_INFO) as TopicCategory[]).map((category) => (
                <button
                  key={category}
                  onClick={() => setActiveCategory(category)}
                  className={`
                    flex items-center gap-2 px-4 py-3 rounded-t-lg
                    font-medium text-sm transition-all
                    ${activeCategory === category
                      ? 'bg-surface text-slate-50 border-t border-x border-secondary-dark -mb-px'
                      : 'text-slate-400 hover:text-slate-300 hover:bg-surface-light/50'
                    }
                  `}
                >
                  {CATEGORY_ICONS[category]}
                  {CATEGORY_INFO[category].label}
                  <span className={`
                    px-2 py-0.5 rounded-full text-xs
                    ${activeCategory === category
                      ? 'bg-primary/20 text-primary'
                      : 'bg-surface-dark text-slate-500'
                    }
                  `}>
                    {getTopicsByCategory(category).length}
                  </span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Search Results */}
        {searchQuery && groupedSearchResults && (
          <div className="space-y-8">
            {displayedTopics.length === 0 ? (
              <div className="text-center py-16">
                <Search className="w-12 h-12 text-slate-600 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-slate-400">No topics found</h3>
                <p className="text-sm text-slate-500 mt-1">
                  Try a different search term or browse by category
                </p>
              </div>
            ) : (
              <>
                <p className="text-sm text-slate-400">
                  Found {displayedTopics.length} topic{displayedTopics.length !== 1 ? 's' : ''} matching "{searchQuery}"
                </p>
                {(Object.keys(groupedSearchResults) as TopicCategory[]).map((category) => {
                  const topics = groupedSearchResults[category];
                  if (topics.length === 0) return null;
                  
                  return (
                    <div key={category}>
                      <div className="flex items-center gap-2 mb-4">
                        {CATEGORY_ICONS[category]}
                        <h2 className="text-lg font-semibold text-slate-300">
                          {CATEGORY_INFO[category].label}
                        </h2>
                        <span className="px-2 py-0.5 rounded-full text-xs bg-surface-light text-slate-400">
                          {topics.length}
                        </span>
                      </div>
                      <div className="grid gap-4 md:grid-cols-2">
                        {topics.map((topic) => (
                          <div
                            key={topic.id}
                            ref={(el) => { topicRefs.current[topic.id] = el; }}
                          >
                            <TopicCard
                              topic={topic}
                              onNavigateToTopic={handleNavigateToTopic}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </>
            )}
          </div>
        )}

        {/* Category View */}
        {!searchQuery && (
          <>
            {/* Category Description */}
            <div className="mb-6 p-4 rounded-lg bg-surface border border-secondary-dark">
              <div className="flex items-center gap-3">
                <div className="p-2 rounded-lg bg-primary/10">
                  {CATEGORY_ICONS[activeCategory]}
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-slate-50">
                    {CATEGORY_INFO[activeCategory].label}
                  </h2>
                  <p className="text-sm text-slate-400">
                    {CATEGORY_INFO[activeCategory].description}
                  </p>
                </div>
              </div>
            </div>

            {/* Topic Cards Grid */}
            <div className="grid gap-4 md:grid-cols-2">
              {displayedTopics.map((topic) => (
                <div
                  key={topic.id}
                  ref={(el) => { topicRefs.current[topic.id] = el; }}
                  className={`
                    transition-all duration-500
                    ${highlightedTopicId === topic.id
                      ? 'ring-2 ring-primary ring-offset-2 ring-offset-background-dark rounded-xl'
                      : ''
                    }
                  `}
                >
                  <TopicCard
                    topic={topic}
                    onNavigateToTopic={handleNavigateToTopic}
                  />
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default EducationCenter;
