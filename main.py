import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from datetime import datetime
from utils import create_ics, people_icon

st.set_page_config(layout="wide")

# Hent begivenheder fra API
def fetch_events():
    url = "https://api.detskeriaarhus.dk/api/v2/events"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        events = []
        for item in data:
            event = {
                "title": item.get("title", "Ingen titel"),
                "lat": item.get("location", {}).get("latitude", 56.162939),
                "lon": item.get("location", {}).get("longitude", 10.203921),
                "start": item.get("start_time", "2025-06-01T20:00:00"),
                "location": item.get("location", {}).get("name", "Ukendt sted"),
                "description": item.get("description", ""),
                "genre": item.get("category", {}).get("name", "Ukendt genre"),
                "people": 100  # Placeholder, da API'et ikke angiver antal
            }
            events.append(event)
        return events
    except requests.RequestException as e:
        st.error(f"Fejl ved hentning af begivenheder: {e}")
        return []

events = fetch_events()

# Filtrering
st.sidebar.header("🎯 Filtrer")
genre = st.sidebar.selectbox("🎭 Genre", ["Alle"] + sorted(set(e["genre"] for e in events)))
date = st.sidebar.date_input("📅 Dato", datetime.today())

filtered = []
for e in events:
    event_date = datetime.fromisoformat(e["start"]).date()
    if (genre == "Alle" or e["genre"] == genre) and event_date == date:
        filtered.append(e)

# Kort
m = folium.Map(location=[56.162939, 10.203921], zoom_start=13)

for e in filtered:
    popup_html = f"""
    <b>{e['title']}</b><br>
    {e['start']}<br>
    {people_icon(e['people'])} {e['people']} personer<br>
    {e['location']}<br>
    <i>{e['description']}</i><br><br>
    <a href="/{create_ics(e)}" download>📅 Tilføj til kalender</a>
    """
    folium.Marker(
        location=[e["lat"], e["lon"]],
        tooltip=e["title"],
        popup=popup_html,
        icon=folium.DivIcon(html=f"""<div style="font-size:24px;">🎈</div>"""),
    ).add_to(m)

st.title("🗓️ Hvad sker der i Aarhus?")
st_folium(m, height=600)
