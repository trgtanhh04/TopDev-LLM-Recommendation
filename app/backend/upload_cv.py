from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from parse_token import get_email_from_token
import cloudinary
import cloudinary.uploader
from supabase_helpers import supabase
import os

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

@router.post("/upload_cv")
async def upload_cv(
    file: UploadFile = File(...),
    email: str = Depends(get_email_from_token)
):
    # Only accept PDF files
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    try:
        # Upload to Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            resource_type="raw",
            folder="cv_uploads"
        )
        cv_url = result["secure_url"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cloudinary upload failed: {e}")

    try:
        # Upsert to Supabase
        result = (
            supabase.table("user_cvs")
            .upsert({
                "email": email,
                "cv_url": cv_url,
                "file_name": file.filename
            })
            .execute()
        )
        # Optionally check for errors in result
        if hasattr(result, "error") and result.error:
            raise Exception(result.error)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    return JSONResponse({"message": "CV uploaded successfully", "cv_url": cv_url})