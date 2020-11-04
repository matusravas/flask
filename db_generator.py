# Run this file to generate pseudo DB stored in csv.

import csv

fieldnames = ['id','name', 'age', 'salary']


data = [{'id': 1, 'name': 'Kebab', 'age': 19, 'salary': 1000},
        {'id': 2, 'name': 'Tibor', 'age': 20, 'salary': 2000},
        {'id': 3, 'name': 'Matus', 'age': 21, 'salary': 3000},
        {'id': 4, 'name': 'Ivan', 'age': 22, 'salary': 4000}]

if __name__ == '__main__':
        with open('users.csv', 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames, delimiter='\t')
                writer.writeheader()
                for row in data:
                        writer.writerow(row)