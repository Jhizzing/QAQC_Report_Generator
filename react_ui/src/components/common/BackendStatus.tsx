/**
 * BackendStatus Component
 * 
 * Shows the connection status to the FastAPI backend.
 * Displays connected (green), checking (yellow), or offline (red) states.
 */

import React from 'react';
import { Server, RefreshCw, Wifi, WifiOff } from 'lucide-react';

interface BackendStatusProps {
    isAvailable: boolean;
    isChecking: boolean;
    onRetry: () => void;
    className?: string;
}

export const BackendStatus: React.FC<BackendStatusProps> = ({
    isAvailable,
    isChecking,
    onRetry,
    className = '',
}) => {
    const getStatusColor = () => {
        if (isChecking) return 'text-yellow-400';
        if (isAvailable) return 'text-green-400';
        return 'text-slate-500';
    };

    const getStatusText = () => {
        if (isChecking) return 'Checking...';
        if (isAvailable) return 'Server Connected';
        return 'Offline Mode';
    };

    const StatusIcon = () => {
        if (isChecking) {
            return <RefreshCw className="w-3.5 h-3.5 animate-spin" />;
        }
        if (isAvailable) {
            return <Wifi className="w-3.5 h-3.5" />;
        }
        return <WifiOff className="w-3.5 h-3.5" />;
    };

    return (
        <div className={`flex items-center gap-2 ${className}`}>
            <button
                onClick={onRetry}
                disabled={isChecking}
                className={`
                    flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium
                    transition-all duration-200
                    ${isAvailable 
                        ? 'bg-green-400/10 hover:bg-green-400/20' 
                        : isChecking
                            ? 'bg-yellow-400/10'
                            : 'bg-surface-light hover:bg-surface cursor-pointer'
                    }
                    ${getStatusColor()}
                `}
                title={isAvailable 
                    ? 'Python backend connected - using server-side analysis' 
                    : 'Backend offline - using client-side analysis (click to retry)'
                }
            >
                <StatusIcon />
                <span className="hidden sm:inline">{getStatusText()}</span>
            </button>
            
            {!isAvailable && !isChecking && (
                <div className="hidden lg:flex items-center gap-1 text-xs text-slate-500">
                    <Server className="w-3 h-3" />
                    <span>Start backend for PDF export</span>
                </div>
            )}
        </div>
    );
};
