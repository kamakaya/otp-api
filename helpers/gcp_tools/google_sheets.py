from flask.wrappers import Response
from helpers.gcp_tools import GCLOUD_CREDENTIALS
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
THINKIFIC_MASTER_DATA = '1AXz5QgL_v1hL_aCKpsqIiMNDXC8L4HfbWaBEC71gLJc'
LOGS_WORKSHEET_RANGE = 'Logs!A1:D1'

def generate_google_sheets_client():
    service = build('sheets', 'v4', credentials=GCLOUD_CREDENTIALS)
    return service

def append_logs_to_worksheet(data: list) -> Response:
    service = generate_google_sheets_client()
    
    request = service.spreadsheets().values().append(
        spreadsheetId = THINKIFIC_MASTER_DATA, 
        range = LOGS_WORKSHEET_RANGE, 
        valueInputOption = 'USER_ENTERED', 
        insertDataOption = 'INSERT_ROWS', 
        body={"values":[data]}
    ).execute()
    
    return request
