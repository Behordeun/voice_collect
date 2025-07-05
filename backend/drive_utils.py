from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'the-mesh-460119-n5-241d99f0eb10.json'
RECORDINGS_FOLDER_ID = '1ipMRzyjwpmcro_BZ4pmM2Qet2xSvrvLX'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=creds)

def get_or_create_participant_folder(participant_id, email):
    folder_name = f"{participant_id}_{email}"
    query = f"'{RECORDINGS_FOLDER_ID}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get('files', [])
    if files:
        return files[0]['id']

    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [RECORDINGS_FOLDER_ID]
    }
    file = drive_service.files().create(body=metadata, fields='id').execute()
    return file.get('id')

def upload_audio_to_drive(filepath, filename, folder_id):
    media = MediaFileUpload(filepath, mimetype='audio/wav')
    drive_service.files().create(
        body={'name': filename, 'parents': [folder_id]},
        media_body=media,
        fields='id'
    ).execute()