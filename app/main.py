import io

import cv2
import numpy as np
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.crud import get_images_by_depth_range, insert_data
from app.database import SessionLocal, init_db
from app.utils import resize_image, apply_colormap

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()
    db = SessionLocal()

    # Read the CSV file and populate the database
    df = pd.read_csv("image_dataset.csv")
    for _, row in df.iterrows():
        depth = row['depth']
        pixel_values = row.drop('depth').values.astype(np.uint8)
        resized_image = resize_image(pixel_values).tobytes()
        try:
            insert_data(db, depth, resized_image)
        except Exception:
            continue

    db.close()


@app.get("/images/pixel_data")
def get_images_with_pixel_data(depth_min: float, depth_max: float, db: Session = Depends(get_db)):
    images = get_images_by_depth_range(db, depth_min, depth_max)
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")

    result = []
    for image in images:
        pixel_values = np.frombuffer(image.pixel_values, dtype=np.uint8)
        colored_image = apply_colormap(pixel_values.reshape((1, 150)))  # Adjust according to actual reshape dimensions
        result.append({
            'depth': image.depth,
            'pixel_values': colored_image.tolist()
        })

    return result


@app.get("/images")
def get_combined_images(depth_min: float, depth_max: float, db: Session = Depends(get_db)):
    images = get_images_by_depth_range(db, depth_min, depth_max)
    if not images:
        raise HTTPException(status_code=404, detail="Images not found")

    # Assume all images are the same size and can be vertically stacked
    combined_image = None
    for image in images:
        pixel_values = np.frombuffer(image.pixel_values, dtype=np.uint8)
        colored_image = apply_colormap(pixel_values.reshape((1, 150)))  #
        if combined_image is None:
            combined_image = colored_image
        else:
            combined_image = np.vstack((combined_image, colored_image))

    # Encode the combined image to a PNG
    _, buffer = cv2.imencode('.png', combined_image)
    io_buffer = io.BytesIO(buffer)

    return StreamingResponse(io_buffer, media_type="image/png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")
