from google.oauth2.service_account import Credentials
import gspread
import json
import csv
import glob

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

spreadsheetPath = ""
with open('./spreadsheet_path.json') as f:
    di = json.load(f)
    spreadsheetPath = di['path']

credentials = Credentials.from_service_account_file(
    'secret.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_url(spreadsheetPath)
sheet = spreadsheet.worksheet("data")

files = glob.glob("../data/*.csv")
for file in files:
    print(file)
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        data = list(reader)
        data.pop(0)
        
        sheet.add_rows(len(data))
        for i, row in enumerate(data):
            sheet.insert_row(row, sheet.row_count - len(data) + i + 1)