from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
import openai
import json

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes with more permissive settings
CORS(app, resources={r"/*": {"origins": "*"}})

# Get API keys from environment variables
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def get_activity_suggestions(city, weather_data):
    try:
        # Create a prompt for ChatGPT
        prompt = f"""Based on the weather in {city} for the next 3 days:
        {weather_data}
        Suggest 3 places to visit for each age group, kids, teens, adults, that would be suitable for this weather. 
        Format the response as a JSON array with 'activity' and 'reason' for each suggestion.
        Example format:
        [
            {{"activity": "Go hiking", "reason": "Perfect weather for outdoor activities"}},
            {{"activity": "Visit a museum", "reason": "Good indoor activity for the weather"}}
        ]"""

        # Get response from ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel guide that suggests activities based on weather conditions. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        
        # Try to parse the response to ensure it's valid JSON
        suggestions = response.choices[0].message.content
        try:
            # If it's already a string containing JSON, parse it
            if isinstance(suggestions, str):
                json.loads(suggestions)  # Validate JSON
            return suggestions
        except json.JSONDecodeError:
            # If parsing fails, return a default format
            return json.dumps([
                {"activity": "Check local attractions", "reason": "Weather conditions are suitable for various activities"},
                {"activity": "Plan indoor activities", "reason": "Good to have backup plans for changing weather"},
                {"activity": "Explore local cuisine", "reason": "Perfect opportunity to try local restaurants"}
            ])
    except Exception as e:
        return json.dumps([
            {"activity": "Error generating suggestions", "reason": str(e)}
        ])

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    # Get current weather
    current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    current_response = requests.get(current_url)
    
    # Get 3-day forecast
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric"
    forecast_response = requests.get(forecast_url)
    
    if current_response.status_code == 200 and forecast_response.status_code == 200:
        current_data = current_response.json()
        forecast_data = forecast_response.json()
        
        # Process forecast data
        daily_forecasts = []
        for item in forecast_data['list'][:8]:  # Get next 24 hours (3-hour intervals)
            daily_forecasts.append({
                'time': item['dt_txt'],
                'temp': item['main']['temp'],
                'description': item['weather'][0]['description']
            })
        
        # Get activity suggestions
        forecast_summary = []
        for f in daily_forecasts:
            forecast_summary.append(f"{f['time']}: {f['description']}, {f['temp']}°C")
        
        weather_summary = f"Current: {current_data['weather'][0]['description']}, {current_data['main']['temp']}°C. Forecast: {', '.join(forecast_summary)}"
        suggestions = get_activity_suggestions(city, weather_summary)
        
        weather = {
            'city': city,
            'current': {
                'temperature': current_data['main']['temp'],
                'description': current_data['weather'][0]['description'],
                'humidity': current_data['main']['humidity'],
                'wind_speed': current_data['wind']['speed']
            },
            'forecast': daily_forecasts,
            'suggestions': suggestions
        }
        return jsonify(weather)
    else:
        return jsonify({'error': 'City not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
