-- create database 
create database test;

-- connect database
\c test

-- create a test table
create table test_table(
    id int primary key,
    name varchar(20)
);