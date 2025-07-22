import os
import uuid
from fastapi import UploadFile
from app.core.config import settings
from app.core.logging import logger

def save_template(file: UploadFile):
    os.makedirs(settings.TEMPLATE_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}.pptx"
    file_path = os.path.join(settings.TEMPLATE_DIR, filename)
    
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    logger.info(f"Saved template: {filename}")
    return file_path