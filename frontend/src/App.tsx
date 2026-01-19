import { useState } from 'react';
import { Header } from './components/Header';
import { UploadZone } from './components/UploadZone';
import { SettingsPanel } from './components/SettingsPanel';
import { LiquidButton } from './components/LiquidButton';
import { ComparisonView } from './components/ComparisonView';
import type { UpscaleState } from './types';
import { AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [processedUrl, setProcessedUrl] = useState<string | null>(null);
  const [status, setStatus] = useState<UpscaleState>('idle');
  const [error, setError] = useState<string | null>(null);

  // Settings
  const [model, setModel] = useState('realesrgan-x4plus');
  const [format, setFormat] = useState('png');

  const handleFileSelect = (selectedFile: File) => {
    setFile(selectedFile);
    setPreviewUrl(URL.createObjectURL(selectedFile));
    setProcessedUrl(null);
    setStatus('idle');
    setError(null);
  };

  const handleUpscale = async () => {
    if (!file) return;

    setStatus('processing');
    setError(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('model', model);
    formData.append('format', format);
    formData.append('scale', '4x');

    try {
      // Note: In development, we need to proxy or use CORS. 
      // Backend is at http://localhost:8000
      const response = await fetch('http://localhost:8000/upscale', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(JSON.parse(errText).detail || 'Upscaling failed');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setProcessedUrl(url);
      setStatus('completed');
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Something went wrong');
      setStatus('error');
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreviewUrl(null);
    setProcessedUrl(null);
    setStatus('idle');
    setError(null);
  };

  return (
    <div className="min-h-screen p-4 md:p-6 flex flex-col items-center justify-center">
      <div className="w-full max-w-2xl">
        <Header />

        <AnimatePresence mode="wait">
          {!file ? (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              key="upload"
            >
              <UploadZone onFileSelect={handleFileSelect} />
            </motion.div>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              key="preview"
              className="space-y-8"
            >
              <SettingsPanel
                model={model} setModel={setModel}
                format={format} setFormat={setFormat}
              />

              {/* Action Area */}
              <div className="flex flex-col items-center gap-4">
                {status === 'error' && (
                  <div className="flex items-center gap-2 text-red-400 bg-red-400/10 p-3 rounded border border-red-400/20">
                    <AlertCircle className="w-4 h-4" />
                    <span className="text-sm font-body">{error}</span>
                  </div>
                )}

                {status !== 'completed' && (
                  <LiquidButton onClick={handleUpscale} isLoading={status === 'processing'}>
                    {status === 'processing' ? 'Enhancing Image...' : 'Upscale Image 4x'}
                  </LiquidButton>
                )}

                {status === 'completed' && (
                  <div className="flex gap-4">
                    {processedUrl && (
                      <a
                        href={processedUrl}
                        download={`upscaled_${Date.now()}.${format}`}
                        className="bg-neon-cyan/20 border border-neon-cyan/50 text-neon-cyan hover:bg-neon-cyan hover:text-black transition-all px-6 py-3 rounded uppercase font-heading tracking-widest text-sm font-bold flex items-center gap-2"
                      >
                        Download Image
                      </a>
                    )}
                    <button
                      onClick={handleReset}
                      className="text-gray-500 hover:text-white underline font-heading tracking-widest text-xs uppercase"
                    >
                      Upload New
                    </button>
                  </div>
                )}
              </div>

              {/* Results View */}
              {status === 'completed' && processedUrl && previewUrl ? (
                <ComparisonView originalUrl={previewUrl} processedUrl={processedUrl} />
              ) : (
                // Just show preview if not done
                <div className="border border-white/10 rounded-lg p-4 bg-obsidian-surface/50 flex justify-center">
                  <img src={previewUrl!} alt="Preview" className="max-h-[400px] object-contain rounded" />
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

export default App;
