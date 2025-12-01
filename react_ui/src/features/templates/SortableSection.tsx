import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, Trash2 } from 'lucide-react';
import type { TemplateSection } from '../../types/reportTemplate';
import { useTemplateStore } from '../../stores/templateStore';

interface SortableSectionProps {
    section: TemplateSection;
    isSelected: boolean;
    onSelect: () => void;
    previewMode: boolean;
}

export const SortableSection: React.FC<SortableSectionProps> = ({
    section,
    isSelected,
    onSelect,
    previewMode
}) => {
    const { deleteSection } = useTemplateStore();

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: section.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
    };

    const handleDelete = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm(`Delete section "${section.label}"?`)) {
            deleteSection(section.id);
        }
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            onClick={onSelect}
            className={`flex items-center gap-2 p-3 rounded-lg cursor-pointer transition-all ${isSelected
                    ? 'bg-primary/10 border-2 border-primary'
                    : 'bg-gray-800 border-2 border-transparent hover:border-gray-700'
                }`}
        >
            {!previewMode && (
                <div {...attributes} {...listeners} className="cursor-move">
                    <GripVertical className="w-4 h-4 text-gray-500" />
                </div>
            )}

            <div className="flex-1 min-w-0">
                <div className="font-medium text-white truncate">{section.label}</div>
                <div className="text-xs text-gray-400">{section.blocks.length} blocks</div>
            </div>

            {section.optional && (
                <span className="px-2 py-0.5 text-xs bg-yellow-900/30 text-yellow-400 rounded">
                    Optional
                </span>
            )}

            {!previewMode && (
                <button
                    onClick={handleDelete}
                    className="p-1 rounded hover:bg-red-900/30 transition-colors"
                    title="Delete Section"
                >
                    <Trash2 className="w-4 h-4 text-red-400" />
                </button>
            )}
        </div>
    );
};
