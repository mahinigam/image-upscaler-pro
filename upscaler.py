"""
Image Upscaler Core Module
High-quality image upscaling using Real-ESRGAN (NCNN Vulkan implementation).
This uses the pre-compiled realesrgan-ncnn-vulkan binary for maximum compatibility
while maintaining the same Real-ESRGAN model quality.
"""

import os
import sys
import stat
import shutil
import platform
import subprocess
import tempfile
import zipfile
import requests
from pathlib import Path
from typing import Optional, Callable

import cv2
import numpy as np
from PIL import Image


class RealESRGANUpscaler:
    """
    High-quality image upscaler using Real-ESRGAN NCNN Vulkan.
    
    This implementation uses the official realesrgan-ncnn-vulkan binary which:
    - Provides the same quality as the PyTorch implementation
    - Works on Apple Silicon with GPU acceleration
    - Has no Python version compatibility issues
    - Includes optimized models for best quality
    """
    
    # Download URLs for realesrgan-ncnn-vulkan
    BINARY_URLS = {
        "darwin_arm64": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip",
        "darwin_x86_64": "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesrgan-ncnn-vulkan-20220424-macos.zip",
    }
    
    # Available models with their scale factors
    MODELS = {
        "realesrgan-x4plus": {"scale": 4, "description": "Best quality for general photos"},
        "realesrnet-x4plus": {"scale": 4, "description": "Faster, slightly less detailed"},
        "realesrgan-x4plus-anime": {"scale": 4, "description": "Optimized for illustrations"},
    }
    
    def __init__(self, models_dir: Optional[str] = None):
        """
        Initialize the upscaler.
        
        Args:
            models_dir: Directory to store binary and models (auto-created if None)
        """
        if models_dir is None:
            models_dir = os.path.join(os.path.dirname(__file__), "bin")
        
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.binary_path = self._get_binary_path()
        self._ensure_binary_exists()
    
    def _get_platform_key(self) -> str:
        """Get the platform key for binary download."""
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "darwin":
            if machine in ("arm64", "aarch64"):
                return "darwin_arm64"
            else:
                return "darwin_x86_64"
        else:
            raise RuntimeError(f"Unsupported platform: {system} {machine}")
    
    def _get_binary_path(self) -> Path:
        """Get the path to the realesrgan binary."""
        binary_name = "realesrgan-ncnn-vulkan"
        return self.models_dir / binary_name
    
    def _ensure_binary_exists(self) -> None:
        """Download and extract the binary if it doesn't exist."""
        if self.binary_path.exists():
            return
        
        platform_key = self._get_platform_key()
        url = self.BINARY_URLS.get(platform_key)
        
        if url is None:
            raise RuntimeError(f"No binary available for {platform_key}")
        
        print(f"[Upscaler] Downloading Real-ESRGAN binary...")
        print(f"[Upscaler] This is a one-time download (~10MB)")
        
        # Download the zip file
        zip_path = self.models_dir / "realesrgan.zip"
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r[Upscaler] Downloading: {percent:.1f}%", end="", flush=True)
        
        print("\n[Upscaler] Extracting...")
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.models_dir)
        
        # Find and move the binary to the expected location
        extracted_dir = None
        for item in self.models_dir.iterdir():
            if item.is_dir() and "realesrgan" in item.name.lower():
                extracted_dir = item
                break
        
        if extracted_dir:
            # Move contents to models_dir
            for item in extracted_dir.iterdir():
                dest = self.models_dir / item.name
                if dest.exists():
                    if dest.is_dir():
                        shutil.rmtree(dest)
                    else:
                        dest.unlink()
                shutil.move(str(item), str(dest))
            extracted_dir.rmdir()
        
        # Make binary executable
        if self.binary_path.exists():
            self.binary_path.chmod(self.binary_path.stat().st_mode | stat.S_IEXEC)
        
        # Clean up zip
        zip_path.unlink()
        
        print("[Upscaler] Setup complete!")
    
    def get_available_models(self) -> dict:
        """Get list of available models."""
        return self.MODELS.copy()
    
    def _run_upscale(
        self,
        input_path: str,
        output_path: str,
        model: str,
        scale: int,
    ) -> None:
        """Run a single upscale pass."""
        cmd = [
            str(self.binary_path),
            "-i", str(input_path),
            "-o", str(output_path),
            "-n", model,
            "-s", str(scale),
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(self.models_dir),
        )
        
        if result.returncode != 0:
            error_msg = result.stderr or result.stdout or "Unknown error"
            raise RuntimeError(f"Upscaling failed: {error_msg}")
    
    def upscale(
        self,
        input_path: str,
        output_path: str,
        scale: int = 4,
        model: str = "realesrgan-x4plus",
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> str:
        """
        Upscale an image file.
        
        Args:
            input_path: Path to input image
            output_path: Path for output image
            scale: Scale factor (2, 4, or 8)
            model: Model name to use
            progress_callback: Optional callback for progress updates (progress, message)
            
        Returns:
            Path to the output file
        """
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        if model not in self.MODELS:
            raise ValueError(f"Unknown model: {model}. Available: {list(self.MODELS.keys())}")
        
        if scale not in [2, 4, 8]:
            raise ValueError(f"Scale must be 2, 4, or 8. Got: {scale}")
        
        try:
            if scale == 8:
                # 8x = two passes of 4x (total: 4 * 4 = 16x, but we control output)
                # Actually: 8x = 4x then 2x = 4*2 = 8x
                if progress_callback:
                    progress_callback(0.1, "Pass 1/2: Applying 4x upscaling...")
                
                # First pass: 4x
                temp_path = output_path + ".temp.png"
                self._run_upscale(input_path, temp_path, model, 4)
                
                if progress_callback:
                    progress_callback(0.5, "Pass 2/2: Applying 2x upscaling...")
                
                # Second pass: 2x on the 4x result
                self._run_upscale(temp_path, output_path, model, 2)
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                
            else:
                # Direct upscale (2x or 4x)
                if progress_callback:
                    progress_callback(0.1, f"Applying {scale}x upscaling...")
                
                self._run_upscale(input_path, output_path, model, scale)
            
            if progress_callback:
                progress_callback(1.0, "Complete!")
            
            return output_path
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("Upscaling timed out")
    
    def upscale_image(
        self,
        image: np.ndarray,
        scale: int = 4,
        model: str = "realesrgan-x4plus",
        progress_callback: Optional[Callable[[float, str], None]] = None,
    ) -> np.ndarray:
        """
        Upscale an image array.
        
        Args:
            image: Input image as numpy array (RGB format)
            scale: Scale factor (2, 4, or 8)
            model: Model name to use
            progress_callback: Optional callback for progress updates
            
        Returns:
            Upscaled image as numpy array (RGB format)
        """
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as input_file:
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as output_file:
            output_path = output_file.name
        
        try:
            # Save input image
            pil_image = Image.fromarray(image)
            pil_image.save(input_path, format="PNG")
            
            # Upscale
            self.upscale(
                input_path=input_path,
                output_path=output_path,
                scale=scale,
                model=model,
                progress_callback=progress_callback,
            )
            
            # Read output image
            output_image = Image.open(output_path)
            result = np.array(output_image)
            
            return result
            
        finally:
            # Clean up temp files
            for path in [input_path, output_path]:
                if os.path.exists(path):
                    os.unlink(path)


def create_upscaler() -> RealESRGANUpscaler:
    """
    Factory function to create an upscaler instance.
    
    Returns:
        Configured RealESRGANUpscaler instance
    """
    return RealESRGANUpscaler()
