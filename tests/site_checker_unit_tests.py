class SiteCheckerTest(unittest.TestCase):
    
    HOSTNAME = 'web528.webfaction.com'
    USERNAME = 'gorrog'
    PASSWORD = 'IsItUpAdmin012'
    DATABASE = 'isitup_test'

    # 12:05am arrives on our server and since our cron job has set
    # site_checker.py to run every 5 minutes, it is launched
        
    def setUp(self):
        self.myConnection = psycopg2.connect( host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE )
    
    def tearDown(self):
        self.myConnection.close()
        
    def test_something(self):
        self.fail("Finish the tests")
        # TODO:
        # The following descriptors have been copied from site_checker_functional_tests.py
        # so some of them will not apply and should be deleted
        
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
        
        # 12:10am arrives on our server and since our cron job has set
        # site_checker.py to run every 5 minutes, it is launched
        # The program attempts to connect to our database
        # Unfortunately, the database server can't be reached.
        # The program creates a new log entry recording this connection error. The date
        # and time of the conneciton attempt are also logged.
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to our database again.
        # This time the connection is successful.
        # Create table for testing purposes
        # The program retrieves a list of all sites and their shedules to be checked
        # The program iterates over the list
        # The first url on the list, cleanshooz.xyz was due to be checked 4 minutes ago
        # The program attempts to connect to the site but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program waits a final 10 seconds, just in case there was a network anomoly.
        # The program attempts to connect to the site again but the connection times out
        # The program records this time out event in the database, linked to the url
        # The program sends a tweet saying that cleanshooz.xyz appears to be unreachable.
        # Included in the tweet is the time it was tried and the IP it was tried from. The
        # tweet mentions the person/organisation who is responsible for it.
        # The second item on the list, monkeyfishboat.ol was due to be checked 20 seconds ago.
        # The program attempts to connect to the site. The site is accessible without an error.
        # The program records this successful access in the database under this URL.
        # The third item on the list, www.hgjdksl.wo is only due to be checked in 3 minutes,
        # so no action is taken.
        
        # All the other items on the list are only due in the future, so the script closes.
    
