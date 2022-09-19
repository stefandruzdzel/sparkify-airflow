# Project: AWS Datawarehouse

This project is for Udacity's Data Engineering Nanodegree

A music streaming company, Sparkify, has decided that it is time to introduce more automation and monitoring to their data warehouse ETL pipelines and come to the conclusion that the best tool to achieve this is Apache Airflow.

They have decided to bring you into the project and expect you to create high grade data pipelines that are dynamic and built from reusable tasks, can be monitored, and allow easy backfills. They have also noted that the data quality plays a big part when analyses are executed on top the data warehouse and want to run tests against their datasets after the ETL steps have been executed to catch any discrepancies in the datasets.

The source data resides in S3 and needs to be processed in Sparkify's data warehouse in Amazon Redshift. The source datasets consist of JSON logs that tell about user activity in the application and JSON metadata about the songs the users listen to.

## Data pipeline

DAG 1: Creates empty Redshift tables
create_tables_dag.py
This DAG has a single node that runs a SQL Query that creates these tables if they do not exist.
This DAG is set to run just once.
At this time, an Airflow pipeline here is not quite necessary since there's only a single step. However I opted to use Airflow because it will help the infrastructure scale as Sparkify's infrastructure becomes more complicated.

DAG 2: ETL Data Pipeline
![alt text](https://github.com/stefandruzdzel/sparkify-airflow/blob/main/ETL%20DAG.jpg?raw=true)


## Data

### Example JSON Song File:
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}

### Data contained in log Files:
artist, auth, firstName, gender, itemInSession, lastName, length, location, method, page, registration, sessionId, song, status, ts, userAgent, userId

## Staging tables:

### staging_events_table
artist, auth, firstName, gender, itemInSession, lastName, length, location, method, page, registration, sessionId, song, status, ts, userAgent, userId

### staging_songs_table
num_songs, artist_id, artist_latitude, artist_longitude, artist_name, song_id, title, duration, year



## Schema for Song Play Analysis

### Fact Table
#### songplays - records in event data associated with song plays i.e. records with page NextSong
songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables
#### users - users in the app
user_id, first_name, last_name, gender, level

#### songs - songs in music database
song_id, title, artist_id, year, duration

#### artists - artists in music database
artist_id, name, location, lattitude, longitude

#### time - timestamps of records in songplays broken down into specific units
start_time, hour, day, week, month, year, weekday