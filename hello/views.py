from django.shortcuts import render
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
@api_view(['GET'])
def hello(request):
    name = request.query_params.get('name', 'visitor')
    client_ip = request.META.get('HTTP_X_FORWARDED_FOR') 
    if client_ip:
        client_ip = client_ip.split(',')[0]  # Take the first IP in the list
    else:
        client_ip = request.META.get('REMOTE_ADDR')


    try:
        if client_ip == '127.0.0.1':
            client_ip = '8.8.8.8'

        location_url = f'https://ipapi.co/{client_ip}/json/'
        location_response = requests.get(location_url)
        location_data = location_response.json()
        if location_response.status_code != 200:
            raise Exception('Failed to get location data: ' + location_data.get('reason', 'Unknown error'))
        city = location_data.get('city', 'Unknow location')
        latitude = location_data.get('latitude')
        longitude = location_data.get('longitude')
        # if not (latitude and longitude):
        #     raise Exception('Latitude and longitude data not found')

        if latitude and longitude:
            weather_api_key = 'f5ed53f338ca46ba117cc4a0e8d8e7fa'
            weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={weather_api_key}')
            weather_data = weather_response.json()
            # if weather_response.status_code != 200:
            #     raise Exception('Failed to get weather data: ' + weather_data.get('message', 'Unknown error'))

            temperature = weather_data['main']['temp']

        else:
            temperature = 'unknown'

            
        response = {
            'client_ip': client_ip,
            'location': city,
            'greeting': f'Hello, {name}!, the temperature is {temperature} degrees celsius in {city}'
        }

        return Response(response)
    
    except Exception as e:
        error_message = str(e)
        response = {
            'Status_massage': 'Error',
            'massage': 'An error occurred: ' +  error_message, 
        }
        return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)