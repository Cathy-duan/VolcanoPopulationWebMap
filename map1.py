import folium
import pandas

data = pandas.read_csv("Volcanoes.txt")
lat=list(data["LAT"])
lon=list(data["LON"])
elev=list(data["ELEV"])
name=list(data["NAME"])

def color_producer(elevation):
    if elevation<1000:
        return 'green'
    elif 1000<=elevation<3000:
        return 'orange'
    else:
        return 'red'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map=folium.Map(location=[33.22254,-87.52745],zoom_start=6,titles="Stamen Terrain")
fgv=folium.FeatureGroup(name="Volcanoes")
fgp=folium.FeatureGroup(name="Population")
for lt,ln,el,name in zip(lat,lon,elev,name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt,ln],popup=folium.Popup(iframe),fill_color=color_producer(el),color=color_producer(el),fill=True,fill_opacity=0.7))
    #fg.add_child(folium.Marker(location=[lt,ln],popup=folium.Popup(iframe),icon=folium.Icon(color=color_producer(el))))

fgv.add_child(folium.Marker(location=[33.22254,-87.52745],popup="Xiao",icon=folium.Icon(colo="blue")))
fgv.add_child(folium.Marker(location=[42.34098,-71.08839],popup="Cathy",icon=folium.Icon(color='pink')))

fgp.add_child(folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']< 10000000
else 'orange' if 10000000 <=x['properties']['POP2005']<20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())
map.save("Map_html_popup_advanced.html")
