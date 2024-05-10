
::deleting existing database
dropdb -U postgres goats
::creatig blank copy
createdb -U lion goats
::running setup.sql on goats
psql -U lion -d goats -a -f setup.sql > dbBuildLog.txt
::activating the virtual environment (prepopulated with all necessary libraries, requires linux machine or vm)
/venv/bin/activate.psl
::navigating to the project root folder
cd venv/final/theGoats
::starting the django web server and display landing page in firefox
py -m manage runserver & start chrome 127.0.0.1:8000/    


