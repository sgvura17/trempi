import streamlit as st
from datetime import datetime, timedelta, date, time
import folium
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# --- IMPORTS ---
import logic 
try:
    from stations_data import my_hubs
    hub_names = sorted([item['name'] for item in my_hubs])
except ImportError:
    st.error("⚠️ שגיאה קריטית: הקובץ stations_data.py חסר.")
    my_hubs = []
    hub_names = []

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Trempi Pro", 
    page_icon="🪖", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .stTextInput > label, .stSelectbox > label, .stDateInput > label, .stTimeInput > label {
        direction: rtl;
        text-align: right;
        font-weight: bold;
        font-size: 1.1rem;
    }
    h1, h2, h3 { text-align: center; font-family: 'Segoe UI', sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 1.4rem !important; color: #007bff; }
    
    /* כפתור החלפה מעוצב */
    div.stButton > button:first-child {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# --- INITIALIZE STATE ---
if 'driver_origin' not in st.session_state: st.session_state.driver_origin = "Kibbutz Beeri"
if 'driver_dest' not in st.session_state: st.session_state.driver_dest = "Rishon LeTsion"
if 'best_options' not in st.session_state: st.session_state.best_options = None
if 'base_route' not in st.session_state: st.session_state.base_route = None
if 'selected_opt_key' not in st.session_state: st.session_state.selected_opt_key = None

# --- CALLBACKS ---
def swap_locations():
    """פונקציה להחלפת מוצא ויעד"""
    temp = st.session_state.driver_origin
    st.session_state.driver_origin = st.session_state.driver_dest
    st.session_state.driver_dest = temp

# --- SIDEBAR UI ---
with st.sidebar:
    st.title("Trempi 🪖")
    st.caption("מערכת אופטימיזציה לשינוע חיילים")
    st.divider()

    st.subheader("🚗 מסלול הנהג")
    
    # שדות קלט מחוברים ל-Session State
    st.text_input("מוצא (מאיפה יוצאים?)", key='driver_origin')
    
    # כפתור החלפה
    col_swap, col_dummy = st.columns([1, 4])
    with col_swap:
        st.button("⇅", on_click=swap_locations, help="החלף כיוון נסיעה", use_container_width=True)
    
    st.text_input("יעד (לאן נוסעים?)", key='driver_dest')
    
    st.divider()
    
    st.subheader("🪖 פרטי החייל")
    passenger_dest = st.selectbox(
        "יעד סופי (בחר תחנה או צומת)", 
        options=hub_names, 
        index=hub_names.index("Haifa Hof HaCarmel (חיפה חוף הכרמל)") if "Haifa Hof HaCarmel (חיפה חוף הכרמל)" in hub_names else 0
    )
    
    st.divider()
    
    col_d, col_t = st.columns(2)
    with col_d:
        trip_date = st.date_input("תאריך", date.today())
    with col_t:
        next_hour = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)
        trip_time = st.time_input("שעה", next_hour.time())

    st.divider()
    
    with st.expander("⚙️ הגדרות מתקדמות"):
        MAX_DETOUR = st.slider("מקסימום עיקוף (דקות)", 5, 60, 15)
        RADIUS = st.slider("רדיוס חיפוש (ק\"מ)", 10, 50, 25)
        MAX_STATIONS = 6

    btn = st.button("🚀 חשב מסלול אופטימלי", type="primary", use_container_width=True)

# --- MAIN LOGIC ---
if btn:
    dept_dt = datetime.combine(trip_date, trip_time)
    st.session_state.selected_opt_key = None 

    # משיכת הערכים מה-State (כי המשתמש אולי ערך אותם ידנית)
    origin_val = st.session_state.driver_origin
    dest_val = st.session_state.driver_dest

    if dept_dt.weekday() == 5 or (dept_dt.weekday() == 4 and dept_dt.hour > 15):
        st.toast("⚠️ חיפוש בסופ\"ש - ייתכן ואין רכבות", icon="🕍")

    with st.spinner('🤖 Trempi מנתח נתונים...'):
        
        # 1. מסלול נהג
        r_points, base_text, base_sec, base_traf = logic.get_route_data(origin_val, dest_val, dept_dt)
        
        if r_points:
            st.session_state.base_route = r_points
            
            # 2. איתור מוקדים
            candidates = logic.find_physically_close_hubs(r_points, my_hubs, RADIUS)
            candidates.sort(key=lambda x: x['geo_distance'])
            
            opts = []
            my_bar = st.progress(0, text="בודק תחנות...")
            
            # 3. בדיקת היתכנות
            limit_check = min(len(candidates), MAX_STATIONS)
            for i, station in enumerate(candidates[:limit_check]):
                my_bar.progress((i + 1) / limit_check, text=f"בודק את {station['name']}...")
                
                detour, d_points, gate_name, gate_coords, arr_hub, traf_stat = logic.calculate_driver_segment(
                    origin_val, dest_val, station, base_sec, dept_dt
                )
                
                if detour is not None and detour <= MAX_DETOUR:
                    tr_min, fin_arr, itin, dep_tm, gap, tr_shape = logic.calculate_passenger_transit(
                        gate_coords, passenger_dest, arr_hub
                    )
                    
                    if tr_min is not None:
                        opts.append({
                            'key': f"opt_{i}",
                            'name': station['name'], 
                            'detour': detour, 
                            'arr_hub': arr_hub,
                            'traffic': traf_stat, 
                            'fin_arr': fin_arr, 
                            'gap': gap,
                            'route': d_points, 
                            'transit_route': tr_shape, 
                            'itinerary': itin,
                            'coords': gate_coords
                        })
            my_bar.empty()
            
            # 4. Full Ride
            driver_dest_arrival = dept_dt + timedelta(seconds=base_traf)
            end_coords = r_points[-1]
            tr_min_full, fin_arr_full, itin_full, _, gap_full, tr_shape_full = logic.calculate_passenger_transit(
                end_coords, passenger_dest, driver_dest_arrival
            )
            
            full_ride_opt = None
            if tr_min_full is not None:
                 full_ride_opt = {
                    'key': 'full_ride',
                    'name': f"Driver's Destination ({dest_val})",
                    'detour': 0,
                    'arr_hub': driver_dest_arrival,
                    'traffic': logic.get_traffic_status(base_sec, base_traf),
                    'fin_arr': fin_arr_full,
                    'gap': gap_full,
                    'route': r_points, 
                    'transit_route': tr_shape_full,
                    'itinerary': itin_full,
                    'coords': end_coords
                }

            final_selection = {}
            if opts:
                opts.sort(key=lambda x: x['fin_arr'])
                final_selection['fastest'] = opts[0]
                opts.sort(key=lambda x: (x['detour'], x['fin_arr']))
                final_selection['driver'] = opts[0]
            
            final_selection['full'] = full_ride_opt
            st.session_state.best_options = final_selection
            
        else:
            st.error("❌ לא הצלחנו לחשב מסלול. בדוק כתובות.")

# --- DISPLAY RESULTS (הצגת התוצאות) ---
st.title("מסלולי נסיעה מומלצים")

if st.session_state.best_options:
    opts = st.session_state.best_options
    def fmt_time(dt): return dt.strftime("%H:%M")
    c1, c2, c3 = st.columns(3)

    def render_card(col, title, icon, opt_key):
        data = opts.get(opt_key)
        with col:
            with st.container(border=True):
                if data:
                    st.markdown(f"#### {icon} {title}")
                    st.markdown(f"**📍 {data['name']}**")
                    t_text, t_color = data['traffic']
                    st.markdown(f"<small>מצב כביש: <span style='color:{t_color}; font-weight:bold'>{t_text}</span></small>", unsafe_allow_html=True)
                    st.divider()
                    col_a, col_b = st.columns(2)
                    with col_a: st.metric("הורדה", fmt_time(data['arr_hub']), delta=f"+{data['detour']} דק'", delta_color="inverse")
                    with col_b: st.metric("יעד חייל", fmt_time(data['fin_arr']))
                    
                    gap = data['gap']
                    if gap >= 15: msg, color = f"☕ יש זמן ({gap} דק')", "green"
                    elif gap >= 5: msg, color = f"👍 מעולה ({gap} דק')", "blue"
                    elif gap >= 0: msg, color = f"🏃 לרוץ! ({gap} דק')", "orange"
                    else: msg, color = f"⚠️ צפוף ({gap} דק')", "red"
                    st.markdown(f"**:{color}[{msg}]**")
                    
                    # כפתורי ניווט
                    lat, lon = data['coords']
                    waze_url = f"https://waze.com/ul?ll={lat},{lon}&navigate=yes"
                    gmaps_url = f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                    c_waze, c_gmaps = st.columns(2)
                    with c_waze: st.link_button("🚗 Waze", waze_url, use_container_width=True)
                    with c_gmaps: st.link_button("🗺️ Maps", gmaps_url, use_container_width=True)

                    with st.expander("📋 פרטי תחבורה"):
                        for step in data['itinerary']: st.markdown(f"- {step}")
                    
                    if st.button("הצג במפה 👁️", key=f"btn_{opt_key}", use_container_width=True):
                        st.session_state.selected_opt_key = opt_key
                else: st.info("לא זמין")

    render_card(c1, "הכי מהיר", "⚡", 'fastest')
    render_card(c2, "נוח לנהג", "🧘", 'driver')
    render_card(c3, "נסיעה מלאה", "🤝", 'full')

    st.divider()

    # --- MAP ---
    if st.session_state.base_route:
        try:
            base_points = st.session_state.base_route
            avg_lat = sum(p[0] for p in base_points) / len(base_points)
            avg_lon = sum(p[1] for p in base_points) / len(base_points)
            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=10, control_scale=True)
            
            folium.PolyLine(base_points, color="#3388ff", weight=4, opacity=0.4).add_to(m)
            folium.Marker(base_points[0], tooltip="מוצא", icon=folium.Icon(color="blue", icon="car", prefix="fa")).add_to(m)
            
            active_key = st.session_state.selected_opt_key
            if not active_key and opts.get('fastest'): active_key = 'fastest'
            
            if active_key and opts.get(active_key):
                sel = opts[active_key]
                folium.PolyLine(sel['route'], color="#e74c3c", weight=5, opacity=0.8).add_to(m)
                if sel.get('transit_route'):
                    folium.PolyLine(sel['transit_route'], color="#2ecc71", weight=5, opacity=0.9, dash_array='10').add_to(m)
                    folium.Marker(sel['transit_route'][-1], tooltip="יעד", icon=folium.Icon(color="green", icon="flag", prefix="fa")).add_to(m)
                folium.Marker(sel['coords'], popup=sel['name'], icon=folium.Icon(color="red", icon="arrow-down", prefix="fa")).add_to(m)
            
            for k, o in opts.items():
                if o and k != active_key:
                    folium.CircleMarker(location=o['coords'], radius=6, color="gray", fill=True, fill_opacity=0.6, tooltip=o['name']).add_to(m)

            map_html = m._repr_html_()
            components.html(map_html, height=500)
        except Exception: st.error("שגיאה במפה")

else:
    st.info("👈 הזן פרטים בתפריט הצדדי.")