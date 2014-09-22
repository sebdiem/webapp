# A simple webapp

This app is a web application which enables a user to query a database column by column.
To make it work, please:
* create a virtualenv named `flask` at the root of the project.
* install flask in this virtualenv: 
** `. flask/bin/activate` 
** `pip install flask` 
* create a directory webapp/resources containing the file `us-census.db`

Then run the webserver with `./run.py` from the root of the project.
The webapplication is available in a web browser at [http://localhost:5000/dataiku](http://localhost:5000/dataiku) (tested with firefox and chrome).
