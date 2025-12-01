import React from 'react';
import { Bell, Search } from 'lucide-react';

export const Header: React.FC = () => {
    return (
        <header className="h-16 bg-surface border-b border-gray-200 dark:bg-surface-dark dark:border-gray-800 flex items-center justify-between px-6">
            <div className="flex items-center gap-4 flex-1">
                <div className="relative w-96">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-300" />
                    <input
                        type="text"
                        placeholder="Search reports, samples, or CRMs..."
                        className="w-full pl-10 pr-4 py-2 bg-gray-100 dark:bg-gray-900 border-none rounded-lg text-sm focus:ring-2 focus:ring-primary/50 outline-none transition-all"
                    />
                </div>
            </div>

            <div className="flex items-center gap-4">
                <button className="p-2 text-gray-300 hover:text-primary transition-colors relative">
                    <Bell className="w-5 h-5" />
                    <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full border-2 border-surface dark:border-surface-dark" />
                </button>

                <div className="h-8 w-px bg-gray-200 dark:bg-gray-700" />

                <button className="flex items-center gap-3 pl-2">
                    <div className="text-right hidden sm:block">
                        <p className="text-sm font-medium text-gray-900 dark:text-white">Geologist</p>
                        <p className="text-xs text-gray-300">Admin Access</p>
                    </div>
                    <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center text-primary font-bold">
                        G
                    </div>
                </button>
            </div>
        </header>
    );
};
