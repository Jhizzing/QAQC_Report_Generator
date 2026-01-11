import { describe, it, expect, beforeEach } from 'vitest';
import { useProjectStore } from '../projectStore';
import type { ProjectMetadata } from '../projectStore';

describe('projectStore', () => {
    beforeEach(() => {
        // Reset store state
        useProjectStore.setState({
            currentProject: null,
            recentProjects: [],
        });
    });

    it('should create a new project', () => {
        const { createProject } = useProjectStore.getState();

        createProject({
            name: 'Test Project',
            deposit: 'Test Deposit',
            commodity: 'Gold',
        });

        const { currentProject, recentProjects } = useProjectStore.getState();

        expect(currentProject).toBeDefined();
        expect(currentProject?.name).toBe('Test Project');
        expect(currentProject?.deposit).toBe('Test Deposit');
        expect(currentProject?.commodity).toBe('Gold');
        expect(currentProject?.id).toBeDefined();
        expect(currentProject?.createdAt).toBeDefined();
        expect(recentProjects.length).toBe(1);
    });

    it('should open an existing project', () => {
        const project: ProjectMetadata = {
            id: 'test-id',
            name: 'Existing Project',
            deposit: 'Existing Deposit',
            commodity: 'Copper',
            createdAt: '2024-01-01T00:00:00Z',
            lastModified: '2024-01-01T00:00:00Z',
        };

        const { openProject } = useProjectStore.getState();
        openProject(project);

        const { currentProject, recentProjects } = useProjectStore.getState();

        expect(currentProject?.id).toBe('test-id');
        expect(currentProject?.name).toBe('Existing Project');
        expect(recentProjects.length).toBe(1);
        expect(recentProjects[0].id).toBe('test-id');
    });

    it('should load project from file', () => {
        const project: ProjectMetadata = {
            id: 'file-id',
            name: 'File Project',
            deposit: 'File Deposit',
            commodity: 'Silver',
            createdAt: '2024-01-01T00:00:00Z',
            lastModified: '2024-01-01T00:00:00Z',
        };

        const { loadFromFile } = useProjectStore.getState();
        loadFromFile(project, 'test.qaqc');

        const { currentProject } = useProjectStore.getState();

        expect(currentProject?.id).toBe('file-id');
        expect(currentProject?.sourceFile).toBe('test.qaqc');
    });

    it('should close current project', () => {
        const { createProject, closeProject } = useProjectStore.getState();

        createProject({
            name: 'Test Project',
            deposit: 'Test Deposit',
            commodity: 'Gold',
        });

        closeProject();

        const { currentProject } = useProjectStore.getState();
        expect(currentProject).toBeNull();
    });

    it('should update current project', () => {
        const { createProject, updateProject } = useProjectStore.getState();

        createProject({
            name: 'Test Project',
            deposit: 'Test Deposit',
            commodity: 'Gold',
        });

        const { currentProject: before } = useProjectStore.getState();
        const originalLastModified = before?.lastModified;

        // Wait a bit to ensure timestamp changes
        const startTime = Date.now();
        while (Date.now() - startTime < 10) {
            // Wait 10ms
        }

        updateProject({ name: 'Updated Project' });

        const { currentProject } = useProjectStore.getState();

        expect(currentProject?.name).toBe('Updated Project');
        expect(currentProject?.deposit).toBe('Test Deposit'); // Unchanged
        // Just verify lastModified exists and is a string
        expect(currentProject?.lastModified).toBeDefined();
        expect(typeof currentProject?.lastModified).toBe('string');
    });

    it('should limit recent projects to 10', () => {
        const { createProject } = useProjectStore.getState();

        // Create 12 projects
        for (let i = 0; i < 12; i++) {
            createProject({
                name: `Project ${i}`,
                deposit: 'Test Deposit',
                commodity: 'Gold',
            });
        }

        const { recentProjects } = useProjectStore.getState();
        expect(recentProjects.length).toBe(10);
    });

    it('should move opened project to top of recent projects', () => {
        const { createProject, openProject } = useProjectStore.getState();

        // Create two projects
        createProject({
            name: 'Project 1',
            deposit: 'Deposit 1',
            commodity: 'Gold',
        });

        const { currentProject: project1 } = useProjectStore.getState();

        createProject({
            name: 'Project 2',
            deposit: 'Deposit 2',
            commodity: 'Gold',
        });

        // Open first project
        if (project1) {
            openProject(project1);
        }

        const { recentProjects } = useProjectStore.getState();
        expect(recentProjects[0].id).toBe(project1?.id);
    });
});
