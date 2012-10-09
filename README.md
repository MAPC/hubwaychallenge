# Hubway Data Visualization Challenge

A website to coordinate the [Hubway Data Visualization Challenge](http://hubwaydatachallenge.org/).

Features:

* Tastypie Data API
* Social Auth user registration
* Challenge submission upload
* Ratings
* Comments

MAPC Project team: Holly St. Clair, Clay Martin, Jessica Robertson, Christian Spanring 

## Dependencies

A PostgreSQL/PostGIS database is required for data storage and GeoDjango functionality. To create one, execute:

    $ createdb hubway -T template_postgis

Python dependencies can be installed through the pip requirements file:

    $ pip install -r requirements.txt

---

Copyright 2012 MAPC