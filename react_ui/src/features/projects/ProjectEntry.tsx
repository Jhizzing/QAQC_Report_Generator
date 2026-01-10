import React, { useState } from 'react';
import { Plus, FolderOpen, ArrowRight, ShieldCheck, Loader2, AlertCircle, ChevronDown } from 'lucide-react';
import { useProjectStore } from '../../stores/projectStore';
import { selectProjectFile, loadProjectFromFile, type QAQCProjectFile } from '../../utils/projectFile';

interface ProjectEntryProps {
    /** Callback when a project file is loaded - passes the full project state */
    onProjectLoaded?: (projectFile: QAQCProjectFile) => void;
}

// Common commodities for quick selection
const COMMON_COMMODITIES = [
    { value: 'Au', label: 'Gold (Au)' },
    { value: 'Cu', label: 'Copper (Cu)' },
    { value: 'Cu-Au', label: 'Copper-Gold (Cu-Au)' },
    { value: 'Ag', label: 'Silver (Ag)' },
    { value: 'Zn-Pb', label: 'Zinc-Lead (Zn-Pb)' },
    { value: 'Ni', label: 'Nickel (Ni)' },
    { value: 'Fe', label: 'Iron Ore (Fe)' },
    { value: 'Li', label: 'Lithium (Li)' },
];

export const ProjectEntry: React.FC<ProjectEntryProps> = ({ onProjectLoaded }) => {
    const { createProject, recentProjects, openProject, loadFromFile } = useProjectStore();
    const [mode, setMode] = useState<'select' | 'create'>('select');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [showCommodityDropdown, setShowCommodityDropdown] = useState(false);

    // Form State - simplified (removed campaign)
    const [formData, setFormData] = useState({
        name: '',
        deposit: '',
        commodity: ''
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.name && formData.deposit && formData.commodity) {
            createProject(formData);
        }
    };

    const handleCommoditySelect = (value: string) => {
        setFormData({ ...formData, commodity: value });
        setShowCommodityDropdown(false);
    };

    const handleOpenProjectFile = async () => {
        setError(null);
        
        try {
            const file = await selectProjectFile();
            if (!file) return;
            
            setIsLoading(true);
            
            const projectFile = await loadProjectFromFile(file);
            loadFromFile(projectFile.metadata, file.name);
            
            if (onProjectLoaded) {
                onProjectLoaded(projectFile);
            }
            
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to open project file');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background-dark flex items-center justify-center p-6">
            <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">

                <div className="flex flex-col justify-center space-y-6">
                    <div className="flex items-center gap-4">
                        <img
                            src="/logiqore-logo.png"
                            alt="LogiQore"
                            className="h-20 transition-all duration-200 hover:scale-105 hover:drop-shadow-[0_0_12px_rgba(251,191,36,0.5)]"
                        />
                        <h1 className="text-3xl font-bold text-slate-50 tracking-tight">LogiQore QAQC Reporter</h1>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-4xl font-extrabold text-slate-50 leading-tight">
                            Secure, Intelligent <br />
                            <span className="text-primary">QAQC Analysis</span>
                        </h2>
                        <p className="text-lg text-slate-400 max-w-md">
                            Start a new session to analyze your assay data locally. Your data never leaves this device.
                        </p>
                    </div>

                    <div className="pt-8 border-t border-secondary-dark">
                        <p className="text-sm font-medium text-slate-400 uppercase tracking-wider mb-4">Recent Sessions</p>
                        <div className="space-y-3">
                            {recentProjects.length === 0 ? (
                                <p className="text-sm text-slate-500 italic">No recent projects found.</p>
                            ) : (
                                recentProjects.slice(0, 3).map(project => (
                                    <button
                                        key={project.id}
                                        onClick={() => openProject(project)}
                                        className="w-full flex items-center justify-between p-4 bg-surface border border-secondary-dark rounded-xl hover:border-primary transition-all group text-left"
                                    >
                                        <div>
                                            <h3 className="font-semibold text-slate-50 group-hover:text-primary transition-colors">
                                                {project.name}
                                            </h3>
                                            <p className="text-xs text-slate-400 mt-1">
                                                {project.deposit} • {project.commodity}
                                            </p>
                                        </div>
                                        <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-primary group-hover:translate-x-1 transition-all" />
                                    </button>
                                ))
                            )}
                        </div>
                    </div>

                    {/* Security Badge */}
                    <div className="flex items-center gap-2 pt-4">
                        <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
                            <ShieldCheck className="w-5 h-5 text-primary" />
                        </div>
                        <div>
                            <p className="text-xs font-semibold text-slate-50">Secure Environment</p>
                            <p className="text-xs text-slate-400">Data processed locally on your device</p>
                        </div>
                    </div>
                </div>

                {/* Right Column: Action Card */}
                <div className="bg-surface rounded-2xl shadow-xl border border-secondary-dark p-8 flex flex-col">
                    {mode === 'select' ? (
                        <div className="flex-1 flex flex-col justify-center space-y-4">
                            <button
                                onClick={() => setMode('create')}
                                className="group relative overflow-hidden p-8 rounded-xl bg-gradient-to-br from-primary to-primary-dark text-slate-50 shadow-lg hover:shadow-primary/25 transition-all duration-300 text-left"
                            >
                                <div className="relative z-10">
                                    <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm group-hover:scale-110 transition-transform">
                                        <Plus className="w-6 h-6 text-slate-50" />
                                    </div>
                                    <h3 className="text-xl font-bold mb-1">New QAQC Session</h3>
                                    <p className="text-primary-light text-sm">Start a fresh analysis project</p>
                                </div>
                                <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-2xl group-hover:bg-white/20 transition-colors" />
                            </button>

                            <button
                                onClick={handleOpenProjectFile}
                                disabled={isLoading}
                                className="group p-8 rounded-xl bg-surface-light/50 border-2 border-dashed border-secondary-light hover:border-primary hover:bg-primary/5 transition-all duration-300 text-left disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <div className="w-12 h-12 bg-secondary rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary/20 group-hover:text-primary transition-colors">
                                    {isLoading ? (
                                        <Loader2 className="w-6 h-6 text-primary animate-spin" />
                                    ) : (
                                        <FolderOpen className="w-6 h-6 text-slate-400 group-hover:text-primary" />
                                    )}
                                </div>
                                <h3 className="text-xl font-bold text-slate-50 mb-1">
                                    {isLoading ? 'Loading...' : 'Open Project File'}
                                </h3>
                                <p className="text-slate-400 text-sm">Load a previously saved .qaqc file</p>
                            </button>

                            {error && (
                                <div className="flex items-center gap-2 p-4 bg-status-error/10 border border-status-error/30 rounded-lg text-status-error">
                                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                                    <p className="text-sm">{error}</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col">
                            <div className="mb-6">
                                <button
                                    onClick={() => setMode('select')}
                                    className="text-sm text-slate-400 hover:text-slate-50 mb-4 flex items-center gap-1"
                                >
                                    ← Back
                                </button>
                                <h2 className="text-2xl font-bold text-slate-50">New Session</h2>
                                <p className="text-slate-400 text-sm mt-1">Enter project details to begin.</p>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-4 flex-1">
                                {/* Project Name */}
                                <div className="space-y-1.5">
                                    <label className="text-sm font-medium text-slate-300">Project Name</label>
                                    <input
                                        required
                                        type="text"
                                        placeholder="e.g. Q4 Drilling Report"
                                        className="w-full px-4 py-3 rounded-lg bg-surface-light border border-secondary-light text-slate-50 placeholder:text-slate-500 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                        value={formData.name}
                                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>

                                {/* Deposit */}
                                <div className="space-y-1.5">
                                    <label className="text-sm font-medium text-slate-300">Deposit / Area</label>
                                    <input
                                        required
                                        type="text"
                                        placeholder="e.g. North Zone, Main Pit"
                                        className="w-full px-4 py-3 rounded-lg bg-surface-light border border-secondary-light text-slate-50 placeholder:text-slate-500 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                        value={formData.deposit}
                                        onChange={e => setFormData({ ...formData, deposit: e.target.value })}
                                    />
                                </div>

                                {/* Commodity with Dropdown Suggestions */}
                                <div className="space-y-1.5 relative">
                                    <label className="text-sm font-medium text-slate-300">Commodity</label>
                                    <div className="relative">
                                        <input
                                            required
                                            type="text"
                                            placeholder="Select or type..."
                                            className="w-full px-4 py-3 pr-10 rounded-lg bg-surface-light border border-secondary-light text-slate-50 placeholder:text-slate-500 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                            value={formData.commodity}
                                            onChange={e => setFormData({ ...formData, commodity: e.target.value })}
                                            onFocus={() => setShowCommodityDropdown(true)}
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setShowCommodityDropdown(!showCommodityDropdown)}
                                            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-200"
                                        >
                                            <ChevronDown className={`w-4 h-4 transition-transform ${showCommodityDropdown ? 'rotate-180' : ''}`} />
                                        </button>
                                    </div>
                                    
                                    {/* Dropdown */}
                                    {showCommodityDropdown && (
                                        <div className="absolute z-10 w-full mt-1 bg-surface-light border border-secondary-light rounded-lg shadow-xl overflow-hidden">
                                            <div className="max-h-48 overflow-y-auto">
                                                {COMMON_COMMODITIES.map(({ value, label }) => (
                                                    <button
                                                        key={value}
                                                        type="button"
                                                        onClick={() => handleCommoditySelect(value)}
                                                        className={`w-full px-4 py-2.5 text-left hover:bg-primary/10 transition-colors flex items-center justify-between ${
                                                            formData.commodity === value ? 'bg-primary/10 text-primary' : 'text-slate-200'
                                                        }`}
                                                    >
                                                        <span className="text-sm">{label}</span>
                                                        <span className="text-xs text-slate-500">{value}</span>
                                                    </button>
                                                ))}
                                            </div>
                                        </div>
                                    )}
                                </div>

                                <div className="pt-4 mt-auto">
                                    <button
                                        type="submit"
                                        disabled={!formData.name || !formData.deposit || !formData.commodity}
                                        className="w-full py-4 bg-primary hover:bg-primary-dark text-slate-900 font-bold rounded-xl shadow-lg shadow-primary/20 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed"
                                    >
                                        Create Session
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </div>

            {/* Close dropdown when clicking outside */}
            {showCommodityDropdown && (
                <div 
                    className="fixed inset-0 z-0" 
                    onClick={() => setShowCommodityDropdown(false)}
                />
            )}
        </div>
    );
};
