"""
Image Upscaler Web Application
A Gradio-based web interface for high-quality image upscaling.
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


def upscale_image(
    input_image: np.ndarray,
    scale_factor: str,
    model_choice: str,
    output_format: str,
    progress: gr.Progress = gr.Progress(),
) -> Tuple[Optional[np.ndarray], str]:
    """
    Upscale an image using Real-ESRGAN.
    
    Args:
        input_image: Input image from Gradio
        scale_factor: Scale factor as string ("2x", "4x")
        model_choice: Model to use
        output_format: Output format
        progress: Gradio progress tracker
        
    Returns:
        Tuple of (upscaled image, status message)
    """
    if input_image is None:
        return None, "Please upload an image first"
    
    try:
        progress(0, desc="Initializing...")
        
        # Get upscaler
        upscaler = get_upscaler()
        
        # Parse scale factor
        scale = int(scale_factor.replace("x", ""))
        
        # Get original dimensions
        h, w = input_image.shape[:2]
        new_h, new_w = h * scale, w * scale
        
        progress(0.1, desc=f"Upscaling {w}x{h} to {new_w}x{new_h}...")
        
        # Define progress callback
        def update_progress(p: float, msg: str):
            progress(0.1 + p * 0.8, desc=msg)
        
        # Map model choice to model name
        model_map = {
            "Real-ESRGAN x4plus (Best Quality)": "realesrgan-x4plus",
            "Real-ESRNet x4plus (Faster)": "realesrnet-x4plus",
            "Real-ESRGAN Anime (Illustrations)": "realesrgan-x4plus-anime",
        }
        model_name = model_map.get(model_choice, "realesrgan-x4plus")
        
        # Upscale
        output_rgb = upscaler.upscale_image(
            image=input_image,
            scale=scale,
            model=model_name,
            progress_callback=update_progress,
        )
        
        progress(1.0, desc="Done!")
        
        status = f"Successfully upscaled: {w}x{h} to {new_w}x{new_h} ({scale}x)"
        return output_rgb, status
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(f"[Error] {error_msg}")
        return None, error_msg


def save_image(image: np.ndarray, output_format: str) -> Optional[str]:
    """Save the upscaled image to a temporary file for download."""
    if image is None:
        return None
    
    # Create temp file with appropriate extension
    ext = output_format.lower()
    if ext == "same as input":
        ext = "png"
    
    temp_file = tempfile.NamedTemporaryFile(
        suffix=f".{ext}",
        delete=False,
        dir=tempfile.gettempdir(),
    )
    
    # Convert to PIL and save
    pil_image = Image.fromarray(image)
    
    if ext in ["jpg", "jpeg"]:
        # Remove alpha for JPEG
        if pil_image.mode == "RGBA":
            pil_image = pil_image.convert("RGB")
        pil_image.save(temp_file.name, quality=95, optimize=True)
    elif ext == "webp":
        pil_image.save(temp_file.name, quality=95, lossless=False)
    else:  # PNG
        pil_image.save(temp_file.name, optimize=True)
    
    return temp_file.name


# Custom CSS for styling
CUSTOM_CSS = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

.title-text {
    text-align: center;
    margin-bottom: 0.5em;
}

.subtitle-text {
    text-align: center;
    color: #666;
    margin-bottom: 1.5em;
}

footer {
    display: none !important;
}
"""


def create_interface() -> gr.Blocks:
    """Create the Gradio interface."""
    
    with gr.Blocks(
        title="Image Upscaler",
        css=CUSTOM_CSS,
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="blue",
        ),
    ) as app:
        # Header
        gr.Markdown(
            """
            # Image Upscaler Pro
            ### High-quality AI-powered image upscaling using Real-ESRGAN
            """,
            elem_classes=["title-text"],
        )
        
        with gr.Row():
            # Left column - Input
            with gr.Column(scale=1):
                input_image = gr.Image(
                    label="Upload Image",
                    type="numpy",
                    sources=["upload", "clipboard"],
                    height=400,
                )
                
                with gr.Group():
                    gr.Markdown("### Settings")
                    
                    scale_factor = gr.Radio(
                        choices=["2x", "4x", "8x"],
                        value="4x",
                        label="Scale Factor",
                        info="4x recommended for best results, 8x for maximum enlargement",
                    )
                    
                    model_choice = gr.Dropdown(
                        choices=[
                            "Real-ESRGAN x4plus (Best Quality)",
                            "Real-ESRNet x4plus (Faster)",
                            "Real-ESRGAN Anime (Illustrations)",
                        ],
                        value="Real-ESRGAN x4plus (Best Quality)",
                        label="Model",
                        info="Choose model based on your image type",
                    )
                    
                    output_format = gr.Dropdown(
                        choices=["PNG", "JPG", "WebP"],
                        value="PNG",
                        label="Output Format",
                        info="PNG = lossless, JPG/WebP = smaller file size",
                    )
                
                upscale_btn = gr.Button(
                    "Upscale Image",
                    variant="primary",
                    size="lg",
                )
            
            # Right column - Output
            with gr.Column(scale=1):
                output_image = gr.Image(
                    label="Upscaled Result",
                    type="numpy",
                    height=400,
                    interactive=False,
                )
                
                status_text = gr.Textbox(
                    label="Status",
                    value="Ready to upscale...",
                    interactive=False,
                    lines=1,
                )
                
                download_btn = gr.Button(
                    "Download Result",
                    variant="secondary",
                    size="lg",
                )
                
                download_file = gr.File(
                    label="Download",
                    visible=False,
                )
        
        # Image comparison slider
        gr.Markdown("### Before / After Comparison")
        comparison = gr.ImageSlider(
            label="Drag to compare",
            type="numpy",
            height=500,
        )
        
        # Footer info
        gr.Markdown(
            """
            ---
            **Tips:**
            - Use **4x** for the best balance of quality and processing time
            - Use **2x** for quick upscaling with good quality
            - **Real-ESRGAN x4plus** provides the highest quality for photos
            - **PNG** format preserves all details (lossless)
            """,
            elem_classes=["subtitle-text"],
        )
        
        # Event handlers
        def process_and_update(image, scale, model, fmt):
            output, status = upscale_image(image, scale, model, fmt)
            # Update comparison slider
            if output is not None and image is not None:
                comparison_value = (image, output)
            else:
                comparison_value = None
            return output, status, comparison_value
        
        upscale_btn.click(
            fn=process_and_update,
            inputs=[input_image, scale_factor, model_choice, output_format],
            outputs=[output_image, status_text, comparison],
            show_progress=True,
        )
        
        def handle_download(image, fmt):
            if image is None:
                return None
            return save_image(image, fmt)
        
        download_btn.click(
            fn=handle_download,
            inputs=[output_image, output_format],
            outputs=[download_file],
        ).then(
            fn=lambda x: gr.update(visible=x is not None),
            inputs=[download_file],
            outputs=[download_file],
        )
    
    return app


def main():
    """Launch the application."""
    print("\n" + "=" * 50)
    print("  Image Upscaler Pro")
    print("  Powered by Real-ESRGAN")
    print("=" * 50 + "\n")
    
    app = create_interface()
    
    # Launch with share=False for local use
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True,
    )


if __name__ == "__main__":
    main()
