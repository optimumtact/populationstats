from dataclasses import dataclass
import pymysql
import click
import plotly.express as px
import pandas as pd
import pickle
from datetime import datetime
from dateutil.relativedelta import relativedelta


@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', prompt='Host', help='The mariadb/mysql host address')
@click.option('--user', prompt='User', help='The mariadb/mysql user name')
@click.option('--password', prompt='Password', help='The mariadb/mysql user password')
@click.option('--database', prompt='Database', help='The mariadb/mysql database')
@click.option('--tablename', default='connection_log', help='The database table containing your connection logging')
@click.option('--filename', default='data.pickle', help='Where the database data is stored')
@click.option('--startdate', type=click.DateTime(formats=["%Y-%m-%d"]), default="2018-01-01", help='The starting date from which to generate the playtime statistics')
def refresh_data(host, user, password, database, tablename, filename, startdate):
    click.echo(f"Refreshing local data from database, starting from {startdate}")
    connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database)
    with connection:
        with connection.cursor() as cursor:
            sql = f'''
                WITH login_log AS
                (
                    SELECT distinct(ckey), TIMESTAMPDIFF(MONTH, '{startdate.strftime("%Y-%m-%d")}', DATETIME) AS login_month
                    FROM {tablename}
                    GROUP BY 1,2
                    ORDER BY 1,2
                ),
                time_lapse AS
                (
                SELECT ckey, login_month, LAG(login_month, 1) over (PARTITION BY ckey ORDER BY ckey, login_month) AS Lag
                FROM login_log
                ),
                time_diff_calc AS
                (
                SELECT ckey, login_month, Lag, login_month - Lag AS time_diff
                FROM time_lapse
                ),
                player_categorized AS
                (
                SELECT  ckey,
                        login_month,
                        CASE 
                            WHEN time_diff = 1 THEN 'retained'
                            WHEN time_diff > 1 THEN 'returning'
                            WHEN time_diff IS NULL then 'new'
                        END AS player_type
                FROM time_diff_calc
                )
                SELECT login_month, player_type, COUNT(ckey)
                FROM player_categorized
                GROUP BY 1, 2
                '''
            cursor.execute(sql)
            result = cursor.fetchall()
            data = {
                "results":result,
                "startdate":startdate
            }
            with open(filename, 'wb') as f:
                pickle.dump(data, f)
@cli.command()
@click.option('--filename', default='data.pickle', help='Where the database data is stored')
def generate_graph(filename):
    with open(filename, 'rb') as f:  # Python 3: open(..., 'rb')
        data = pickle.load(f)
    startdate = data['startdate']
    result = data['results']
    
    #graph calculation
    data = pd.DataFrame.from_records(result, columns = ['Month', 'Series', 'Data'])
    totals = data.groupby(by="Month")["Data"].sum()
    for month, total in totals.iteritems():
        data.loc[len(data.index)] = [month, 'Total', total]
    data["Date"] = data.apply(calculate_date, 1, args=[startdate])
    fig = px.line(data, x="Date", y="Data", color="Series")
    
    fig.show()

def calculate_date(row, startdate):
    return startdate + relativedelta(months=row.Month)

if __name__ == '__main__':
    cli()
