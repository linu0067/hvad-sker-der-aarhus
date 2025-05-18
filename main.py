import streamlit as st
from streamlit_folium import st_folium
import folium
from utils import create_ics, people_icon

# Dummydata
events = [
    {
        "title": "Street Food Festival",
        "lat": 56.1629,
        "lon": 10.2039,
        "start": "2025-06-15 17:00",
        "location": "Aarhus Street Food",
        "description": "Mad og musik i det fri",
        "genre": "Mad",
        "subcategory": "Festival",
        "area": "Midtbyen",
        "people": 800
    },
    {
        "title": "Yoga i Botanisk Have",
        "lat": 56.1678,
        "lon": 10.1973,
        "start": "2025-06-16 08:00",
        "location": "Botanisk Have",
        "description": "Morgenyoga for alle niveauer",
        "genre": "Krop og sind",
        "subcategory": "Workshop",
        "area": "Trøjborg",
        "people": 30
    }
]

# 🎛️ Filtrering
with st.sidebar:
    st.header("🎯 Filtrer")
    genre = st.selectbox("🎭 Genre", ["Alle"] + sorted(set(e["genre"] for e in events)))
    date = st.date_input("📅 Dato")
    show_advanced = st.checkbox("Flere filtre", value=False)

    if show_advanced:
        subcategory = st.selectbox("🧩 Underkategori", ["Alle"] + sorted(set(e["subcategory"] for e in events)))
        area = st.selectbox("📍 Område", ["Alle"] + sorted(set(e["area"] for e in events)))
        people_range = st.selectbox("👥 Antal mennesker", ["Alle", "0–20", "20–50", "50–250", "250–1000", "1000+"])
    else:
        subcategory = area = people_range = "Alle"

# 🌗 Tema toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

toggle = st.checkbox("🌙 Skift til mørkt tema" if not st.session_state.dark_mode else "🔆 Skift til lyst tema")

if toggle:
    st.session_state.dark_mode = not st.session_state.dark_mode

st.markdown(
    f"""
    <style>
        body {{
            background-color: {'#1e1e1e' if st.session_state.dark_mode else '#f3f3f3'};
            color: {'white' if st.session_state.dark_mode else 'black'};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# 🔍 Filter logik
def match(event):
    return (
        (genre == "Alle" or event["genre"] == genre)
        and (subcategory == "Alle" or event["subcategory"] == subcategory)
        and (area == "Alle" or event["area"] == area)
        and (
            people_range == "Alle" or
            (people_range == "0–20" and event["people"] < 20) or
            (people_range == "20–50" and 20 <= event["people"] < 50) or
            (people_range == "50–250" and 50 <= event["people"] < 250) or
            (people_range == "250–1000" and 250 <= event["people"] < 1000) or
            (people_range == "1000+" and event["people"] >= 1000)
        )
    )

filtered = list(filter(match, events))

# 🗺️ Kort
m = folium.Map(location=[56.1629, 10.2039], zoom_start=13)

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
