import psycopg2
import pandas as pd
import streamlit as st

# class result
class result:
    def __init__(self, name, postcode, abn, num_of_rows, activity):
        self.name = name 
        self.postcode = postcode
        self.abn = abn
        self.num_of_rows = num_of_rows
        self.activity = activity
        self.df_result = None
        self.con = psycopg2.connect(database= 'postgres', user='postgres', password='postgres', host='localhost', port='5432')

    # define query method to create query
    def data_process(self):
        
        # connect to database (change the credentials first)
        # create cursor object to execute SQL queries
        cursor = self.con.cursor()

        # store the two tables into dataframes
        cursor.execute('select * from whs_ilab2.web_content')
        df_contents = pd.DataFrame(cursor.fetchall())

        cursor.execute('select * from whs_ilab2.abn')
        df_abn = pd.DataFrame(cursor.fetchall())

        # if the search doesn't require activity
        if self.activity == None:
            # create query without activity requirement
            for i in [self.name, self.postcode, self.abn]:
                not_empty = []
                if i != None:
                    not_empty.append(i)
            if len(not_empty) == 0:
                st.write('Please enter at least one search criteria.')
            else:
                name_str = f'name like "%{self.name}%"'
                postcode_str = f'location like "%{self.postcode}"'
                abn_str = f'abn = {self.abn}'

                reference = {}
                



                

