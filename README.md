# ArchivesSpace Collection Control Toolbox
Simple tools to make the most of collection control functionality in ArchivesSpace

## What's in this Toolbox

* SQL scripts to analyze your data and prepare update spreadsheets
* Python scripts to make bulk updates to collection control data
* More SQL scripts to report on your updated collection control data
* FAQ
* Suggestions for further study

## General Tips:

* Test scripts thoroughly before running in production
* Use SQL to analyze and report on data, use the API to update data

## Database Tools

* Analyze your data to identify remediation needs
* Run reports on your holdings once collection control data is in ArchivesSpace

### Requirements

* SQL Client (i.e. MySQL Workbench, HeidiSQL)
* ArchivesSpace 1.5+
* Access to ArchivesSpace database

### Remediation

#### Get Archival Objects

* Retrieve archival objects to which you would like to add container instances

#### get_container_profiles.sql

* Gets a list of container profiles with titles and URIs

#### get_locations.sql

* Gets a list of locations with titles and URIs

#### get_top_containers.sql

* Gets a list of existing top containers, with location and container profile data

### Reporting

#### Container Lists

* Retrieves a container list for a given collection

#### Access Restrictions

* Retrieves a list of restricted materials of a given type or end date

## API Tools

Quickly add collection control data to ArchivesSpace using spreadsheets and the ArchivesSpace API

### Requirements

* Python 3.4+
* Python `requests`, `pymysql` modules
* ArchivesSpace version 1.5+
* Access to ArchivesSpace API

### Container Profiles
Add container profiles to ArchivesSpace

#### container_profile_template.csv

* Use this spreadsheet to enter your container profile data

#### create_container_profiles.py

* This script takes the data from your container_profile_template spreadsheet and posts to ArchivesSpace

### Locations
Add locations data to ArchivesSpace

#### locations_template.csv

* Use this spreadsheet to enter your location data

#### create_locations.py

* This script takes the data from your completed locations_template spreadsheet and posts to ArchivesSpace

### Top Containers

#### Create Top Containers

##### top_container_template.csv

* Use this spreadsheet to enter your top container data

##### create_top_containers.py

* This script takes the data from your completed top_container_template spreadsheet and posts to ArchivesSpace

#### Link Top Containers to One or More Archival Objects

##### tc_instance_template.csv

* Use this spreadsheet to enter your top container instance data

##### create_container_instance.py

* This script takes the data from your completed tc_instance_template spreadsheet and posts to ArchivesSpace

#### Update Top Containers

### Restrictions
Add machine-actionable restrictions to ArchivesSpace

#### resource_level_restrictions_template.csv

* Use this spreadsheet to enter your resource-level restriction data

#### create_resource_restrictions.py

* This script takes the data from your completed resource_level_restrictions_template spreadsheet and posts to ArchivesSpace

#### archival_object_level_restrictions_template.csv

* Use this spreadsheet to enter your archival object-level restriction data

#### create_archival_object_restrictions.py

* This script takes the data from your completed archival_object_level_restrictions_template spreadsheet and posts to ArchivesSpace

### Reporting with Python and SQL

#### Barcode Audit

## FAQ

### How do I log into the ArchivesSpace API?

### How do I access the ArchivesSpace database?

### I'm logged in. I have access. Now what?

## Software Downloads/Tutorials/Further Reading

* Python 3: https://www.python.org/downloads/
* HeidiSQL: https://www.heidisql.com/download.php
* MySQL Workbench: https://dev.mysql.com/downloads/workbench/
* Installing third-party Python modules: https://python4astronomers.github.io/installation/packages.html
                                         https://docs.python.org/3/installing/
* ArchivesSpace API reference: http://archivesspace.github.io/archivesspace/api/ 
* Python 3 Syntax: https://docs.python.org/3/tutorial/
* SQL Syntax: https://dev.mysql.com/doc/refman/5.7/en/tutorial.html

