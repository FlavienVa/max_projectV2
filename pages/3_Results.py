import streamlit as st
import st_tailwind as tw
import folium
from streamlit_folium import folium_static
from components.quiz_questions import QUIZ_QUESTIONS
from utils.api_client import api_client

def calculate_group(answers):
    scores = {"Nature": 0, "Relax": 0, "City": 0}
    
    for i, answer in answers.items():
        question = QUIZ_QUESTIONS[i]
        weights = question['weights'][answer]
        for group, weight in weights.items():
            scores[group] += weight
    
    # Get the group with highest score
    return max(scores.items(), key=lambda x: x[1])[0]

def get_itinerary(group, season):
    itineraries = {
        "Nature": {
            "Summer": {
                "title": "Nature - Summer Itinerary",
                "destinations": [
                    {
                        "name": "Verbier",
                        "activities": ["Hiking the Mont Fort Trail", "Mountain Biking", "Paragliding"]
                    },
                    {
                        "name": "Zermatt",
                        "activities": ["Five Lakes Walk", "Gornergrat Railway", "Village Exploration"]
                    },
                    {
                        "name": "Interlaken",
                        "activities": ["Paragliding", "Lake Thun Cruise", "Hiking to Harder Kulm"]
                    }
                ]
            },
            "Winter": {
                "title": "Nature - Winter Itinerary",
                "destinations": [
                    {
                        "name": "Verbier",
                        "activities": ["Skiing (4 Vallées)", "Snowshoeing", "Dog sledding"]
                    },
                    {
                        "name": "Zermatt",
                        "activities": ["Skiing/Snowboarding", "Gornergrat Railway", "Ice Skating"]
                    },
                    {
                        "name": "Interlaken",
                        "activities": ["Sledding", "Snowshoe Tours", "Winter Kayaking"]
                    }
                ]
            }
        },
        "Relax": {
            "title": "Relax Itinerary",
            "destinations": [
                {
                    "name": "Lucerne",
                    "activities": ["Chapel Bridge", "Mount Pilatus Excursion", "Lake Lucerne Cruise"]
                },
                {
                    "name": "Weggis",
                    "activities": ["Rigi Kaltbad Thermal Baths", "Easy hiking trails", "Lakeside dining"]
                },
                {
                    "name": "Vitznau",
                    "activities": ["Mount Rigi cogwheel train", "Paddleboarding", "Outdoor concerts"]
                }
            ]
        },
        "City": {
            "title": "City Itinerary",
            "destinations": [
                {
                    "name": "Geneva",
                    "activities": ["Jet d'Eau Fountain", "Old Town Walk", "Patek Philippe Museum"]
                },
                {
                    "name": "Bern",
                    "activities": ["Zytglogge Clock Tower", "Bear Park", "Rose Garden"]
                },
                {
                    "name": "Zurich",
                    "activities": ["Altstadt", "Lake Zurich Promenade", "Kunsthaus Art Museum"]
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
        info = api_client.get_destination_info(dest['name'])
        if info and 'geo' in info:
            locations.append({
                'name': dest['name'],
                'lat': info['geo'].get('latitude'),
                'lon': info['geo'].get('longitude')
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
    st.title("Your Personalized Swiss Itinerary")
    
    if 'quiz_answers' not in st.session_state:
        st.error("Please complete the quiz first!")
        if tw.button("Go to Quiz", classes="bg-blue-500 text-white px-4 py-2 rounded"):
            st.switch_page("pages/2_Quiz.py")
        return
    
    # Get user's answers and calculate group
    answers = st.session_state.quiz_answers
    group = calculate_group(answers)
    
    # Get season from the last question
    season = answers[len(QUIZ_QUESTIONS)-1]
    
    # Get itinerary based on group and season
    itinerary = get_itinerary(group, season)
    
    # Display results
    st.header(itinerary["title"])
    
    # Display the map
    st.subheader("Your Itinerary Map")
    map_obj = create_itinerary_map(itinerary["destinations"])
    if map_obj:
        folium_static(map_obj)
    else:
        st.info("Map data not available for all destinations.")
    
    # Display destinations and activities
    for destination in itinerary["destinations"]:
        with st.expander(f"📍 {destination['name']}"):
            st.write("Activities:")
            for activity in destination["activities"]:
                st.write(f"• {activity}")
            
            # Add a button to show more information
            if st.button(f"Show more about {destination['name']}", key=f"btn_{destination['name']}"):
                display_destination_info(destination["name"])
    
    # Navigation buttons
    with tw.container(classes="flex justify-between mt-8"):
        if tw.button("Back to Quiz", classes="bg-gray-200 text-gray-800 px-4 py-2 rounded"):
            st.switch_page("pages/2_Quiz.py")
        if tw.button("Back to Home", classes="bg-blue-500 text-white px-4 py-2 rounded"):
            st.switch_page("app.py")

if __name__ == "__main__":
    main() 