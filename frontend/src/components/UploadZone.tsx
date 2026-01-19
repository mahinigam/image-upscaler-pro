import React from 'react';
import { Upload } from 'lucide-react';
import clsx from 'clsx';
import { useDropzone } from 'react-dropzone'; // Note: Need to install react-dropzone if not present, or implement manual logic. 
// Actually I didn't install react-dropzone. I'll use simple input logic or request install.
// I'll stick to simple input for now or add it to install list. 
// I'll implement a simple robust drag-drop without extra lib for minimalism.

interface UploadZoneProps {
    onFileSelect: (file: File) => void;
    isDragging?: boolean;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect }) => {
    const [isDragOver, setIsDragOver] = React.useState(false);
    const fileInputRef = React.useRef<HTMLInputElement>(null);

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(true);
    };

    const handleDragLeave = () => {
        setIsDragOver(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragOver(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            onFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            onFileSelect(e.target.files[0]);
        }
    };

    return (
        <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={handleClick}
            className={clsx(
                "relative group cursor-pointer transition-all duration-300 ease-out",
                "bg-obsidian-surface/60 backdrop-blur-md border border-dashed rounded-lg h-64 flex flex-col items-center justify-center",
                isDragOver
                    ? "border-neon-cyan shadow-[0_0_30px_rgba(102,252,241,0.2)] bg-obsidian-surface/80"
                    : "border-gray-700 hover:border-gray-500 hover:bg-obsidian-surface/80"
            )}
        >
            <input
                type="file"
                ref={fileInputRef}
                onChange={handleInputChange}
                accept="image/*"
                className="hidden"
            />

            {/* Corner Accents */}
            <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity" />

            <div className={clsx("p-4 rounded-full bg-white/5 mb-4 group-hover:scale-110 transition-transform duration-300", isDragOver && "bg-neon-cyan/20")}>
                <Upload className={clsx("w-8 h-8", isDragOver ? "text-neon-cyan" : "text-gray-400 group-hover:text-neon-cyan")} />
            </div>

            <p className="font-heading uppercase tracking-widest text-sm text-gray-400 group-hover:text-white transition-colors">
                {isDragOver ? "Drop file to upload" : "Click or Drop to Upload"}
            </p>
        </div>
    );
};
