from django.shortcuts import render
from django.http import HttpResponse
# from django.template import render
# Create your views here.
import psycopg2
from psycopg2 import extras
# controller for progeny report index.html
def index(request):
    #connect to database.  replace user and password to match your postgres database credentials
    connection = psycopg2.connect(database="goats", user="lion", password="lion", host="localhost", port=5432)
    cursor = connection.cursor()
    curr = connection.cursor(cursor_factory = psycopg2.extras.DictCursor)
    #building queries

    #getting sale weights
    q = 'Select * from sws order by animal_id;'
    curr.execute(q)
    sws = curr.fetchall()
    sws = {sw['animal_id']:sw for sw in sws}
    #getting dam data
    q = "Select damwbw.*, ww.alpha_value as wean_weight from damwbw left join ww on damwbw.animal_id=ww.animal_id where tag <> '' order by dob;"
    cursor.execute(q)
    dams = cursor.fetchall()
    #getting winterweight data
    winweights = {}
    q = "select animal_id, alpha_value, extract(month from when_measured), extract(year from when_measured) from winterweights order by animal_id,when_measured;"
    curr.execute(q)
    wws = curr.fetchall()
    #put winter weights into a list by animal_id
    for ww in wws:
        if not (ww[0] in winweights.keys()):
            winweights[ww[0]] = [(ww[1],ww[2],ww[3])]
        else:
            winweights[ww[0]].append((ww[1],ww[2],ww[3]))
    #filling in missing data for dams 
    damsnkids = {}
    for dam in dams:
        tmp = dam[2]
        damsnkids[tmp] =[]
        if not (dam[0] in winweights.keys()):
            winweights[dam[0]] = [('not found','n','a')]
        if not (dam[0] in sws.keys()):
            sws[dam[0]] = ['','','not sold']
    #get column headers
    colnames = [desc[0] for desc in cursor.description]

    #get kid data
    q = 'Select kidwbw.*, ww.alpha_value as wean_weight from kidwbw left join ww on kidwbw.animal_id=ww.animal_id order by dob, animal_id;'
    cursor.execute(q)
    kids = cursor.fetchall()
    #fill in missing data and append kid to it's dams list of children
    for kid in kids:
        id = kid[2]
        did = kid[4]
        if not (kid[0] in winweights.keys()):
            winweights[kid[0]] = [('not found','n','a')]
        if not (kid[0] in sws.keys()):
            sws[kid[0]] = ['','','not sold']
        if did in damsnkids.keys():
            damsnkids[did].append([x for x in kid])

    return render(request,'progeny/index.html',{'dam2':winweights,'dams':dams,'colnames':colnames,'dk':damsnkids,'sws':sws})