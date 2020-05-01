This documentation is on the things that need to be revamped, not necessarily all the things that are yet to be done.

## Homepage.py
* This is the main flask file that is run that contains all the url endpoint functions
    * Since the file contains all the url endpoints, it is very overcrowded
        * Make the url endpoints imported from other file to reduce clutter

## Printers Status
* The html for this is `templates/status.html` from the root directory
* Ajax was used to make a call to the printers to pause/resume
    * Currently, ajax uses four get methods to call one of four url endpoints
        * Make one ajax function to use post method and send the printer and action that is desired
        * Change the four functions that ajax calls to one function that uses the printer and action that were sent by ajax
* Uses `<meta http-equiv="refresh" content="5">` to refresh the entire page every 5 seconds
    * It is not desireable to refresh the page to update the information
    * Change to use an ajax call to get the information and update it every so often
* Uses hidden buttons to pass text from flask to the html to javascript
    * Currently loads the button into javascript and takes the text inside the button to do comparison
    * Find a way to send the information from html to js in the function call possibly
* Possibly add video of the printers for Xerox and Gutenberg

## Request Form
* The html for this is `templates/form.html` from the root directory
* To pass things in the request object, use the `name` tag not the `id` tag
    * `id` tag is for js, requests only notices the `name` tag
* In `homepage.py` actually save the variables to the db
    * Currently the db and form do not match up on data
        * The current saving to the db was just for showing that it actually saves to the db
        * Will need to refactor both the request form and db to better reflect what needs to be captured

## Print Queue
* The html for this is `templates/queue.html` from the root directory
* Actually query the db for the prints
* Display the prints in a table
* Possibly allow active workers select a print to make their responsibility
    * This would allow people to know who to contact for their print

## Members
* The html for this is `templates/members.html` from the root directory
* Actual query the db for the active workers
* Display the active workers
* The admin page with the ability to give/remove access was a temporary one to manipulate the worker db
    * Should go to an actual page on submission, not just bring up text
    * Make more user friendly and just all around more nice to look at
