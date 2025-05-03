# Swiss Tourism Application – Project Overview

## User Flow

1. User lands on the homepage.
2. User completes a quiz (8 questions, each with 3 predefined answers).
3. Based on the user's answers, the system assigns them to one of three
   travel groups:  
   a. Nature (with subgroups: Summer or Winter)  
   b. Relax  
   c. City
4. The user is then shown a predefined itinerary (based on the group) that
   includes:  
   a. Destinations  
   b. 2–3 handpicked activities per destination
5. The user also receives an estimated weather report for each destination
   during the selected travel season/month

## Quiz Setup

- Build a quiz with 8 questions.
- Each question must offer 3 answer choices.
- At the end, the system should count how many answers point to which
  group (Nature, Relax, City) and assign the user accordingly.
- If the user selects “Winter” or “Summer,” this sub-selects the Nature
  Winter or Nature Summer itinerary.

## Quiz Questions

1. What kind of scenery do you prefer? (Mountains, Cities, Countryside)
2. Who are you traveling with? (Family, Couple, Friends)
3. What is your age group? (18–30, 30–50, 50+)
4. Preferred travel style? (Relaxation, Adventure, Culture)
5. Travel pace? (Fast-paced, Mix of both, Slow and immersive)
6. Preferred transportation? (Hiking/VTT, Private car, Public transport)
7. Evening plans? (Camping, Spa, Partying)
8. When are you planning to travel? (Spring, Summer, Fall, Winter)

Important clarification about the last quiz question ("When are you planning to
travel?"):

- This question is not used to assign the user to a group (Nature, Relax,
  City).

- It is used only for two things:

  - To determine the weather forecast: based on the selected
    season (Spring, Summer, Fall, or Winter), fetch the approximate
    weather using historical MeteoSwiss data.

  - For the Nature group only: if the user is assigned to the Nature
    group and selects Winter or Summer, it decides which version of the
    itinerary (Verbier–Zermatt–Interlaken in Summer or in Winter) to
    display.

- For users assigned to Relax or City groups, the season selection
  affects only the weather forecast, not the itinerary itself.

## Group Assignment Logic

- Assign a user to the group where they gave the most answers aligned with
  that theme.
- If "When are you planning to travel?" is Winter or Summer, use this to pick the correct Nature itinerary variant.

## Predefined Itineraries + Activities

### Group: Nature – Summer

Itinerary: Verbier – Zermatt – Interlaken  
Activities per destination:  
Verbier  
• Hiking the Mont Fort Trail  
• Mountain Biking  
• Paragliding  
Zermatt  
• Five Lakes Walk  
• Gornergrat Railway  
• Village Exploration  
Interlaken  
• Paragliding  
• Lake Thun Cruise  
• Hiking to Harder Kulm

### Group: Nature - Winter

Itinerary: Verbier – Zermatt – Interlaken  
Activities per destination:  
Verbier  
• Skiing (4 Vallées)  
• Snowshoeing  
• Dog sledding  
Zermatt  
• Skiing/Snowboarding  
• Gornergrat Railway  
• Ice Skating  
Interlaken  
• Sledding  
• Snowshoe Tours  
• Winter Kayaking

### Group Relax

Itinerary: Around Lake Lucerne — Lucerne, Weggis, Vitznau  
Lucerne  
• Chapel Bridge  
• Mount Pilatus Excursion  
• Lake Lucerne Cruise  
Weggis  
• Rigi Kaltbad Thermal Baths  
• Easy hiking trails  
• Lakeside dining  
Vitznau  
• Mount Rigi cogwheel train  
• Paddleboarding  
• Outdoor concerts

### Group City

Itinerary: Geneva – Bern – Zurich  
Geneva  
• Jet d’Eau Fountain  
• Old Town Walk  
• Patek Philippe Museum  
Bern  
• Zytglogge Clock Tower  
• Bear Park  
• Rose Garden  
Zurich  
• Altstadt  
• Lake Zurich Promenade  
• Kunsthaus Art Museum

## Weather Forecast Integration

Use the MeteoSwiss API to retrieve monthly historical weather data.  
• Apply a machine learning model to estimate probable weather
conditions (temperature range + conditions) for each destination based on
the selected season or month.  
• Display this as a compact weather summary alongside the itinerary
(e.g., "Zermatt in Winter: -4°C to 2°C, mostly snow").

Once the user receives their itinerary, display a small interactive map showing all the
destinations included.  
• Each destination should be marked with a clickable pin.  
• The route between destinations should be visually indicated (if possible) 3. → we need a map showing the different points of the itinerary
