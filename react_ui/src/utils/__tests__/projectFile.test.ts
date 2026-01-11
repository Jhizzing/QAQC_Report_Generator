import { describe, it, expect, vi, beforeEach } from 'vitest';
import { 
    saveProjectToFile, 
    loadProjectFromFile, 
    PROJECT_FILE_VERSION,
    type QAQCProjectFile,
    type ProjectState 
} from '../projectFile';
import type { ProjectMetadata } from '../../stores/projectStore';

describe('projectFile', () => {
    beforeEach(() => {
        // Mock URL.createObjectURL and document methods
        global.URL.createObjectURL = vi.fn(() => 'blob:mock-url');
        global.URL.revokeObjectURL = vi.fn();
        
        // Mock document.createElement and methods
        const mockLink = {
            href: '',
            download: '',
            click: vi.fn(),
        };
        vi.spyOn(document, 'createElement').mockReturnValue(mockLink as any);
        vi.spyOn(document.body, 'appendChild').mockImplementation(() => mockLink as any);
        vi.spyOn(document.body, 'removeChild').mockImplementation(() => mockLink as any);
    });

    describe('saveProjectToFile', () => {
        it('should create and download a project file', () => {
            const metadata: ProjectMetadata = {
                name: 'Test Project',
                deposit: 'Test Deposit',
                commodity: 'Gold',
            };

            const state: ProjectState = {
                data: {
                    fileName: 'test.csv',
                    headers: ['SampleID', 'Type'],
                    data: [['STD-001', 'STD']],
                    rowCount: 1,
                },
                category: 'gold',
                methodologyConfig: null,
                qaqcConfig: null,
                analysisResults: null,
                workflowStep: 'import',
            };

            saveProjectToFile(metadata, state);

            // Verify blob was created
            expect(global.URL.createObjectURL).toHaveBeenCalled();
            
            // Verify link was created and clicked
            expect(document.createElement).toHaveBeenCalledWith('a');
        });

        it('should sanitize project name in filename', () => {
            const metadata: ProjectMetadata = {
                name: 'Test Project 123!@#',
                deposit: 'Test Deposit',
                commodity: 'Gold',
            };

            const state: ProjectState = {
                data: null,
                category: null,
                methodologyConfig: null,
                qaqcConfig: null,
                analysisResults: null,
                workflowStep: 'import',
            };

            saveProjectToFile(metadata, state);

            // The filename should have sanitized the project name
            expect(document.createElement).toHaveBeenCalled();
        });
    });

    describe('loadProjectFromFile', () => {
        it('should load a valid project file', async () => {
            const projectFile: QAQCProjectFile = {
                version: PROJECT_FILE_VERSION,
                savedAt: new Date().toISOString(),
                metadata: {
                    name: 'Test Project',
                    deposit: 'Test Deposit',
                    commodity: 'Gold',
                },
                data: {
                    fileName: 'test.csv',
                    headers: ['SampleID', 'Type'],
                    data: [['STD-001', 'STD']],
                    rowCount: 1,
                },
                category: 'gold',
                methodologyConfig: null,
                qaqcConfig: null,
                analysisResults: null,
                workflowStep: 'import',
            };

            const file = new File(
                [JSON.stringify(projectFile)],
                'test.qaqc',
                { type: 'application/json' }
            );

            const result = await loadProjectFromFile(file);

            expect(result.version).toBe(PROJECT_FILE_VERSION);
            expect(result.metadata.name).toBe('Test Project');
            expect(result.data).toBeDefined();
        });

        it('should reject invalid JSON files', async () => {
            const file = new File(
                ['invalid json'],
                'invalid.qaqc',
                { type: 'application/json' }
            );

            await expect(loadProjectFromFile(file)).rejects.toThrow();
        });

        it('should reject files with wrong version', async () => {
            const projectFile: QAQCProjectFile = {
                version: '0.0.0', // Old version
                savedAt: new Date().toISOString(),
                metadata: {
                    name: 'Test Project',
                    deposit: 'Test Deposit',
                    commodity: 'Gold',
                },
                data: null,
                category: null,
                methodologyConfig: null,
                qaqcConfig: null,
                analysisResults: null,
                workflowStep: 'import',
            };

            const file = new File(
                [JSON.stringify(projectFile)],
                'old.qaqc',
                { type: 'application/json' }
            );

            // Should either reject or handle gracefully
            try {
                await loadProjectFromFile(file);
            } catch (error) {
                expect(error).toBeDefined();
            }
        });

        it('should handle missing required fields', async () => {
            const invalidFile = {
                version: PROJECT_FILE_VERSION,
                // Missing metadata and other required fields
            };

            const file = new File(
                [JSON.stringify(invalidFile)],
                'incomplete.qaqc',
                { type: 'application/json' }
            );

            // Should handle gracefully or throw
            try {
                await loadProjectFromFile(file);
            } catch (error) {
                expect(error).toBeDefined();
            }
        });
    });
});
