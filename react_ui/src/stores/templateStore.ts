/**
 * Template Store - Zustand state management for report templates
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { ReportTemplate, TemplateSection, TemplateBlock, TemplateValidation } from '../types/reportTemplate';
import jorcFullTemplate from '../templates/jorc_full.json';

interface TemplateState {
    // Active template being edited/used
    activeTemplate: ReportTemplate | null;

    // All available templates
    templates: ReportTemplate[];

    // Currently selected section/block in editor
    selectedSectionId: string | null;
    selectedBlockId: string | null;

    // Actions
    loadTemplate: (templateId: string) => void;
    setActiveTemplate: (template: ReportTemplate) => void;
    saveTemplate: (template: ReportTemplate) => void;
    deleteTemplate: (templateId: string) => void;

    // Section actions
    addSection: (section: TemplateSection) => void;
    updateSection: (sectionId: string, updates: Partial<TemplateSection>) => void;
    deleteSection: (sectionId: string) => void;
    reorderSections: (oldIndex: number, newIndex: number) => void;

    // Block actions
    addBlock: (sectionId: string, block: TemplateBlock) => void;
    updateBlock: (sectionId: string, blockId: string, updates: Partial<TemplateBlock>) => void;
    deleteBlock: (sectionId: string, blockId: string) => void;
    reorderBlocks: (sectionId: string, oldIndex: number, newIndex: number) => void;

    // Selection
    selectSection: (sectionId: string | null) => void;
    selectBlock: (blockId: string | null) => void;

    // Validation
    validateTemplate: (template: ReportTemplate) => TemplateValidation;

    // Import/Export
    exportTemplate: (templateId: string) => string;
    importTemplate: (json: string) => void;
}

export const useTemplateStore = create<TemplateState>()(
    persist(
        (set, get) => ({
            activeTemplate: jorcFullTemplate as ReportTemplate,
            templates: [jorcFullTemplate as ReportTemplate],
            selectedSectionId: null,
            selectedBlockId: null,

            loadTemplate: (templateId) => {
                const template = get().templates.find(t => t.template_id === templateId);
                if (template) {
                    set({ activeTemplate: template });
                }
            },

            setActiveTemplate: (template) => {
                set({ activeTemplate: template });
            },

            saveTemplate: (template) => {
                set((state) => {
                    const existing = state.templates.findIndex(t => t.template_id === template.template_id);
                    if (existing >= 0) {
                        const updated = [...state.templates];
                        updated[existing] = template;
                        return { templates: updated, activeTemplate: template };
                    } else {
                        return {
                            templates: [...state.templates, template],
                            activeTemplate: template
                        };
                    }
                });
            },

            deleteTemplate: (templateId) => {
                set((state) => ({
                    templates: state.templates.filter(t => t.template_id !== templateId),
                    activeTemplate: state.activeTemplate?.template_id === templateId ? null : state.activeTemplate
                }));
            },

            addSection: (section) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: [...state.activeTemplate.sections, section]
                        }
                    };
                });
            },

            updateSection: (sectionId, updates) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.map(s =>
                                s.id === sectionId ? { ...s, ...updates } : s
                            )
                        }
                    };
                });
            },

            deleteSection: (sectionId) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.filter(s => s.id !== sectionId)
                        },
                        selectedSectionId: state.selectedSectionId === sectionId ? null : state.selectedSectionId
                    };
                });
            },

            reorderSections: (oldIndex, newIndex) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    const sections = [...state.activeTemplate.sections];
                    const [moved] = sections.splice(oldIndex, 1);
                    sections.splice(newIndex, 0, moved);
                    // Update order numbers
                    sections.forEach((section, index) => {
                        section.order = index;
                    });
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections
                        }
                    };
                });
            },

            addBlock: (sectionId, block) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.map(s =>
                                s.id === sectionId
                                    ? { ...s, blocks: [...s.blocks, block] }
                                    : s
                            )
                        }
                    };
                });
            },

            updateBlock: (sectionId, blockId, updates) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.map(s =>
                                s.id === sectionId
                                    ? {
                                        ...s,
                                        blocks: s.blocks.map(b =>
                                            b.id === blockId ? { ...b, ...updates } : b
                                        )
                                    }
                                    : s
                            )
                        }
                    };
                });
            },

            deleteBlock: (sectionId, blockId) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.map(s =>
                                s.id === sectionId
                                    ? { ...s, blocks: s.blocks.filter(b => b.id !== blockId) }
                                    : s
                            )
                        },
                        selectedBlockId: state.selectedBlockId === blockId ? null : state.selectedBlockId
                    };
                });
            },

            reorderBlocks: (sectionId, oldIndex, newIndex) => {
                set((state) => {
                    if (!state.activeTemplate) return state;
                    return {
                        activeTemplate: {
                            ...state.activeTemplate,
                            sections: state.activeTemplate.sections.map(s => {
                                if (s.id !== sectionId) return s;
                                const blocks = [...s.blocks];
                                const [moved] = blocks.splice(oldIndex, 1);
                                blocks.splice(newIndex, 0, moved);
                                // Update order numbers
                                blocks.forEach((block, index) => {
                                    block.order = index + 1;
                                });
                                return { ...s, blocks };
                            })
                        }
                    };
                });
            },

            selectSection: (sectionId) => {
                set({ selectedSectionId: sectionId, selectedBlockId: null });
            },

            selectBlock: (blockId) => {
                set({ selectedBlockId: blockId });
            },

            validateTemplate: (template) => {
                const errors: string[] = [];
                const warnings: string[] = [];

                if (!template.template_id) {
                    errors.push('Template must have an ID');
                }

                if (!template.title) {
                    errors.push('Template must have a title');
                }

                if (template.sections.length === 0) {
                    errors.push('Template must have at least one section');
                }

                template.sections.forEach((section, sIndex) => {
                    if (!section.id) {
                        errors.push(`Section ${sIndex + 1} missing ID`);
                    }
                    if (!section.label) {
                        errors.push(`Section "${section.id}" missing label`);
                    }
                    if (section.blocks.length === 0) {
                        warnings.push(`Section "${section.label}" has no blocks`);
                    }

                    section.blocks.forEach((block, bIndex) => {
                        if (!block.id) {
                            errors.push(`Block ${bIndex + 1} in section "${section.label}" missing ID`);
                        }
                        if (!block.type) {
                            errors.push(`Block "${block.id}" missing type`);
                        }
                        if (!block.label) {
                            errors.push(`Block "${block.id}" missing label`);
                        }
                        if (!block.key && block.type !== 'text_user') {
                            warnings.push(`Block "${block.label}" missing data binding key`);
                        }
                    });
                });

                return {
                    valid: errors.length === 0,
                    errors,
                    warnings
                };
            },

            exportTemplate: (templateId) => {
                const template = get().templates.find(t => t.template_id === templateId);
                if (!template) throw new Error('Template not found');
                return JSON.stringify(template, null, 2);
            },

            importTemplate: (json) => {
                try {
                    const template = JSON.parse(json) as ReportTemplate;
                    const validation = get().validateTemplate(template);
                    if (!validation.valid) {
                        throw new Error(`Invalid template: ${validation.errors.join(', ')}`);
                    }
                    get().saveTemplate(template);
                } catch (error) {
                    throw new Error(`Failed to import template: ${error}`);
                }
            }
        }),
        {
            name: 'template-storage',
            partialize: (state) => ({
                templates: state.templates,
                activeTemplate: state.activeTemplate
            })
        }
    )
);
