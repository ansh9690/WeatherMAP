import requests
from django.shortcuts import render, redirect
from .models import CityName
from .forms import CityForm
from django.contrib import messages


def home(request):
    weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&APPID=' \
                  '9c76d6ba35cba71d7887caf8aee26926'

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['city_name']
            existing_city = CityName.objects.filter(city_name=new_city).count()
            if existing_city == 0:
                r = requests.get(weather_url.format(new_city))
                results = r.json()
                if results['cod'] == 200:
                    form.save()
                else:
                    messages.error(request, "City Does Not Exist")
            else:
                messages.error(request, "City Already Exist")
        else:
            messages.success(request, "City Added Successfully")
    form = CityForm()

    all_city = CityName.objects.all()

    weather_data = []
    for city in all_city:
        r = requests.get(weather_url.format(city))
        results = r.json()
        weather_params = {
            'temperature': results['main']['temp'],
            'city': city.city_name,
            'icon': results['weather'][0]['icon'],
            'description': results['weather'][0]['description'],
        }
        weather_data.append(weather_params)
    context = {'all_cities_weather': weather_data, 'form': form}
    return render(request, 'weather/home.html', context)


def delete_city(request, city_name):
    CityName.objects.get(city_name=city_name).delete()
    return redirect('home')
