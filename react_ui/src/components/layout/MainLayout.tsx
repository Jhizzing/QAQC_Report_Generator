import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface MainLayoutProps {
    children: React.ReactNode;
    onSidebarNavigate?: (section: string) => void;
    activeSection?: string;
    hasData?: boolean;
    hasAnalysis?: boolean;
    completedSteps?: string[];
}

export const MainLayout: React.FC<MainLayoutProps> = ({ 
    children, 
    onSidebarNavigate, 
    activeSection,
    hasData,
    hasAnalysis,
    completedSteps
}) => {
    return (
        <div className="flex h-screen bg-background-dark overflow-hidden">
            <Sidebar 
                onNavigate={onSidebarNavigate} 
                activeSection={activeSection}
                hasData={hasData}
                hasAnalysis={hasAnalysis}
                completedSteps={completedSteps}
            />

            <div className="flex-1 flex flex-col min-w-0">
                <Header />

                <main className="flex-1 overflow-y-auto p-6">
                    <div className="max-w-7xl mx-auto">
                        {children}
                    </div>
                </main>
            </div>
        </div>
    );
};
