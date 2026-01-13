import React from 'react';
import { AlertTriangle, X, RefreshCw, Info } from 'lucide-react';

export interface ErrorDisplayProps {
    error: Error | string;
    title?: string;
    onDismiss?: () => void;
    onRetry?: () => void;
    showDetails?: boolean;
    className?: string;
}

export const ErrorDisplay: React.FC<ErrorDisplayProps> = ({
    error,
    title = 'An error occurred',
    onDismiss,
    onRetry,
    showDetails = false,
    className = '',
}) => {
    const errorMessage = typeof error === 'string' ? error : error.message;
    const errorStack = typeof error === 'string' ? undefined : error.stack;

    return (
        <div
            className={`
                bg-status-error/10 border border-status-error/30 rounded-lg p-4
                ${className}
            `}
        >
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0 p-2 bg-status-error/20 rounded-lg">
                    <AlertTriangle className="w-5 h-5 text-status-error" />
                </div>

                <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-2 mb-2">
                        <h3 className="text-sm font-semibold text-status-error">
                            {title}
                        </h3>
                        {onDismiss && (
                            <button
                                onClick={onDismiss}
                                className="flex-shrink-0 p-1 text-status-error/70 hover:text-status-error transition-colors"
                                aria-label="Dismiss error"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        )}
                    </div>

                    <p className="text-sm text-slate-300 mb-3">{errorMessage}</p>

                    {showDetails && errorStack && (
                        <details className="mb-3">
                            <summary className="text-xs text-slate-400 cursor-pointer hover:text-slate-300 mb-2">
                                Show error details
                            </summary>
                            <pre className="text-xs text-slate-500 bg-surface-dark p-3 rounded overflow-auto max-h-40 font-mono">
                                {errorStack}
                            </pre>
                        </details>
                    )}

                    {(onRetry || onDismiss) && (
                        <div className="flex items-center gap-2">
                            {onRetry && (
                                <button
                                    onClick={onRetry}
                                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium bg-status-error/20 text-status-error rounded-md hover:bg-status-error/30 transition-colors"
                                >
                                    <RefreshCw className="w-3 h-3" />
                                    Retry
                                </button>
                            )}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export interface ValidationErrorDisplayProps {
    errors: Record<string, string>;
    className?: string;
}

export const ValidationErrorDisplay: React.FC<ValidationErrorDisplayProps> = ({
    errors,
    className = '',
}) => {
    if (Object.keys(errors).length === 0) {
        return null;
    }

    return (
        <div
            className={`
                bg-status-warning/10 border border-status-warning/30 rounded-lg p-4
                ${className}
            `}
        >
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0 p-2 bg-status-warning/20 rounded-lg">
                    <Info className="w-5 h-5 text-status-warning" />
                </div>

                <div className="flex-1">
                    <h3 className="text-sm font-semibold text-status-warning mb-2">
                        Validation Errors
                    </h3>
                    <ul className="space-y-1">
                        {Object.entries(errors).map(([field, message]) => (
                            <li key={field} className="text-sm text-slate-300">
                                <span className="font-medium">{field}:</span> {message}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export interface SuccessMessageProps {
    message: string;
    onDismiss?: () => void;
    className?: string;
}

export const SuccessMessage: React.FC<SuccessMessageProps> = ({
    message,
    onDismiss,
    className = '',
}) => {
    return (
        <div
            className={`
                bg-status-success/10 border border-status-success/30 rounded-lg p-4
                ${className}
            `}
        >
            <div className="flex items-start gap-3">
                <div className="flex-shrink-0 p-2 bg-status-success/20 rounded-lg">
                    <Info className="w-5 h-5 text-status-success" />
                </div>

                <div className="flex-1">
                    <p className="text-sm text-slate-300">{message}</p>
                </div>

                {onDismiss && (
                    <button
                        onClick={onDismiss}
                        className="flex-shrink-0 p-1 text-status-success/70 hover:text-status-success transition-colors"
                        aria-label="Dismiss message"
                    >
                        <X className="w-4 h-4" />
                    </button>
                )}
            </div>
        </div>
    );
};
