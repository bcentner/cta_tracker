import requests
import json
import os

def get_list_of_el_stops():
    resp = requests.get("https://data.cityofchicago.org/resource/8pix-ypme.json")
    data = resp.json()
    
    with open("cta_tracker/resources/list_of_el_stops.json", "w") as f:
        json.dump(data, f, indent=2)
        
get_list_of_el_stops()