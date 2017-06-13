#!/usr/bin/env python3
import requests
import json
import getpass
import pprint
import csv

def login (api_url, username, password):
    '''This function logs into the ArchivesSpace REST API returning an acccess token'''
    auth = requests.post(api_url+'/users/'+username+'/login?password='+password).json()
    session = auth["session"]
    headers = {'X-ArchivesSpace-Session':session}
    return headers

if __name__ == '__main__':
    api_url = input('Please enter the URL for the ArchivesSpace API: ')
    username = getpass.getuser()
    check_username = input('Is your username ' + username + '?: ')
    if check_username.lower() not in ('y', 'yes', 'yep', 'you know it'):
        username = input('Please enter ArchivesSpace username:  ')
    password = getpass.getpass(prompt=username + ', please enter your ArchivesSpace Password: ', stream=None)
    print('Logging in', api_url)
    headers = login(api_url, username, password)
    if headers != '':
        print('Success!')
    else:
        print('Ooops! something went wrong')

input_csv = input("Please enter path to input CSV: ")

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        name = row[0]
        extent_dimension = row[1]
        height = row[2]
        width = row[3]
        depth = row[4]
        dimension_units = row[5]
        new_container_profile = {'jsonmodel_type': 'container_profile', 'name': name,
                                 'extent_dimension': extent_dimension, 'height': height,
                                 'width': width, 'depth': depth, 'dimension_units': dimension_units}
        container_profile_data = json.dumps(new_container_profile)
        create_profile = requests.post(api_url + '/container_profiles', headers=headers, data=container_profile_data).json()
        print(create_profile)
#add outfile for error logging
print('All Done!')
