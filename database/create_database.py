import pyscopg2
import pandas as pd


# create variables to store database connection details
db_name = 'postgres'
db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'

# connect to the database
conn = psycopg2.connect