import requests
import flask
import psycopg2
 


page = requests.get('http://www.sabcsport.co.za/', timeout=5)
# pdb.set_trace()

# DB details
# username gorrog(totally not)
# IsItUpAdmin012
# hostname: web528.webfaction.com
# port: 5432
# database name: isitup



#!/usr/bin/python

hostname = 'web528.webfaction.com'
username = 'gorrog'
password = 'IsItUpAdmin012'
database = 'isitup'




# print "Using psycopg2"
# import psycopg2
# import pdb; pdb.set_trace()
myConnection = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
sql_string = '''
    CREATE
    TABLE
    "test"
    (
    "col1" int,
    "col2" text
    );
'''
# doQuery( myConnection )
cur = myConnection.cursor()
cur.execute(sql_string)
myConnection.commit()

myConnection.close()
