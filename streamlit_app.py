import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.distance import geodesic
import plotly.express as px

st.title("CarbonCount Home")

## make a selector for two points: start and destination, choose walk, bike, bus, personal car/
## feature 2. add plane/boat for long distances -> needs checker for distance/cross-water?
## display calculated values for carbon footprint for each depending on distance
## print messages for each: walk/bike: nice, bus/car: safe travels, try to decrease CO2 
## when you can, plane/boat: have a safe trip!
## idea to select country (i.e. Europe) that makes people pay fees for driving gas cars. 

#text
st.text("CarbonCount is a web-app that estimates your carbon footprint bas"
"ed on a single instance of one-way transportation. For example, going from your "
"house to school. "
"With CarbonCount, you may select a start point, destination, and your method of travel, "
"and we will calculate an approximation of your carbon footprint. If you would like to see "
"how we do this, click the button below.")

#button-styling
st.markdown("""
    <style>"
    div.stButton > button {
        cursor: pointer !important;
    }          
    </style>
""", unsafe_allow_html = True)

#button to go to page 1
st.markdown('<div class = "button-container">', unsafe_allow_html = True)
if st.button("How It Works"):
    st.switch_page("Pages/1_How-It-Works.py")
st.markdown('</div>', unsafe_allow_html = True)

##end of day 1 work, for day 2: input google maps, format window to fit, make sure it allows for zooming in/out, scrolling, clicking(?))

st.write("Click on two points on the map: Start and End. The app will calculate the real-world distance.")

# Initialize session state for start & end points
if "points" not in st.session_state:
    st.session_state.points = []

if "show_plane" not in st.session_state:
    st.session_state.show_plane = False

# Create a Folium map centered at a default location
m = folium.Map(location=[37.7749, -122.4194], zoom_start=5)  # San Francisco as default

# Function to add markers dynamically
for point in st.session_state.points:
    folium.Marker(location=point, popup=f"Point: {point}").add_to(m)

# Capture user click event
map_data = st_folium(m, height=500, width=700)

# Process user clicks
if map_data and map_data["last_clicked"]:
    lat, lon = map_data["last_clicked"]["lat"], map_data["last_clicked"]["lng"]
    
    # Add the new point if we have less than 2 stored
    if len(st.session_state.points) < 2:
        st.session_state.points.append([lat, lon])

# Display selected points
if len(st.session_state.points) == 2:
    start, end = st.session_state.points

    st.write(f"**Start:** {start}")
    st.write(f"**End:** {end}")

    # Calculate real-world distance (Haversine formula)
    distance = geodesic(start, end).kilometers
    distancemi = geodesic(start, end).miles
    st.write(f"**Approximate Distance:** {distance:.2f} km")
    st.write(f'**Approximate Distance:** {distancemi:.2f} miles')

    caremit = round(distancemi * 411,3)
    busemit = round(distancemi * 290, 3)
    trainemit = round(distancemi * 180, 3)
    walkemit = 0
    bikeemit = 0
    planeemit = round(distancemi * 24176, 3)

    data = {
        "Walk": walkemit,
        "Bicycle": bikeemit,
        "Train": trainemit,
        "Bus": busemit,
        "Car": caremit,
    }

    modes = list(data.keys())

    emissions = list(data.values())

    fig = px.bar(
        x=emissions,
        y=modes,
        orientation = "h",
        labels={"x": "Carbon Emissions (grams CO2)", "y": "Transport Mode"},
        title=f"Carbon Emissions for {round(distancemi,4)} Miles",
        text=emissions
    )

    st.plotly_chart(fig)

    if st.button("Flying somewhere?"):
        st.session_state.show_plane = not st.session_state.show_plane

    if st.session_state.show_plane:
        data["Plane"] = planeemit

    fig = px.bar(
        x=list(data.values()),
        y=list(data.keys()),
        orientation="h",
        labels={"x": "Carbon Emissions (grams CO2)", "y": "Transport Mode"},
        title=f"Carbon Emissions for {distancemi:.2f} Miles",
        text=list(data.values())
    )

    st.plotly_chart(fig)




    # Reset button
    if st.button("Reset"):
        st.session_state.points = []

