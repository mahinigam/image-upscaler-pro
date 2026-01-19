# Image Upscaler Pro

A high-quality, AI-powered image upscaler using Real-ESRGAN. Optimized for Apple Silicon (M1/M2/M3/M4) with GPU acceleration.

## Features

- **AI-Powered Upscaling** - Uses Real-ESRGAN for best-in-class quality
- **Multiple Scale Factors** - 2x and 4x upscaling
- **Multiple Models** - Choose the best model for your image type
- **Detail Preservation** - Maintains textures, edges, and fine details
- **Web Interface** - Easy drag-and-drop with before/after comparison
- **M4 Optimized** - Hardware-accelerated using Vulkan
- **Fully Offline** - All processing happens locally

## Quick Start

### Option 1: Using the run script (Recommended)

```bash
# Make the script executable (first time only)
chmod +x run.sh

# Run the application
./run.sh
```

### Option 2: Manual setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Then open **http://localhost:7860** in your browser.

## Usage

1. **Upload** - Drag and drop an image or click to browse
2. **Configure** - Select scale factor (2x, 4x), model, and output format
3. **Upscale** - Click "Upscale Image" and wait for processing
4. **Compare** - Use the before/after slider to see the difference
5. **Download** - Save the upscaled result

## Available Models

| Model | Best For | Quality |
|-------|----------|---------|
| Real-ESRGAN x4plus | General photos, portraits | Highest |
| Real-ESRNet x4plus | Fast processing needs | High |
| Real-ESRGAN Anime | Illustrations, artwork | Highest for anime |

## Supported Formats

- **Input**: PNG, JPG, JPEG, WebP, BMP, TIFF
- **Output**: PNG (lossless), JPG, WebP

## System Requirements

- macOS with Apple Silicon (M1/M2/M3/M4) - Recommended
- Python 3.10 or higher
- 8GB+ RAM recommended for large images

## First Run

On first run, the application will download the Real-ESRGAN binary (~10MB). This is a one-time download.

## License

MIT License - Free for personal and commercial use.
