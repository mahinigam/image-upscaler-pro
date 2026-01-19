<p align="center">
  <h1 align="center">Image Upscaler Pro</h1>
  <p align="center">
    High-quality AI-powered image upscaling using Real-ESRGAN
    <br />
    <a href="#quick-start">Quick Start</a>
    ·
    <a href="#features">Features</a>
    ·
    <a href="#how-it-works">How It Works</a>
  </p>
</p>

---

## Overview

Image Upscaler Pro is a local, offline image upscaling tool that uses **Real-ESRGAN** - a state-of-the-art deep learning model for image super-resolution. It preserves fine details, textures, and edges while enlarging images up to 8x their original size.

**Key Highlights:**
- Same quality as Real-ESRGAN PyTorch implementation
- Runs entirely offline - your images never leave your device
- Optimized for Apple Silicon (M1/M2/M3/M4) with GPU acceleration
- Simple web interface - no command line required

---

## Features

| Feature | Description |
|---------|-------------|
| **AI Upscaling** | Real-ESRGAN neural network for best-in-class quality |
| **Multiple Scales** | 2x, 4x, and 8x enlargement options |
| **Model Selection** | Choose between quality-focused and speed-focused models |
| **Format Support** | PNG (lossless), JPG, WebP output formats |
| **Before/After** | Interactive comparison slider |
| **Drag & Drop** | Simple web interface with file upload |
| **Privacy First** | 100% offline - no cloud processing |

---

## Quick Start

### Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4) or Intel
- Python 3.10 or higher

### Installation

```bash
# Clone the repository
git clone https://github.com/mahinigam/image-upscaler.git
cd image-upscaler

# Make the run script executable
chmod +x run.sh

# Run the application
./run.sh
```

The application will:
1. Create a virtual environment
2. Install dependencies
3. Launch the web interface at **http://localhost:7860**

### First Run

On your first upscale, the Real-ESRGAN binary (~10MB) will be downloaded automatically. This is a one-time setup.

---

## Usage

1. **Upload** - Drag and drop an image or click to browse
2. **Configure** - Select scale factor and model
3. **Upscale** - Click "Upscale Image"
4. **Compare** - Use the before/after slider
5. **Download** - Save the result

### Scale Factors

| Scale | Output Size | Best For |
|-------|-------------|----------|
| 2x | 2× width & height | Quick enhancement |
| 4x | 4× width & height | Recommended balance |
| 8x | 8× width & height | Maximum enlargement |

### Models

| Model | Quality | Speed | Best For |
|-------|---------|-------|----------|
| Real-ESRGAN x4plus | Highest | Slower | Photos, portraits |
| Real-ESRNet x4plus | High | Faster | Batch processing |
| Real-ESRGAN Anime | Highest | Slower | Illustrations, artwork |

---

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                        Architecture                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Web UI (Gradio)                                              │
│        │                                                        │
│        ▼                                                        │
│   Python Backend ──────► realesrgan-ncnn-vulkan                │
│        │                        │                               │
│        │                        ▼                               │
│        │                 Real-ESRGAN Model                      │
│        │                 (RRDB Neural Network)                  │
│        │                        │                               │
│        │                        ▼                               │
│        │                 GPU (Vulkan/Metal)                     │
│        │                        │                               │
│        ▼                        ▼                               │
│   Upscaled Image ◄──────────────┘                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

The tool uses the official **realesrgan-ncnn-vulkan** binary from the Real-ESRGAN authors. This provides:
- Identical model weights and quality as the PyTorch version
- Native GPU acceleration via Vulkan (Metal on macOS)
- No Python version compatibility issues

---

## Supported Formats

**Input:** PNG, JPG, JPEG, WebP, BMP, TIFF

**Output:** PNG (lossless), JPG (quality 95), WebP

---

## Project Structure

```
image-upscaler/
├── app.py              # Gradio web interface
├── upscaler.py         # Core upscaling engine
├── requirements.txt    # Python dependencies
├── run.sh              # Startup script
├── README.md           # This file
└── bin/                # Downloaded binary (auto-created)
```

---

## System Requirements

| Component | Requirement |
|-----------|-------------|
| OS | macOS 11+ (Big Sur or later) |
| CPU | Apple Silicon (M1/M2/M3/M4) or Intel |
| RAM | 8GB minimum, 16GB recommended |
| Python | 3.10 or higher |
| Disk | ~500MB for dependencies and binary |

---

## Troubleshooting

**App won't start?**
```bash
# Remove virtual environment and reinstall
rm -rf venv
./run.sh
```

**Binary download fails?**
- Check your internet connection
- The binary is downloaded from GitHub releases

**Slow performance?**
- Close other GPU-intensive applications
- Use 2x scale for faster processing

---

## Acknowledgments

- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) - The underlying super-resolution model
- [NCNN](https://github.com/Tencent/ncnn) - High-performance neural network inference framework
- [Gradio](https://gradio.app/) - Web interface framework

---

## License

MIT License - Free for personal and commercial use.

---

<p align="center">
  Made with Python and Real-ESRGAN
</p>
