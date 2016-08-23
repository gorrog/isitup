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
        myConnection = psycopg2.connect(host = host_name, user = user_name, 
        password = password, dbname = database)
        return myConnection
    except:
        my_logger = logging.getLogger()
        my_logger.error("Can't connect to database. Exiting.")
        raise ConnectionError("Could not connect to the database! Aborting")

    
def init():
    '''
    Add the log message handler to the logger
    Loggin file sizes limited to 5 files of about 100 Kb
    TODO: fix warning from file not closed caused by 3 lines below
    '''
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.INFO) 
    handler = logging.handlers.RotatingFileHandler(
                  LOG_FILE, maxBytes=100000, backupCount=4)
    my_logger.addHandler(handler)

    my_logger.info("Started at {}".format(datetime.datetime.now()))

def finish():
    '''
    
    '''
    my_logger = logging.getLogger()
    my_logger.info("Finished at {}".format(datetime.datetime.now()))
    

def check_all_sites(host_name = HOSTNAME, user_name = USERNAME, 
                password = PASSWORD, database = DATABASE):
    '''
    Checks the list of sites in the database and updates the database according
    to each site's availability
    '''
    # Get the list of sites to check
    init()
    # print("host_name is {}, user_name is {}, password is {}, database is 
    # {}".format(host_name, user_name, password, database))
    
    my_connection = connect_db(host_name, user_name, password, database)
    sites_list = get_sites(my_connection) 
    # For each site:
    for site_data in sites_list:
        print(site_data)
        # See if it is due for a check according to the schedule
        schedule = site_data[1]
        last_checked = site_data[3]
        # If it is due, check it and update the status and last checked date
        if schedule_due(schedule, last_checked, my_connection):
            print("The schedule is due!")
            url = site_data[0]
            status_code = check_site(url)
            update_site(my_connection, url, status_code, last_checked.tzinfo)
            if status_code == 999:
                print("The status for url {} is {}".format(url, status_code))
        else:
            print("The schedule isn't due")
        # If there was an error add a new record to the error table.
    finish()
    

def get_sites(my_connection):
    ''' 
    Get the list of sites to check from the database.
    '''
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


def schedule_due(schedule, last_checked, my_connection):
    '''
    Passing the data for a website that is overdue for a checkup 
    '''
    current_date_time = datetime.datetime.now(tz=last_checked.tzinfo)
    if (last_checked + schedule) <= current_date_time:
        return True
    else:
        return False

def check_site(url):
    '''
    Tries to access a URL. Returns the status returned by the server, or '999'
    if the site is unreachable
    '''
    try:
        r = requests.get(url)
        return(r.status_code)
    # requests.get() will raise a connection error if a connection isn't
    # possible
    except requests.exceptions.ConnectionError:
        return(999)
    # We should not get here. Raise an error if we do!
    raise RuntimeError(
        "Function check_site() was unable to check the requested url, Exiting!"
    )
        
    
def update_site(my_connection, url, status_code, timezone):
    ''' 
    Update the current site with a status code and last_checked value
    '''
    sql_string="""
        UPDATE 
        site
        SET
        last_status = %s,
        last_checked = %s
        WHERE
        url = %s;
    """
    current_date_time = datetime.datetime.now(tz=timezone)
    cur = my_connection.cursor()
    data = (status_code, current_date_time, url)
    cur.execute(sql_string, data)
    my_connection.commit()
    
