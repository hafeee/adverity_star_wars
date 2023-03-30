# Star Wars Explorer Django application

Small Django app for fetching and displaying Star wars characters.

To run:
```
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

For testing run: 
```
python manage.py test
```

Solution will be displayed in native [Local Host link](http://127.0.0.1:8000/).

As instructed, to minimize amount of requests, we fetch all the homeworlds, than all the people, transform the data and save it in CSV. After, we send all the CSV data to frontend template where we deal with counting the data and loading more (instead of sending requests for each of those funcitonalities).

This app can also be more modularised (if needed), But, as it is really simple, I left it all in core module.
