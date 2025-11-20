import React, { useState } from 'react';
import { Plus, FolderOpen, ArrowRight, ShieldCheck } from 'lucide-react';
import { useProjectStore } from '../../stores/projectStore';
// import { cn } from '../../utils/cn';

export const ProjectEntry: React.FC = () => {
    const { createProject, recentProjects, openProject } = useProjectStore();
    const [mode, setMode] = useState<'select' | 'create'>('select');

    // Form State
    const [formData, setFormData] = useState({
        name: '',
        deposit: '',
        commodity: '',
        campaign: ''
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (formData.name && formData.deposit && formData.commodity) {
            createProject(formData);
        }
    };

    return (
        <div className="min-h-screen bg-background dark:bg-background-dark flex items-center justify-center p-6">
            <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-2 gap-8">

                {/* Left Column: Welcome & Context */}
                <div className="flex flex-col justify-center space-y-6">
                    <div className="flex items-center gap-3">
                        <div className="w-12 h-12 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary/20">
                            <ShieldCheck className="w-7 h-7 text-white" />
                        </div>
                        <h1 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">QAQC Pro</h1>
                    </div>

                    <div className="space-y-4">
                        <h2 className="text-4xl font-extrabold text-gray-900 dark:text-white leading-tight">
                            Secure, Intelligent <br />
                            <span className="text-primary">Geological Analysis</span>
                        </h2>
                        <p className="text-lg text-gray-500 dark:text-gray-400 max-w-md">
                            Start a new session to analyze your assay data locally. Your data never leaves this device.
                        </p>
                    </div>

                    <div className="pt-8 border-t border-gray-200 dark:border-gray-800">
                        <p className="text-sm font-medium text-gray-500 uppercase tracking-wider mb-4">Recent Sessions</p>
                        <div className="space-y-3">
                            {recentProjects.length === 0 ? (
                                <p className="text-sm text-gray-400 italic">No recent projects found.</p>
                            ) : (
                                recentProjects.slice(0, 3).map(project => (
                                    <button
                                        key={project.id}
                                        onClick={() => openProject(project)}
                                        className="w-full flex items-center justify-between p-4 bg-surface dark:bg-surface-dark border border-gray-200 dark:border-gray-800 rounded-xl hover:border-primary dark:hover:border-primary transition-all group text-left"
                                    >
                                        <div>
                                            <h3 className="font-semibold text-gray-900 dark:text-white group-hover:text-primary transition-colors">
                                                {project.name}
                                            </h3>
                                            <p className="text-xs text-gray-500 mt-1">
                                                {project.deposit} • {project.commodity}
                                            </p>
                                        </div>
                                        <ArrowRight className="w-4 h-4 text-gray-400 group-hover:text-primary group-hover:translate-x-1 transition-all" />
                                    </button>
                                ))
                            )}
                        </div>
                    </div>
                </div>

                {/* Right Column: Action Card */}
                <div className="bg-surface dark:bg-surface-dark rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800 p-8 flex flex-col">
                    {mode === 'select' ? (
                        <div className="flex-1 flex flex-col justify-center space-y-4">
                            <button
                                onClick={() => setMode('create')}
                                className="group relative overflow-hidden p-8 rounded-xl bg-gradient-to-br from-primary to-primary-dark text-white shadow-lg hover:shadow-primary/25 transition-all duration-300 text-left"
                            >
                                <div className="relative z-10">
                                    <div className="w-12 h-12 bg-white/20 rounded-lg flex items-center justify-center mb-4 backdrop-blur-sm group-hover:scale-110 transition-transform">
                                        <Plus className="w-6 h-6 text-white" />
                                    </div>
                                    <h3 className="text-xl font-bold mb-1">New QAQC Session</h3>
                                    <p className="text-primary-light text-sm">Start a fresh analysis project</p>
                                </div>
                                <div className="absolute top-0 right-0 w-32 h-32 bg-white/10 rounded-full -translate-y-1/2 translate-x-1/2 blur-2xl group-hover:bg-white/20 transition-colors" />
                            </button>

                            <button
                                className="group p-8 rounded-xl bg-gray-50 dark:bg-gray-800/50 border-2 border-dashed border-gray-300 dark:border-gray-700 hover:border-primary dark:hover:border-primary hover:bg-primary/5 transition-all duration-300 text-left"
                            >
                                <div className="w-12 h-12 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary/20 group-hover:text-primary transition-colors">
                                    <FolderOpen className="w-6 h-6 text-gray-500 dark:text-gray-400 group-hover:text-primary" />
                                </div>
                                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-1">Open Project File</h3>
                                <p className="text-gray-500 text-sm">Load a previously saved .qaqc file</p>
                            </button>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col">
                            <div className="mb-8">
                                <button
                                    onClick={() => setMode('select')}
                                    className="text-sm text-gray-500 hover:text-gray-900 dark:hover:text-white mb-4 flex items-center gap-1"
                                >
                                    ← Back
                                </button>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">New Session</h2>
                                <p className="text-gray-500 text-sm mt-1">Enter project details to begin.</p>
                            </div>

                            <form onSubmit={handleSubmit} className="space-y-5">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Project Name</label>
                                    <input
                                        required
                                        type="text"
                                        placeholder="e.g. Q4 Drilling Report"
                                        className="w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                        value={formData.name}
                                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Deposit / Area</label>
                                        <input
                                            required
                                            type="text"
                                            placeholder="e.g. North Zone"
                                            className="w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                            value={formData.deposit}
                                            onChange={e => setFormData({ ...formData, deposit: e.target.value })}
                                        />
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Commodity</label>
                                        <input
                                            required
                                            type="text"
                                            placeholder="e.g. Au, Cu-Au"
                                            className="w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                            value={formData.commodity}
                                            onChange={e => setFormData({ ...formData, commodity: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Campaign ID <span className="text-gray-400 font-normal">(Optional)</span></label>
                                    <input
                                        type="text"
                                        placeholder="e.g. RC_2024_01"
                                        className="w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                                        value={formData.campaign}
                                        onChange={e => setFormData({ ...formData, campaign: e.target.value })}
                                    />
                                </div>

                                <div className="pt-4">
                                    <button
                                        type="submit"
                                        className="w-full py-4 bg-primary hover:bg-primary-dark text-white font-bold rounded-xl shadow-lg shadow-primary/20 transition-all active:scale-[0.98]"
                                    >
                                        Create Session
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
