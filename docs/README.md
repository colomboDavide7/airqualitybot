# airQuality

Welcome to airQuality repository.

This repository is owned by Davide Colombo.

All the scripts provided in this repository are written by Davide Colombo.

# What do you find here

The repository is structured in seven folder, going from up to down there are:

- airquality: 	core folder of the project in which there are all scripts and classes
- docs:		documentation folder
- fetch:		fetch bot module 	(runnable)
- geo:		geo bot module	 	(runnable)
- initialize:	initialize bot module 	(runnable)
- sample:	folder that contains the sample files for project settings
- test:		unit test folder

# Project purposes

The purpose of this python project is to define a set of 'bots', i.e. a computer 
program that operates as an agent for a user or other program, that basically fetches
data from air quality sensor API and store them into a database.

# Bot types

There are three bot types:

- fetch: 	fetches data from sensor's API and store into the database

- geo:		fetches the sensor's geolocation and if it differs from the one
		already stored into the database, updates it

- initialize: 	searches for new sensors in a given geographic area and if they  
		are not present into the database, it inserts them

# Supported APIs

The project supports three type of API:

- PurpleAir API
- ThingSpeak API
- AtmoTube API

# Bot personalities

There are three personality:

- atmotube
- purpleair
- thingspeak

A bot personality must be passed as argument for running a bot.

# Initialize bot (PurpleAir)

The purpose of this bot is to initialize the database with the PurpleAir
sensors.

This bot fetches ThingSpeak API ids and keys and geolocation information
from the PurpleAir API for all the sensors within a given geographic area 
specified by the 'nwlng, nwlat, selng, selat' optional parameters that can 
be used in the PurpleAir URL querystring.

The bot selects all the sensors stored into the database from the personality
identifier then fetches data from PurpleAir API and filters out the sensors that
are already present into the database to avoid inserting duplicates.

# Geo bot (PurpleAir)

The purpose of this bot is to check if the geolocation of a sensor already present 
into the database is changed and eventually update it.

This bot fetches geolocation data from the PurpleAir API for all the sensors within a 
given geohraphic area specified by the 'nwlng, nwlat, selng, selat' optional 
parameters that can be used in the PurpleAir URL querystring.

The bot fetches data from the PurpleAir API, then selects all the sensors already
stored into the database and keeps API packets coming from only those sensors 
already presents into the database. Then it compares the current geolocation with
the new fetched by the API: if they differ the sensor's geolocation is updated 
into the database.

# Fetch bot (ThingSpeak)

The purpose of this bot is to fetch air quality measurement data from the ThingSpeak
API for all the PurpleAir sensors stored into the database.

Each sensor has 2 channels and each channel has both primary and secondary data.

The bot works based on the timestamp of the last measurement corresponding to the
given sensor stored into the database. This allows the bot to fetch the historical 
data from 2018-01-01 to the moment the bot is ran.

If there are no PurpleAir sensors stored into the database, the bot stops immediately.

# Fetch bot (AtmoTube)

The purpose of this bot is to fetch air quality measurement data from the AtmoTube
API for all the AtmoTube sensors stored into the database.

The bot works based on the timestamp of the last measurement corresponding to
the given sensor stored into the database. This allows bot to fetch all data 
from time of creation the first time it is ran for a given sensor and then 
the next times it fetches only data from the last acquisition on.

If there are no AtmoTube sensors stored into the database, the bot stops immediately.

# Dependencies

- python,   v 3.9
- psycopg2, v 2.8.6 (connection to database)

# Run the program

To run the program from the command line, you simply have to type:

python -m bot_type bot_personality api_address_number

# Run Unit Tests

To run all the unit tests from the command line, you simply have to type:

python -m unittest discover -s test -p 'test_*.py' 

# More detailed documentation

You can find more information about how the program works in the 'docs/instructions.txt'.

Davide Colombo
