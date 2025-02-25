from django.shortcuts import render
import requests

def home(request):
    weather_data = None
    
    if 'location' in request.GET:
        location = request.GET['location']
        api_key = '9dc061c4433903c4a1987a2e3062bd2b'
        api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}&units=m'
        
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            
            if 'current' in data:
                weather_data = {
                    'temperature': data['current']['temperature'],
                    'description': data['current']['weather_descriptions'][0],
                    'humidity': data['current']['humidity'],
                    'icon': data['current']['weather_icons'][0]
                }
            else:
                weather_data = {'error': 'Location not found'}
                
        except requests.exceptions.RequestException as e:
            weather_data = {'error': 'Failed to connect to weather service'}         
            
    return render(request, 'weather/home.html', {'weather': weather_data} )
