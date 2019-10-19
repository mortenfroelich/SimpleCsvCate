"""SimpleCsvCate

Usage:
    SimpleCsCate.py FILE

Options:
    -h --help     Show this screen.
    --version     Show version.
"""
import csv
import json
import os
from docopt import docopt

mapcache = dict()


def main(arguments):
    global mapcache
    if os.path.isfile('output.csv'):
        raise FileExistsError('File output.csv already exists')
    if os.path.isfile('mapcache.json'):
        with open('mapcache.json') as mapcachefile:
            mapcache = json.load(mapcachefile)
    with open(arguments['FILE']) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        data = []
        workingData = []
        for row in csvreader:
            workingData.append(row)
        workingData = mapKnown(data, workingData)
        while workingData:
            print('Remaining items: ' + str(len(workingData)))
            current = workingData.pop(0)
            category = getCategory(current)
            current.append(category)
            data.append(current)
            workingData = mapKnown(data, workingData)
    with open('output.csv', 'x', newline='') as output:
        csvwriter = csv.writer(output)
        csvwriter.writerows(data)
    with open('mapcache.json', 'w') as mapcachefile:
        json.dump(mapcache, mapcachefile, sort_keys=True, indent=4)


with open('categories.json') as categoryfile:
    menu = json.load(categoryfile)
options = menu.keys()
options = sorted(options)


def getCategory(current):
    while True:
        for entry in options:
            print(entry, menu[entry])

        print(','.join(current))
        selection = input("Please Select:")
        if selection[:1] == '!' and selection[1:] in options:
            return menu[selection[1:]]
        if selection in options:
            saveMapping(menu[selection], current)
            return menu[selection]
        else:
            print("Unknown Option")


def saveMapping(category, row):
    mapcache[row[2]] = category


def mapKnown(data, workingData):
    notMapped = []
    for row in workingData:
        category = mapcache.get(row[2], None)
        if(category):
            row.append(category)
            data.append(row)
        else:
            notMapped.append(row)
    return notMapped


if __name__ == '__main__':
    arguments = docopt(__doc__, version='SimpleCsvCate 0.1')
    main(arguments)
