import requests
import csv


def downloader():
    data = requests.get('https://data.cityofnewyork.us/api/views/7z8d-msnt/rows.csv?accessType=DOWNLOAD')
    with open('./tables/attend.csv', 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            writer.writerow(row)

    data = requests.get('https://data.cityofnewyork.us/api/views/itfs-ms3e/rows.csv?accessType=DOWNLOAD')
    with open('./tables/ap_col.csv', 'w') as f:
        writer = csv.writer(f)
        reader = csv.reader(data.text.splitlines())

        for row in reader:
            writer.writerow(row)