\"Air pollution is a major cause of premature death and disease, 
and is the single largest environmental health risk in Europe. 
Latest estimates by the European Environment Agency (EEA) show 
that fine particulate matter (PM2.5) continues to cause the most
 substantial health impacts.\" - EEA, 2021/12/01
 
 Learn more at https://www.eea.europa.eu/themes/air/health-impacts-of-air-pollution.
 
 This program is entirely developed by Davide Colombo for University of Pavia.
 The program follows the workflow below:
 
 get data from a source -> do some manipulation -> store data to database
 
 The source can be local or remote. 
 A local source can be an entire directory or a single file.
 The remote source can be an API.
 
 The \"manipulation\" step consists of filtering data to avoid duplicates and database inconsistencies.
 
 ------------------------------ COMMANDS DESCRIPTION ------------------------------
 The program gives you three commands for doing the work: [ init | update | fetch ]
 
 The \"init\" command is the one you can use to initialize something into the database.
                    - No DELETE operation is performed by this command. -
 Data that are already present into the database are ignored.
 
 The \"update\" command can be used to keep data up-to-date.
                    - No DELETE operation is performed by this command. -
Data that are consistent with the current state are ignored.

The \"fetch\" command can be used to download sensor measurements.
The program starts from last acquisition and continue until the moment the program is run.
                   - No DELETE operation is performed by this command. -
Data that are already present into the database are filtered out.

------------------------------ TARGETS DESCRIPTION ------------------------------
The program works by using one of the above command on a TARGET.

The targets defined in this program are: [ purpleair | atmotube | thingspeak | geonames ]

The \"purpleair\" target is used for hitting the PurpleAir API and storing the sensor data into the database.

This target can be used on commands: [ init | update ]
The \"init purpleair\" command hits three tables: [ sensor | api_param | sensor_at_location ]
The \"update purpleair\" command hits one table: [ sensor_at_location ]

The \"atmotube\" target is used for hitting the Atmotube API and storing the sensor measurements in a time range.

This target can be used on command: [ fetch ]
The \"fetch atmotube\" command hits two table: [ mobile_measurements | api_param ]

The \"thingspeak\" target is used for hitting the Thingspeak API and storing the sensor measurements in a time range.

This target can be used on command: [ fetch ]
The \"fetch thingspeak\" command hits two table: [ station_measurements | api_param ]

------------------------------ RECAP ------------------------------

init purpleair:     insert sensors and information into the database
init geonames:      insert places information into the database
update purpleair:   check if a sensor has a different location and if it is, change it
fetch atmotube:     insert atmotube measurements into the database in time range: [ last_acquisition - now ]
fetch thingspeak:   insert thingspeak measurements into the database in time range: [ last_acquisition - now ]

------------------------------ PROGRAM USAGE ------------------------------

python(version) -m airquality command target

Have fun, 
Davide.
