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
#text file for update info
outfile = input("Please enter path to output text file: ")

with open(input_csv, 'r', encoding='utf-8') as csvfile, open(outfile, 'a') as txtout:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        building = row[0]
        room = row[1]
        coordinate_1_label = row[2]
        coordinate_1_indicator = row[3]
        coordinate_2_label = row[4]
        coordinate_2_indicator = row[5]
        coordinate_3_label = row[6]
        coordinate_3_indicator = row[7]
        location_profile = row[8]
        if location_profile != '':
            new_location = {'jsonmodel_type': 'location', 'building': building,
                                     'room': room, 'coordinate_1_label': coordinate_1_label,
                                     'coordinate_1_indicator': coordinate_1_indicator,
                                     'coordinate_2_label': coordinate_2_label,
                                     'coordinate_2_indicator': coordinate_2_indicator,
                                     'coordinate_3_label': coordinate_3_label,
                                     'coordinate_3_indicator': coordinate_3_indicator,
                                     'location_profile': {'ref': location_profile}}
        else:
            new_location = {'jsonmodel_type': 'location', 'building': building,
                                     'room': room, 'coordinate_1_label': coordinate_1_label,
                                     'coordinate_1_indicator': coordinate_1_indicator,
                                     'coordinate_2_label': coordinate_2_label,
                                     'coordinate_2_indicator': coordinate_2_indicator,
                                     'coordinate_3_label': coordinate_3_label,
                                     'coordinate_3_indicator': coordinate_3_indicator}
        location_data = json.dumps(new_location)
        create_location = requests.post(api_url + '/locations', headers=headers, data=location_data).json()
        print(create_location)
        for key, value in create_location.items():
            if key == 'status':
                txtout.write('%s:%s\n' % (key, value))
            if key == 'uri':
                txtout.write('%s:%s\n' % (key, value) + '\n')
            if key == 'error':
                txtout.write('%s:%s\n' % (key, value))
    txtout.close()
    
print('All Done!')
        
        
