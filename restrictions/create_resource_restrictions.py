#!/usr/bin/env python3
import requests
import json
import getpass
import pprint
import csv

#login biz
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
        #URIs to act upon
        resource_URI = row[0]
        #this is the local machine-actionable restriction type
        restriction_type = row[1]
        #free text restrictions
        restriction_text = row[2]
        #this can be empty
        begin_date = row[3]
        #can also be empty
        end_date = row[4]
        #gets resource to edi
        resource_json = requests.get(api_url + resource_URI, headers=headers).json()
        #build JSON 
        new_restriction = {'jsonmodel_type': 'note_multipart',
            'publish': True,
            'rights_restriction': {'begin': begin_date, 'end': end_date, 'local_access_restriction_type': [restriction_type]},
            'subnotes': [{'content': restriction_text,
                          'jsonmodel_type': 'note_text',
                          'publish': True}],
            'type': 'accessrestrict'}
        #append to resource
        resource_json['notes'].append(new_restriction)
        #dump
        resource_data = json.dumps(resource_json)
        #post
        resource_update = requests.post(api_url + resource_URI, headers=headers, data=resource_data).json()
        #what's happening?
        print(resource_update)
#add outfile for error logging
print('All Done!')      
