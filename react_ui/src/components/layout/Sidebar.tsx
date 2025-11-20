import React from 'react';
import {
    LayoutDashboard,
    FileBarChart,
    Settings,
    Database,
    Upload,
    ShieldCheck
} from 'lucide-react';

interface SidebarProps {
    className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({ className = '' }) => {
    const menuItems = [
        { icon: LayoutDashboard, label: 'Dashboard', active: true },
        { icon: Upload, label: 'Data Import', active: false },
        { icon: FileBarChart, label: 'Analysis', active: false },
        { icon: Database, label: 'CRM Database', active: false },
        { icon: Settings, label: 'Settings', active: false },
    ];

    return (
        <aside className={`flex flex-col w-64 bg-surface-dark border-r border-gray-800 text-gray-300 ${className}`}>
            <div className="p-6 flex items-center gap-3">
                <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                    <ShieldCheck className="w-5 h-5 text-white" />
                </div>
                <h1 className="text-xl font-bold text-white tracking-tight">QAQC Pro</h1>
            </div>

            <nav className="flex-1 px-4 py-4 space-y-1">
                {menuItems.map((item) => (
                    <button
                        key={item.label}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 group
              ${item.active
                                ? 'bg-primary/10 text-primary-light border-l-2 border-primary'
                                : 'hover:bg-gray-800 hover:text-white'
                            }`}
                    >
                        <item.icon className={`w-5 h-5 ${item.active ? 'text-primary-light' : 'text-gray-500 group-hover:text-white'}`} />
                        <span className="font-medium">{item.label}</span>
                    </button>
                ))}
            </nav>

            <div className="p-4 border-t border-gray-800">
                <div className="bg-gray-800/50 rounded-lg p-4">
                    <p className="text-xs font-medium text-gray-500 uppercase mb-2">System Status</p>
                    <div className="flex items-center gap-2 text-sm text-green-400">
                        <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                        <span>Secure Environment</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};
