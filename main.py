import cv2
import numpy as np
import psycopg2
from fastapi import FastAPI, Body, Query, HTTPException, status
from imageProcessor import ImageProcessor
from config import db

app = FastAPI()


@app.exception_handler(psycopg2.OperationalError)
def database_error(error):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection error")


@app.exception_handler(Exception)
def internal_error(error):
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")


@app.post("/images", status_code=status.HTTP_201_CREATED)
async def store_image(depth: int, image_data: bytes = Body(...)):
    try:
        # Process image (resizing, colormap) using ImageProcessor
        processed_image = ImageProcessor().resize_image(
            cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        )
        processed_image = ImageProcessor().apply_colormap(processed_image)

        # Store image in database
        db.store_image(depth, cv2.imencode(".jpg", processed_image)[1].tobytes())

        return {"message": "Image stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        db.close()


@app.get("/images")
async def get_images_by_depth(depth_min: int = Query(None), depth_max: int = Query(None)):
    try:
        images = db.get_images_by_depth(depth_min, depth_max)
        return [image for image in images]  # Handle potential binary data for images
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", access_log=True)
