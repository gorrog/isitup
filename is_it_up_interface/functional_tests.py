from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
        # He sees an 'admin' link on the main page
        # screen.
        admin_link = self.browser.find_element_by_link_text("Admin")
        # He clicks the login link
        admin_link.click()

        # He's taken to a login page containing a username and password box
        self.assertIn('Log in', self.browser.title)
        username_field = self.browser.find_element_by_id("id_username")
        password_field = self.browser.find_element_by_id("id_password")

        # Arnold enters his username and password.
        # Unfortunately, Arnold types his password incorrectly. He hits enter.
        username_field.send_keys("MrAdmin")
        password_field.send_keys("MRADMIN123")
        password_field.send_keys(Keys.ENTER)
        # The page refreshes and alerts him that either his username or password were incorrect

        target_string = "Please enter the correct username and password"
        error_message = self.browser.find_element_by_class_name("errornote")
        self.assertIn(target_string, error_message.text)

        # Arnold realises that he had caps lock on. He fixes this and now enters his password
        # and username correctly. He hits enter.
        username_field = self.browser.find_element_by_id("id_username")
        password_field = self.browser.find_element_by_id("id_password")
        username_field.clear()
        username_field.send_keys("MrAdmin")
        password_field.clear()
        password_field.send_keys("MrAdmin123")
        password_field.send_keys(Keys.ENTER)
        # The page takes him to an admin page titled "Site administration"
        target_string = "Site administration"
        self.assertIn(target_string, self.browser.title)

        ## We don't need to test further as Arnold since this is the Django admin we didn't write.
        ## We assume for the sake of sanity and time that this actually works.

class UserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_user_login(self):
        print("now insite the UserTest test class")
        self.fail("Finish the test")
        # Ursula User has heard about this site for monitoring South African Government
        # e-services and wants to see if the site she is in charge of is on the list.

        # She navigates to the website's hompage
        self.browser.get('http://localhost:8000/')
        # She sees that the page title mentions monitoring Government E-Services
        target_string = "South African Digital Services"
        self.fail("Finish the tests")

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
    unittest.main()
