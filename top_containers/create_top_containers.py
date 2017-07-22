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
output_txt = input("Please enter path to output TXT: ")

#NOTE - top containers don't actually hold info about linked records, these are related through the top container reference
#in the archival objects themselves. Thus, 2 different things have to happen here. First, the script creates top containers
#which are not linked to anything, and then another operation links those top containers to archival objects. Unfortunately
#this linking operation has to use a different script, because

with open(input_csv, 'r', encoding='utf-8') as csvfile, open(output_txt, 'a') as txtout:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        barcode = row[0]
        indicator = row[1]
        container_profile_uri = row[2]
        locations = row[3]
        start_date = row[4]
        repo_num = row[5]
        if barcode != '':
            create_tc = {'barcode': barcode, 'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                         'container_locations': [{'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': start_date,
                                                  'ref': locations}],
                         'jsonmodel_type': 'top_container', 'repository': {'ref': repo_num}}
        else:
            create_tc = {'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                         'container_locations': [{'jsonmodel_type': 'container_location', 'status': 'current', 'start_date': start_date,
                                                  'ref': locations}],
                         'jsonmodel_type': 'top_container', 'repository': {'ref': repo_num}}
        tcdata = json.dumps(create_tc)
        tcupdate = requests.post(api_url + repo_num + '/top_containers', headers=headers, data=tcdata).json()
        print(tcupdate)
        for key, value in tcupdate.items():
            if key == 'status':
                txtout.write('%s:%s\n' % (key, value))
            if key == 'uri':
                txtout.write('%s:%s\n' % (key, value) + '\n')
            if key == 'error':
                txtout.write('%s:%s\n' % (key, value))
    txtout.close()


print('All Done!')
        
