from django.shortcuts import render
import os
import requests
from .models import City
from .forms import CityForm

# Create your views here.

# Get environment variables
apikey = os.getenv('API_WEATHER')


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    cities = City.objects.all()  # return all the cities in the database
    # city = 'Madrid'

    if request.method == 'POST':  # only true if form is submitted
        # add actual request data to form for processing
        form = CityForm(request.POST)
        # will validate and save if validate
        form.save()

    form = CityForm()

    weather_data = []

    for city in cities:

        # request the API data and convert the JSON to Python data types
        city_weather = requests.get(url.format(city, apikey)).json()
        # print(city_weather)

        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        # add the data for the current city into our list
        weather_data.append(weather)

    context = {'weather_data': weather_data, 'form': form}

    # returns the index.html template
    return render(request, 'weather/index.html', context)
