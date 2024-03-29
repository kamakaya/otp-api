from google.oauth2 import service_account
from pathlib import Path

#TODO: Update all config info on here

service_account_path = Path('one-time-password-via-api-b715a9a5e72b.json').resolve()
GCP_PROJECT_ID = '966262794836' 
GCLOUD_PROJECT = 'one-time-password-via-api'
GCLOUD_REGION = 'us-west1'
GCLOUD_CREDENTIALS = service_account.Credentials.from_service_account_file(str(service_account_path))
GCLOUD_SA_EMAIL = 'otp-sa@one-time-password-via-api.iam.gserviceaccount.com'
APP_URL = 'https://one-time-password-via-api-rzmipdxtnq-uw.a.run.app'

SYNC_URLS = {
    'DEV': f'https://development---{APP_URL}/get_otp',
    'PROD': f'https://production---{APP_URL}/get_otp'
}