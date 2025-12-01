import React from 'react';
import { DndContext, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { Plus } from 'lucide-react';
import { useTemplateStore } from '../../stores/templateStore';
import { SortableSection } from './SortableSection';

interface SectionListProps {
    previewMode: boolean;
}

export const SectionList: React.FC<SectionListProps> = ({ previewMode }) => {
    const {
        activeTemplate,
        selectedSectionId,
        selectSection,
        reorderSections,
        addSection
    } = useTemplateStore();

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        })
    );

    const handleDragEnd = (event: DragEndEvent) => {
        const { active, over } = event;
        if (!over || active.id === over.id) return;

        const oldIndex = activeTemplate!.sections.findIndex(s => s.id === active.id);
        const newIndex = activeTemplate!.sections.findIndex(s => s.id === over.id);

        reorderSections(oldIndex, newIndex);
    };

    const handleAddSection = () => {
        const newSection = {
            id: `section_${Date.now()} `,
            label: 'New Section',
            order: (activeTemplate?.sections.length || 0) + 1,
            optional: false,
            blocks: []
        };
        addSection(newSection);
    };

    if (!activeTemplate) return null;

    return (
        <div className="p-4">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-white">Sections</h2>
                {!previewMode && (
                    <button
                        onClick={handleAddSection}
                        className="p-2 rounded-lg bg-gray-800 hover:bg-gray-700 transition-colors"
                        title="Add Section"
                    >
                        <Plus className="w-4 h-4 text-primary" />
                    </button>
                )}
            </div>

            <DndContext
                sensors={sensors}
                collisionDetection={closestCenter}
                onDragEnd={handleDragEnd}
            >
                <SortableContext
                    items={activeTemplate.sections.map(s => s.id)}
                    strategy={verticalListSortingStrategy}
                >
                    <div className="space-y-2">
                        {activeTemplate.sections.map((section) => (
                            <SortableSection
                                key={section.id}
                                section={section}
                                isSelected={selectedSectionId === section.id}
                                onSelect={() => selectSection(section.id)}
                                previewMode={previewMode}
                            />
                        ))}
                    </div>
                </SortableContext>
            </DndContext>
        </div>
    );
};
