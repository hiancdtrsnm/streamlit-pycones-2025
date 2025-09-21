import streamlit as st
import requests
from datetime import datetime
import pytz

st.title("📅 Horario PyConES 2025")


@st.cache_data
def fetch_schedule():
    """Fetch schedule data from PyConES API"""
    try:
        response = requests.get(
            "https://pretalx.com/pycones-2025/schedule/v/0.3/widgets/schedule.json"
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error al cargar el horario: {e}")
        return None


data = fetch_schedule()

if data and "talks" in data:
    talks = data["talks"]

    # Filter talks that have a 'code' field (actual talks, not registration/breaks)
    actual_talks = [talk for talk in talks if "code" in talk and talk.get("code")]

    # Group talks by date
    talks_by_date = {}
    for talk in actual_talks:
        if "start" in talk:
            # Parse the start time
            start_time = datetime.fromisoformat(talk["start"].replace("Z", "+00:00"))
            # Convert to Madrid timezone for display
            madrid_tz = pytz.timezone("Europe/Madrid")
            start_time_madrid = start_time.astimezone(madrid_tz)
            date_key = start_time_madrid.strftime("%Y-%m-%d")

            if date_key not in talks_by_date:
                talks_by_date[date_key] = []
            talks_by_date[date_key].append(talk)

    # Display talks grouped by date
    for date, day_talks in sorted(talks_by_date.items()):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        st.subheader(f"📆 {date_obj.strftime('%A, %d de %B de %Y')}")

        # Sort talks by start time
        day_talks.sort(key=lambda x: x.get("start", ""))

        for talk in day_talks:
            with st.expander(f"🎤 {talk.get('title', 'Sin título')}"):
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.write("**Detalles:**")
                    if "start" in talk:
                        start_time = datetime.fromisoformat(
                            talk["start"].replace("Z", "+00:00")
                        )
                        madrid_tz = pytz.timezone("Europe/Madrid")
                        start_time_madrid = start_time_madrid = start_time.astimezone(
                            madrid_tz
                        )
                        st.write(f"⏰ **Hora:** {start_time_madrid.strftime('%H:%M')}")

                    if "duration" in talk:
                        st.write(f"⏱️ **Duración:** {talk['duration']} min")

                    if "room" in talk:
                        st.write(f"🏢 **Sala:** {talk['room']}")

                    if "track" in talk:
                        st.write(f"🎯 **Track:** {talk['track']}")

                    if "code" in talk:
                        st.write(f"🔖 **Código:** {talk['code']}")

                with col2:
                    if "abstract" in talk and talk["abstract"]:
                        st.write("**Resumen:**")
                        st.write(
                            talk["abstract"][:500]
                            + ("..." if len(talk["abstract"]) > 500 else "")
                        )

                    if "speakers" in talk and talk["speakers"]:
                        st.write("**Ponentes:**")
                        for speaker in talk["speakers"]:
                            st.write(f"👤 {speaker}")
else:
    st.error("No se pudo cargar el horario. Por favor, inténtalo más tarde.")
    st.info(
        "💡 Asegúrate de tener conexión a internet para acceder a los datos del evento."
    )
