# ArchivesSpace Collection Control Toolbox
Simple tools to make the most of collection control functionality in ArchivesSpace

## What's in this Toolbox

* Standalone SQL scripts to analyze your collection control data before update, prepare update spreadsheets, and report on data after update
* Standalone Python scripts to make bulk updates to collection control data
* Simple GUIs which package the standalone scripts into easy-to-use interfaces
* FAQ
* Suggestions for further study

## General Tips:

* Test scripts thoroughly before running in production
* Use SQL to analyze and report on data, use the API to update data

## Database Tools

* Analyze your data to identify remediation needs
* Run reports on your holdings once collection control data is in ArchivesSpace

### Requirements

* Standalone scripts: SQL Client (i.e. MySQL Workbench, HeidiSQL)
* GUI: Python 3, `pymysql` module
* ArchivesSpace 1.5+
* Access to ArchivesSpace database

### Container Profiles

#### get_container_profiles.sql

* Gets a list of container profiles with titles and URIs

### Locations

#### get_locations.sql

* Gets a list of locations with titles and URIs

### Archival Objects, Top Containers, and Top Container Instances

#### get_archival_objects.sql

* Retrieve a list of archival objects for a given collection, with parent-child relationships indicated

#### get_archival_object_instances.sql

* Retrieve a list of archival object instances (a container list, essentially) for a given collection

#### get_top_containers.sql

* Gets a list of existing top containers, with location and container profile data

### Restrictions

#### get_arch_obj_restrictions.sql
#### get_resource_restrictions.sql

* Retrieves a list of access restrictions, either at the archival object or resource levels

## API Tools

Quickly add collection control data to ArchivesSpace using spreadsheets and the ArchivesSpace API

### Requirements

* Python 3.4+
* Python `requests`, `pymysql` modules. The `requests` module comes with Anaconda (see below); the `pymysql` module can be installed in Anaconda by opening the Anaconda shell and typing `conda install pymysql`
* ArchivesSpace version 1.5+
* Access to ArchivesSpace API

### Recommendations

* Anaconda: https://www.continuum.io/downloads. Anaconda is a free, open source Python distribution which comes with a number of useful modules for data analysis and manipulation
* OpenRefine: http://openrefine.org/. OpenRefine is a free, open source data cleaning tool 
* Python `pandas` module. The `pandas` module comes with Anaconda.

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

#### restrictions_template.csv

* Use this spreadsheet to enter your restriction data, at either the resource or archival object levels

#### create_restrictions.py

* This script takes the data from your completed restrictions_template spreadsheet and posts to ArchivesSpace

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

