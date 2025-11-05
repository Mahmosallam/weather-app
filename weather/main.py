from flask import Flask, jsonify, make_response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def health():
    return "The service is running", 200

@app.errorhandler(Exception)
def handle_error(error):
    response = {
        "message": "Internal server error",
        "error": str(error)
    }
    return make_response(jsonify(response), 500)

@app.route('/<city>')
def get_weather(city):
    # Check if API key exists
    api_key = os.getenv("APIKEY")
    if not api_key:
        return make_response(jsonify({"message": "API key not configured"}), 500)
    
    # Step 1: Convert city name to coordinates using geocoding
    geocode_url = "https://nominatim.openstreetmap.org/search"
    geocode_params = {"q": city, "format": "json", "limit": 1}
    geocode_headers = {"User-Agent": "WeatherApp/1.0"}
    
    try:
        # Get coordinates
        geo_response = requests.get(geocode_url, params=geocode_params, headers=geocode_headers, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return make_response(jsonify({"message": f"City '{city}' not found"}), 404)
        
        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]
        
        # Step 2: Get weather forecast using coordinates
        weather_url = "https://open-weather13.p.rapidapi.com/fivedaysforcast"
        querystring = {
            "latitude": latitude,
            "longitude": longitude,
            "lang": "EN"
        }
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "open-weather13.p.rapidapi.com"
        }
        
        weather_response = requests.get(weather_url, headers=headers, params=querystring, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        return jsonify(weather_data)
    
    except requests.exceptions.Timeout:
        return make_response(jsonify({"message": "Request timeout"}), 504)
    
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code if e.response else 500
        if status_code == 401 or status_code == 403:
            return make_response(jsonify({"message": "API authentication failed. Check your API key."}), 401)
        else:
            return make_response(jsonify({
                "message": "API error",
                "error": str(e),
                "status_code": status_code
            }), 502)
    
    except requests.exceptions.RequestException as e:
        return make_response(jsonify({"message": "Request error", "error": str(e)}), 500)
    
    except ValueError as e:
        return make_response(jsonify({"message": "Invalid JSON response", "error": str(e)}), 502)
    
    except Exception as e:
        return make_response(jsonify({"message": "Unexpected error", "error": str(e)}), 500)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=False)