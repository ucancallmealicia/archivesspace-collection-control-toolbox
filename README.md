# ArchivesSpace Collection Control Toolbox
Simple tools to make the most of collection control functionality in ArchivesSpace

## What's in this Toolbox

* 

## General Tips:

* Test scripts thoroughly before running in production
* Use SQL to analyze and report on data, use the API to update data

## Database Tools

* Analyze your data to identify remediation needs
* Run reports on your holdings once collection control data is in ArchivesSpace

### Requirements

* SQL Client (i.e. SQL Workbench, HeidiSQL)
* ArchivesSpace 1.5+
* Access to ArchivesSpace database

### Remediation

#### Get Archival Objects

* Retrieve archival objects to which you would like to add container instances

#### Get Container Profiles

#### Get Locations

#### Get Top Containers/Barcodes

### Reporting

#### Container Lists

#### Access Restrictions

#### Container Types

## API Tools

Quickly add collection control data to ArchivesSpace using spreadsheets and the ArchivesSpace API

### Requirements

* Python 3.4+
* Python `requests`, `pymysql` modules
* ArchivesSpace version 1.5+
* Access to ArchivesSpace API

### Container Profiles

* Add container profiles to ArchivesSpace

#### container_profile_template.csv

* Use this spreadsheet to enter your container profile data

#### create_container_profiles.py

* This script takes the data from your container_profile_template spreadsheet and posts to ArchivesSpace

### Locations

* Add locations data to ArchivesSpace

#### locations_template.csv

* Use this spreadsheet to enter your location data

#### create_locations.py

* This script takes the data from your completed locations_template spreadsheet and posts to ArchivesSpace

### Top Containers

#### Create Top Containers

##### top_container_template.csv

* Use this spreadsheet to enter your top container data

##### create_top_containers.py

* This script takes the data from your completed top_container_template spreadsheet and poss to ArchivesSpace

#### Update Top Containers

#### Link Top Container Instances to One or More Archival Objects

##### tc_instance_template.csv

* Use this spreadsheet to enter your top container instance data

##### create_container_instance.py

* This script takes the data from your completed tc_instance_template spreadsheet and posts to ArchivesSpace

### Restrictions

#### restrictions_template.csv

* Use this spreadsheet to enter your restriction data

#### add_restrictions.py

* This script takes the data from your completed restrictions_template spreadsheet and posts to ArchivesSpace

### Reporting with Python and SQL

#### Barcode Audit

## Further Reading/Tutorials

* Installing third-party Python modules
* ArchivesSpace API reference
* Python 3 Syntax
* SQL Syntax
