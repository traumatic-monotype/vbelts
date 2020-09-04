import csv

def read_csv_data(filename:str):
    with open(f'{filename}.csv') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            print(row)