from selenium import webdriver
import unittest
# from django.contrib.auth.models import User

class AdminTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        # Arnold Admin wants to add a new site to the site checker program list
        # He navigates to the site checker site
        self.browser.get('http://localhost:8000/')
        # He sees a 'login' link on the main page
        # screen.
        login_link = self.browser.find_element_by_link_text("Log in")
        # He clicks the login link
        login_link.click()

        # He's taken to a login page
        self.browser.get('http://localhost:8000/')

        self.assertIn('Log in', self.browser.title)
        self.fail('Finish the Tests!')

# Arnold enters his username but forgets to enter a password and hits 'Enter'
# The page refreshes and alerts him that either his username or password were incorrect

# Arnold enters his password but forgets to enter a username and hits 'Enter'
# The page refreshes and alerts him that either his username or password were incorrect

# Arnold stupidly thinks that a blank password and username will get him in.
# The page refreshes and alerts him that either his username or password were incorrect

# Arnold now recalls that he did in fact register as an Admin a while back. He
# finds his username and password on a piece of paper and types them both in.
# Unfortunately, Arnold types his password incorrectly. He hits enter.
# The page refreshes and alerts him that either his username or password were incorrect

# Arnold realises that he had caps lock on. He fixes this and now enters his password
# and username correctly. He hits enter.
# The page takes him to an admin page titled "Site administration"

## We don't need to test further as Arnold since this is the Django admin we didn't write.
## We assume for the sake of sanity and time that this actually works.

# Ursula User has heard about this site for monitoring South African Government
# e-services and wants to see if the site she is in charge of is on the list.

# She navigates to http://isitupza.gorrog.org
# She sees that the page title mentions monitoring Government E-Services

# She sees that there are 3 lists of sites: Offline, Errors and Healthy.
# She sees that 'http://postoffice.co.za is in the 'healthy' list.

# She looks for http://www.gov.za, but doesn't see it on the list. She wonders
# if there is a way to submit sites for inclusion in the monitoring list.

# Fortunately, she sees that there is a link for submitting a website
# She clicks the link

# She is taken to a page with a title mentioning submitting a website.
# She reads throught the terms and conditions.

# She's happy with the terms and conditions so she starts filling out the form.
# She fills out the url and hits enter

# The page refreshes, telling her that she must enter a site name as well.
# She does so and hits enter.

# She is taken to a page thanking her for her submission.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
