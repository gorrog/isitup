# -*- coding: utf-8 -*-
import requests
# import flask
import psycopg2
import logging
import logging.handlers
import datetime
 
from site_checker.settings import (
    HOSTNAME,
    USERNAME,
    PASSWORD,
    DATABASE,
    LOG_FILE
    )

def connect_db(host_name, user_name, password, database):
    try:
        myConnection = psycopg2.connect(host = host_name, user = user_name, password = password, dbname = database)
        return myConnection
    except:
        my_logger = logging.getLogger()
        my_logger.error("Can't connect to database. Exiting.")

    
def init():
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO) 
    # Add the log message handler to the logger
    # Loggin file sizes limited to 5 files of about 100 Kb
    # TODO: fix warning from file not closed caused by 3 lines below
    handler = logging.handlers.RotatingFileHandler(
                  LOG_FILE, maxBytes=100000, backupCount=4)
    my_logger.addHandler(handler)

    my_logger.info("Started at {}".format(datetime.datetime.now()))

def finish():
    my_logger = logging.getLogger()
    my_logger.info("Finished at {}".format(datetime.datetime.now()))
    

def check_site(host_name = HOSTNAME, user_name = USERNAME, password = PASSWORD, database = DATABASE):
    init()
    print("This is running in site_checker.py")
    print("host_name is {}, user_name is {}, password is {}, database is {}".format(host_name, user_name, password, database))
    
    my_connection = connect_db(host_name, user_name, password, database)
    finish()