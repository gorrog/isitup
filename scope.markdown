# Demo Day Project
## Scope Document
### Project Summary
#### Team Members
Landon Simmons & Roger Gordon (Captain)
#### App Name
    Is It Up?
#### App Summary
    This app will be a websiste monitor, capable of monitoring an arbitrary number of websites, and publishing status messages to a public Twitter account. Monitoring will be periodic, and changes in status of the monitored site will result in one or more of the following actions.

    * Data about the site will be added to a data store of some kind.
    * A public tweet may be sent to a predefined account regarding the change of status.

### Project Details
#### Motivation
    To increase public awareness and scrutiny of South Africa's Government e-Services websites. If a website goes offline or does not function in some pre-defined way, drawing public attention to this fact may help to resolve whatever issue is causing the outage. Twitter is widely used in South Africa and displaying important website outage related information on Twitter should allow website managers and the public at large to keep an eye on critical digital services.

### List of Features
    * The ability for an administrator to add a website to be monitored to a list
    * The ability for an administrator to set a monitoring period for a website
    * The ability for an administrator to set a Twitter account for all website status updates to be posted to
    * The ability to show a listing of all monitored sites with current statuses to a public user.
    * Maybe: The ability for a member of the public to submit a URL to be monitored. TODO: if we go for this option, we will need to have an anti-spam solution like a captcha. Having an unprotected form is just asking for trouble...
    * Maybe: The ability for an administrator to approve or reject the URL submission.
    * Maybe: The system should email the administrator when a new URL is submitted.
    * TODO: Apart from being online/offline, what other criteria would be good to monitor and report on?

### Services to be Used
    * Each website added to the list will be contacted periodically at its public URL.
    * Twitter's API will be used to post status updates.

### Technical Details
    * The app will be hosted somewhere. TODO: Decide where. Roger has server space he pays for. Could host there
    * The app will use Flask for the admin and public interfaces. TODO: Figure out if Flask is the right choice here. I think it's a good idea since we both have experience with it, but I wonder how much time could be saved if we used the ORM in Django rather than writing SQL queires all the time. We could also investigate useing SQL Alchemy with Flask which may save time.
    * The app will store data somewhere. TODO: Figure out what the best choice here is. Again, Roger has access to various databases that can run on his hosted space.
    * In addition to the web interface, the app will have a constantly running Python script that does the checking of the sites. TODO: Figure out how to do this and see if this is going to be impossibly hard or not. This is the biggest unknown in the project since everything else has been at least touched on in the Rmotr course. There is something called a 'cron' job. Perhaps this can be set to automatically run a Python program.
    * If possible, it would be excellent to use Test Driven Development for this app. At the very least, having a user story will be good for defining our exact functions, even if we don't use it for functional tests.
    * Documentation will be handled by Landon? Roger? Both?
    * The app will be manually deployed somewhere unless we learn how to automatically deploy it. If hosting it on Roger's hosting provider, will automatic deployment even be possible?
    * The code will be open-sourece and will live on one (or both) of our Github accounts. Anyone will be welcome to copy and use the code.
    * The code will be licenced under the ??? licence.
