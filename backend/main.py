from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from drive_utils import get_or_create_participant_folder, upload_audio_to_drive
from sentence_utils import get_next_sentence, log_sentence
import os
import aiofiles  # For asynchronous file handling

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/login")
def login(participant_id: str = Form(...), email: str = Form(...)):
    return {
        "message": "Login successful",
        "participant_id": participant_id,
        "email": email
    }

@app.get("/sentence")
def get_sentence(participant_id: str):
    sentence, index = get_next_sentence(participant_id)
    if sentence:
        return {"sentence": sentence, "index": index}
    return {"message": "All sentences completed."}

@app.post("/upload_audio/")
async def upload_audio(
    file: UploadFile,
    participant_id: str = Form(...),
    email: str = Form(...),
    sentence_index: int = Form(...)
):
    # Ensure temp directory exists
    temp_dir = "backend/temp"
    os.makedirs(temp_dir, exist_ok=True)

    # Define full path for temporary audio file
    temp_path = f"{temp_dir}/{participant_id}_s{sentence_index}.wav"

    # Asynchronously write uploaded audio to file
    async with aiofiles.open(temp_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Upload to Google Drive
    folder_id = get_or_create_participant_folder(participant_id, email)
    upload_audio_to_drive(temp_path, os.path.basename(temp_path), folder_id)

    # Clean up
    os.remove(temp_path)

    # Log sentence completion
    log_sentence(participant_id, sentence_index)

    return {"message": "Upload successful"}