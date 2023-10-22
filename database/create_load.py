import psycopg2
import pandas as pd


# create variables to store database connection details
db_name = 'postgres'
db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'

# connect to the database
conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
# create cursor object to execute SQL queries
cursor = conn.cursor()

# create schema
cursor.execute('CREATE SCHEMA IF NOT EXISTS whs_ilab2;')

# drop the two tables if they already exist
cursor.execute('drop table if exists whs_ilab2.web_content;')
cursor.execute('drop table if exists whs_ilab2.abn;')

# create temp table
cursor.execute('''
    create table if not exists whs_ilab2.temp (
               name text not null,
               website text null,
               location text null,
               postcode int null,
               detail_url text null,
               abn text null,
               abn_look_up text null,
               contents text null,
               abn_content text null)
               ''')

# create abn table
cursor.execute('''
    create table if not exists whs_ilab2.abn (
                name text not null,
                website text null, 
                location text null,
                detail_url text null,
                abn text null,
                abn_look_up text null,
                contents text null,
                postcode int null,
                abn_website text null)
              ''')

# read data from yellowpages5.xlsx into a pandas dataframe
df_abn = pd.read_excel('construction_data.xlsx')

# load data into abn table
for i in range(len(df_abn)):
    cursor.execute('''
        insert into whs_ilab2.abn (name, website, location, detail_url, abn, abn_look_up, contents, postcode, abn_website)
        values (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        (df_abn.iloc[i]['name'],
         df_abn.iloc[i]['website'],
         df_abn.iloc[i]['location'],
         df_abn.iloc[i]['detail_url'],
         df_abn.iloc[i]['abn'],
         df_abn.iloc[i]['abn_look_up'],
         df_abn.iloc[i]['contents'],
         df_abn.iloc[i]['postcode'],
         df_abn.iloc[i]['abn_website']))
         


# commit change
conn.commit()



# close connection
conn.close()