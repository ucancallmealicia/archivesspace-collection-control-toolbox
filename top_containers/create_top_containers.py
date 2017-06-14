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

#NOTE - top containers don't actually hold info about linked records, these are related through the top container reference
#in the archival objects themselves. Thus, 2 different things have to happen here. First, the script creates top containers
#which are not linked to anything, and then another operation links those top containers to archival objects. Unfortunately
#this linking operation has to use a different script, because

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        barcode = row[0]
        indicator = row[1]
        container_profile_uri = row[2]
        if len(barcode) == 14:
            create_tc = {'barcode': barcode, 'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                     'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
        else:
            create_tc = {'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                     'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
        tcdata = json.dumps(create_tc)
        tcupdate = requests.post(api_url + '/repositories/12/top_containers', headers=headers, data=tcdata).json()
        print(tcupdate)


print('All Done!')
        
