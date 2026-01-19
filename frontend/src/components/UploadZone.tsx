import React, { useCallback } from 'react';
import { Upload } from 'lucide-react';
import clsx from 'clsx';
import { useDropzone } from 'react-dropzone';

interface UploadZoneProps {
    onFileSelect: (file: File) => void;
}

export const UploadZone: React.FC<UploadZoneProps> = ({ onFileSelect }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        if (acceptedFiles && acceptedFiles.length > 0) {
            onFileSelect(acceptedFiles[0]);
        }
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': []
        },
        multiple: false
    });

    return (
        <div
            {...getRootProps()}
            className={clsx(
                "relative group cursor-pointer transition-all duration-300 ease-out",
                "bg-obsidian-surface/60 backdrop-blur-md border border-dashed rounded-3xl h-48 flex flex-col items-center justify-center",
                isDragActive
                    ? "border-neon-cyan shadow-[0_0_30px_rgba(102,252,241,0.2)] bg-obsidian-surface/80"
                    : "border-gray-700 hover:border-gray-500 hover:bg-obsidian-surface/80"
            )}
        >
            <input {...getInputProps()} />

            {/* Corner Accents - only visible on hover when not dragging, or always if we want */}
            <div className="absolute top-0 left-0 w-4 h-4 border-t-2 border-l-2 border-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity" />
            <div className="absolute bottom-0 right-0 w-4 h-4 border-b-2 border-r-2 border-neon-cyan opacity-0 group-hover:opacity-100 transition-opacity" />

            <div className={clsx("p-4 rounded-full bg-white/5 mb-4 group-hover:scale-110 transition-transform duration-300", isDragActive && "bg-neon-cyan/20")}>
                <Upload className={clsx("w-8 h-8", isDragActive ? "text-neon-cyan" : "text-gray-400 group-hover:text-neon-cyan")} />
            </div>

            <p className="font-heading uppercase tracking-widest text-sm text-gray-400 group-hover:text-white transition-colors">
                {isDragActive ? "Drop file to upload" : "Click or Drop to Upload"}
            </p>
        </div>
    );
};
