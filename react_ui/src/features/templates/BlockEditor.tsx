import React from 'react';
import { DndContext, closestCenter, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { Plus, FileText, Table, BarChart3, Tag } from 'lucide-react';
import { useTemplateStore } from '../../stores/templateStore';
import { SortableBlock } from './SortableBlock';
import type { BlockType } from '../../types/reportTemplate';

interface BlockEditorProps {
    previewMode: boolean;
}

const BLOCK_TYPE_OPTIONS: { type: BlockType; label: string; icon: React.ReactNode }[] = [
    { type: 'text_auto', label: 'Auto-Generated Text', icon: <FileText className="w-4 h-4" /> },
    { type: 'text_user', label: 'User Input Text', icon: <FileText className="w-4 h-4" /> },
    { type: 'table_auto', label: 'Auto-Generated Table', icon: <Table className="w-4 h-4" /> },
    { type: 'figure_auto', label: 'Auto-Generated Figure', icon: <BarChart3 className="w-4 h-4" /> },
    { type: 'meta', label: 'Metadata Field', icon: <Tag className="w-4 h-4" /> },
];

export const BlockEditor: React.FC<BlockEditorProps> = ({ previewMode }) => {
    const {
        activeTemplate,
        selectedSectionId,
        addBlock,
        reorderBlocks
    } = useTemplateStore();

    const sensors = useSensors(
        useSensor(PointerSensor, {
            activationConstraint: {
                distance: 8,
            },
        })
    );

    const selectedSection = activeTemplate?.sections.find(s => s.id === selectedSectionId);

    const handleDragEnd = (event: DragEndEvent) => {
        if (!selectedSectionId) return;

        const { active, over } = event;
        if (!over || active.id === over.id) return;

        const blocks = selectedSection!.blocks;
        const oldIndex = blocks.findIndex(b => b.id === active.id);
        const newIndex = blocks.findIndex(b => b.id === over.id);

        reorderBlocks(selectedSectionId, oldIndex, newIndex);
    };

    const handleAddBlock = (type: BlockType) => {
        if (!selectedSectionId) return;

        const newBlock = {
            id: `block_${Date.now()}`,
            type,
            label: `New ${type.replace('_', ' ')}`,
            order: (selectedSection?.blocks.length || 0) + 1,
            required: false
        };

        addBlock(selectedSectionId, newBlock);
    };

    if (!activeTemplate || !selectedSection) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="text-center">
                    <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <p className="text-gray-400">Select a section to edit its blocks</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-6">
            <div className="mb-6">
                <h2 className="text-2xl font-bold text-white mb-2">{selectedSection.label}</h2>
                <p className="text-gray-400">{selectedSection.blocks.length} blocks</p>
            </div>

            <DndContext
                sensors={sensors}
                collisionDetection={closestCenter}
                onDragEnd={handleDragEnd}
            >
                <SortableContext
                    items={selectedSection.blocks.map(b => b.id)}
                    strategy={verticalListSortingStrategy}
                >
                    <div className="space-y-3 mb-6">
                        {selectedSection.blocks.map((block) => (
                            <SortableBlock
                                key={block.id}
                                block={block}
                                sectionId={selectedSectionId}
                                previewMode={previewMode}
                            />
                        ))}
                    </div>
                </SortableContext>
            </DndContext>

            {!previewMode && (
                <div className="mt-6">
                    <details className="bg-gray-800 rounded-lg">
                        <summary className="cursor-pointer px-4 py-3 font-medium text-white hover:bg-gray-700 transition-colors flex items-center gap-2" data-tour="add-block">
                            <Plus className="w-4 h-4 text-primary" />
                            Add Block
                        </summary>
                        <div className="p-4 space-y-2">
                            {BLOCK_TYPE_OPTIONS.map((option) => (
                                <button
                                    key={option.type}
                                    onClick={() => handleAddBlock(option.type)}
                                    className="w-full flex items-center gap-3 px-4 py-3 bg-gray-900 hover:bg-gray-700 rounded-lg transition-colors text-left"
                                >
                                    <div className="text-primary">{option.icon}</div>
                                    <span className="text-white font-medium">{option.label}</span>
                                </button>
                            ))}
                        </div>
                    </details>
                </div>
            )}
        </div>
    );
};
