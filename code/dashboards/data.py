import pandas as pd
from datetime import datetime
import math

def data_prep():
    df = pd.read_csv("dataset.csv")
    df[["latitude", "longitude"]] = df[["latitude", "longitude"]].round(4)
    return df

def geo_centroid():
    # calculate the center location from all geo locations
    df = data_prep()
    max_long = df["longitude"].max()
    min_long = df["longitude"].min()
    max_lat = df["latitude"].max()
    min_lat = df["latitude"].min()
    longitude = ((max_long - min_long)/2) + min_long
    latitude = ((max_lat - min_lat)/2) + min_lat
    return {'lon': longitude, 'lat': latitude}

def calc_zoom():
    # formula for setting the zoom
    df = data_prep()
    max_long = df["longitude"].max()
    min_long = df["longitude"].min()
    max_lat = df["latitude"].max()
    min_lat = df["latitude"].min()
    width_y = max_lat - min_lat
    width_x = max_long - min_long
    zoom_y = -1.446*math.log(width_y) + 7.2753
    zoom_x = -1.415*math.log(width_x) + 8.7068
    return min(round(zoom_y,2),round(zoom_x,2))
