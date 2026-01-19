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
/* Industrial Monolith Theme */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

:root {
    --mono-bg: #000000;
    --mono-surface: #0a0a0a;
    --mono-fg: #ffffff;
    --mono-dim: #666666;
    --mono-border: 1px solid #333333;
    --mono-accent: #ffffff;
}

/* Global Reset */
body, .gradio-container {
    background-color: var(--mono-bg) !important;
    background-image: 
        radial-gradient(#222 1px, transparent 1px) !important;
    background-size: 40px 40px !important;
    font-family: 'Space Grotesk', monospace !important;
    color: var(--mono-fg) !important;
    margin: 0 !important;
    padding: 0 !important;
}

.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    padding: 80px 20px !important;
}

/* Typography */
.header-title {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 700 !important;
    letter-spacing: -1px !important;
    text-transform: uppercase;
    margin-bottom: 5px !important;
    color: var(--mono-fg) !important;
}

.header-subtitle {
    text-align: center;
    color: var(--mono-dim) !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase;
    margin-bottom: 4rem !important;
}

/* Reset Containers */
.gr-box, .gr-panel, .settings-row {
    background: var(--mono-surface) !important;
    border: var(--mono-border) !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    padding: 20px !important;
}

/* Inputs */
.gr-input, .gr-dropdown, .gr-radio {
    background: #000 !important;
    border: var(--mono-border) !important;
    color: var(--mono-fg) !important;
    border-radius: 0 !important;
    font-family: 'Space Grotesk', monospace !important;
}

/* Labels */
label span, .block-label {
    text-transform: uppercase !important;
    font-size: 0.7rem !important;
    letter-spacing: 1px !important;
    color: var(--mono-dim) !important;
    font-weight: 600 !important;
}

/* Image Container */
.image-container {
    background: #050505 !important;
    border: var(--mono-border) !important;
    border-radius: 0 !important;
}

/* Main Action Button - Inverted Block */
.primary-btn {
    background: var(--mono-fg) !important;
    color: var(--mono-bg) !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 18px 0 !important;
    margin-top: 20px !important;
    transition: all 0.2s ease !important;
}
.primary-btn:hover {
    background: #ddd !important;
}

/* Accordion */
.gr-accordion {
    background: transparent !important;
    border: var(--mono-border) !important;
    border-radius: 0 !important;
}
.gr-accordion .label-wrap {
    color: var(--mono-fg) !important;
}

/* Status Text */
.status-text {
    font-family: 'Space Grotesk', monospace;
    color: var(--mono-dim);
    text-transform: uppercase;
    font-size: 0.8rem;
    margin-top: 15px;
}

/* Utilities */
footer { display: none !important; }
.image-container button[aria-label="Download"] { display: none !important; }
.gr-image-slider { border: none !important; border-radius: 0 !important; }
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
