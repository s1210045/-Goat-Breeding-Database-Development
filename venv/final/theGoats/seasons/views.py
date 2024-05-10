from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
from psycopg2 import extras
# Create your views here.
def index(request):
    #connect to database, change user and password to match your postgres database credentials
    connection = psycopg2.connect(database="goats", user="lion", password="lion", host="localhost", port=5432)
    curr = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    # building queries

    #building births by month
    q = 'select month::integer as month, count from bbm;'
    curr.execute(q)
    bbm = curr.fetchall()
    # bbm = {birth month:count}
    bbm = {b[0]:b[1] for b in bbm}
    #calculate adg by animal (first dams, then kids, then union of the two results)
    q = 'create or replace view maxweight as select animal_id, when_measured, max(alpha_value) as max_weight from weight group by animal_id, when_measured order by animal_id;'
    curr.execute(q)
    q = "Create or replace view adgd as SELECT mw.animal_id, ((cast(mw.max_weight as double precision) - cast(coalesce(g.birth_weight, '0') as double precision)) / (datetoint(mw.when_measured)- datetoint(g.dob))) AS adg, g.dob FROM maxweight as mw inner join damwbw as g on g.animal_id = mw.animal_id;"
    curr.execute(q)
    q = "Create or replace view adgk as SELECT mw.animal_id, ((cast(mw.max_weight as double precision) - cast(coalesce(g.birth_weight, '0') as double precision)) / (datetoint(mw.when_measured)- datetoint(g.dob))) AS adg, g.dob FROM maxweight as mw inner join kidwbw as g on g.animal_id = mw.animal_id;"
    curr.execute(q)
    q = 'Create or replace view adg as select * from adgd UNION select * from adgk;'
    curr.execute(q)
    #get the by month average adg
    q = 'create or replace view adgbymonth as select extract(month from dob) as month, avg(adg) as adg from adg group by month;'
    curr.execute(q)
    q = 'create or replace view adgbymonthse as select s.season, a.month, a.adg from adgbymonth as a inner join season_month as s on a.month = s.month;'
    curr.execute(q)
    q = 'create or replace view adgsnm as select s.seasonname, a.month, a.adg from adgbymonthse as a inner join season as s on a.season = s.season;'
    curr.execute(q)
    q = "select * from adgsnm;"
    curr.execute(q)
    m = curr.fetchall()
    m = [month for month in m]
    #get the by season average adg
    q = 'Create or replace view adgbyseason as select a.animal_id, a.adg, sm.season from adg as a inner join season_month as sm on extract(month from a.dob) = sm.month;'
    curr.execute(q)
    q = 'create or replace view withsn as select a.animal_id, a.adg, s.seasonname from adgbyseason as a natural join season as s;'
    curr.execute(q)
    q = 'Create or replace view almost as Select seasonname, avg(adg) as averageADG from withsn group by seasonname;'
    curr.execute(q)
    q = 'Select s.seasonname, a.averageADG from season as s natural join almost as a;'
    curr.execute(q)
    s = curr.fetchall()
    #manipulate season data:
    s = [season for season in s]
    for season in s:
        season.append(season[1])
        #build list of months for each season where data exists
        season[1] = [int(month[1]) for month in m if month[0] == season[0]]
        total = 0
        for month in season[1]:
            # add up births in season
            total += int(bbm[month])
        season.append(total)
        total = 0
    for month in m:
        #add births by month data
        month.append(bbm[month[1]])   

    context={'s':s,'m':m,'bbm':bbm }
    return render(request,'seasons/index.html',context)
# Create your views here.

