import csv


def assert_checks(file_name, header, rows):
    assert (len(file_name) > 0), 'Name must be greater than 0 characters.'
    assert (len(header) > 0), f'Length of header must be greater than 0. Empty List {header}'
    assert (len(rows) > 0), f'Length of rows must be greater than 0. Empty List {header}'
    assert (isinstance(rows, list)), f'rows must be list object. Type {type(rows)}'
    assert (isinstance(i, list) for i in rows), f'Each object Inside rows must be list object.'
    assert (len(header) == len(rows[0])), f'Lengths of headers and rows must be the same. Inconsistent lengths header {len(header)}, rows {len(rows)}'


def save_csv(file_name, header, rows, encoding='utf-8'):
    assert_checks(file_name, header, rows)

    with open(f'{file_name}.csv', 'w', newline='', encoding=encoding) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)


def open_csv(file_name):

        with open(f'{file_name}.csv', 'r', newline='') as csv_file:
            reader = [i for i in csv.reader(csv_file)]

            return reader







