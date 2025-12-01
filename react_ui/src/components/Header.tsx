import React from 'react';

interface HeaderProps {
    className?: string;
}

export const Header: React.FC<HeaderProps> = ({ className = '' }) => {
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
                </div>
            </div>
        </header>
    );
};
