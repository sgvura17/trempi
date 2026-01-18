import googlemaps
import polyline
import math
from datetime import datetime, timedelta
import streamlit as st
import pytz

# --- הגדרת שעון ישראל ---
IL_TZ = pytz.timezone('Asia/Jerusalem')

try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("⚠️ שגיאה: מפתח ה-API חסר. נא להגדיר את GOOGLE_API_KEY ב-secrets.")
    st.stop()

# --- פונקציות עזר ---

def ensure_israel_time(dt_obj):
    if dt_obj is None: return None
    if dt_obj.tzinfo is None:
        return IL_TZ.localize(dt_obj)
    return dt_obj.astimezone(IL_TZ)

def reverse_geocode(lat, lon):
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        res = gmaps.reverse_geocode((lat, lon))
        if res: return res[0]['formatted_address']
    except Exception: pass
    return None

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def get_traffic_status(normal_seconds, traffic_seconds):
    if not traffic_seconds: return "Unknown", "gray"
    delay_min = (traffic_seconds - normal_seconds) / 60
    if delay_min < 5: return "זורם (Free Flow)", "green"
    elif delay_min < 15: return f"עומס קל (+{int(delay_min)} דק')", "orange"
    else: return f"פקוק (+{int(delay_min)} דק')", "red"

def find_physically_close_hubs(driver_route_points, hubs_database, radius_km):
    candidates = []
    for hub in hubs_database:
        min_dist = float('inf')
        for point in driver_route_points:
            dist = haversine_distance(point[0], point[1], hub['lat'], hub['lon'])
            if dist < min_dist: min_dist = dist
        if min_dist <= radius_km:
            hub['geo_distance'] = min_dist 
            candidates.append(hub)
    return candidates

def get_route_data(origin, destination, departure_time):
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        departure_time = ensure_israel_time(departure_time)
        directions = gmaps.directions(origin, destination, mode="driving", departure_time=departure_time)
        if not directions: return None, None, None, None
        
        points = polyline.decode(directions[0]['overview_polyline']['points'])
        leg = directions[0]['legs'][0]
        duration_val = leg['duration']['value']
        duration_traffic_val = leg.get('duration_in_traffic', {}).get('value', duration_val)
        return points, leg['duration']['text'], duration_val, duration_traffic_val
    except Exception as e:
        print(f"API Error: {e}")
        return None, None, None, None

def calculate_driver_segment(origin, driver_dest, hub, base_seconds, departure_time):
    gmaps = googlemaps.Client(key=API_KEY)
    departure_time = ensure_israel_time(departure_time)
    
    best_detour_mins = float('inf')
    best_route_points = None
    best_gate_name = None       
    best_gate_coords = None     
    arrival_time_at_hub = None
    segment_traffic_status = ("Unknown", "gray")

    gates = hub.get('gates', [{'label': 'Main Drop-off', 'lat': hub['lat'], 'lon': hub['lon']}])

    for gate in gates:
        try:
            waypoints = [f"{gate['lat']},{gate['lon']}"]
            directions = gmaps.directions(origin, driver_dest, waypoints=waypoints, mode="driving", departure_time=departure_time)
            if directions:
                leg1 = directions[0]['legs'][0]
                total_seconds = sum(leg['duration']['value'] for leg in directions[0]['legs'])
                added_minutes = int((total_seconds - base_seconds) / 60)
                seconds_to_hub = leg1['duration']['value']
                traffic_seconds_to_hub = leg1.get('duration_in_traffic', {}).get('value', seconds_to_hub)
                
                if added_minutes < best_detour_mins:
                    best_detour_mins = added_minutes
                    best_route_points = polyline.decode(directions[0]['overview_polyline']['points'])
                    arrival_time_at_hub = departure_time + timedelta(seconds=traffic_seconds_to_hub)
                    segment_traffic_status = get_traffic_status(seconds_to_hub, traffic_seconds_to_hub)
                    best_gate_name = gate['label']                 
                    best_gate_coords = (gate['lat'], gate['lon'])  
        except Exception: continue
        
    return best_detour_mins, best_route_points, best_gate_name, best_gate_coords, arrival_time_at_hub, segment_traffic_status

# --- הלוגיקה המשופרת לחייל ---
def calculate_passenger_transit(origin, passenger_dest, arrival_time):
    gmaps = googlemaps.Client(key=API_KEY)
    arrival_time = ensure_israel_time(arrival_time)
    
    origin_str = ""
    # 1. טיפול חכם בשם התחנה: הוספת "Train Station" כדי למנוע הליכה מהעיר
    if isinstance(origin, str):
        # מנקה סוגריים בעברית אם יש, ומוסיף Train Station
        clean_name = origin.split('(')[0].strip()
        origin_str = f"{clean_name} Train Station, Israel"
    elif isinstance(origin, (tuple, list)):
        origin_str = f"{origin[0]},{origin[1]}"

    # 2. ה"צ'יט" לפתרון באג ה-2 דקות:
    # אנחנו מחפשים רכבת כאילו הגענו 5 דקות קודם. 
    # זה יגרום לגוגל "לתפוס" את הרכבת הקרובה, והמערכת שלנו תציג "לרוץ!" (פער שלילי)
    fake_arrival_time = arrival_time - timedelta(minutes=5)
    
    selected_route = None
    
    try:
        # ניסיון ראשון: חיפוש רגיל מהזמן המוקדם
        directions = gmaps.directions(
            origin=origin_str,
            destination=passenger_dest,
            mode="transit", transit_mode="train", departure_time=fake_arrival_time
        )
        
        # לוגיקת בחירה: מחפשים את הרכבת הראשונה שיוצאת *אחרי* ההגעה האמיתית (או ממש קרוב אליה)
        if directions:
            for route in directions:
                leg = route['legs'][0]
                dep_time_val = leg['departure_time']['value']
                dep_time = datetime.fromtimestamp(dep_time_val, IL_TZ)
                
                # חישוב הפער מההגעה *האמיתית* (לא המזויפת)
                gap_minutes = (dep_time - arrival_time).total_seconds() / 60
                
                # אנחנו מתירים גם מינוס קטן (למשל מינוס 2 דקות) כי אולי החייל ירוץ
                if gap_minutes >= -2: 
                    selected_route = route
                    break 
        
        if not selected_route: return None, None, [], None, None, None

        leg = selected_route['legs'][0]
        transit_duration_mins = int(leg['duration']['value'] / 60)
        
        arrival_at_final_dest_timestamp = leg['arrival_time']['value']
        final_arrival_dt = datetime.fromtimestamp(arrival_at_final_dest_timestamp, IL_TZ)
        
        train_departure_timestamp = leg['departure_time']['value']
        train_departure_dt = datetime.fromtimestamp(train_departure_timestamp, IL_TZ)
        
        # חישוב זמן המתנה אמיתי
        wait_time_at_platform = int((train_departure_dt - arrival_time).total_seconds() / 60)
        transit_polyline_points = polyline.decode(selected_route['overview_polyline']['points'])
        
        itinerary = []
        if 'steps' in leg:
            for step in leg['steps']:
                duration = step['duration']['text']
                mode = step.get('travel_mode')
                
                if mode == 'WALKING':
                    if "min" in duration:
                        try:
                            mins = int(duration.split()[0])
                            # מסנן הליכות קצרות בתוך התחנה
                            if mins > 5: itinerary.append(f"🚶 הליכה ({duration})")
                        except: pass
                
                elif mode == 'TRANSIT':
                    details = step.get('transit_details', {})
                    line = details.get('line', {})
                    vehicle = line.get('vehicle', {}).get('name', 'Bus')
                    short_name = line.get('short_name', '') 
                    headsign = details.get('headsign', '') 
                    
                    step_dep_ts = details.get('departure_time', {}).get('value')
                    if step_dep_ts:
                        step_time_str = datetime.fromtimestamp(step_dep_ts, IL_TZ).strftime("%H:%M")
                    else:
                        step_time_str = details.get('departure_time', {}).get('text', '')

                    info = f"🚆 {vehicle} **{short_name}** לכיוון {headsign}" if short_name else f"🚌 {vehicle} לכיוון {headsign}"
                    itinerary.append(f"{info} (יוצא ב-{step_time_str})")
                    
        return transit_duration_mins, final_arrival_dt, itinerary, train_departure_dt, wait_time_at_platform, transit_polyline_points

    except Exception as e: 
        print(f"Logic Error: {e}")
        return None, None, [], None, None, None
