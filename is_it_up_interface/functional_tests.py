from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
# from django.contrib.auth.models import User

# Test interacting with the site from the perspective of an Administrator
class AdminTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        # Arnold Admin wants to add a new site to the site checker program list
        # He navigates to the site checker site
        self.browser.get("http://localhost:8000/")

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

# Test interacting with the site from the perspective of a public user
class UserTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_user_login(self):
        # Ursula User has heard about this site for monitoring South African Government
        # e-services and wants to see if the site she is in charge of is on the list.

        # She navigates to the website's hompage
        self.browser.get("http://localhost:8000/")

        # She sees that the page title mentions monitoring Government E-Services
        target_string = "South African Digital Services"

        # She sees that there are 3 lists of sites: Offline, Errors and Healthy.
        # She sees that 'http://postoffice.co.za is in the 'healthy' list.
        offline_heading = self.browser.find_element_by_id("Offline")
        self.assertIn('Offline', offline_heading.text)
        problem_heading = self.browser.find_element_by_id("Problem")
        self.assertIn('Problem', problem_heading.text)
        healthy_heading = self.browser.find_element_by_id("Healthy")
        self.assertIn('Healthy', healthy_heading.text)

	# She looks for http://www.gov.za, but doesn't see it on the list. She wonders
        # if there is a way to submit sites for inclusion in the monitoring list.
        # Fortunately, she sees that there is a link for submitting a website
        submit_link = self.browser.find_element_by_link_text("Submit a Website for Monitoring")
        # She clicks the link
        submit_link.click()

        # She is taken to a page with a title mentioning submitting a website.
        # She reads throught the terms and conditions.
        target_string = "Submit"
        self.assertIn(target_string, self.browser.title)

        # She's happy with the terms and conditions so she starts filling out the form.
        # She fills out the url and hits enter
        url_field = self.browser.find_element_by_id("id_url")
        site_name_field = self.browser.find_element_by_id("id_site_name")
        responsible_account_field = self.browser.find_element_by_id("id_responsible_account")
        url_field.send_keys("http://www.gov.za")
        site_name_field.send_keys("South African Government")
        responsible_account_field.send_keys("Somone")
        responsible_account_field.send_keys(Keys.ENTER)

        # She is taken to a page thanking her for her submission.
        target_string = "Thank You"
        title = self.browser.title
        self.assertIn(target_string, title)

        # Ursula is satisfied that she has done her job and leaves the site.

if __name__ == '__main__':
    unittest.main()
