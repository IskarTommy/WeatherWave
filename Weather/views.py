from django.shortcuts import render
import requests
from datetime import timedelta
from django.utils import timezone
from dotenv import load_dotenv
import os
from .models import CachedWeather, Location  # Import your models

# Load environment variables
load_dotenv()

def home(request):
    weather_data = None
    
    if 'location' in request.GET:
        location_query = request.GET['location']
        
        try:
            # Try to get cached data first
            cached_data = get_weather(location_query)
            if cached_data:
                weather_data = cached_data
            else:
                # Fetch from API if no valid cache
                api_key = os.getenv('API_KEY')
                api_base_url = os.getenv('API_BASE_URL')
                api_url = f"{api_base_url}?access_key={api_key}&query={location_query}&units=m"
                
                response = requests.get(api_url)
                response.raise_for_status()
                data = response.json()
                
                if 'current' in data and 'location' in data:
                    weather_data = extract_weather_data(data)
                    save_to_cache(location_query, weather_data)
                else:
                    weather_data = {'error': 'Location not found'}
                    
        except requests.exceptions.RequestException as e:
            weather_data = {'error': 'Failed to connect to weather service'}
            
    return render(request, 'weather/home.html', {'weather': weather_data})

def get_weather(location_query):
    # Get or create Location object
    location_obj, created = Location.objects.get_or_create(
        city=location_query.split(',')[0].strip(),
        defaults={'latitude': 0, 'longitude': 0}  # Update with actual coords if available
    )
    
    cached = CachedWeather.objects.filter(
        location=location_obj,
        expires_at__gt=timezone.now()  # Fixed double underscore for field lookup
    ).first()
    
    return cached.data if cached else None

def extract_weather_data(data):
    return {
        'temperature': data['current']['temperature'],
        'description': data['current']['weather_descriptions'][0],
        'humidity': data['current']['humidity'],
        'icon': data['current']['weather_icons'][0],
        'wind_speed': data['current']['wind_speed'],
        'wind_degree': data['current']['wind_degree'],
        'wind_dir': data['current']['wind_dir'],
        'pressure': data['current']['pressure'],
        'lat': data['location']['lat'],
        'lon': data['location']['lon'],
        'feelslike': data['current']['feelslike'],
        'uv_index': data['current']['uv_index'],
        'visibility': data['current']['visibility'],
        'is_day': data['current']['is_day'],
        'city': data['location']['name']
    }

def save_to_cache(location_query, weather_data):
    # Get or create Location object
    location_obj, created = Location.objects.get_or_create(
        city=location_query.split(',')[0].strip(),
        defaults={
            'latitude': weather_data['lat'],
            'longitude': weather_data['lon'],
            'country': 'Unknown'  # You might want to extract this from the API response
        }
    )
    
    # Update location coordinates if they exist
    if not created:
        location_obj.latitude = weather_data['lat']
        location_obj.longitude = weather_data['lon']
        location_obj.save()
    
    # Create new cache entry
    CachedWeather.objects.create(
        location=location_obj,
        data=weather_data,
        expires_at=timezone.now() + timedelta(minutes=10)
    )