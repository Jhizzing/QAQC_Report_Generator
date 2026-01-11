import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface ProjectMetadata {
    id: string;
    name: string;
    deposit: string;
    commodity: string;
    campaign?: string;
    createdAt: string;
    lastModified: string;
    /** Path/name of file this was loaded from (optional) */
    sourceFile?: string;
}

interface ProjectState {
    currentProject: ProjectMetadata | null;
    recentProjects: ProjectMetadata[];

    // Actions
    createProject: (metadata: Omit<ProjectMetadata, 'id' | 'createdAt' | 'lastModified'>) => void;
    openProject: (project: ProjectMetadata) => void;
    /** Load project from a .qaqc file - sets metadata and adds to recent */
    loadFromFile: (metadata: ProjectMetadata, sourceFileName: string) => void;
    closeProject: () => void;
    updateProject: (metadata: Partial<ProjectMetadata>) => void;
}

export const useProjectStore = create<ProjectState>()(
    persist(
        (set) => ({
            currentProject: null,
            recentProjects: [],

            createProject: (metadata) => {
                const newProject: ProjectMetadata = {
                    ...metadata,
                    id: crypto.randomUUID(),
                    createdAt: new Date().toISOString(),
                    lastModified: new Date().toISOString(),
                };

                set((state) => ({
                    currentProject: newProject,
                    recentProjects: [newProject, ...state.recentProjects].slice(0, 10) // Keep max 10 recent projects
                }));
            },

            openProject: (project) => {
                set((state) => ({
                    currentProject: { ...project, lastModified: new Date().toISOString() },
                    recentProjects: [
                        { ...project, lastModified: new Date().toISOString() },
                        ...state.recentProjects.filter(p => p.id !== project.id)
                    ].slice(0, 10) // Keep max 10 recent projects
                }));
            },

            loadFromFile: (metadata, sourceFileName) => {
                const loadedProject: ProjectMetadata = {
                    ...metadata,
                    lastModified: new Date().toISOString(),
                    sourceFile: sourceFileName,
                };

                set((state) => ({
                    currentProject: loadedProject,
                    recentProjects: [
                        loadedProject,
                        ...state.recentProjects.filter(p => p.id !== metadata.id)
                    ].slice(0, 10) // Keep max 10 recent projects
                }));
            },

            closeProject: () => set({ currentProject: null }),

            updateProject: (metadata) =>
                set((state) => {
                    if (!state.currentProject) return state;
                    const updated = { ...state.currentProject, ...metadata, lastModified: new Date().toISOString() };
                    return {
                        currentProject: updated,
                        recentProjects: state.recentProjects.map(p => p.id === updated.id ? updated : p)
                    };
                }),
        }),
        {
            name: 'qaqc-project-storage',
        }
    )
);
