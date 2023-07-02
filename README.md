# airquality

> Download and store air pollution sensor's data for making analysis. And more...

![Airquality Version][air-version]
![Airquality Tests][test-out]

**The code in this repository is entirely written by Me during
my master thesis activity at University of Pavia.**

The purpose of this project is to fetch the **air quality** data from sensors
through the API services of the corresponding manufacturer and collects,
process and persistently store them into a SQL database.

Moreover, this project was extended to **weather** and **geographical**
data.

###### Supported sensors are:
* [Atmotube](https://atmotube.com)
* [PurpleAir](https://www2.purpleair.com)

###### Supported services are:
* [Thingspeak](https://thingspeak.com)
* [Geonames](http://www.geonames.org)
* [OpenWeatherMap](https://openweathermap.org)

## General workflow

The main workflow consists of four steps:

1. _fetching_ the data from a **source**, (a _file_ or a _URL_)
2. _parsing_ and _reshape_ the data, (coherently with the expected **datamodel**)
3. **(optional)** _validating_ the data, (basically a **filtering** operation)
4. and _inserting_ the data into the **database**.

## Installation

To install and use the **airquality** project in this repository, simply clone
this repository on your local machine.

This operation requires having [git](https://git-scm.com) installed
locally on your machine.

## Requirements

The external dependencies required by the **airquality** project are:

* python 3+
* [psycopg2](https://pypi.org/project/psycopg2/)
* [dotenv](https://pypi.org/project/python-dotenv/)

Follow the instructions provided in the package documentation linked above
to install them correctly.

## Environment Setup

The **airquality** project uses a **'.env'** file to load all the environment
variables. In the **sample** directory that you can find at project level, there is a file
called _sample_dot_env_. Please, follow the instructions in that file for the
environment file setup.

## Tests

The **airquality** project is tested by using [unittest](https://docs.python.org/3/library/unittest.html)
framework implementation from the standard library.

Run all tests at once:

```sh
python3 -m unittest discover -s test -p 'test_*.py'
```

Run a single test:

```sh
python3 -m test.path.to.test.file
```

by replacing 'path.to.test.file' with the path of the file of interest.

Note that to run the tests no internet connection is required neither a database.

Citing Uncle Bob,

> you can run your tests a 30.000 meters in an airplane drinking
a Martini

or something similar, but you get the point.

## Coverage

Together with unit testing it is good practice to run unit tests with a coverage tool that inform you about _how much your application is tested_.

I have used [coverage](https://coverage.readthedocs.io/en/6.2/) package to accomplish this goal.

Running coverage is easy as running the command:

```sh
coverage run --source airquality -m unittest discover && coverage report --skip-covered
```

## Usage

The **airquality** project supports five different personalities, i.e., atmotube,
purpleair, thingspeak, geonames and openweathermap.

##### downloading Atmotube data and storing into the database

```sh
python3 -m airquality atmotube
```

##### downloading PurpleAir data and storing into the database

```sh
python3 -m airquality thingspeak
```

This command can be counterintuitive but the reason is that PurpleAir offers
the possibility to fetch sensor's data (from creation time up to now) by
Thingspeak API.

##### inserting new PurpleAir sensors into the database

```sh
python3 -m airquality purpleair
```

##### loading Geonames country data into the database

```sh
python3 -m airquality geonames
```

This command requires you have properly filled the **resources/geonames/country_data/** directory with the '.txt' files of your country of interest
downloaded at [this link](http://download.geonames.org/export/zip/).

Unzip the downloaded file and put only the '.txt' file named with the uppercase
2-alpha ISO code of the country (e.g., ES.txt for Spain, IT.txt for Italy, and so on)
into the directory.

##### loading weather city data into the database

```sh
python3 -m airquality openweathermap
```

This command requires you have properly setup the **weather_cities.json** file
you can find in the sample directory at the project level.

Copy that file and fill in with your cities of interest.

Be careful because the country's and city's name specified in this file **MUST MATCH** the respective geonames names **AND ALSO** you must pre-load into the database those data taken from geonames service by running the _geonames command_
explained above.

## Logging

Create a log directory at the project level called **log** for logging errors
and other useful events.

Run the following command from the command line inside the project directory to
make it:

```sh
mkdir log
```

This directory will be filled with two files:

* errors.log: collects all the errors occurred with a longer format,
* infos.log: collects all the useful events and also errors.

## Author

Davide Colombo - email: davide.colombo02@universitadipavia.it

This project was entirely develop by Me during my master thesis activity at
University of Pavia.

<!-- Useful variable references (not displayed) -->

[air-version]: https://img.shields.io/badge/airquality-v1.0.0-orange
[test-out]: https://img.shields.io/badge/tests-passing-brightgreen
