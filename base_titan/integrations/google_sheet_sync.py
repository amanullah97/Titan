import gspread
from oauth2client.service_account import ServiceAccountCredentials
from base_titan.models import Provider
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials/google_key.json", scope)
client = gspread.authorize(creds)
sheet = client.open("https://docs.google.com/spreadsheets/d/1e3AvQTv3BMwEO-MjKHpjEE2G6dCZdFLEeswyTLgJ2YE/edit#gid=0")
worksheet = sheet.get_worksheet(0)  # Select a specific worksheet
data = worksheet.get_all_records()  # This will fetch all the data as a list of dictionaries

for row in data:
    Provider.objects.create(
        name=row['Provider'],
                # Add other fields as needed
    )

