# IsItUpZA
A website monitor that sends a tweet if a website is down or comes back online, and shows a list of monitored sites with current statuses.

## Project Details
### Motivation
To increase public awareness and scrutiny of South Africa's Government e-Services websites. If a website goes offline or does not function correctly, drawing public attention to this fact may help to resolve whatever issue is causing the outage. Twitter is widely used in South Africa and displaying important website outage and error related information on Twitter should allow website managers and the public at large to keep an eye on critical digital services.

### List of Features
*Public* users have access to the following

1. A home page (This implementation is online at [isitupza.gorrog.org](http://isitupza.gorrog.org)) showing a list of sites being monitored. Sites are grouped into 'offline' (unreachable), 'problem' (sending an error code), and 'healthy' lists.
  * All groupings show the last time the site was pinged
  * The 'problem' grouping shows the error code the site is returning.

2. An interface where details about a new site can be submitted.

3. A Twitter account (Our implementation uses [@IsItUpZA](https://twitter.com/IsItUpZA)) showing tweets regarding sites that are experiencing issues or that have restored service. Public users are encouraged to follow this account in Twitter so that they will be notified whenever a critical e-service goes offline or becomes 'healthy' again after experienceing issues.

In addition to the features above, *Administrators* can

1. Add, edit and remove websites from the list. In addition to the URL, the following information is stored
  * Monitoring period - How often should the site be checked?
  * Website name
  * Optional Twitter handle of a user who is responsible or interested in the status of this site. They will be '@mention'ed in any tweets relating to the site
2. Access the list of submitted sites, and add remove edit these

### Services Used:
* Each website on the list is contacted periodically at its public URL.
* Twitter's API is used to post status updates.

### Technical Details

This service consist of 2 parts

1. A website monitoring application called `site_checker`.
  * Written in Python 3
  * Runs as a Cron job according to a predefined schedule (every 5 minutes is recommended)
  * Updates the `last_status` and `last_checked` fields of the `interface_site` table for each site that is due to be checked.
  * Adds error information such as the error code, (we use `999` for completely offline) returned by the server and the error time to the `interface_error` table
  * Sends a tweet to a predefined Twitter account if a site changes status from being healthy to either offline or problem (returning any HTTP status code > `399`).
  * Sends a tweet to a predefined Twitter account if a site changes status from being either offline or problem (returning any HTTP status code > `399`) to healthy again.
  * Written for a PostgreSQL database, but can be adapted to other databases through updating the relevant SQL queries.
  * Backed by tests located at `site_checker/tests`. Run the tests from the `site_checker` directory with the command `PYTHONPATH=. python tests/functional_tests.py` (if you have multiple versions of python installed, change the command from `python` to `python3`.)

2. A web front end called `is_it_up_interface`.
  * Uses Django 1.10
  * Uses Django's stock Admin interface for interacting with the `interface_site`, `interface_error`, and `interface_submission` (used for user submitted sites tables).
  * Backed by tests located at `is_it_up_interface/functional_tests.py`. Run them with this command from the project root directory: `python is_it_up_interface/functional_tests.py` (if you have multiple versions of python installed, change the command from `python` to `python3`.)
    * Note that these tests use Selenium to drive a Firefox browser window, so you'll need Firefox installed. As of today (3/9/2016), only Firefox 46 appears to be working (on my Mac at least - the latest versions on other platforms may work).

### Credit
Written by Roger Gordon ([gorrog](http://gorrog.org)) and Landon Simmons ([landonain](https://github.com/landonain)) in August/September 2016 for the 'Demo Day' final project concluding [Rmotr.com](http://rmotr.com)'s Advanced Python class.

### Licence
This project and all code and images are licenced under the GNU GENERAL PUBLIC LICENSE Version 3. Please see LICENCE.txt for details. All supporting libraries, software and services used are licenced under their own licences.
