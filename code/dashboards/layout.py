import keys
import data

layout_map = dict(
    autosize=True,
    height=500, # vertical px length of map
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
    title='Geo Map',
    mapbox=dict(
        accesstoken=keys.mapbox_access_token,
        style="light", # {light, dark, ...}
        center=data.geo_centroid(), # dict('lat': 50, 'lon': 4) calculated middle of dataset
        zoom=data.calc_zoom()  # how much of the map is visible, created zoom formula
    )
)
