import streamlit as st
import st_tailwind as tw
import folium
from streamlit_folium import folium_static
from utils.api_client import api_client
import pandas as pd
from components.train_model import predict_holiday_type

def get_itinerary(group, season):
    itineraries = {
        "Nature": {
            "Summer": {
                "title": "Nature - Summer Itinerary",
                "destinations": [
                    {
                        "name": "Verbier",
                        "activities": ["Hiking the Mont Fort Trail", "Mountain Biking", "Paragliding"],
                        "latitude": 46.0961,
                        "longitude": 7.2266
                    },
                    {
                        "name": "Zermatt",
                        "activities": ["Five Lakes Walk", "Gornergrat Railway", "Village Exploration"],
                        "latitude": 46.0207,
                        "longitude": 7.7491
                    },
                    {
                        "name": "Interlaken",
                        "activities": ["Paragliding", "Lake Thun Cruise", "Hiking to Harder Kulm"],
                        "latitude": 46.6863,
                        "longitude": 7.8632
                    }
                ]
            },
            "Winter": {
                "title": "Nature - Winter Itinerary",
                "destinations": [
                    {
                        "name": "Verbier",
                        "activities": ["Skiing (4 Vallées)", "Snowshoeing", "Dog sledding"],
                        "latitude": 46.0961,
                        "longitude": 7.2266
                    },
                    {
                        "name": "Zermatt",
                        "activities": ["Skiing/Snowboarding", "Gornergrat Railway", "Ice Skating"],
                        "latitude": 46.0207,
                        "longitude": 7.7491
                    },
                    {
                        "name": "Interlaken",
                        "activities": ["Sledding", "Snowshoe Tours", "Winter Kayaking"],
                        "latitude": 46.6863,
                        "longitude": 7.8632
                    }
                ]
            }
        },
        "Relax": {
            "title": "Relax Itinerary",
            "destinations": [
                {
                    "name": "Lucerne",
                    "activities": ["Chapel Bridge", "Mount Pilatus Excursion", "Lake Lucerne Cruise"],
                    "latitude": 47.0502,
                    "longitude": 8.3093
                },
                {
                    "name": "Weggis",
                    "activities": ["Rigi Kaltbad Thermal Baths", "Easy hiking trails", "Lakeside dining"],
                    "latitude": 47.0331,
                    "longitude": 8.4333
                },
                {
                    "name": "Vitznau",
                    "activities": ["Mount Rigi cogwheel train", "Paddleboarding", "Outdoor concerts"],
                    "latitude": 47.00987200738584,
                    "longitude": 8.484811962790728
                }
            ]
        },
        "City": {
            "title": "City Itinerary",
            "destinations": [
                {
                    "name": "Geneva",
                    "activities": ["Jet d'Eau Fountain", "Old Town Walk", "Patek Philippe Museum"],
                    "latitude": 46.2044,
                    "longitude": 6.1432
                },
                {
                    "name": "Bern",
                    "activities": ["Zytglogge Clock Tower", "Bear Park", "Rose Garden"],
                    "latitude": 46.9480,
                    "longitude": 7.4474
                },
                {
                    "name": "Zurich",
                    "activities": ["Altstadt", "Lake Zurich Promenade", "Kunsthaus Art Museum"],
                    "latitude": 47.3769,
                    "longitude": 8.5417
                }
            ]
        }
    }
    # Only Nature group has seasonal variations
    if group == "Nature":
        return itineraries[group][season]
    return itineraries[group]

def get_icon_for_transport(transport):
    """Return appropriate icon for transport type"""
    icons = {
        "Reachable by train": "🚂",
        "Reachable by car": "🚗",
        "Reachable by bus": "🚌",
        "Reachable by boat": "⛴️",
        "Reachable by local bus": "🚌",
    }
    return icons.get(transport, "🚶")

def get_icon_for_place_type(place_type):
    """Return appropriate icon for place type"""
    icons = {
        "Villages": "🏘️",
        "Mountains": "⛰️",
        "Mountain Lakes": "🏞️",
        "Regions": "🗺️",
    }
    return icons.get(place_type, "📍")

def create_itinerary_map(destinations):
    """Create a map showing the itinerary destinations"""
    # Get coordinates for all destinations
    locations = []
    for dest in destinations:
            locations.append({
                'name': dest['name'],
                'lat': dest['latitude'],
                'lon': dest['longitude']
            })
    
    if not locations:
        return None
    
    # Create map centered on the first location
    m = folium.Map(
        location=[locations[0]['lat'], locations[0]['lon']],
        zoom_start=8
    )
    
    # Add markers for each location
    for i, loc in enumerate(locations):
        if loc['lat'] and loc['lon']:
            # Add marker with number
            folium.Marker(
                [loc['lat'], loc['lon']],
                popup=f"{i+1}. {loc['name']}",
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 12pt; color: white; background-color: #1E90FF; border-radius: 50%; width: 30px; height: 30px; display: flex; justify-content: center; align-items: center;">{i+1}</div>'
                )
            ).add_to(m)
    
    # Add lines connecting the locations
    if len(locations) > 1:
        points = [[loc['lat'], loc['lon']] for loc in locations if loc['lat'] and loc['lon']]
        folium.PolyLine(
            points,
            color='#1E90FF',
            weight=2,
            opacity=0.8
        ).add_to(m)
    
    return m

def display_destination_info(destination_name):
    """Display additional information about a destination from the API"""
    info = api_client.get_destination_info(destination_name)
    
    if info:
        st.subheader("Additional Information")
        
        # Display basic information
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(info['abstract'])
        with col2:
            if info['photo']:
                st.image(info['photo'], caption=destination_name)
        
        # Display selected classifications
        if info['classifications']:
            st.subheader("Key Information")
            
            # Create columns for the information
            col1, col2, col3 = st.columns(3)
            
            # Display distance to airport
            with col1:
                st.markdown("### ✈️ Airport Distance")
                if 'distancetoairport' in info['classifications']:
                    st.write(info['classifications']['distancetoairport'][0])
                else:
                    st.write("Not specified")
            
            # Display transport options
            with col2:
                st.markdown("### 🚌 Transport Options")
                if 'reachability' in info['classifications']:
                    for transport in info['classifications']['reachability']:
                        st.write(f"{get_icon_for_transport(transport)} {transport}")
                else:
                    st.write("Not specified")
            
            # Display place type
            with col3:
                st.markdown("### 📍 Place Type")
                if 'placetypes' in info['classifications']:
                    for place_type in info['classifications']['placetypes']:
                        st.write(f"{get_icon_for_place_type(place_type)} {place_type}")
                else:
                    st.write("Not specified")
        
        # Display link to official website
        if info['url']:
            st.markdown(f"[Visit official website]({info['url']})")
    else:
        st.info("No additional information available for this destination.")

def main():
    st.title("🇨🇭 Your Personalized Swiss Itinerary")
    st.markdown(
        "<h3 style='color:#1E90FF;'>Discover your perfect Swiss adventure, tailored just for you!</h3>",
        unsafe_allow_html=True,
    )

    if 'quiz_answers' not in st.session_state:
        st.error("Please complete the quiz first!")
        if tw.button("Go to Quiz", classes="bg-blue-500 text-white px-4 py-2 rounded"):
            st.switch_page("pages/2_Quiz.py")
        return

    answers = st.session_state.quiz_answers
    input_data = pd.DataFrame([answers])

    predicted_label, predicted_probability, class_probabilities = predict_holiday_type(input_data)

    # Stylish summary card
    st.markdown(
        f"""
        <div style="background: linear-gradient(90deg, #1E90FF 60%, #87CEFA 100%); 
                    border-radius: 12px; padding: 1.5rem 2rem; color: white; margin-bottom: 1.5rem;">
            <h2 style="margin-bottom:0.5rem;">✨ Recommended Holiday Type: <b>{predicted_label}</b></h2>
            <p style="margin:0;">Confidence: <b>{predicted_probability:.0%}</b></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Class probabilities as a horizontal bar chart
    st.markdown("#### Model Confidence for Each Holiday Type")
    st.bar_chart(pd.DataFrame([class_probabilities]))

    season = answers["Are you planning a summer or winter holiday?"]
    itinerary = get_itinerary(predicted_label, season)

    st.header(f"🗺️ {itinerary['title']}")

    # Display the map in a card
    with st.container():
        st.markdown(
            "<div style='background-color:#f0f8ff; border-radius:10px; padding:1rem; margin-bottom:1.5rem;'>"
            "<h3 style='margin-top:0;'>Your Itinerary Map</h3>",
            unsafe_allow_html=True,
        )
        map_obj = create_itinerary_map(itinerary["destinations"])
        if map_obj:
            folium_static(map_obj)
        else:
            st.info("Map data not available for all destinations.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("Destinations & Activities")
    for idx, destination in enumerate(itinerary["destinations"], 1):
        with st.expander(f"**{idx}. {destination['name']}**", expanded=(idx == 1)):
            st.markdown(
                "<ul style='margin-bottom:1rem;'>"
                + "".join([f"<li style='font-size:1.1em;'> {activity}</li>" for activity in destination["activities"]])
                + "</ul>",
                unsafe_allow_html=True,
            )
            if st.button(f"Show more about {destination['name']}", key=f"btn_{destination['name']}"):
                display_destination_info(destination["name"])

    # Navigation buttons
    with tw.container(classes="flex justify-between mt-8"):
        if tw.button("⬅️ Back to Quiz", classes="bg-gray-200 text-gray-800 px-4 py-2 rounded"):
            st.switch_page("pages/2_Quiz.py")
        if tw.button("🏠 Back to Home", classes="bg-blue-500 text-white px-4 py-2 rounded"):
            st.switch_page("app.py")

if __name__ == "__main__":
    main()