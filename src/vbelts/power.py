import csv
import os

def _read_csv_data(filename:str):
    # use the full path and pass the file path as filename
    file_path = os.path.join(os.path.dirname(__file__), 'data', filename)
    li_result = []
    with open(f'{file_path}.csv', mode='r') as csv_file:
        reader = csv.reader(csv_file, quoting=csv.QUOTE_NONNUMERIC)
        next(reader)
        for line in reader:
            li_result.append(line)
        return li_result