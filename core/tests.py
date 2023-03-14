from django.test import TestCase, Client
from .models import Collection
from.views import *
from django.http import HttpRequest, HttpResponse
import petl as etl
from os import path
from django.urls import reverse
from bs4 import BeautifulSoup

class CollectionTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(CollectionTestCase, cls).setUpClass()
        print("Fetching up the data")
        Index.fetch(HttpRequest())
    
    def setUp(self):
        self.client = Client()
        self.last_collection = Collection.objects.latest('date')
        
        

    def test_fetch_method(self):
        # In this method we will check basic functionailites and existance of the instances

        # We check if the result of the fetch methond (metadata) are properly saved in the DB
        self.assertEqual(len(Collection.objects.all()), 1)

        # check if it is not None
        self.assertIsNotNone( self.last_collection )

        # check if the path exists
        path.exists(self.last_collection.pathToCSV)

    def test_date_format(self):
        table = etl.fromcsv(self.last_collection.pathToCSV)
        for row in table[1:]:
            # We will just check if it is in correct format, more advanced methods can be made
            self.assertRegex(row[-1], r'^\d\d\d\d-\d\d-\d\d$')
    
    def test_homeworld_format(self):
        table = etl.fromcsv(self.last_collection.pathToCSV)
        for row in table[1:]:
            # We will just check if it is not the link, more advanced methods can be made
            self.assertNotIn(row[-2], '/')
    
    def test_index_url(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_content_index(self):
        url = reverse('index')
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(len(soup.find_all('tr')), 2) # We check if another row was properly shown in view
    
    def test_content_counter(self):
        url = reverse('counter', args=[1])
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'counter.html')
        self.assertEqual(len(soup.find_all('tr')), 0) # We check if nothing is shown at the beginning, we can not test buttons since we are on django
    
    def test_content_collection(self):
        url = reverse('collection', args=[1])
        response = self.client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'collection.html')
        self.assertEqual(len(soup.find_all('tr')), 11) # We check if nothing is shown at the beginning, we can not test buttons since we are on django

