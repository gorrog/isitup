# -*- coding: utf-8 -*-
import unittest
import psycopg2
import requests
import os
from site_checker.site_checker import check_all_sites
import datetime
import logging
from testfixtures import LogCapture

from test_settings import (
    HOSTNAME,
    USERNAME,
    PASSWORD,
    DATABASE
    )

# TODO: Reformat all lines to not go over column 79

class SiteCheckerTest(unittest.TestCase):
    

    # 12:05am arrives on our server and since our cron job has set
    # site_checker.py to run every 5 minutes, it is launched
        
    def setUp(self):
        self.myConnection = psycopg2.connect( host=HOSTNAME, user=USERNAME, 
        password=PASSWORD, dbname=DATABASE )
        self.initialise_database()
    
    def tearDown(self):
        self.myConnection.close()
        
    def test_bad_database_connection_results_in_log_entries(self):
        # The program attempts to connect to our database
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. 
        # The date and time of the conneciton attempt are also logged.
        # The program saves a log entry saying it is exiting, and then closes.
        # import pdb; pdb.set_trace()
        with self.assertRaisesRegex(ConnectionError, 
        "Could not connect to the database! Aborting"):
            with LogCapture(level = logging.ERROR) as l:
                # We pass the check_site() function bad conneciton data
                check_all_sites(password = 'BadPassword')
                l.check(
                 ('root', 'ERROR', "Can't connect to database. Exiting.")
                ) 
            
      
        
    def test_unavailable_site(self):
        # rewrite /// later
        # The first url on the list to be checked, gorrog.org/
        # blah was due to be checked some time ago
        # The program attempts to connect to the site 
        # but the connection times out
        # The program records this time out event in the database,
        # linked to the url
        # The program waits 10 seconds, just in case there was a network anomaly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits a final 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
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
            'http://gorrog.org/blah',
            '30 minutes',
            '2016-08-20 12:15:03.946442+00',
            200
            )
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        self.myConnection.commit() 
        # run the test function with our test database. Other credentials are the
        # same
        check_all_sites(database = DATABASE)
        sql_string = """
            SELECT 
                site_id,
                error_timestamp,
                error_code
            
            from
            error;
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        results = cur.fetchall()
        if not results:
            self.fail("Program didn't add an error to the error table")
        site_id = results[0][0]
        error_timestamp = results[0][1]
        error_code = results[0][2]
        self.assertEquals(site_id == 1)
        current_date_time = datetime.datetime.now(tz=error_timestamp.tzinfo)
        self.assertTrue(current_date_time - error_timestamp < datetime.timedelta(seconds=60))
        self.assertEqual(error_code, 404)
        # The first url on the list to be checked, gorrog.org/blah was due to be checked some time ago
        # The program attempts to connect to the site but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits a final 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        
    def test_tweet_unavailable_site(self):
        self.fail("Finish the tests")
        # The program sends a tweet saying that cleanshooz.xyz appears to be unreachable.
        # Included in the tweet is the time it was tried and the IP it was tried from. The
        # tweet mentions the person/organisation who is responsible for it.
        
    def test_available_site(self):
        # The second item on the list, gorrog.org was due to be checked some time ago.
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
            'http://gorrog.org',
            '30 minutes',
            '2016-08-20 12:15:03.946442+00',
            200
            )
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        self.myConnection.commit()
        check_all_sites(database = DATABASE)
        sql_string = """
            SELECT
            last_checked,
            last_status
            FROM
            site
            WHERE
            url = 'http://gorrog.org'
        """
        cur = self.myConnection.cursor()
        cur.execute(sql_string)
        results = cur.fetchall()
        # The program records this successful access in the database under this URL
        # by updating the 'last_checked' value.
        returned_time = results[0][0]
        returned_status = results[0][1]
        current_date_time = datetime.datetime.now(tz=returned_time.tzinfo)
        self.assertTrue(current_date_time - returned_time < datetime.timedelta(seconds=60))
        self.assertEqual(returned_status, 200)
    
        
    def test_site_not_yet_due(self):
        self.fail("Finish the tests")
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
            cur.execute(statement)
            self.myConnection.commit()
        
if __name__ == '__main__':
    unittest.main()
    