import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('no', scope)
client = gspread.authorize(creds)

sheet = client.open("2024 Finances").sheet1

range_to_clear = "A3:D1000"

sheet.batch_clear([range_to_clear])

start_row = 3

data_to_insert = []
with open("transactions.csv", mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        date_str = row[0]  
        date_value = f"{date_str}/2024" 
        category = row[1]
        amount = float(row[2]) 
        description = row[3]

        data_to_insert.append([date_value, category, amount, description])

cell_range = f'A{start_row}:D{start_row + len(data_to_insert) - 1}'
cell_list = sheet.range(cell_range)

flat_data = [item for sublist in data_to_insert for item in sublist]

for i, cell in enumerate(cell_list):
    cell.value = flat_data[i]

sheet.update_cells(cell_list)

sheet.format(f"C{start_row}:C{start_row + len(data_to_insert) - 1}", {
    "numberFormat": {
        "type": "CURRENCY",
        "pattern": "$#,##0.00;[Red]-$#,##0.00" 
    }
})

print("CSV data successfully inserted into Google Sheets.")
