# -*- coding: utf-8 -*-
import requests
import urllib
# import flask
import psycopg2
import logging
import logging.handlers
import datetime
from twitter import *
import time

from site_checker.settings import (
    DATABASE_SETTINGS,
    LOG_SETTINGS,
    TWITTER_SETTINGS
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
                  LOG_SETTINGS['log_file'], maxBytes=100000, backupCount=4)
    my_logger.addHandler(handler)

    my_logger.info("Started at {}".format(datetime.datetime.now()))

def finish():
    '''
    '''
    my_logger = logging.getLogger()
    my_logger.info("Finished at {}".format(datetime.datetime.now()))

def check_all_sites(
    database_settings=DATABASE_SETTINGS,
    log_settings=LOG_SETTINGS,
    twitter_settings=TWITTER_SETTINGS
    ):
    '''
    Checks the list of sites in the database and updates the database according
    to each site's availability
    '''
    # Get the list of sites to check
    init()
    # delete_all_tweets(twitter_settings)
    my_connection = connect_db(database_settings['host_name'], database_settings['user_name'], database_settings['password'], database_settings['database'])
    sites_list = get_sites(my_connection)
    # For each site:
    for site_data in sites_list:
        # See if it is due for a check according to the schedule
        schedule = site_data[2]
        last_checked = site_data[4]
        # If it is due, check it and update the status and last checked date
        if schedule_due(schedule, last_checked, my_connection):
            url = site_data[1]
            site_id = site_data[0]
            status_code = check_site(url)
            current_date_time = datetime.datetime.now(last_checked.tzinfo)
            update_site(my_connection, site_id, status_code, current_date_time)
            # If there was an error add a new record to the error table.
            last_status = site_data[3]
            site_name = site_data[5]
            responsible_account = site_data[6]
            if status_code > 399:
                add_error(my_connection, site_id, status_code, current_date_time)
                if last_status < 399:
                   # The status of this site has changed from being up to now showing an error. We should tweet about this.
                   tweet_error(url, site_name, status_code, responsible_account, twitter_settings)
            elif status_code <= 399 and last_status > 399:
                # This means there previously was an error, but now things are OK. We should tweet about this.
                tweet_site_back_online(url, site_name, responsible_account, twitter_settings)
    finish()

def get_sites(my_connection):
    '''
    Get the list of sites to check from the database.
    '''
    sql_string="""
        SELECT
            id,
            url,
            schedule,
            last_status,
            last_checked,
            site_name,
            responsible_account
        FROM
        site;
    """
    cur = my_connection.cursor()
    cur.execute(sql_string)
    results = cur.fetchall()
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

def update_site(my_connection, id, status_code, current_date_time):
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
        id = %s;
    """
    cur = my_connection.cursor()
    data = (status_code, current_date_time, id)
    cur.execute(sql_string, data)
    my_connection.commit()


def add_error(my_connection, site_id, status_code, current_date_time):
    '''
    Add an error entry to the database for the given site and url
    '''
    sql_string="""
        INSERT
        INTO
        error
        (
        site_id,
        error_timestamp,
        error_code
        )
        VALUES
        (
        %s,
        %s,
        %s
        )
    """
    cur = my_connection.cursor()
    data = (site_id, current_date_time, status_code)
    cur.execute(sql_string, data)
    my_connection.commit()

def tweet_error(url, site_name, status_code, responsible_account,  twitter_settings):
    key = twitter_settings['twitter_access_token']
    secret = twitter_settings['twitter_access_token_secret']
    consumer_key = twitter_settings['twitter_consumer_key']
    consumer_secret = twitter_settings['twitter_consumer_secret']

    t = Twitter(
        auth=OAuth(
            key, secret, consumer_key, consumer_secret
        )
    )

    status_text = ''
    if responsible_account:
        status_text += '@{}: '.format(responsible_account)
    if status_code == 999:
        status_text += "{} at {} is offline. We'll monitor and tweet when it's back online again."
        status_text = status_text.format(site_name, url)
    elif status_code > 399:
        status_text += "The {} site ({}) is returning a {} error. We'll tweet when it's back to normal."
        status_text = status_text.format(site_name,url, status_code)
    else:
        raise NotImplementedError("Something has gone wrong: no need to tweet if the status isn't either > 399 or 999")
    t.statuses.update(status=status_text)

def tweet_site_back_online(url, site_name, responsible_account,  twitter_settings):
    key = twitter_settings['twitter_access_token']
    secret = twitter_settings['twitter_access_token_secret']
    consumer_key = twitter_settings['twitter_consumer_key']
    consumer_secret = twitter_settings['twitter_consumer_secret']

    t = Twitter(
        auth=OAuth(
            key, secret, consumer_key, consumer_secret
        )
    )

    status_text = ''
    if responsible_account:
        status_text += '@{}: '.format(responsible_account)
    status_text += "Good news! The {} site ({}) is back online."
    status_text = status_text.format(site_name,url)
    t.statuses.update(status=status_text)

def delete_all_tweets(twitter_settings):
    key = twitter_settings['twitter_access_token']
    secret = twitter_settings['twitter_access_token_secret']
    consumer_key = twitter_settings['twitter_consumer_key']
    consumer_secret = twitter_settings['twitter_consumer_secret']
    time.sleep(2)
    t = Twitter(
        auth=OAuth(
            key, secret, consumer_key, consumer_secret
        )
    )
    tweets = t.statuses.home_timeline(count=10)
    for tweet in tweets:
        id = tweet['id']
        time.sleep(2)
        t.statuses.destroy(_id=id)
