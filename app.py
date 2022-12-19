from flask import Flask
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import pandas as pd
from pandas import json_normalize
import numpy as np

import geocoder
import folium
from folium import Map, Marker, GeoJson, LayerControl

API_KEY = 'e13626d03d8e4c03ac07f95541b3091b'

def bus_pos_extract():
    headers = {
        # Request headers
        'api_key': API_KEY,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'Lat': '{number}',
        'Lon': '{number}',
        'Radius': '{number}',
    })

    conn = http.client.HTTPSConnection('api.wmata.com')
    conn.request("GET", "/Bus.svc/json/jBusPositions?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    data_str = data.decode()
    data_dict = json.loads(data_str)
    return (data_dict)

def bus_pos_transform(data_dict: dict):
    df = json_normalize(data_dict["BusPositions"])
    return(df)

app = Flask(__name__)

@app.route("/")
def home():
    location = 'Union Station, Washington, DC'
    loc = geocoder.osm(location)
    latlng = [loc.lat, loc.lng]
    bus_map = Map(location=latlng,
                zoom_start=13)
    bus_map.add_child(Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')))
    df = bus_pos_transform(bus_pos_extract())
    for i in range(df.shape[0]):
        folium.features.RegularPolygonMarker(location = [df['Lat'][i], df['Lon'][i]],
                                            popup = 'Route %s to %s' % (df['RouteID'], df['TripHeadsign']),
                                            number_of_sides = 3,
                                            radius = 10,
                                            weight = 1,
                                            fill_opacity = 0.8).add_to(bus_map)
    return bus_map._repr_html_()

if __name__ == "__main__":
    app.run()