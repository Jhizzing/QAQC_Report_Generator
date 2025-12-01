import React, { useState } from 'react';
import { GraduationCap, Sparkles, X, Book, Layout } from 'lucide-react';
import { useOnboardingStore } from '../../stores/onboardingStore';
import { APP_WORKFLOW_TOUR, TEMPLATE_EDITOR_TOUR } from '../../data/tours';

export const WelcomeModal: React.FC = () => {
    const { settings, updateSettings, startTour } = useOnboardingStore();
    const [selectedTour, setSelectedTour] = useState<string | null>(null);

    if (settings.hasSeenWelcome) return null;

    const handleStartTour = (tourId: string) => {
        const tour = tourId === 'app-workflow' ? APP_WORKFLOW_TOUR : TEMPLATE_EDITOR_TOUR;
        updateSettings({ hasSeenWelcome: true });
        startTour(tour);
    };

    const handleSkip = () => {
        updateSettings({ hasSeenWelcome: true });
    };

    return (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-[10003] flex items-center justify-center p-4">
            <div className="bg-gradient-to-br from-gray-900 via-gray-900 to-gray-800 border border-gray-700 rounded-2xl shadow-2xl max-w-2xl w-full overflow-hidden animate-scale-in">
                {/* Header with gradient */}
                <div className="relative bg-gradient-to-r from-primary/20 to-purple-500/20 p-8 border-b border-gray-700">
                    <button
                        onClick={handleSkip}
                        className="absolute top-4 right-4 p-2 hover:bg-gray-800/50 rounded-lg transition-colors"
                    >
                        <X className="w-5 h-5 text-gray-400" />
                    </button>

                    <div className="flex items-center gap-4 mb-4">
                        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary to-primary-dark flex items-center justify-center shadow-lg shadow-primary/30">
                            <GraduationCap className="w-8 h-8 text-gray-900" />
                        </div>
                        <div>
                            <h2 className="text-3xl font-bold text-white">Welcome to LogiQore</h2>
                            <p className="text-gray-300 text-sm mt-1">QAQC Reporter for Geological Data</p>
                        </div>
                    </div>

                    <p className="text-gray-300 leading-relaxed">
                        Let's get you started with a quick guided tour! Choose which part of the application you'd like to explore first.
                    </p>
                </div>

                {/* Tour selection cards */}
                <div className="p-8 space-y-4">
                    <TourCard
                        id="app-workflow"
                        icon={<Book className="w-6 h-6" />}
                        title="App Workflow Tour"
                        description="Learn the complete workflow: create projects, import data, run analysis, and generate reports"
                        duration="~3 minutes"
                        isSelected={selectedTour === 'app-workflow'}
                        onSelect={() => setSelectedTour('app-workflow')}
                    />

                    <TourCard
                        id="template-editor"
                        icon={<Layout className="w-6 h-6" />}
                        title="Template Editor Tour"
                        description="Master the template editor: create custom report templates with sections, blocks, and data bindings"
                        duration="~2 minutes"
                        isSelected={selectedTour === 'template-editor'}
                        onSelect={() => setSelectedTour('template-editor')}
                    />
                </div>

                {/* Footer */}
                <div className="p-8 pt-0 flex items-center justify-between">
                    <button
                        onClick={handleSkip}
                        className="text-sm text-gray-400 hover:text-white transition-colors"
                    >
                        Skip for now
                    </button>

                    <button
                        onClick={() => selectedTour && handleStartTour(selectedTour)}
                        disabled={!selectedTour}
                        className="px-8 py-3 bg-primary text-gray-900 rounded-xl font-bold hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg shadow-primary/20 flex items-center gap-2"
                    >
                        <Sparkles className="w-4 h-4" />
                        Start Tour
                    </button>
                </div>
            </div>

            <style>{`
        @keyframes scale-in {
          from {
            opacity: 0;
            transform: scale(0.95);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }

        .animate-scale-in {
          animation: scale-in 0.3s ease-out;
        }
      `}</style>
        </div>
    );
};

interface TourCardProps {
    id: string;
    icon: React.ReactNode;
    title: string;
    description: string;
    duration: string;
    isSelected: boolean;
    onSelect: () => void;
}

const TourCard: React.FC<TourCardProps> = ({
    icon,
    title,
    description,
    duration,
    isSelected,
    onSelect,
}) => {
    return (
        <button
            onClick={onSelect}
            className={`w-full p-6 rounded-xl border-2 transition-all text-left ${isSelected
                    ? 'border-primary bg-primary/5 shadow-lg shadow-primary/10'
                    : 'border-gray-700 hover:border-gray-600 bg-gray-800/50'
                }`}
        >
            <div className="flex items-start gap-4">
                <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${isSelected ? 'bg-primary text-gray-900' : 'bg-gray-700 text-gray-400'
                    }`}>
                    {icon}
                </div>

                <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                        <h3 className={`text-lg font-bold ${isSelected ? 'text-primary' : 'text-white'}`}>
                            {title}
                        </h3>
                        <span className="text-xs text-gray-400 bg-gray-700 px-2 py-1 rounded">
                            {duration}
                        </span>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed">{description}</p>
                </div>

                <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${isSelected ? 'border-primary bg-primary' : 'border-gray-600'
                    }`}>
                    {isSelected && <div className="w-2.5 h-2.5 rounded-full bg-gray-900" />}
                </div>
            </div>
        </button>
    );
};
