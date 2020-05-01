import layout


def gen_map(map_data):

    return {
        "data": [{
            "type": "scattermapbox",
            "lat": list(map_data['latitude']),
            "lon": list(map_data['longitude']),
            "hoverinfo": "text",
            "hovertext": [["Name: {} <br>Age: {}".format(i, j)]
                          for i, j in zip(map_data['name'], map_data['age'])],
            "mode": "markers",
            "name": list(map_data['name']),
            "marker": {
                    "size": 6,
                    "opacity": 0.7
            }
        }],
        "layout": layout.layout_map
    }
