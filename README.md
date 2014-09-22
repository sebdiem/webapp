# A simple webapp

This app is a web application which enables a user to query a database column by column.

## How to?
To make it work, please:
- create a virtualenv named `flask` at the root of the project.
- install flask in this virtualenv: 
 - `. flask/bin/activate` 
 - `pip install flask` 
- create a directory webapp/resources containing the file `us-census.db`

Then run the webserver with `./run.py` from the root of the project.
The webapplication is available in a web browser at [http://localhost:5000/dataiku](http://localhost:5000/dataiku) (tested with firefox and chrome).

## Principle:
### Server side:
The webserver provides an API to access two resources:
- the list of columns in the database through `dataiku/columns`
* some statistics on a given column `column_name` through `dataiku/columns/column_name`
The server sends back the data in `json` format.
### Clien side:
The client javascript application starts by asking for the list of columns.
Then, the user can ask for statistics on a given column by selecting the column in the list.
