import streamlit as st
import folium
from streamlit_folium import st_folium
from datetime import date

st.set_page_config(layout="wide")

events = [
    {
        "navn": "Rock i Parken",
        "lat": 56.162939,
        "lng": 10.203921,
        "genre": "🎵",
        "dato": "2025-06-01",
        "tid": "20:00",
        "antal": "50–250",
        "link": "https://example.com/rockiparken"
    },
    {
        "navn": "Food Festival",
        "lat": 56.155,
        "lng": 10.210,
        "genre": "🍔",
        "dato": "2025-06-02",
        "tid": "12:00",
        "antal": "1000–10000",
        "link": "https://example.com/foodfestival"
    },
    {
        "navn": "Teateraften",
        "lat": 56.162,
        "lng": 10.195,
        "genre": "🎭",
        "dato": "2025-06-03",
        "tid": "19:00",
        "antal": "250–1000",
        "link": "https://example.com/teateraften"
    }
]

col1, col2, col3 = st.columns(3)

with col1:
    valgt_dato = st.date_input("📅 Dato", value=date.today())

with col2:
    valgt_genre = st.selectbox("🎭 Genre", ["Alle"] + list(set([e["genre"] for e in events])))

with col3:
    valgt_antal = st.selectbox("👥 Antal mennesker", ["Alle", "0–20", "20–50", "50–250", "250–1000", "1000–10000", "10000+"])

filtered = []
for e in events:
    if valgt_genre != "Alle" and e["genre"] != valgt_genre:
        continue
    if valgt_antal != "Alle" and e["antal"] != valgt_antal:
        continue
    if str(valgt_dato) != e["dato"]:
        continue
    filtered.append(e)

m = folium.Map(location=[56.162939, 10.203921], zoom_start=13, control_scale=True)

for e in filtered:
    popup_html = f"""
    <b>{e['genre']} {e['navn']}</b><br>
    📅 {e['dato']} kl. {e['tid']}<br>
    👥 {e['antal']}<br>
    <a href="{e['link']}" target="_blank">Se begivenhed</a><br>
    <a href="#">📅 Tilføj til kalender</a>
    """
    folium.Marker(
        location=[e['lat'], e['lng']],
        popup=popup_html,
        icon=folium.DivIcon(html=f"<div style='font-size:24px'>{e['genre']}</div>")
    ).add_to(m)

st_folium(m, width=1200, height=700)
