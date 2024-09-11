import os, uuid, base64, io

from fastapi import UploadFile, File, HTTPException
from pathlib import Path

async def convert_base64_to_uploadfile(image_base64: str, filename: str):
    try:
        image_bytes = base64.b64decode(image_base64)
        file = UploadFile(filename=filename, file=io.BytesIO(image_bytes))
        return file
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {e}")

async def generate_unique_filename():
    extension = 'png'
    unique_name = f"{uuid.uuid4()}.{extension}"
    return unique_name

async def upload_files(files: list[str] | None = File(None)):
    if not files:
        return [""]
    
    UPLOAD_DIR = Path("uploads")
    UPLOAD_DIR.mkdir(exist_ok=True)

    saved_paths = []

    for i in files:
        unique_filename = generate_unique_filename()
        file_location = UPLOAD_DIR / unique_filename
        file = convert_base64_to_uploadfile(i, unique_filename)
        
        with open(file_location, "wb") as f:
            f.write(await file.read())
        
        saved_paths.append(str(file_location))
    
    return saved_paths

async def delete_files(file_paths: list[str]):
    for file_path in file_paths:
        file_location = Path(file_path)

        if file_location.exists() and file_location.is_file():
            os.remove(file_location)
