import psycopg2
import pandas as pd
import ast

# create variables to store database connection details
db_name = 'postgres'
db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'


# class a connector to initiate the connection to the database
class Connector:
    def __init__(self, db_name, db_user, db_password, db_host, db_port):
        self.conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

# connect to the database
conn = Connector(db_name, db_user, db_password, db_host, db_port).conn

# create cursor object to execute SQL queries
cursor = conn.cursor()

# create schema
cursor.execute('CREATE SCHEMA IF NOT EXISTS whs_ilab2;')

# drop the two tables if they already exist
cursor.execute('drop table if exists whs_ilab2.web_content;')
cursor.execute('drop table if exists whs_ilab2.abn;')

# drop the constraints if they already exist
cursor.execute('alter table if exists whs_ilab2.web_content drop constraint if exists web_content_pkey;')
cursor.execute('alter table if exists whs_ilab2.abn drop constraint if exists abn_pkey;')

# create web_content table
cursor.execute('''
    create table if not exists whs_ilab2.web_content (
               name text not null,
               website text null,
               content text null,
               sublinks text[] null,
               subcontents text null)
               ''')

# create abn table
cursor.execute('''
    create table if not exists whs_ilab2.abn (
              name text not null,
              website text null, 
              location text null,
              abn text null)
              ''')


# load data from all_text_4.xlsx into a pandas dataframe
df_contents = pd.read_excel('all_text_4.xlsx')

# change dataframe type to align with the database table
df_contents['website'] = df_contents['website'].astype(str)
df_contents['name'] = df_contents['name'].astype(str)
df_contents['text'] = df_contents['text'].astype(str)
df_contents['sublinkstext'] = df_contents['sublinkstext'].astype(str)

# load data into content table
for i in range(len(df_contents)):
    try: 
        cursor.execute('''
            insert into whs_ilab2.web_content (name, website, content, sublinks, subcontents)
            values (%s, %s, %s, %s, %s)''',
            (df_contents.iloc[i]['name'],
            df_contents.iloc[i]['website'],
            df_contents.iloc[i]['text'],
            ast.literal_eval(df_contents.iloc[i]['sublinks']),
            df_contents.iloc[i]['sublinkstext']))
    except:
        pass

# commit change 
conn.commit()
# read data from yellowpages5.xlsx into a pandas dataframe
df_abn = pd.read_excel('yellowpages5.xlsx')

# load data into abn table
for i in range(len(df_abn)):
    cursor.execute('''
        insert into whs_ilab2.abn (name, website, location, abn)
        values (%s, %s, %s, %s)''',
        (df_abn.iloc[i]['name'],
         df_abn.iloc[i]['website'],
         df_abn.iloc[i]['location'],
         df_abn.iloc[i]['abn']))

# commit change
conn.commit()

# select from the web_content table
print(cursor.execute('select * from whs_ilab2.web_content'))



# close connection
conn.close()