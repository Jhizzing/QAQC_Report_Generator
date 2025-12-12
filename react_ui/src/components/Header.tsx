import React from 'react';
import { Save, FolderOpen } from 'lucide-react';
import { useProjectStore } from '../stores/projectStore';
import { selectProjectFile, loadProjectFromFile, type QAQCProjectFile } from '../utils/projectFile';

interface HeaderProps {
    className?: string;
    onSaveProject?: () => void;
    onProjectLoaded?: (projectFile: QAQCProjectFile) => void;
}

export const Header: React.FC<HeaderProps> = ({ className = '', onSaveProject, onProjectLoaded }) => {
    const { loadFromFile } = useProjectStore();

    const handleOpenProject = async () => {
        try {
            const file = await selectProjectFile();
            if (!file) return;

            const projectFile = await loadProjectFromFile(file);
            loadFromFile(projectFile.metadata, file.name);
            
            if (onProjectLoaded) {
                onProjectLoaded(projectFile);
            }
        } catch (error) {
            console.error('Failed to open project:', error);
            alert(error instanceof Error ? error.message : 'Failed to open project file');
        }
    };

    return (
        <header className={`bg-surface-glass backdrop-blur-md border-b border-secondary-dark sticky top-0 z-50 ${className}`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <img
                            src="/logiqore-logo.png"
                            alt="LogiQore"
                            className="h-12 transition-all duration-200 hover:scale-105 hover:drop-shadow-[0_0_12px_rgba(245,158,11,0.5)]"
                        />
                        <div>
                            <h1 className="text-xl font-bold text-slate-50 tracking-tight">
                                LogiQore QAQC Reporter
                            </h1>
                            <p className="text-sm text-slate-400 font-medium">
                                Professional Assay Quality Control Analysis
                            </p>
                        </div>
                    </div>

                    {/* Project Actions */}
                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleOpenProject}
                            className="flex items-center gap-2 px-3 py-2 text-sm text-slate-300 hover:text-white hover:bg-slate-800/50 rounded-lg transition-colors"
                            title="Open Project File"
                        >
                            <FolderOpen className="w-4 h-4" />
                            <span className="hidden sm:inline">Open</span>
                        </button>

                        {onSaveProject && (
                            <button
                                onClick={onSaveProject}
                                className="flex items-center gap-2 px-3 py-2 text-sm bg-primary/20 text-primary hover:bg-primary/30 rounded-lg transition-colors"
                                title="Save Project"
                            >
                                <Save className="w-4 h-4" />
                                <span className="hidden sm:inline">Save Project</span>
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </header>
    );
};
