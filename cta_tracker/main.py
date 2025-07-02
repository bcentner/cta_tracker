from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import requests
from cta_tracker.helpers import parse_xml_to_pydantic
from cta_tracker.models.eta import CTATT, ETA

app = Flask(__name__, static_folder="static", static_url_path="/cta-tracker/static")

# Additional static file route for development access
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

with open("cta_tracker/resources/list_of_el_stops.json", "r") as f:
    all_stops = json.load(f)

# TODO: make secrets class, can be part of setup
with open(".secrets", "r") as f:
    secrets = json.load(f)
    
TRAIN_API_KEY = secrets["cta"]["train"]


@app.route("/")
def main_page():
    lines = ["Pink", "Blue", "Red", "Orange", "Green"]
    return render_template("index.html", lines=lines)

@app.route("/stops/<line>")
def get_stops(line):
    line_key = {
        "Pink": "pnk",
        "Blue": "blue",
        "Red": "red",
        "Orange": "o",
        "Green": "g",
        "Brown": "brn"
    }.get(line, None)

    if line_key is None:
        return jsonify({"error": "Invalid line color"}), 400
    
    
    
    # Filter stops by selected line
    filtered_stops = [stop for stop in all_stops if stop.get(line_key, False)]
    return jsonify(filtered_stops)

@app.route("/get_estimate", methods=["GET"])
def fetch_next_train():
    stop_name = request.args.get("stop_name")
    if not stop_name:
        return jsonify({"error": "Stop name is required"}), 400

    # Match stop name with its ID
    stop = next((s for s in all_stops if s["stop_name"] == stop_name), None)
    if not stop:
        return jsonify({"error": "Stop not found"}), 404

    mapId = stop["map_id"]  # Get the stop ID
    print(f"Found stop: {mapId}")

    # Call the CTA API
    api_url = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"
    params = {
        "key": TRAIN_API_KEY,
        "mapid": mapId,
        "max": 5
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data: CTATT = parse_xml_to_pydantic(response.text)
        print(f"validated data: {data}")

        next_trains: list[ETA] = data.eta
        if not next_trains:
            return jsonify({"error": "No train arrival data available"}), 404

        time = next_trains[0].arrival_time
        return jsonify({"stop_name": stop_name, "time": time})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

# WSGI application wrapper for subdirectory deployment
class PrefixMiddleware:
    def __init__(self, app, prefix='/cta-tracker'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ.get('PATH_INFO', '').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)

# Wrap the app for subdirectory deployment
application = PrefixMiddleware(app)
@app.route('/static/<path:filename>')
def static_files_dev(filename):
    return send_from_directory(app.static_folder, filename)

# WSGI application wrapper for subdirectory deployment
class PrefixMiddleware:
    def __init__(self, app, prefix='/cta-tracker'):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):
        if environ.get('PATH_INFO', '').startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
        return self.app(environ, start_response)

# Wrap the app for subdirectory deployment
application = PrefixMiddleware(app)

if __name__ == "__main__":
    app.run()