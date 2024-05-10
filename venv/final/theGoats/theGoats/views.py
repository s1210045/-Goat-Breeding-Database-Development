from django.shortcuts import render
from django.http import HttpResponse
from progeny import urls
from seasons import urls
# Create your views here.
def index(request):
    links = {
        'The Progeny Report':'pindex',
        'The Seasonal Birth Cohort Report':'sindex'
        }
    descs = {
        'pindex':
        'This is a report that presents all the dams in the herd in a table\nWhen you click on a row, it will expand to display info about all of her kids',
        'sindex':
        'The Seasonal Birth Cohort report summarizes health based on birth by season.\nADG is used as the main determining factor of health'
        }
    return render(request,'theGoats/index.html',context={'links':links,'desc':descs})