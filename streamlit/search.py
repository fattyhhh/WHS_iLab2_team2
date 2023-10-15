import psycopg2
import pandas as pd
import streamlit as st
from keyword_search import Abn_search

# class result
class Search:
    def __init__(self, name, postcode, abn, num_of_rows, activity):
        self.name = name 
        self.postcode = postcode
        self.abn = abn
        self.num_of_rows = num_of_rows
        self.activity = activity
        self.df_result = None
        self.con = psycopg2.connect(database= 'postgres', user='postgres', password='postgres', host='localhost', port='5432')

    # define query method to create query
    def get_result(self):
        
        # connect to database (change the credentials first)
        # create cursor object to execute SQL queries
        cursor = self.con.cursor()

        cursor.execute('select * from whs_ilab2.abn')
        df_abn = pd.DataFrame(cursor.fetchall())


        if self.activity == '':
            # create query 
            not_none_key = []
            for key, value in {'name': self.name, 'postcode': self.postcode, 'abn': self.abn}.items():
                
                if value != '':
                            not_none_key.append(key)
            if len(not_none_key) == 0:
                st.write('Please enter at least one search criteria.')
            else:
                name_str = f"name like '%{self.name}%'"
                postcode_str = f'postcode = {self.postcode}'
                abn_str = f"abn = '{self.abn}'"

                reference = {'name': name_str, 'postcode': postcode_str, 'abn': abn_str}

                if len(not_none_key) == 1:
                    where_clause = reference[not_none_key[0]]
                elif len(not_none_key) == 2:
                    where_clause = reference[not_none_key[0]] + ' and ' + reference[not_none_key[1]]
                else:
                    where_clause = reference[not_none_key[0]] + ' and ' + reference[not_none_key[1]] + ' and ' + reference[not_none_key[2]]
                if self.num_of_rows == '':
                    query = f'''select * from whs_ilab2.abn where {where_clause};'''

                else:
                    query = f'''select * from whs_ilab2.abn where {where_clause} limit {self.num_of_rows};'''    
                # execute query
                cursor.execute(query)
                # fetch all the results
                columns_name = [desc[0] for desc in cursor.description]
                self.df_result = pd.DataFrame(cursor.fetchall(), columns = columns_name).reset_index(drop = True)
        # if business activity is not empty
        elif self.activity != '':
            activities = list(self.activity.split(', '))
            result_1 = Abn_search(activities, df_abn)
            for i in range(len(df_abn)):
                cursor.execute('''
                insert into whs_ilab2.temp (name, website, location, postcode, abn, abn_look_up, contents, abn_content)
                values (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (result_1.iloc[i]['name'],
                 result_1.iloc[i]['website'],
                 result_1.iloc[i]['location'],
                 result_1.iloc[i]['postcode'],
                 result_1.iloc[i]['abn'],
                 result_1.iloc[i]['abn_look_up'],
                 result_1.iloc[i]['contents'],
                 result_1.iloc[i]['abn_content']))
            
            self.con.commit()

            for key, value in {'name': self.name, 'postcode': self.postcode, 'abn': self.abn}.items():
                not_none_key = []
                if value != None:
                            not_none_key.append(key)
            if len(not_none_key) == 0:
                st.write('Caution: Company Name, Postcode and Abn .')

                if self.num_of_rows == '':
                    query = f'''select * from whs_ilab2.temp;'''
                else:
                    query = f'''select * from whs_ilab2.temp limit {self.num_of_rows};'''
                # execute query
                cursor.execute(query)
                # fetch all the results
                columns = [desc[0] for desc in cursor.description]
                self.df_result = pd.DataFrame(cursor.fetchall(), columns = columns)

                     
            

            else:
                name_str = f'name like "%{self.name}%"'
                postcode_str = f'postcode = {self.postcode}'
                abn_str = f'abn = {self.abn}'

                reference = {'name': name_str, 'postcode': postcode_str, 'abn': abn_str}

                if len(not_none_key) == 1:
                    where_clause = reference[not_none_key[0]]
                elif len(not_none_key) == 2:
                    where_clause = reference[not_none_key[0]] + ' and ' + reference[not_none_key[1]]
                else:
                    where_clause = reference[not_none_key[0]] + ' and ' + reference[not_none_key[1]] + ' and ' + reference[not_none_key[2]]
                if self.num_of_rows == '':
                    query = f'''select * from whs_ilab2.temp where {where_clause};'''

                else:
                    query = f'''select * from whs_ilab2.temp where {where_clause} limit {self.num_of_rows};'''    
                # execute query
                cursor.execute(query)
                # fetch all the results
                columns = [desc[0] for desc in cursor.description]
                self.df_result = pd.DataFrame(cursor.fetchall(), columns = columns)

        # clear temp table
        cursor.execute('truncate whs_ilab2.temp;')
        self.con.commit()
        # close cursor and connection
        cursor.close()
    

            


             
            

                



                

