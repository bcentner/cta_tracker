from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

with open("cta_tracker/resources/list_of_el_stops.json", "r") as f:
    all_stops = json.load(f)


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


if __name__ == "__main__":
    app.run()