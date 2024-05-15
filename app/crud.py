from sqlalchemy.orm import Session
from models import ResizedImage


def get_images_by_depth_range(db: Session, depth_min: float, depth_max: float):
    return db.query(ResizedImage).filter(ResizedImage.depth >= depth_min, ResizedImage.depth <= depth_max).all()


def create_resized_image(db: Session, depth: float, pixel_values: bytes):
    db_image = ResizedImage(depth=float(depth), pixel_values=pixel_values)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image
