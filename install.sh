
#deleting existing database
dropdb goats
#creatig blank copy
createdb goats
#running setup.sql on goats
psql -U lion -d goats -a -f setup.sql > dbBuildLog.txt
#activating the virtual environment (prepopulated with all necessary libraries, requires linux machine or vm)
source venv/bin/activate
#navigating to the project root folder
cd venv/final/theGoats
#starting the django web server and display landing page in firefox
python -m manage runserver & firefox 127.0.0.1:8000/    


