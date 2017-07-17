#python 3

import pandas as pd
import csv

#A handful of pandas-based scripts to analyze and edit your spreadsheet-based collection control data

##Data Remediation
#Combine two datasets
def combine_csvs():
    dataset_a = input('Please enter path to first CSV: ')
    dataset_b = input('Please enter path to second CSV: ')
    #fill in index column or add line for input...or don't have it?
    data_a = pd.read_csv(dataset_a, index_col='')
    data_b = pd.read_csv(dataset_b, index_col='')

    if len(data_a.columns) == len(data_b.columns):
        newdataset = data_a.append(data_b)
    else:
        newdataset = pd.concat([data_a, data_b])
    newdataset.to_csv('alldren.csv', encoding='utf-8')

#Join two spreadsheets on a common column
def join_csvs():
    dataset_a = input('Please enter path to first CSV: ')
    dataset_b = input('Please enter path to second CSV: ')
    mergevar = input('Enter common column: ')
    merged = dataset_a.join(dataset_b)

##Data Analysis
#Get all values that meet a certain criteria
def group_by():
    dataset = input('Please enter path to input CSV: ')
    columnname = input('In what column is your group located?: ')
    groupname = input('What value are you looking for?')
    group = dataset.groupby(columnname)
    grouped = group.get_group(groupname)
    grouped.to_csv('group.csv', encoding='utf-8')

#Get count of values in a column
def get_val_counts():
    data = input('Please enter path to input CSV: ')
    dataset = pd.read_csv(data)
    headerlist = dataset.columns.values.tolist()
    headlist = str(headerlist)
    head = headlist[1:-1]
    print('Columns: ' + head)
    columnname = input('Please enter column name: ')
    counts = dataset[columnname].value_counts()
    #count add to a text file or CSV...
    print(counts)

#Get a summary of data
def describe():
    dataset = input('Please enter path to input CSV: ')
    data = pd.read_csv(dataset)
    description = data.describe()
    description.to_csv('description.csv', encoding='utf-8')

#Get a date range
def get_date_range():
    dataset = input('Please enter path to input CSV: ')
    
startit = True
def start():
    userselect = input('''Enter a number to select an action:

        1 - Combine two spreadsheets
        2 - Join two spreadsheets
        3 - Group data
        4 - Get counts of each value in a column
        5 - Get a summary of your data
        6 - Get a date range

        Selection: ''')

    if userselect == '1':
        print('\nYou have selected Action 1 - Combine two spreadsheets\n')
        combine_csvs()
    if userselect == '2':
        print('\nYou have selected Action 2 - Join two spreadsheets\n')
        join_csvs()
    if userselect == '3':
        print('\nYou have selected Action 3 - Group data\n')
        group_by()
    if userselect == '4':
        print('\nYou have selected Action 4 - Get value counts\n')
        get_val_counts()
    if userselect == '5':
        print('\nYou have selected Action 5 - Describe your dataset\n')
        describe()
    if userselect == '6':
        print('\nYou have selected Action 6 - Get a date range\n')
        get_date_range()

while startit:
    start()

