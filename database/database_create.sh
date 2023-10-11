# create variables to store database information 
# database name
username="postgres"
database="postgres"

# run sql file to create database
psql -U $username -d $database -a -f ~/database_create.sql