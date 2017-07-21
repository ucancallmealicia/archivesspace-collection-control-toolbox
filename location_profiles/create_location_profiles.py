#!/usr/bin/env python3
import requests
import json
import getpass
import csv

#login procedure - enter ArchivesSpace API url, credentials
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

#The magic happens here...
#Enter full path to spreadsheet where container profile data is stored
input_csv = input("Please enter path to input CSV: ")
#text file for update info
outfile = input("Please enter path to output text file: ")

#Opens spreadsheet, reads data into memory
with open(input_csv, 'r', encoding='utf-8') as csvfile, open(outfile, 'a') as txtout::
    csvin = csv.reader(csvfile)
    #skip header row
    next(csvin, None)
    #loops through spreadsheet one row at a time, adding container profile
    for row in csvin:
        name = row[0]
        dimension_units = row[1]
        depth = row[2]
        width = row[3]
        height = row[4]
        #takes data from spreadsheet and builds JSON
        new_location_profile = {'jsonmodel_type': 'location_profile', 'name': name,
                                 'height': height, 'width': width, 'depth': depth,
                                'dimension_units': dimension_units}
        location_profile_data = json.dumps(new_location_profile)
        #Posts JSON to ArchivesSpace
        create_profile = requests.post(api_url + '/location_profiles', headers=headers, data=location_profile_data).json()
        #Prints what is happening to IDLE window - will add an error log as well
        print(create_profile)
        for key, value in create_profile.items():
            if key == 'status':
                txtout.write('%s:%s\n' % (key, value))
                x = x +1
            if key == 'uri':
                txtout.write('%s:%s\n' % (key, value) + '\n')
            if key == 'error':
                txtout.write('%s:%s\n' % (key, value))
    txtout.close()
    
print('All Done!')
