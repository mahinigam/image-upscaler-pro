import React from 'react';

interface SettingsPanelProps {
    model: string;
    setModel: (m: string) => void;
    format: string;
    setFormat: (f: string) => void;
}

export const SettingsPanel: React.FC<SettingsPanelProps> = ({ model, setModel, format, setFormat }) => {
    return (
        <div className="bg-obsidian-surface/60 backdrop-blur-md border border-white/10 rounded-3xl p-5 mb-6 mt-6 shadow-[0_20px_50px_rgba(0,0,0,0.4)]">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Model Selection */}
                <div className="space-y-2">
                    <label className="block font-heading uppercase text-xs tracking-widest text-gray-400">Model</label>
                    <select
                        value={model}
                        onChange={(e) => setModel(e.target.value)}
                        className="w-full bg-[#0a0a10] border border-white/10 text-gray-200 p-2.5 rounded-xl focus:border-neon-cyan focus:outline-none transition-colors font-body text-xs"
                    >
                        <option value="realesrgan-x4plus">RealESRGAN x4 Plus (General)</option>
                        <option value="realesrgan-x4plus-anime">RealESRGAN x4 Plus (Anime)</option>
                    </select>
                </div>

                {/* Format Selection */}
                <div className="space-y-2">
                    <label className="block font-heading uppercase text-xs tracking-widest text-gray-400">Output Format</label>
                    <select
                        value={format}
                        onChange={(e) => setFormat(e.target.value)}
                        className="w-full bg-[#0a0a10] border border-white/10 text-gray-200 p-2.5 rounded-xl focus:border-neon-cyan focus:outline-none transition-colors font-body text-xs"
                    >
                        <option value="png">PNG (Lossless)</option>
                        <option value="jpg">JPG (Small Size)</option>
                        <option value="webp">WebP (Efficient)</option>
                    </select>
                </div>
            </div>
        </div>
    );
};
