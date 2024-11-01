import pymysql
import json
from creationQuerries import *
from insertionQuerries import *

# Load the JSON data from the file
secrets = open('data/secrets.json', 'r')
data = json.load(secrets)

#Start a connection
db = pymysql.connect(host=data['mysql']['host'], user=data['mysql']['user'], password=data['mysql']['password'])

#Create the database cursor
c = db.cursor()

#Drop the database if already exists
try:
    c.execute("DROP DATABASE ScrambleGame;")
except pymysql.err.DatabaseError:
    pass

#Create Datatbase
c.execute("CREATE DATABASE ScrambleGame;")

#Access the database
c.execute("USE ScrambleGame;")

#Create tables
c.execute(createGame())
c.execute(createPlayer())
c.execute(createWord())
c.execute(createGameWords())
c.execute(insertWords())

#Save any changes to the database
db.commit()
c.close()
db.close()