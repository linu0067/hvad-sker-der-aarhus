from datetime import datetime, timedelta
from ics import Calendar, Event

# ICS-generator til kalenderfil
def create_ics(event):
    c = Calendar()
    e = Event()
    e.name = event["title"]
    e.begin = datetime.strptime(event["start"], "%Y-%m-%d %H:%M")
    e.duration = timedelta(minutes=event.get("duration", 60))
    e.location = event.get("location", "Aarhus")
    e.description = event.get("description", "")
    c.events.add(e)

    filename = f'{event["title"].replace(" ", "_")}.ics'
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(c)
    return filename

# Emoji-generator til antal mennesker
def people_icon(count):
    if count < 20:
        return "👤"
    elif count < 50:
        return "👥"
    elif count < 250:
        return "🧑‍🤝‍🧑"
    elif count < 1000:
        return "👨‍👩‍👧‍👦"
    elif count < 10000:
        return "🎉"
    else:
        return "🏟️"
