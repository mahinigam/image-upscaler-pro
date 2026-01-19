export type UpscaleState = 'idle' | 'uploading' | 'processing' | 'completed' | 'error';

export interface UpscaleResponse {
    url: string; // Blob URL or path
    originalUrl: string;
}

// Design Tokens (Obsidian Chrome)
export const theme = {
    colors: {
        bg: '#0b0c10', // Obsidian Base
        surface: '#1f2833', // Obsidian Surface
        accent: '#66fcf1', // Neon Cyan
        accentSecondary: '#c5a3ff', // Neon Purple
        border: 'rgba(255, 255, 255, 0.15)',
    },
    fonts: {
        heading: 'Saira, sans-serif',
        body: 'Outfit, sans-serif',
    }
};
