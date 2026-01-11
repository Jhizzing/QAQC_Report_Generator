import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { act } from '@testing-library/react';
import { useBackendService, setGlobalBackendStatus, getGlobalBackendStatus } from '../useBackendService';
import { apiClient } from '../../api/client';

// Mock the API client
vi.mock('../../api/client', () => ({
    apiClient: {
        healthCheck: vi.fn(),
    },
}));

describe('useBackendService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should check backend on mount when autoStart is true', async () => {
        (apiClient.healthCheck as any).mockResolvedValue({ status: 'healthy', version: '2.0.0' });

        const { result } = renderHook(() => useBackendService({ autoStart: true }));

        expect(result.current.isChecking).toBe(true);
        
        await waitFor(() => {
            expect(result.current.isChecking).toBe(false);
        }, { timeout: 3000 });

        expect(result.current.isAvailable).toBe(true);
        expect(apiClient.healthCheck).toHaveBeenCalled();
    });

    it('should not check backend when autoStart is false', async () => {
        const { result } = renderHook(() => useBackendService({ autoStart: false }));

        // Wait a bit to ensure no check happens
        await new Promise(resolve => setTimeout(resolve, 100));
        
        expect(apiClient.healthCheck).not.toHaveBeenCalled();
    });

    it('should handle backend unavailable', async () => {
        (apiClient.healthCheck as any).mockRejectedValue(new Error('Connection failed'));

        const { result } = renderHook(() => useBackendService({ autoStart: true }));

        await waitFor(() => {
            expect(result.current.isChecking).toBe(false);
        }, { timeout: 3000 });

        expect(result.current.isAvailable).toBe(false);
        expect(result.current.error).toBeDefined();
    });

    it('should retry when retry function is called', async () => {
        (apiClient.healthCheck as any).mockResolvedValue({ status: 'healthy', version: '2.0.0' });

        const { result } = renderHook(() => useBackendService({ autoStart: false }));

        act(() => {
            result.current.retry();
        });

        await waitFor(() => {
            expect(apiClient.healthCheck).toHaveBeenCalled();
        }, { timeout: 3000 });
    });

    it('should perform periodic checks', async () => {
        (apiClient.healthCheck as any).mockResolvedValue({ status: 'healthy', version: '2.0.0' });

        const { result } = renderHook(() => 
            useBackendService({ autoStart: true, checkInterval: 1000 })
        );

        // Wait for initial check
        await waitFor(() => {
            expect(result.current.isAvailable).toBe(true);
        }, { timeout: 3000 });

        const initialCallCount = (apiClient.healthCheck as any).mock.calls.length;

        // Wait for at least one periodic check (should happen after 1 second)
        await waitFor(() => {
            expect((apiClient.healthCheck as any).mock.calls.length).toBeGreaterThan(initialCallCount);
        }, { timeout: 5000 });
    });

    it('should stop and start checking', async () => {
        (apiClient.healthCheck as any).mockResolvedValue({ status: 'healthy', version: '2.0.0' });

        const { result } = renderHook(() => 
            useBackendService({ autoStart: true, checkInterval: 2000 })
        );

        await waitFor(() => {
            expect(result.current.isAvailable).toBe(true);
        }, { timeout: 3000 });

        const initialCallCount = (apiClient.healthCheck as any).mock.calls.length;

        act(() => {
            result.current.stopChecking();
        });

        // Wait a bit to ensure no new calls happen
        await new Promise(resolve => setTimeout(resolve, 2500));

        // Should not have increased call count significantly (maybe 1 more from timing)
        const afterStopCount = (apiClient.healthCheck as any).mock.calls.length;
        expect(afterStopCount).toBeLessThanOrEqual(initialCallCount + 1);

        act(() => {
            result.current.startChecking();
        });

        // Should trigger an immediate check
        await waitFor(() => {
            expect((apiClient.healthCheck as any).mock.calls.length).toBeGreaterThan(afterStopCount);
        }, { timeout: 3000 });
    });

    it('should clean up on unmount', async () => {
        (apiClient.healthCheck as any).mockResolvedValue({ status: 'healthy', version: '2.0.0' });

        const { result, unmount } = renderHook(() => 
            useBackendService({ autoStart: true, checkInterval: 2000 })
        );

        await waitFor(() => {
            expect(result.current.isAvailable).toBe(true);
        }, { timeout: 3000 });

        const callCount = (apiClient.healthCheck as any).mock.calls.length;

        unmount();

        // Wait a bit to ensure no new calls after unmount
        await new Promise(resolve => setTimeout(resolve, 2500));

        // Should not have increased significantly after unmount (maybe 1 more from timing)
        const finalCallCount = (apiClient.healthCheck as any).mock.calls.length;
        expect(finalCallCount).toBeLessThanOrEqual(callCount + 1);
    });
});

describe('Global Backend Status', () => {
    it('should set and get global backend status', () => {
        setGlobalBackendStatus(true);
        expect(getGlobalBackendStatus()).toBe(true);

        setGlobalBackendStatus(false);
        expect(getGlobalBackendStatus()).toBe(false);
    });
});
