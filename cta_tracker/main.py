from flask import Flask, render_template, request, jsonify
import json
import requests

app = Flask(__name__)

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

@app.route("/FAKE_ENDPOINT", methods=["GET"])
def fetch_next_train():
    stop_name = request.args.get("stop_name")
    if not stop_name:
        return jsonify({"error": "Stop name is required"}), 400

    # Match stop name with its ID
    stop = next((s for s in all_stops if s["stop_name"] == stop_name), None)
    if not stop:
        return jsonify({"error": "Stop not found"}), 404

    stpId = stop["stop_id"]  # Get the stop ID
    print(f"Found stop: {stpId}")

    # Call the CTA API
    api_url = f"http://lapi.transitchicago.com/api/1.0/ttarrivals.aspx"
    params = {
        "key": TRAIN_API_KEY,
        "stpId": stpId,
        "max": 5
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status() 
        data = response.json() 

        next_train = data.get("ctatt", {}).get("eta", [{}])[0]
        if not next_train:
            return jsonify({"error": "No train arrival data available"}), 404

        minutes = next_train.get("arrT", "Unknown") 
        return jsonify({"stop_name": stop_name, "minutes": minutes})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500


if __name__ == "__main__":
    app.run()