from django.shortcuts import redirect, render
from django.views import View
import requests
import csv
from .models import Collection
from .serializers import CollectionSerializer

from datetime import datetime
import os
import petl as etl
import json


class Index(View):
    template = 'index.html'

    def get(self, request):
        
        return render(request, self.template, {'my_list':  Collection.objects.all()})
    
    # Now, we fetch all hometowns every time, what we can do is to save it in additional CSV, and just load that file, and if we are missing some of the IDs, just load all the hometowns again
    def get_hometowns(request_link):
        hometown_dict = dict()
        while True:
            print('Calling ', request_link)
            try:
                x = requests.get(request_link).json()
            except:
                print("Request was invalid.")
            for result in x['results']:
                hometown_dict[result['url']] = result['name']
            if x['next'] != None:
                request_link = x['next']
            else:
                break
        return hometown_dict


    def fetch(request):
        print(request)
        dirname = 'CSVs'
        now_time = datetime.now()
        filename = dirname + '/' + now_time.strftime("%Y.%m.%d.%H.%M.%S")

        os.makedirs(dirname, exist_ok=True)
        link = 'https://swapi.dev/api/people'
        file =  open(filename + '.csv', 'w', newline='') 
        writer = csv.writer(file)
        # this is where we will filter what fields we will save in our CSV
        fields = ["name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "homeworld", "date"]
        writer.writerow(fields)
        hometowns = Index.get_hometowns('https://swapi.dev/api/planets/')
         

        while True:
            print('Calling', link)

            try:
                x = requests.get(link).json()
            except:
                print("Request was invalid.")

            for result in x['results']:
                writing_list = []
                for value in fields:
                    if value == 'date':
                        # datetime.strptime(date_string, format)
                        writing_list.append(datetime.strptime(result['edited'], '%Y-%m-%dT%H:%M:%S.%fZ' ).strftime('%Y-%m-%d'))
                    elif value == 'homeworld':
                        writing_list.append(hometowns[result[value]])
                    else:
                        writing_list.append(result[value])


                writer.writerow(writing_list)
            if x['next'] != None:
                link = x['next']
            else:
                break
        # if we fetched all the data properly, we save the metadata in the DB
        collection = Collection(name=now_time.strftime("%b. %d, %Y, %I:%M %p").replace("AM", "a.m.").replace("PM", "p.m."), date=now_time, pathToCSV=filename + '.csv')
        collection.save()
            
        # instead of re-directing, I could have done this part in JS using AJAX, but I wanted to have most Django-alike solution
        return redirect('index')
    
class Counter(View):
    def getCounter(request, pk):
        star_wors_collection = Collection.objects.get(id=pk)
        table1 = etl.fromcsv(star_wors_collection.pathToCSV)
        context = {'headers': table1[0], 'main_items': list(table1[1:]), 'queryLength': 10, 'json_main_items': json.dumps(list(table1[1:])), 'id': star_wors_collection.id, 'name': star_wors_collection.name}
        return render(request, 'counter.html', context=context)
    

class CollectionView(View):
    def getCollection(request, pk):
        star_wors_collection = Collection.objects.get(id=pk)
        table1 = etl.fromcsv(star_wors_collection.pathToCSV)

        context = {'headers': table1[0], 'main_items': list(table1[1:]), 'queryLength': 10, 'json_main_items': json.dumps(list(table1[1:]))}
        return render(request, 'collection.html', context=context)