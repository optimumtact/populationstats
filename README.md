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