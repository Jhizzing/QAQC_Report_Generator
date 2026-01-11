import React from 'react';
import {
    LayoutDashboard,
    FileBarChart,
    Settings,
    Database,
    Upload,
    ShieldCheck,
    GraduationCap,
    Lock,
    Check
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';

export type SidebarSection = 'dashboard' | 'import' | 'setup' | 'analysis' | 'crm' | 'education' | 'settings';

interface MenuItem {
    icon: LucideIcon;
    label: string;
    id: SidebarSection;
    workflowStep?: string; // Maps to App.tsx workflow step
    requiresData?: boolean;
    requiresAnalysis?: boolean;
    disabled?: boolean;
    disabledReason?: string;
}

interface SidebarProps {
    className?: string;
    onNavigate?: (section: string) => void;
    activeSection?: string;
    hasData?: boolean;
    hasAnalysis?: boolean;
    completedSteps?: string[];
}

export const Sidebar: React.FC<SidebarProps> = ({ 
    className = '', 
    onNavigate, 
    activeSection = 'dashboard',
    hasData = false,
    hasAnalysis = false,
    completedSteps = []
}) => {
    const menuItems: MenuItem[] = [
        { 
            icon: LayoutDashboard, 
            label: 'Dashboard', 
            id: 'dashboard',
            workflowStep: 'dashboard',
            requiresAnalysis: true,
            disabledReason: 'Run analysis first'
        },
        { 
            icon: Upload, 
            label: 'Data Import', 
            id: 'import',
            workflowStep: 'import'
        },
        { 
            icon: FileBarChart, 
            label: 'Analysis Setup', 
            id: 'setup',
            workflowStep: 'setup',
            requiresData: true,
            disabledReason: 'Import data first'
        },
        { 
            icon: Database, 
            label: 'CRM Database', 
            id: 'crm',
            workflowStep: 'crm'
        },
        { 
            icon: GraduationCap, 
            label: 'Learn', 
            id: 'education',
            workflowStep: 'education'
        },
        { 
            icon: Settings, 
            label: 'Settings', 
            id: 'settings',
            workflowStep: 'settings'
        },
    ];

    const isItemAvailable = (item: MenuItem): boolean => {
        if (item.disabled) return false;
        if (item.requiresData && !hasData) return false;
        if (item.requiresAnalysis && !hasAnalysis) return false;
        return true;
    };

    const isItemCompleted = (item: MenuItem): boolean => {
        if (!item.workflowStep) return false;
        return completedSteps.includes(item.workflowStep);
    };

    return (
        <aside className={`flex flex-col w-64 bg-surface-dark border-r border-secondary-dark text-slate-400 ${className}`}>
            <div className="p-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                    <ShieldCheck className="w-5 h-5 text-slate-50" />
                </div>
                <h1 className="text-xl font-bold text-slate-50 tracking-tight">QAQC Pro</h1>
            </div>

            <nav className="flex-1 px-4 py-4 space-y-1">
                {menuItems.map((item) => {
                    const isActive = activeSection === item.id || activeSection === item.workflowStep;
                    const isAvailable = isItemAvailable(item);
                    const isCompleted = isItemCompleted(item);

                    return (
                        <button
                            key={item.id}
                            onClick={() => isAvailable && onNavigate?.(item.workflowStep || item.id)}
                            disabled={!isAvailable}
                            title={!isAvailable ? item.disabledReason : item.label}
                            className={`
                                w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group
                                ${isActive
                                    ? 'bg-primary/10 text-primary-light border-l-2 border-primary'
                                    : isAvailable
                                        ? 'hover:bg-surface-light hover:text-slate-50'
                                        : 'opacity-50 cursor-not-allowed'
                                }
                            `}
                        >
                            <div className="relative">
                                <item.icon 
                                    className={`w-5 h-5 ${
                                        isActive 
                                            ? 'text-primary-light' 
                                            : isAvailable 
                                                ? 'text-slate-400 group-hover:text-slate-50' 
                                                : 'text-slate-600'
                                    }`} 
                                />
                                {/* Completed indicator */}
                                {isCompleted && !isActive && (
                                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-status-success rounded-full flex items-center justify-center">
                                        <Check className="w-2 h-2 text-slate-900" />
                                    </div>
                                )}
                            </div>
                            <span className={`font-medium ${!isAvailable ? 'text-slate-600' : ''}`}>
                                {item.label}
                            </span>
                            
                            {/* Status badges */}
                            {item.id === 'education' && (
                                <span className="ml-auto px-2 py-0.5 text-xs rounded-full bg-amber-500/20 text-amber-400">
                                    New
                                </span>
                            )}
                            {!isAvailable && !item.disabled && (
                                <Lock className="ml-auto w-4 h-4 text-slate-600" />
                            )}
                            {item.disabled && (
                                <span className="ml-auto px-2 py-0.5 text-xs rounded-full bg-slate-700 text-slate-500">
                                    Soon
                                </span>
                            )}
                        </button>
                    );
                })}
            </nav>

            <div className="p-4 border-t border-secondary-dark">
                <div className="bg-surface-light/50 rounded-lg p-4">
                    <p className="text-xs font-medium text-slate-400 uppercase mb-2">System Status</p>
                    <div className="flex items-center gap-2 text-sm text-status-success">
                        <div className="w-2 h-2 bg-status-success rounded-full animate-pulse" />
                        <span>Secure Environment</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};
