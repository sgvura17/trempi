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

def calculate_driver_segment(origin, driver_dest, hub, base_seconds, departure_time, driver_start_coords=None):
    # בדיקת מרחק אפס - אם קרובים לתחנה, מחזירים 0 זמן ומסלול ריק
    if driver_start_coords:
        dist_from_start = haversine_distance(driver_start_coords[0], driver_start_coords[1], hub['lat'], hub['lon'])
        if dist_from_start < 0.4: 
            return 0, [], hub['name'], (hub['lat'], hub['lon']), departure_time, ("כבר במקום", "green")

    gmaps = googlemaps.Client(key=API_KEY)
    departure_time = ensure_israel_time(departure_time)
    
    best_detour_mins = float('inf')
    best_route_points = [] # אתחול כרשימה ריקה למקרה חירום
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


# --- הפונקציה המתוקנת עם הניתוח הכירורגי ---
def calculate_passenger_transit(origin, passenger_dest, arrival_time):
    gmaps = googlemaps.Client(key=API_KEY)
    arrival_time = ensure_israel_time(arrival_time)
    
    origin_str = ""
    is_station_origin = False # דגל: האם המוצא הוא תחנה שמית?

    if isinstance(origin, str):
        is_station_origin = True
        clean_name = origin.split('(')[0].strip()
        # מוסיפים ישראל כדי למקד, אבל בלי Train Station בשביל הניסוי, או עם - נבדוק
        origin_str = f"{clean_name} Train Station, Israel"
    elif isinstance(origin, (tuple, list)):
        origin_str = f"{origin[0]},{origin[1]}"

    fake_arrival_time = arrival_time - timedelta(minutes=5)
    
    selected_route = None
    
    try:
        directions = gmaps.directions(
            origin=origin_str,
            destination=passenger_dest,
            mode="transit", transit_mode="train", departure_time=fake_arrival_time
        )
        
        if directions:
            for route in directions:
                leg = route['legs'][0]
                
                # --- תיקון באג הליכה מוגזמת ---
                # אם הצעד הראשון הוא הליכה ארוכה והמוצא הוא תחנה, אנחנו מתעלמים מההליכה הזו
                # כי אנחנו מניחים שהחייל כבר בתחנה
                first_step = leg['steps'][0]
                time_offset_seconds = 0
                
                if is_station_origin and first_step['travel_mode'] == 'WALKING':
                    walk_seconds = first_step['duration']['value']
                    # אם ההליכה גדולה מ-3 דקות (180 שניות), זה חשוד כבאג של גוגל
                    if walk_seconds > 180:
                        # אנחנו נחשיב את זמן היציאה כזמן של הצעד *הבא* (התחב"צ עצמו)
                        # ונבטל את זמן ההליכה מהחישוב
                        pass # נטפל בזה למטה בחישוב ה-Wait Time
                
                # בדיקת זמנים
                dep_time_val = leg['departure_time']['value']
                dep_time = datetime.fromtimestamp(dep_time_val, IL_TZ)
                
                gap_minutes = (dep_time - arrival_time).total_seconds() / 60
                if gap_minutes >= -2: 
                    selected_route = route
                    break 
        
        if not selected_route: return None, None, [], None, None, None

        leg = selected_route['legs'][0]
        
        # --- בניית המסלול מחדש (ללא הליכת הפתיחה המיותרת) ---
        itinerary = []
        is_first_step = True
        
        for step in leg['steps']:
            duration = step['duration']['text']
            mode = step.get('travel_mode')
            duration_val = step['duration']['value']
            
            # אם זה הצעד הראשון, הוא הליכה, הוא ארוך, ואנחנו בתחנה -> דלג עליו!
            if is_first_step and mode == 'WALKING' and is_station_origin and duration_val > 180:
                is_first_step = False
                continue 
            
            is_first_step = False # אחרי שבדקנו את הראשון, מפסיקים לבדוק
            
            if mode == 'WALKING':
                if "min" in duration:
                    try:
                        mins = int(duration.split()[0])
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

        # נתונים סופיים
        final_arrival_ts = leg['arrival_time']['value']
        final_arrival_dt = datetime.fromtimestamp(final_arrival_ts, IL_TZ)
        transit_polyline_points = polyline.decode(selected_route['overview_polyline']['points'])
        
        # חישוב זמן יציאה "אמיתי" (של הרכבת/אוטובוס הראשון, לא ההליכה)
        # אנחנו מחפשים את הצעד ה-TRANSIT הראשון
        first_transit_dep = None
        for step in leg['steps']:
             if step['travel_mode'] == 'TRANSIT':
                 ts = step['transit_details']['departure_time']['value']
                 first_transit_dep = datetime.fromtimestamp(ts, IL_TZ)
                 break
        
        if first_transit_dep:
            train_departure_dt = first_transit_dep
        else:
            # Fallback
            train_departure_dt = datetime.fromtimestamp(leg['departure_time']['value'], IL_TZ)

        wait_time_at_platform = int((train_departure_dt - arrival_time).total_seconds() / 60)
        transit_duration_mins = int((final_arrival_dt - train_departure_dt).total_seconds() / 60)

        return transit_duration_mins, final_arrival_dt, itinerary, train_departure_dt, wait_time_at_platform, transit_polyline_points

    except Exception as e: 
        print(f"Logic Error: {e}")
        return None, None, [], None, None, None
