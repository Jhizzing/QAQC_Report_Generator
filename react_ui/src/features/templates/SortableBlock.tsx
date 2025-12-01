import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, Trash2, Edit, FileText, Table, BarChart3, Tag } from 'lucide-react';
import type { TemplateBlock, BlockType } from '../../types/reportTemplate';
import { useTemplateStore } from '../../stores/templateStore';

interface SortableBlockProps {
    block: TemplateBlock;
    sectionId: string;
    previewMode: boolean;
}

const BLOCK_ICONS: Record<BlockType, React.ReactNode> = {
    'text_auto': <FileText className="w-5 h-5 text-blue-400" />,
    'text_user': <FileText className="w-5 h-5 text-green-400" />,
    'text_mixed': <FileText className="w-5 h-5 text-purple-400" />,
    'table_auto': <Table className="w-5 h-5 text-cyan-400" />,
    'table_user': <Table className="w-5 h-5 text-teal-400" />,
    'figure_auto': <BarChart3 className="w-5 h-5 text-amber-400" />,
    'meta': <Tag className="w-5 h-5 text-pink-400" />
};

export const SortableBlock: React.FC<SortableBlockProps> = ({
    block,
    sectionId,
    previewMode
}) => {
    const { selectBlock, deleteBlock } = useTemplateStore();

    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: block.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        opacity: isDragging ? 0.5 : 1,
    };

    const handleEdit = () => {
        selectBlock(block.id);
    };

    const handleDelete = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (window.confirm(`Delete block "${block.label}"?`)) {
            deleteBlock(sectionId, block.id);
        }
    };

    return (
        <div
            ref={setNodeRef}
            style={style}
            className="bg-gray-800 rounded-lg p-4 border-2 border-transparent hover:border-gray-700 transition-all"
        >
            <div className="flex items-start gap-3">
                {!previewMode && (
                    <div {...attributes} {...listeners} className="cursor-move pt-1">
                        <GripVertical className="w-5 h-5 text-gray-500" />
                    </div>
                )}

                <div className="pt-0.5">
                    {BLOCK_ICONS[block.type]}
                </div>

                <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-medium text-white truncate">{block.label}</h3>
                        {block.required && (
                            <span className="px-2 py-0.5 text-xs bg-red-900/30 text-red-400 rounded">
                                Required
                            </span>
                        )}
                    </div>

                    {block.description && (
                        <p className="text-sm text-gray-400 mb-2">{block.description}</p>
                    )}

                    <div className="flex items-center gap-3 text-xs">
                        <span className="px-2 py-1 bg-gray-900 text-gray-300 rounded">
                            {block.type.replace('_', ' ')}
                        </span>
                        {block.key && (
                            <code className="px-2 py-1 bg-gray-900 text-primary rounded font-mono">
                                {block.key}
                            </code>
                        )}
                    </div>
                </div>

                {!previewMode && (
                    <div className="flex gap-2">
                        <button
                            onClick={handleEdit}
                            className="p-2 rounded hover:bg-gray-700 transition-colors"
                            title="Edit Block"
                        >
                            <Edit className="w-4 h-4 text-gray-400" />
                        </button>
                        <button
                            onClick={handleDelete}
                            className="p-2 rounded hover:bg-red-900/30 transition-colors"
                            title="Delete Block"
                        >
                            <Trash2 className="w-4 h-4 text-red-400" />
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};
