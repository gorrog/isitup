# -*- coding: utf-8 -*-
import unittest
import psycopg2
import requests
import os
from site_checker.site_checker import (
    check_site
    )
import datetime
HOSTNAME = 'web528.webfaction.com'
USERNAME = 'gorrog'
PASSWORD = 'IsItUpAdmin012'
DATABASE = 'isitup_test'

class SiteCheckerTest(unittest.TestCase):
    
    

    # 12:05am arrives on our server and since our cron job has set
    # site_checker.py to run every 5 minutes, it is launched
        
    def setUp(self):
        print("Setting up now")
        self.myConnection = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE )
        self.initialise_database()
    
    def tearDown(self):
        self.myConnection.close()
        
    def test_bad_connection_results_in_log_entries(self):
        pass
        # The program attempts to connect to our database
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. The date
        # and time of the conneciton attempt are also logged.
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to our database again.
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. The date
        # and time of the conneciton attempt are also logged.
        # The program attempts to connect to our database for the last time.
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. The date
        # and time of the conneciton attempt are also logged.
        # If the latest entry in the email log is older than today send an email to the
        # administrator alerting them to this conneciton problem.
        # The program saves a log entry saying it is exiting, and then closes.
        
    def test_successful_connection(self):
        pass
        # 12:10am arrives on our server and since our cron job has set
        # site_checker.py to run every 5 minutes, it is launched
        # The program attempts to connect to our database
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. The date
        # and time of the conneciton attempt are also logged.
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to our database again.
        # This time the connection is successful.
        
    def test_unavailable_site(self):
        pass
    
        # The first url on the list to be checked, cleanshooz.xyz was due to be checked 4 minutes ago
        # The program attempts to connect to the site but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits a final 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        
    def test_tweet_unavailable_site(self):
        pass
        # The program sends a tweet saying that cleanshooz.xyz appears to be unreachable.
        # Included in the tweet is the time it was tried and the IP it was tried from. The
        # tweet mentions the person/organisation who is responsible for it.
        
    def test_available_site(self):
        # The second item on the list, monkeyfishboat.ol was due to be checked some time ago.
        # The program attempts to connect to the site. The site is accessible without an error.
        sql_string = """
            INSERT
            INTO
            site
            (
            url,
            schedule,
            last_checked,
            last_status
            )
            VALUES
            (
            'monkeyfishboat.ol',
            '30 minutes',
            '2016-08-20 12:15:03.946442+00',
            200
            )
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        self.myConnection.commit()
        
        print ("inserted values in the table")
        check_site()
        sql_string = """
            SELECT
            last_checked
            FROM
            site
            WHERE
            url = 'monkeyfishboat.ol'
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        results = cur.fetchall()
        print(results)
        # The program records this successful access in the database under this URL
        # by updating the 'last_checked' value.
        returned_time = results[0][0]
        current_date_time = datetime.datetime.now(tz=returned_time.tzinfo)
        print current_date_time - returned_time
        self.assertTrue(current_date_time - returned_time < datetime.timedelta(seconds=60))
        
        # if current_date_time - returned_time < datetime.timedelta(seconds=60):
        #     self.assert
        # else:
        #     print("failed")
        
        
        
        
    def test_site_not_yet_due(self):
        pass
        # The third item on the list, www.hgjdksl.wo is only due to be checked in 3 minutes,
        # so no action is taken.
        
        # All the other items on the list are only due in the future, so the script closes.
    
    def initialise_database(self):
        # Initialise test database
        file_path=os.path.normpath(os.path.join(os.getcwd(),'site_checker','is_it_up_schema.sql'))
        with open(file_path, 'r') as f:
            sql_query = f.read()
        cur = self.myConnection.cursor()
        for statement in sql_query.split(';'):
            cur.execute(statement + ';')
            self.myConnection.commit()
        
if __name__ == '__main__':
    unittest.main()
    