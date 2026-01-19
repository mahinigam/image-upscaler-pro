import React from 'react';
import { ReactCompareSlider, ReactCompareSliderImage } from 'react-compare-slider';

interface ComparisonViewProps {
    originalUrl: string;
    processedUrl: string;
}

export const ComparisonView: React.FC<ComparisonViewProps> = ({ originalUrl, processedUrl }) => {
    return (
        <div className="border border-white/10 rounded-lg overflow-hidden shadow-[0_20px_50px_rgba(0,0,0,0.5)] mt-8 relative group">
            <div className="absolute top-4 left-4 z-10 bg-black/60 backdrop-blur-sm px-3 py-1 rounded text-xs font-heading font-bold uppercase tracking-wider text-white border border-white/10">
                Original
            </div>
            <div className="absolute top-4 right-4 z-10 bg-neon-cyan/80 backdrop-blur-sm px-3 py-1 rounded text-xs font-heading font-bold uppercase tracking-wider text-black">
                Upscaled 4x
            </div>

            <ReactCompareSlider
                itemOne={<ReactCompareSliderImage src={originalUrl} alt="Original" />}
                itemTwo={<ReactCompareSliderImage src={processedUrl} alt="Processed" />}
                className="h-[600px] w-full bg-[#050510]"
                style={{ objectFit: 'contain' }}
            />
        </div>
    );
};
