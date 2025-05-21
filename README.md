# Weather App with Activity Suggestions

A full-stack application that provides weather information and AI-generated activity suggestions based on weather conditions. Built with React, Flask, and OpenAI.

## Features

- Current weather conditions
- 24-hour weather forecast
- AI-generated activity suggestions based on weather
- Temperature display in both Celsius and Fahrenheit
- Responsive design with two-pane layout

## Prerequisites

- Docker and Docker Compose
- OpenWeatherMap API key
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd weather-app
```

2. Create a `.env` file in the root directory with your API keys:
```
WEATHER_API_KEY=your_openweathermap_api_key
OPENAI_API_KEY=your_openai_api_key
```

3. Build and run the containers:
```bash
docker-compose up --build
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5001

## Project Structure

```
weather-app/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env
└── README.md
```

## Development

- Backend: Flask application running on port 5001
- Frontend: React application running on port 3000
- Docker containers are connected through a custom network
- Hot-reloading enabled for development

## API Endpoints

- `GET /api/health`: Health check endpoint
- `GET /api/weather?city=<city_name>`: Get weather and activity suggestions

## Technologies Used

- Frontend:
  - React
  - CSS3
  - Docker

- Backend:
  - Flask
  - OpenAI API
  - OpenWeatherMap API
  - Docker

## License

MIT License 