from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.crud import get_images_by_depth_range, create_resized_image
from utils import resize_image, apply_colormap
import pandas as pd
import numpy as np

app = FastAPI()


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    init_db()  # Initialize the database tables
    db = SessionLocal()

    # Read the CSV file and populate the database
    df = pd.read_csv("../image_dataset.csv")
    for _, row in df.iterrows():
        depth = row['depth']
        pixel_values = row.drop('depth').values.astype(np.uint8)
        resized_image = resize_image(pixel_values).tobytes()
        create_resized_image(db, depth, resized_image)

    db.close()


@app.post("/images/upload/")
def upload_images(csv_file: str, db: Session = Depends(get_db)):
    df = pd.read_csv(csv_file)
    resized_df = resize_image(df)
    for _, row in resized_df.iterrows():
        depth = row['depth']
        pixel_values = row.drop('depth').values.tobytes()
        create_resized_image(db, depth, pixel_values)
    return {"status": "images uploaded and resized"}


@app.get("/images")
def get_images(depth_min: float, depth_max: float, db: Session = Depends(get_db)):
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, log_level="info")
