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
TEMP_DIR = os.path.abspath("temp_uploads")
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
            
        # Prepare output path
        output_filename = f"upscaled_{int(time.time())}.{format}"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        # Run Upscaling
        # upscaler.upscale takes (input_path, output_path, scale, model, callback)
        result_path = upscaler.upscale(
            input_path=input_path,
            output_path=output_path,
            scale=4, # Hardcoded 4x as per standard
            model=model
        )
        
        if result_path and os.path.exists(result_path):
            return FileResponse(result_path, media_type=f"image/{format}", filename=os.path.basename(result_path))
        else:
            raise HTTPException(status_code=500, detail="Upscaling returned no output")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup input? Maybe keep for debugging for now or clean up later.
        pass
