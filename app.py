from flask import Flask
import pandas as pd
import geocoder
import folium
from folium import Map, Marker
from google.cloud import bigquery

bigquery_Client = bigquery.Client.from_service_account_json('/root/bus_project/bus_app/midyear-cursor-371415-a5bbee084fb8 copy.json')

selectQuery = """SELECT * FROM midyear-cursor-371415.bus_dataset.bus_pos_w_incident"""
df = bigquery_Client.query(selectQuery).to_dataframe()

def bus_pos_extract():
    selectQuery = """SELECT * FROM midyear-cursor-371415.bus_dataset.bus_pos_w_incident"""
    df = bigquery_Client.query(selectQuery).to_dataframe()
    def coordinate_split(coordiante_value):
        return coordiante_value.split(' ')
    df['bus_coordinate'] = df['bus_coordinate'].apply(coordinate_split)
    return df

app = Flask(__name__)

@app.route("/")
def home():
    location = 'Union Station, Washington, DC'
    loc = geocoder.osm(location)
    latlng = [loc.lat, loc.lng]
    bus_map = Map(location=latlng,
                zoom_start=13)
    bus_map.add_child(Marker(location=latlng, popup=loc.address, icon = folium.Icon(color = 'blue')))
    df = bus_pos_extract()
    for i in range(df.shape[0]):
        if df['is_bus_impacted'][i] == 'False':
            folium.features.RegularPolygonMarker(location = [df['bus_coordinate'][i][0], df['bus_coordinate'][i][1]],
                                                # popup = 'Route %s to %s' % (df['RouteID'], df['TripHeadsign']),
                                                fill_color='#38b516',
                                                number_of_sides = 10,
                                                radius = 3,
                                                weight = 1,
                                                fill_opacity = 0.8).add_to(bus_map)
        else :
            folium.features.RegularPolygonMarker(location = [df['bus_coordinate'][i][0], df['bus_coordinate'][i][1]],
                                                # popup = 'Route %s to %s' % (df['RouteID'], df['TripHeadsign']),
                                                number_of_sides = 3,
                                                fill_color='#eb0202',
                                                radius = 8,
                                                weight = 1,
                                                fill_opacity = 0.8).add_to(bus_map)
        
    return bus_map._repr_html_()

if __name__ == "__main__":
    app.run()