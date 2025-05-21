import React, { useState } from 'react';
import './Weather.css';

const Weather = () => {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchWeather = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      console.log('Fetching from:', process.env.REACT_APP_API_URL || 'http://localhost:5001');
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:5001'}/api/weather?city=${encodeURIComponent(city)}`);
      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Received data:', data);
      
      // Parse the suggestions if they're in JSON format
      try {
        if (typeof data.suggestions === 'string') {
          data.suggestions = JSON.parse(data.suggestions);
        }
      } catch (e) {
        console.log('Suggestions are not in JSON format');
      }
      setWeather(data);
    } catch (err) {
      console.error('Error details:', err);
      setError(err.message || 'Failed to connect to the server');
    } finally {
      setLoading(false);
    }
  };

  const renderSuggestions = (suggestions) => {
    if (!suggestions) return null;
    
    try {
      // If suggestions is a string, try to parse it as JSON
      const parsedSuggestions = typeof suggestions === 'string' ? JSON.parse(suggestions) : suggestions;
      
      if (Array.isArray(parsedSuggestions)) {
        return (
          <div className="suggestions-list">
            {parsedSuggestions.map((suggestion, index) => (
              <div key={index} className="suggestion-item">
                <h4>{suggestion.activity}</h4>
                <p>{suggestion.reason}</p>
              </div>
            ))}
          </div>
        );
      }
    } catch (e) {
      console.log('Error parsing suggestions:', e);
    }
    
    // Fallback to displaying as plain text
    return <p className="suggestions-content">{suggestions}</p>;
  };

  return (
    <div className="weather-container">
      <h1>Weather App</h1>
      <form onSubmit={fetchWeather} className="weather-form">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Get Activity Suggestions'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {weather && (
        <div className="weather-info">
          <div className="weather-pane">
            <h2>Weather in {weather.city}</h2>
            
            <div className="current-weather">
              <h3>Current Weather</h3>
              <div className="weather-details">
                <p>
                  Temperature: {weather.current.temperature}°C
                  <span className="fahrenheit">({Math.round(weather.current.temperature * 9/5 + 32)}°F)</span>
                </p>
                <p>Description: {weather.current.description}</p>
                <p>Humidity: {weather.current.humidity}%</p>
                <p>Wind Speed: {weather.current.wind_speed} m/s</p>
              </div>
            </div>

            <div className="forecast">
              <h3>24-Hour Forecast</h3>
              <div className="forecast-grid">
                {weather.forecast.map((forecast, index) => (
                  <div key={index} className="forecast-item">
                    <p className="time">{new Date(forecast.time).toLocaleTimeString()}</p>
                    <p className="temp">
                      {forecast.temp}°C
                      <span className="fahrenheit">({Math.round(forecast.temp * 9/5 + 32)}°F)</span>
                    </p>
                    <p className="desc">{forecast.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="activities-pane">
            <h3>Suggested Activities</h3>
            {renderSuggestions(weather.suggestions)}
          </div>
        </div>
      )}
    </div>
  );
};

export default Weather; 