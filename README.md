This project uses pandas, pymysql, click and plotly to generate a population graph for a ss13 server

## Installation
Install poetry https://python-poetry.org/docs/#installation

    cd populationstats
    poetry init
    poetry run python populationstats/script.py 

## Usage
First you need to refresh the local data from your servers database

    poetry run python populationstats/script.py refresh-data

The script will prompt you for any required remaining values, but you can also pass them as options

Once this completes, you will have a local pickle file with the data from the database, now you can generate a graph using
    
    poetry run python populationstats/script.py show-graph

It will open a browser window where you can examine the graph

## Command reference
```
python populationstats/script.py
Usage: script.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  refresh-data  Grab the latest connection records from your database,...
  save-graph    Crunch the local data and write to an html file for...
  show-graph    Crunch the local data and open the resulting plotly plot...


Usage: script.py refresh-data [OPTIONS]

Options:
  --host TEXT             The mariadb/mysql host address
  --user TEXT             The mariadb/mysql user name
  --password TEXT         The mariadb/mysql user password
  --database TEXT         The mariadb/mysql database
  --tablename TEXT        The database table containing your connection
                          logging
  --filename TEXT         Where the database data is stored
  --startdate [%Y-%m-%d]  The starting date from which to generate the
                          playtime statistics
  --help                  Show this message and exit.

Usage: script.py save-graph [OPTIONS]

  Crunch the local data and write to an html file for display on the web

Options:
  --filename TEXT         Where the database data is stored
  --target-filename TEXT  Where to write the html page for the plot
  --help                  Show this message and exit.

Usage: script.py show-graph [OPTIONS]

  Crunch the local data and open the resulting plotly plot in your browser

Options:
  --filename TEXT  Where the database data is stored
  --help           Show this message and exit.
```