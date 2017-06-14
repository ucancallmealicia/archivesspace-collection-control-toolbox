#python3
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
#in the archival objects. Thus, two different things have to happen to create top containers and link them to archival objects. 
#First, this script creates all the top containers you need, unlinked to any records, and then another script links these top
#containers to archival objects as instances. Unfortunately, if using a spreadsheet to make these updates it is necessary to 
#do the linking in a different script - because each archival object is represented by a single row, multiple rows in the 
#spreadsheet will contain the same barcodes, indicators, etc., and AS will throw an error telling you that a barcode can't 
#be assigned to multiple containers (which is a good thing!). And if try just taking out the barcodes the script will create
#a bunch of erroneous top containers with the same indicators, and each archival object will be linked to a different top container...

with open(input_csv, 'r', encoding='utf-8') as csvfile:
    csvin = csv.reader(csvfile)
    next(csvin, None)
    for row in csvin:
        barcode = row[0]
        indicator = row[1]
        container_profile_uri = row[2]
        #this part here depends on the length of your barcodes - but it is needed in case the barcode column is empty
        #could ask for user input - i.e what is the length of your barcodes? and then store that as a variable and add here
        if len(barcode) == 14:
            create_tc = {'barcode': barcode, 'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                     'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
        #for when barcode column is empty
        else:
            create_tc = {'container_profile': {'ref': container_profile_uri}, 'indicator': indicator,
                     'jsonmodel_type': 'top_container', 'repository': {'ref': '/repositories/12'}}
        tcdata = json.dumps(create_tc)
        #post top container to AS
        tcupdate = requests.post(api_url + '/repositories/12/top_containers', headers=headers, data=tcdata).json()
        #prints what is happening to the screen
        print(tcupdate)
  #add error log/URI list

print('All Done!')
