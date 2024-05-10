-- build tables and import the data from csv files
\i ddl.sql;
-- populate the 'season' and 'season_month' date
\i dmlDBPopulate.sql
-- create views for goats 
\i views.sql
-- create view for weaning weights
\i ww.sql
-- create view for winter weights
\i wintweight.sql
-- create psql function to convert a datetime to an integer (days since 0 ad)
\i datetoint.sql
-- exit psql
\q

