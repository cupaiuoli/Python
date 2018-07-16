import folium
import pandas

# Generates an HTML file with a layered map. One layer marks vulcanos in the USA, 
# another discriminate country population with colors, 
# and the last one points to GooglePlex location

map = folium.Map(location=[37.422, -122.084], zoom_start=15)
fgGooglePlex = folium.FeatureGroup(name="Google Plex");
fgVolcanoes = folium.FeatureGroup(name="Vulcanoes");
fgPopulation = folium.FeatureGroup(name="Population");

fgGooglePlex.add_child(folium.Marker(location=[37.422, -122.084], popup="Mark", icon=folium.Icon(color='green')))

def colorProducer(elev):
    if elev < 1000:
        return "green"
    elif 1000 <= elev < 3000:
        return "orange"
    else:
        return "red"

data = pandas.read_csv("Volcanoes_USA.csv")
lons = data["LON"]
lats = data["LAT"]
names = data["NAME"]
elevs = data["ELEV"]

for lat, lon, elev, name in zip(lats, lons, elevs, names):
    popup = folium.Popup(name + " - " + str(elev) + "mts", parse_html=True)
    fgVolcanoes.add_child(folium.CircleMarker(location=[lat, lon], popup=popup, fill_color=colorProducer(elev), color=colorProducer(elev), fill_opacity=0.7))

fgPopulation.add_child(folium.GeoJson(data=(open('world.json', 'r', encoding='utf-8-sig').read()),
style_function = lambda x: {'fillColor':'green' if x["properties"]['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgVolcanoes)
map.add_child(fgPopulation)
map.add_child(fgGooglePlex)

map.add_child(folium.LayerControl())

map.save("generatedMap.html")
