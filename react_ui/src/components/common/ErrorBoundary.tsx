import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
    children: ReactNode;
    fallback?: ReactNode;
    onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
    hasError: boolean;
    error: Error | null;
    errorInfo: ErrorInfo | null;
}

export class ErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            hasError: false,
            error: null,
            errorInfo: null,
        };
    }

    static getDerivedStateFromError(error: Error): Partial<State> {
        return {
            hasError: true,
            error,
        };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        // Log error for debugging
        console.error('ErrorBoundary caught an error:', error, errorInfo);
        
        this.setState({
            error,
            errorInfo,
        });

        // Call optional error handler
        if (this.props.onError) {
            this.props.onError(error, errorInfo);
        }
    }

    handleReset = () => {
        this.setState({
            hasError: false,
            error: null,
            errorInfo: null,
        });
    };

    handleReload = () => {
        window.location.reload();
    };

    handleGoHome = () => {
        window.location.href = '/';
    };

    render() {
        if (this.state.hasError) {
            // Use custom fallback if provided
            if (this.props.fallback) {
                return this.props.fallback;
            }

            // Default error UI
            return (
                <div className="min-h-screen bg-background-dark flex items-center justify-center p-4">
                    <div className="max-w-2xl w-full bg-surface rounded-xl border border-status-error/30 p-8">
                        <div className="flex items-start gap-4 mb-6">
                            <div className="p-3 bg-status-error/20 rounded-lg">
                                <AlertTriangle className="w-8 h-8 text-status-error" />
                            </div>
                            <div className="flex-1">
                                <h1 className="text-2xl font-bold text-slate-50 mb-2">
                                    Something went wrong
                                </h1>
                                <p className="text-slate-400">
                                    An unexpected error occurred. Don't worry, your data is safe.
                                </p>
                            </div>
                        </div>

                        {this.state.error && (
                            <div className="mb-6 p-4 bg-surface-light rounded-lg border border-secondary-dark">
                                <p className="text-sm font-mono text-status-error mb-2">
                                    {this.state.error.name}: {this.state.error.message}
                                </p>
                                {process.env.NODE_ENV === 'development' && this.state.errorInfo && (
                                    <details className="mt-2">
                                        <summary className="text-xs text-slate-400 cursor-pointer hover:text-slate-300">
                                            Stack trace
                                        </summary>
                                        <pre className="mt-2 text-xs text-slate-500 overflow-auto max-h-40">
                                            {this.state.error.stack}
                                        </pre>
                                    </details>
                                )}
                            </div>
                        )}

                        <div className="flex flex-wrap gap-3">
                            <button
                                onClick={this.handleReset}
                                className="flex items-center gap-2 px-4 py-2 bg-primary text-slate-900 rounded-lg font-medium hover:bg-primary-dark transition-colors"
                            >
                                <RefreshCw className="w-4 h-4" />
                                Try Again
                            </button>
                            <button
                                onClick={this.handleReload}
                                className="flex items-center gap-2 px-4 py-2 bg-surface-light text-slate-300 rounded-lg font-medium hover:bg-surface hover:text-slate-50 transition-colors border border-secondary-dark"
                            >
                                <RefreshCw className="w-4 h-4" />
                                Reload Page
                            </button>
                            <button
                                onClick={this.handleGoHome}
                                className="flex items-center gap-2 px-4 py-2 bg-surface-light text-slate-300 rounded-lg font-medium hover:bg-surface hover:text-slate-50 transition-colors border border-secondary-dark"
                            >
                                <Home className="w-4 h-4" />
                                Go Home
                            </button>
                        </div>

                        <div className="mt-6 pt-6 border-t border-secondary-dark">
                            <p className="text-xs text-slate-500">
                                If this problem persists, please contact support with the error details above.
                            </p>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
