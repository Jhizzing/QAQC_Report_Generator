/**
 * useBackendService Hook
 * 
 * Auto-detects FastAPI backend availability and provides connection status.
 * Performs periodic health checks to maintain accurate status.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { apiClient } from '../api/client';

export interface BackendStatus {
    isAvailable: boolean;
    isChecking: boolean;
    lastChecked: Date | null;
    error: string | null;
    version: string | null;
}

interface UseBackendServiceOptions {
    /** Interval between health checks in milliseconds (default: 30000) */
    checkInterval?: number;
    /** Whether to start checking immediately (default: true) */
    autoStart?: boolean;
}

export function useBackendService(options: UseBackendServiceOptions = {}) {
    const { checkInterval = 30000, autoStart = true } = options;
    
    const [status, setStatus] = useState<BackendStatus>({
        isAvailable: false,
        isChecking: true,
        lastChecked: null,
        error: null,
        version: null,
    });
    
    const intervalRef = useRef<NodeJS.Timeout | null>(null);
    const isMountedRef = useRef(true);

    const checkBackend = useCallback(async () => {
        if (!isMountedRef.current) return;
        
        setStatus(prev => ({ ...prev, isChecking: true, error: null }));
        
        try {
            const response = await apiClient.healthCheck();
            
            if (!isMountedRef.current) return;
            
            setStatus({
                isAvailable: response.status === 'healthy',
                isChecking: false,
                lastChecked: new Date(),
                error: null,
                version: '2.0.0', // From the API response
            });
        } catch (error) {
            if (!isMountedRef.current) return;
            
            setStatus({
                isAvailable: false,
                isChecking: false,
                lastChecked: new Date(),
                error: error instanceof Error ? error.message : 'Connection failed',
                version: null,
            });
        }
    }, []);

    // Initial check and periodic checks
    useEffect(() => {
        isMountedRef.current = true;
        
        if (autoStart) {
            // Immediate check on mount
            checkBackend();
            
            // Set up periodic checks
            intervalRef.current = setInterval(checkBackend, checkInterval);
        }
        
        return () => {
            isMountedRef.current = false;
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
            }
        };
    }, [checkBackend, checkInterval, autoStart]);

    // Manual retry function
    const retry = useCallback(() => {
        checkBackend();
    }, [checkBackend]);

    // Stop periodic checks
    const stopChecking = useCallback(() => {
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
            intervalRef.current = null;
        }
    }, []);

    // Resume periodic checks
    const startChecking = useCallback(() => {
        if (!intervalRef.current) {
            checkBackend();
            intervalRef.current = setInterval(checkBackend, checkInterval);
        }
    }, [checkBackend, checkInterval]);

    return {
        ...status,
        retry,
        stopChecking,
        startChecking,
    };
}

// Singleton status for use outside of React components
let globalBackendAvailable = false;

export function setGlobalBackendStatus(available: boolean) {
    globalBackendAvailable = available;
}

export function getGlobalBackendStatus(): boolean {
    return globalBackendAvailable;
}
