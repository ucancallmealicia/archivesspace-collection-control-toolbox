#!/usr/bin/env python3

import requests
import json
import getpass
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
        archival_object_uri = row[0]
        top_container_uri = row[1]
        barcode = row[2]
        indicator = row[3]
        location_uri = row[4]
        location_start_date = row[5]
        archival_object_json = requests.get(api_url + archival_object_uri, headers=headers).json()
        new_instance = {"container": {"barcode_1": barcode, "container_locations": [{"jsonmodel_type": "container_location", 
                            "ref": location_uri, "start_date": location_start_date, "status": "current"}], "indicator_1": indicator, "type_1": "box"}, 
                            "instance_type": "mixed_materials", "jsonmodel_type": "instance", "sub_container": {"jsonmodel_type": "sub_container", 
                            "top_container": {"ref": top_container_uri}}}
        archival_object_json["instances"].append(new_instance)
        archival_object_data = json.dumps(archival_object_json)
        archival_object_update = requests.post(api_url+archival_object_uri, headers=headers, data=archival_object_data).json()
        print(archival_object_update)

print('All Done!')
