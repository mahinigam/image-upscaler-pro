from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import time
from typing import Optional
from backend.upscaler import RealESRGANUpscaler
import cv2
import numpy as np

app = FastAPI(title="Image Upscaler Pro API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Upscaler
upscaler = RealESRGANUpscaler()

# Ensure temp directory exists
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"status": "online", "model": "Real-ESRGAN"}

@app.post("/upscale")
async def upscale_image(
    file: UploadFile = File(...),
    scale: str = Form("4x"), # kept as str to match old interface but currently only 4x supported
    model: str = Form("realesrgan-x4plus"),
    format: str = Form("png")
):
    try:
        # Save uploaded file
        input_path = os.path.join(TEMP_DIR, f"input_{int(time.time())}_{file.filename}")
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Read image to numpy for upscaler compatibility (wrapper logic)
        # Actually our upscaler.py takes a path or numpy array. 
        # Let's check upscaler.py logic. It expects numpy array in `upscale` method, 
        # but `_run_upscale` takes paths.
        # Let's load it as numpy to pass to our existing class if needed, 
        # OR just modify logic to handle paths.
        # Looking at legacy upscaler.py, `upscale` accepts `image: np.ndarray`.
        
        img = cv2.imread(input_path)
        if img is None:
            raise HTTPException(status_code=400, detail="Invalid image format")
        
        # Convert BGR to RGB (OpenCV loads BGR)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Run Upscaling
        # Note: upscaler.upscale takes (image_rgb, scale, model_name, format)
        # and returns (output_rgb, output_path, message)
        
        output_rgb, output_path, message = upscaler.upscale(img_rgb, 4, model, format)
        
        if output_path and os.path.exists(output_path):
            return FileResponse(output_path, media_type=f"image/{format}", filename=os.path.basename(output_path))
        else:
            raise HTTPException(status_code=500, detail=f"Upscaling failed: {message}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup input? Maybe keep for debugging for now or clean up later.
        pass
