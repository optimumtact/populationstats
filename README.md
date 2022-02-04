This project uses pandas, pymysql, click and plotly to generate a population graph for a ss13 server

## Installation
Install poetry https://python-poetry.org/docs/#installation

    cd populationstats
    poetry init
    poetry run python populationstats/script.py 

## Usage
First you need to refresh the local data from the repository

    poetry run python populationstats/script.py refresh-data --host 172.28.4.21 --user <youruser> --database <yourdatabase>

The script will prompt you for any required remaining values

Once this completes, you will have a local pickle file with the data from the database, now you can generate a graph using
    
    poetry run python populationstats/script.py generate-graph

It will open a browser window where you can examine the graph

## Command reference
```
Usage: script.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate-graph
  refresh-data


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

Usage: script.py generate-graph [OPTIONS]

Options:
  --filename TEXT  Where the database data is stored
  --help           Show this message and exit.
```