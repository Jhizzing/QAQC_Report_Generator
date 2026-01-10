/**
 * Project File Utilities
 * 
 * Handles saving and loading QAQC project files (.qaqc format).
 * The .qaqc format is a JSON file containing all project state.
 */

import type { ProjectMetadata } from '../stores/projectStore';
import type { ProcessedData } from './fileProcessor';
import type { MethodologyConfig } from '../features/analysis/MethodologyWizard';
import type { QAQCConfig } from '../features/analysis/QAQCRuleConfig';
import type { QAQCAnalysisOutput } from '../features/analysis/qaqcAnalysis';

// Current file format version
export const PROJECT_FILE_VERSION = '1.0.0';

// Workflow steps type (includes legacy steps for backwards compatibility)
export type WorkflowStep = 'entry' | 'import' | 'setup' | 'category' | 'methodology' | 'qaqcRules' | 'dashboard' | 'report' | 'template_editor';

// Data category type
export type DataCategory = 'gold' | 'pxrf' | 'multi' | 'photon' | null;

/**
 * Complete project file structure
 * This is what gets saved to/loaded from .qaqc files
 */
export interface QAQCProjectFile {
    // File format metadata
    version: string;
    savedAt: string;
    
    // Project metadata
    metadata: ProjectMetadata;
    
    // Imported data
    data: ProcessedData | null;
    
    // Configuration
    category: DataCategory;
    methodologyConfig: MethodologyConfig | null;
    qaqcConfig: QAQCConfig | null;
    
    // Analysis results
    analysisResults: QAQCAnalysisOutput | null;
    
    // Current workflow position
    workflowStep: WorkflowStep;
}

/**
 * Project state interface for App.tsx
 * Used to pass state between components
 */
export interface ProjectState {
    data: ProcessedData | null;
    category: DataCategory;
    methodologyConfig: MethodologyConfig | null;
    qaqcConfig: QAQCConfig | null;
    analysisResults: QAQCAnalysisOutput | null;
    workflowStep: WorkflowStep;
}

/**
 * Save project state to a .qaqc file
 * Triggers browser download of the file
 */
export function saveProjectToFile(
    metadata: ProjectMetadata,
    state: ProjectState
): void {
    const projectFile: QAQCProjectFile = {
        version: PROJECT_FILE_VERSION,
        savedAt: new Date().toISOString(),
        metadata,
        data: state.data,
        category: state.category,
        methodologyConfig: state.methodologyConfig,
        qaqcConfig: state.qaqcConfig,
        analysisResults: state.analysisResults,
        workflowStep: state.workflowStep,
    };

    // Convert to JSON with nice formatting
    const jsonContent = JSON.stringify(projectFile, null, 2);
    
    // Create blob and download
    const blob = new Blob([jsonContent], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    
    // Generate filename from project name
    const safeName = metadata.name.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filename = `${safeName}_${new Date().toISOString().split('T')[0]}.qaqc`;
    
    // Trigger download
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Cleanup
    URL.revokeObjectURL(url);
}

/**
 * Load and parse a .qaqc project file
 * Returns the parsed project data or throws an error
 */
export async function loadProjectFromFile(file: File): Promise<QAQCProjectFile> {
    return new Promise((resolve, reject) => {
        // Validate file extension
        if (!file.name.toLowerCase().endsWith('.qaqc')) {
            reject(new Error('Invalid file type. Please select a .qaqc file.'));
            return;
        }

        const reader = new FileReader();
        
        reader.onload = (event) => {
            try {
                const content = event.target?.result as string;
                const projectFile = JSON.parse(content) as QAQCProjectFile;
                
                // Validate file structure
                if (!projectFile.version || !projectFile.metadata) {
                    throw new Error('Invalid project file format: missing required fields');
                }
                
                // Check version compatibility
                const [major] = projectFile.version.split('.');
                const [currentMajor] = PROJECT_FILE_VERSION.split('.');
                if (major !== currentMajor) {
                    throw new Error(`Incompatible project file version: ${projectFile.version}. Expected version ${PROJECT_FILE_VERSION}.`);
                }
                
                resolve(projectFile);
            } catch (error) {
                if (error instanceof SyntaxError) {
                    reject(new Error('Invalid project file: unable to parse JSON content'));
                } else {
                    reject(error);
                }
            }
        };
        
        reader.onerror = () => {
            reject(new Error('Failed to read project file'));
        };
        
        reader.readAsText(file);
    });
}

/**
 * Extract project state from a loaded project file
 */
export function extractProjectState(projectFile: QAQCProjectFile): ProjectState {
    return {
        data: projectFile.data,
        category: projectFile.category,
        methodologyConfig: projectFile.methodologyConfig,
        qaqcConfig: projectFile.qaqcConfig,
        analysisResults: projectFile.analysisResults,
        workflowStep: projectFile.workflowStep,
    };
}

/**
 * Create file input element for selecting .qaqc files
 * Returns a promise that resolves with the selected file
 */
export function selectProjectFile(): Promise<File | null> {
    return new Promise((resolve) => {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = '.qaqc';
        
        input.onchange = (event) => {
            const target = event.target as HTMLInputElement;
            const file = target.files?.[0] || null;
            resolve(file);
        };
        
        // Handle cancel
        input.oncancel = () => resolve(null);
        
        // Fallback for browsers that don't support oncancel
        window.addEventListener('focus', function focusHandler() {
            setTimeout(() => {
                if (!input.files?.length) {
                    resolve(null);
                }
                window.removeEventListener('focus', focusHandler);
            }, 300);
        }, { once: true });
        
        input.click();
    });
}

