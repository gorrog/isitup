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
        # He navigates to the site checker site and is presented with a login
        # screen.
        self.browser.get('http://localhost:8000')
        self.assertIn('Login', self.browser.title)
        
        self.fail('Finish the Test!')
    

# He enters his uername and password
# He sees that there is a list of sites that are currently being monitored

# He sees that there is a link to add a new site
# He clicks on the link

# He's taken to a page titled 'Add new' with a form inviting him to add
# details of a new site to be monitored.

# He tries to fill in the required fieds and clicks submit
# However, he fogets to put in the site URL.

# The page refreshes after submitting and an error is shown alerting him to
# his omission of the required URL field.

# He fills it in correctly this time and hits submit.
# The page refreshes and he is taken back to the list of sites. A message at
# the top of the screen advises him that his new entry has been added.

# He can see his new entry listed among the other sites in alphabetical order of
# site name

# Arnold now wants to edit the site he just put in.

# He clicks on the name of the site.
# The site detail opens up in a new page and he can edit any of the fields
# he chooses to. This time he decides to change the schedule.
# He hits submit and is taken back to the list of sites.
# A message at the top of the screeen informs him that his site has been successfully
# updated.

# Arnold decides that one of the sites does not need to be monitored any more.
# He clicks on the site that he wishes to remove and is taken to the detail of that
# site.

# He notices that there is a button that says 'Delete' at the bottom.
# He clicks the button, and is shown a confirmation screen asking if he really
# wants to delete the site.

# He clicks 'Yes' and is taken back to the list of sites.
# A message at the top of the list informs him that his site has been deleted and
# he can see that it is no longer present in the list.


if __name__ == '__main__':
    unittest.main(warnings='ignore')