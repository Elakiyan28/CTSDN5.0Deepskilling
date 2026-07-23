def read_csv(file_path):
    import csv
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
