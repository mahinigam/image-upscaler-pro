import React from 'react';

export const Header: React.FC = () => {
    return (
        <div className="text-center mb-12">
            <h1 className="font-heading font-bold text-5xl md:text-6xl uppercase tracking-[0.15em] mb-2 bg-gradient-to-b from-white to-gray-500 bg-clip-text text-transparent drop-shadow-[0_0_35px_rgba(255,255,255,0.1)]">
                Image Upscaler Pro
            </h1>
            <p className="font-heading text-neon-cyan uppercase tracking-[0.2em] text-lg opacity-80 drop-shadow-[0_0_10px_rgba(102,252,241,0.3)]">
                AI-Powered Enhancement
            </p>
        </div>
    );
};
