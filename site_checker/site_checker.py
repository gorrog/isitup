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
    # print("host_name is {}, user_name is {}, password is {}, database is {}".format(host_name, user_name, password, database))
    my_connection = connect_db(host_name, user_name, password, database)
    # Get the list of sites to check
    sites_list = get_sites(my_connection)
    
    # For each one:
    # See if it is due for a check according to the schedule
    # If it is due, check it and update the status and last checked date
    # If there was an error add a new record to the error table.
    for site_data in sites_list:
        print(site_data)
        schedule = site_data[1]
        last_checked = site_data[3]
        if schedule_due(schedule, last_checked):
            print("The schedule is due!")
        else:
            print("The schedule isn't due")
    
    finish()
    

def get_sites(my_connection):
    sql_string="""
        SELECT 
            url,
            schedule,
            last_status,
            last_checked
        FROM
        site;
    """
    cur = my_connection.cursor()
    cur.execute(sql_string)
    results = cur.fetchall()
    print(results)
    return results
    


def schedule_due(schedule, last_checked):
    ''' Passing the data for a website that is overdue for a checkup '''
    current_date_time = datetime.datetime.now(tz=last_checked.tzinfo)
    if (last_checked + schedule) <= current_date_time:
        return True
    else:
        return False