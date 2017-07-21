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
#text file for update info
outfile = input("Please enter path to output text file: ")

with open(input_csv, 'r', encoding='utf-8') as csvfile, open(outfile, 'a') as txtout:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        archival_object_uri = row[0]
        top_container_uri = row[1]
        barcode = row[2]
        indicator = row[3]
        archival_object_json = requests.get(api_url + archival_object_uri, headers=headers).json()
        new_instance = {"container": {"barcode_1": barcode, "indicator_1": indicator, "type_1": "box"}, 
                            "instance_type": "mixed_materials", "jsonmodel_type": "instance", "sub_container": {"jsonmodel_type": "sub_container", 
                            "top_container": {"ref": top_container_uri}}}
        archival_object_json["instances"].append(new_instance)
        archival_object_data = json.dumps(archival_object_json)
        archival_object_update = requests.post(api_url+archival_object_uri, headers=headers, data=archival_object_data).json()
        print(archival_object_update)
        for key, value in archival_object_update.items():
            if key == 'status':
                txtout.write('%s:%s\n' % (key, value))
            if key == 'uri':
                txtout.write('%s:%s\n' % (key, value) + '\n')
            if key == 'error':
                txtout.write('%s:%s\n' % (key, value))
    txtout.close()

print('All Done!')
