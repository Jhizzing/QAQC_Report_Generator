import React from 'react';

interface HeaderProps {
    className?: string;
}

export const Header: React.FC<HeaderProps> = ({ className = '' }) => {
    return (
        <header className={`bg-surface-dark border-b border-gray-800 ${className}`}>
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <img
                            src="/logiqore-logo.png"
                            alt="LogiQore"
                            className="h-12 transition-all duration-200 hover:scale-105 hover:drop-shadow-[0_0_8px_rgba(251,191,36,0.4)]"
                        />
                        <div>
                            <h1 className="text-xl font-semibold text-white">
                                LogiQore QAQC Reporter
                            </h1>
                            <p className="text-sm text-gray-400">
                                Professional Assay Quality Control Analysis
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
};
