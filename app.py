"""
Image Upscaler Web Application
A clean, modern Gradio-based web interface for high-quality image upscaling.
"""

import os
import tempfile
import numpy as np
import gradio as gr
from PIL import Image
from typing import Tuple, Optional
from upscaler import RealESRGANUpscaler, create_upscaler


# Global upscaler instance (lazy loaded)
_upscaler: Optional[RealESRGANUpscaler] = None


def get_upscaler() -> RealESRGANUpscaler:
    """Get or create the global upscaler instance."""
    global _upscaler
    if _upscaler is None:
        _upscaler = create_upscaler()
    return _upscaler


def save_image_to_file(image: np.ndarray, output_format: str) -> str:
    """Save the image to a file with the correct format."""
    format_map = {"PNG": "png", "JPG": "jpg", "WebP": "webp"}
    ext = format_map.get(output_format, "png")
    
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, f"upscaled_image.{ext}")
    
    pil_image = Image.fromarray(image)
    
    if ext == "jpg":
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")
        pil_image.save(temp_path, format="JPEG", quality=95)
    elif ext == "webp":
        pil_image.save(temp_path, format="WEBP", quality=95)
    else:
        pil_image.save(temp_path, format="PNG")
    
    return temp_path


def upscale_image(
    input_image: np.ndarray,
    scale_factor: str,
    model_choice: str,
    output_format: str,
    progress: gr.Progress = gr.Progress(),
) -> Tuple[Optional[np.ndarray], Optional[str], str]:
    """Upscale an image using Real-ESRGAN."""
    if input_image is None:
        return None, None, "Upload an image to get started"
    
    try:
        progress(0.05, desc="Starting...")
        
        upscaler = get_upscaler()
        scale = int(scale_factor.replace("x", ""))
        h, w = input_image.shape[:2]
        new_h, new_w = h * scale, w * scale
        
        def update_progress(p: float, msg: str):
            progress(0.05 + p * 0.85, desc=msg)
        
        model_map = {
            "Best Quality": "realesrgan-x4plus",
            "Faster": "realesrnet-x4plus",
            "Anime/Illustration": "realesrgan-x4plus-anime",
        }
        model_name = model_map.get(model_choice, "realesrgan-x4plus")
        
        output_rgb = upscaler.upscale_image(
            image=input_image,
            scale=scale,
            model=model_name,
            progress_callback=update_progress,
        )
        
        progress(0.95, desc="Saving...")
        download_path = save_image_to_file(output_rgb, output_format)
        
        progress(1.0, desc="Done!")
        status = f"Done! {w}x{h} -> {new_w}x{new_h} ({scale}x upscale)"
        
        return output_rgb, download_path, status
        
    except Exception as e:
        return None, None, f"Error: {str(e)}"


# Modern, clean CSS
CUSTOM_CSS = """
/* obsidian-chrome.css */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700&family=Saira:wght@400;500;600;700&display=swap');

:root {
    --obsidian-base: #050510;
    --obsidian-surface: #121218;
    --obsidian-overlay: rgba(20, 20, 30, 0.6);
    --chrome-border: 1px solid rgba(255, 255, 255, 0.12);
    --chrome-highlight: 1px solid rgba(255, 255, 255, 0.25);
    --neon-cyan: #00f3ff;
    --neon-purple: #bc13fe;
    --text-primary: #e0e0e0;
    --text-secondary: #a0a0a0;
}

/* Base Reset & Background */
body {
    background-color: var(--obsidian-base) !important;
    background-image: 
        linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    background-attachment: fixed !important; /* Ensures grid stays while scrolling */
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    background: transparent !important; /* Let body grid show through */
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 60px 20px !important;
    border: none !important;
}

/* Header Typography */
.header-title {
    text-align: center;
    font-family: 'Saira', sans-serif !important;
    font-size: 4rem !important;
    font-weight: 700 !important;
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 0.5rem !important;
    background: linear-gradient(180deg, #ffffff 0%, #a0a0a0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(255,255,255,0.15);
}

.header-subtitle {
    text-align: center;
    color: var(--neon-cyan) !important;
    font-family: 'Saira', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 4rem !important;
    opacity: 0.9;
    text-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
}

/* Component Styling - Ultra Modern & Seamless */
/* Remove old-school boxes */
.gr-box, .gr-panel {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Settings Row - Floating Tech Bar */
.settings-row {
    background: rgba(18, 18, 24, 0.6) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 8px !important;
    padding: 24px !important;
    margin: 20px 0 !important;
    box-shadow: 0 20px 50px rgba(0,0,0,0.4) !important;
}

/* Input Fields - High Tech */
.gr-input, .gr-dropdown, .gr-dropdown > button, .gr-radio {
    background: #0a0a10 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: var(--text-primary) !important;
    border-radius: 0px !important; /* Sharp corners */
    font-family: 'Outfit', sans-serif !important;
    transition: all 0.2s ease;
}

.gr-input:focus, .gr-dropdown:focus-within {
    border-color: var(--neon-cyan) !important;
    box-shadow: 0 0 15px rgba(0, 243, 255, 0.1) !important;
}

/* Labels */
label span, .block-label {
    font-family: 'Saira', sans-serif !important;
    text-transform: uppercase !important;
    font-size: 0.75rem !important;
    letter-spacing: 1.5px !important;
    color: var(--neon-cyan) !important;
    margin-bottom: 10px !important;
    text-shadow: 0 0 5px rgba(0, 243, 255, 0.2);
}

/* Image Containers - Cyberpunk Frames */
.image-container {
    background: rgba(10, 10, 16, 0.5) !important;
    border: 1px solid #333 !important;
    border-radius: 4px !important;
    position: relative;
}
/* Corner Accents for Tech Look */
.image-container::before {
    content: '';
    position: absolute;
    top: -1px; left: -1px;
    width: 20px; height: 20px;
    border-top: 2px solid var(--neon-cyan);
    border-left: 2px solid var(--neon-cyan);
    z-index: 10;
}
.image-container::after {
    content: '';
    position: absolute;
    bottom: -1px; right: -1px;
    width: 20px; height: 20px;
    border-bottom: 2px solid var(--neon-cyan);
    border-right: 2px solid var(--neon-cyan);
    z-index: 10;
}

/* Primary Action Button (Liquid Metal) */
.primary-btn {
    background: linear-gradient(90deg, #1a1a20 0%, #2a2a35 100%) !important;
    border: 1px solid rgba(102, 252, 241, 0.3) !important;
    color: var(--neon-cyan) !important;
    font-family: 'Saira', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1.3rem !important;
    padding: 20px 0 !important;
    border-radius: 0px !important; /* Sharp */
    text-transform: uppercase;
    letter-spacing: 4px;
    transition: all 0.3s ease !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.05);
    margin-top: 20px !important;
    width: 100%;
}

.primary-btn:hover {
    background: var(--neon-cyan) !important;
    color: #000 !important;
    box-shadow: 0 0 50px rgba(0, 243, 255, 0.3) !important;
    letter-spacing: 6px; /* Text expansion effect */
}

/* Accordion */
.gr-accordion {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 0px !important;
}
.gr-accordion .label-wrap {
    color: var(--text-primary) !important;
    font-family: 'Saira', sans-serif !important;
    text-transform: uppercase;
    letter-spacing: 2px;
}

/* Comparison Slider */
.gr-image-slider {
    border: none !important;
    border-radius: 0 !important;
}

/* Status Text */
.status-text {
    font-family: 'Saira', sans-serif;
    color: var(--neon-purple);
    letter-spacing: 2px;
}

/* Footer & Utilities */
footer { display: none !important; }
.download-section { margin-top: 20px; }
.image-container button[aria-label="Download"] { display: none !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 8px; background: #000; }
::-webkit-scrollbar-thumb { background: #333; }
@media (max-width: 768px) {
    .gradio-container {
        padding: 20px !important;
    }
}
"""


def create_interface() -> gr.Blocks:
    """Create a clean, modern Gradio interface."""
    
    with gr.Blocks(
        title="Image Upscaler Pro",
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
            neutral_hue="slate",
        ),
    ) as app:
        
        # Clean Header
        gr.Markdown(
            "# Image Upscaler Pro",
            elem_classes=["header-title"],
        )
        gr.Markdown(
            "AI-powered image upscaling using Real-ESRGAN",
            elem_classes=["header-subtitle"],
        )
        
        # Main content: Side-by-side images
        with gr.Row(equal_height=True):
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="Original",
                    type="numpy",
                    sources=["upload", "clipboard"],
                    height=350,
                    elem_classes=["image-container"],
                )
            
            with gr.Column(scale=1):
                output_image = gr.Image(
                    label="Upscaled",
                    type="numpy",
                    height=350,
                    interactive=False,
                    elem_classes=["image-container"],
                )
        
        # Settings in a clean horizontal layout
        with gr.Group(elem_classes=["settings-row"]):
            with gr.Row():
                model_choice = gr.Dropdown(
                    choices=["Best Quality", "Anime/Illustration"],
                    value="Best Quality",
                    label="Model",
                    scale=1,
                )
                
                output_format = gr.Dropdown(
                    choices=["PNG", "JPG", "WebP"],
                    value="PNG",
                    label="Format",
                    scale=1,
                )
        
        # Action button - centered
        with gr.Row():
            with gr.Column(scale=1):
                pass
            with gr.Column(scale=2):
                upscale_btn = gr.Button(
                    "Upscale Image",
                    variant="primary",
                    size="lg",
                    elem_classes=["primary-btn"],
                )
            with gr.Column(scale=1):
                pass
        
        # Status message
        status_text = gr.Markdown(
            "Upload an image to get started",
            elem_classes=["status-text"],
        )
        
        # Download section - appears after processing
        with gr.Group(elem_classes=["download-section"], visible=False) as download_group:
            download_file = gr.File(
                label="Download Upscaled Image",
            )
        
        # Before/After comparison - collapsible
        with gr.Accordion("Before / After Comparison", open=False) as comparison_section:
            comparison = gr.ImageSlider(
                label="Drag to compare",
                type="numpy",
            )
        
        # State to track download visibility
        def process_image(image, model, fmt):
            output, download_path, status = upscale_image(image, "4x", model, fmt)
            
            if output is not None and image is not None:
                # Resize original to match upscaled for comparison
                from PIL import Image as PILImage
                original_pil = PILImage.fromarray(image)
                original_resized = original_pil.resize(
                    (output.shape[1], output.shape[0]),  # width, height
                    PILImage.Resampling.LANCZOS
                )
                original_for_comparison = np.array(original_resized)
                
                return (
                    output,
                    status,
                    gr.update(visible=True),
                    download_path,
                    (original_for_comparison, output),  # comparison slider - same size
                )
            else:
                return (
                    None,
                    status,
                    gr.update(visible=False),
                    None,
                    None,
                )
        
        def clear_status():
            return ""
        
        upscale_btn.click(
            fn=clear_status,
            outputs=status_text,
            queue=False,
        ).then(
            fn=process_image,
            inputs=[input_image, model_choice, output_format],
            outputs=[output_image, status_text, download_group, download_file, comparison],
            show_progress="minimal",
        )
    
    return app


def main():
    """Launch the application."""
    print("\n" + "=" * 50)
    print("  Image Upscaler Pro")
    print("  Powered by Real-ESRGAN")
    print("=" * 50 + "\n")
    
    app = create_interface()
    
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True,
    )


if __name__ == "__main__":
    main()
