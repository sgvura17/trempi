# מאגר נתונים ארצי - רכבות, תחנות מרכזיות וצמתים
# מעודכן לינואר 2026 - כולל רשת צמתים מורחבת (בית ליד, מגידו, גילת ועוד)

my_hubs = [
    # ==========================================
    # 🚆 רכבת ישראל - כל התחנות (Train Stations)
    # ==========================================
    
    # --- קו החוף הצפוני וגליל מערבי ---
    {"name": "Nahariya (נהריה)", "lat": 33.0056, "lon": 35.0989, "type": "Train"},
    {"name": "Akko (עכו)", "lat": 32.9287, "lon": 35.0833, "type": "Train"},
    {"name": "Karmiel (כרמיאל)", "lat": 32.9272, "lon": 35.2965, "type": "Train"},
    {"name": "Ahihud (אחיהוד)", "lat": 32.9126, "lon": 35.1764, "type": "Train"},
    {"name": "Kiryat Motzkin (קרית מוצקין)", "lat": 32.8436, "lon": 35.0747, "type": "Train"},
    {"name": "Kiryat Haim (קרית חיים)", "lat": 32.8272, "lon": 35.0583, "type": "Train"},
    {"name": "Hutzot HaMifratz (חוצות המפרץ)", "lat": 32.8093, "lon": 35.0437, "type": "Train"},
    
    # --- חיפה והעמקים ---
    {"name": "Lev HaMifratz (מרכזית המפרץ)", "lat": 32.7932, "lon": 35.0345, "type": "Train"},
    {"name": "Haifa Center HaShmona (חיפה מרכז השמונה)", "lat": 32.8196, "lon": 35.0016, "type": "Train"},
    {"name": "Haifa Bat Galim (חיפה בת גלים)", "lat": 32.8306, "lon": 34.9806, "type": "Train"},
    {"name": "Haifa Hof HaCarmel (חיפה חוף הכרמל)", "lat": 32.7937, "lon": 34.9567, "type": "Train"},
    {"name": "Yokneam Kfar Yehoshua (יקנעם - כפר יהושע)", "lat": 32.6738, "lon": 35.0970, "type": "Train"},
    {"name": "Migdal HaEmek Kfar Baruch (מגדל העמק - כפר ברוך)", "lat": 32.6465, "lon": 35.1972, "type": "Train"},
    {"name": "Afula (עפולה)", "lat": 32.6200, "lon": 35.2936, "type": "Train"},
    {"name": "Beit Shean (בית שאן)", "lat": 32.5113, "lon": 35.5033, "type": "Train"},
    
    # --- מישור החוף (חיפה-ת"א) ---
    {"name": "Atlit (עתלית)", "lat": 32.6894, "lon": 34.9388, "type": "Train"},
    {"name": "Binyamina (בנימינה)", "lat": 32.5140, "lon": 34.9505, "type": "Train"},
    {"name": "Caesarea Pardes Hanna (קיסריה - פרדס חנה)", "lat": 32.4883, "lon": 34.9622, "type": "Train"},
    {"name": "Hadera West (חדרה מערב)", "lat": 32.4385, "lon": 34.9048, "type": "Train"},
    {"name": "Netanya (נתניה)", "lat": 32.3168, "lon": 34.8710, "type": "Train"},
    {"name": "Netanya Sapir (נתניה ספיר)", "lat": 32.2797, "lon": 34.8560, "type": "Train"},
    {"name": "Beit Yehoshua (בית יהושע)", "lat": 32.2598, "lon": 34.8622, "type": "Train"},
    {"name": "Herzliya (הרצליה)", "lat": 32.1636, "lon": 34.8197, "type": "Train"},
    
    # --- אזור השרון ---
    {"name": "Raanana West (רעננה מערב)", "lat": 32.1736, "lon": 34.8385, "type": "Train"},
    {"name": "Raanana South (רעננה דרום)", "lat": 32.1666, "lon": 34.8655, "type": "Train"},
    {"name": "Hod HaSharon Sokolov (הוד השרון סוקולוב)", "lat": 32.1461, "lon": 34.8903, "type": "Train"},
    {"name": "Kfar Saba Nordau (כפר סבא נורדאו)", "lat": 32.1705, "lon": 34.9224, "type": "Train"},
    {"name": "Rosh HaAyin North (ראש העין צפון)", "lat": 32.1098, "lon": 34.9392, "type": "Train"},
    {"name": "Petah Tikva Segula (פתח תקווה סגולה)", "lat": 32.1158, "lon": 34.8966, "type": "Train"},
    {"name": "Petah Tikva Kiryat Arye (פתח תקווה קרית אריה)", "lat": 32.1065, "lon": 34.8624, "type": "Train"},
    {"name": "Bnei Brak (בני ברק)", "lat": 32.1005, "lon": 34.8322, "type": "Train"},

    # --- תל אביב וגוש דן ---
    {"name": "Tel Aviv University (תל אביב אוניברסיטה)", "lat": 32.1034, "lon": 34.8048, "type": "Train"},
    {"name": "Tel Aviv Savidor Center (תל אביב סבידור מרכז)", "lat": 32.0833, "lon": 34.7960, "type": "Train"},
    {"name": "Tel Aviv HaShalom (תל אביב השלום)", "lat": 32.0734, "lon": 34.7925, "type": "Train"},
    {"name": "Tel Aviv HaHagana (תל אביב ההגנה)", "lat": 32.0537, "lon": 34.7836, "type": "Train"},
    {"name": "Holon Junction (צומת חולון)", "lat": 32.0315, "lon": 34.7738, "type": "Train"},
    {"name": "Holon Wolfson (חולון וולפסון)", "lat": 32.0366, "lon": 34.7600, "type": "Train"},
    {"name": "Bat Yam Yoseftal (בת ים יוספטל)", "lat": 32.0135, "lon": 34.7554, "type": "Train"},
    {"name": "Bat Yam Komemiyut (בת ים קוממיות)", "lat": 31.9997, "lon": 34.7525, "type": "Train"},
    {"name": "Rishon LeTsion Moshe Dayan (ראשל''צ משה דיין)", "lat": 31.9868, "lon": 34.7578, "type": "Train"},
    {"name": "Rishon LeTsion HaRishonim (ראשל''צ הראשונים)", "lat": 31.9486, "lon": 34.8033, "type": "Train"},
    
    # --- שפלה ומרכז דרומי ---
    {"name": "Lod (לוד)", "lat": 31.9443, "lon": 34.8767, "type": "Train"},
    {"name": "Lod Ganei Aviv (לוד גני אביב)", "lat": 31.9678, "lon": 34.8711, "type": "Train"},
    {"name": "Ramla (רמלה)", "lat": 31.9283, "lon": 34.8783, "type": "Train"},
    {"name": "Be'er Ya'akov (באר יעקב)", "lat": 31.9405, "lon": 34.8344, "type": "Train"},
    {"name": "Rehovot (רחובות)", "lat": 31.9056, "lon": 34.8061, "type": "Train"},
    {"name": "Yavne East (יבנה מזרח)", "lat": 31.8674, "lon": 34.7438, "type": "Train"},
    {"name": "Yavne West (יבנה מערב)", "lat": 31.8906, "lon": 34.7311, "type": "Train"},
    {"name": "Ashdod Ad Halom (אשדוד עד הלום)", "lat": 31.7850, "lon": 34.6730, "type": "Train"},
    {"name": "Mazkeret Batya (מזכרת בתיה)", "lat": 31.8488, "lon": 34.8466, "type": "Train"},
    {"name": "Kiryat Malakhi Yoav (קרית מלאכי יואב)", "lat": 31.7588, "lon": 34.8197, "type": "Train"},
    {"name": "Kiryat Gat (קרית גת)", "lat": 31.6025, "lon": 34.7725, "type": "Train"},

    # --- ירושלים ומודיעין ---
    {"name": "Ben Gurion Airport (נתב''ג)", "lat": 32.0004, "lon": 34.8705, "type": "Train"},
    {"name": "Modiin Central (מודיעין מרכז)", "lat": 31.8963, "lon": 35.0084, "type": "Train"},
    {"name": "Modiin Paatei (מודיעין פאתי)", "lat": 31.8997, "lon": 34.9666, "type": "Train"},
    {"name": "Jerusalem Navon (ירושלים יצחק נבון)", "lat": 31.7876, "lon": 35.2030, "type": "Train"},
    {"name": "Jerusalem Malha (ירושלים מלחה)", "lat": 31.7483, "lon": 35.1878, "type": "Train"},
    {"name": "Jerusalem Biblical Zoo (ירושלים גן החיות)", "lat": 31.7455, "lon": 35.1761, "type": "Train"},
    {"name": "Beit Shemesh (בית שמש)", "lat": 31.7583, "lon": 34.9922, "type": "Train"},

    # --- דרום ---
    {"name": "Ashkelon (אשקלון)", "lat": 31.6772, "lon": 34.6051, "type": "Train"},
    {"name": "Sderot (שדרות)", "lat": 31.5160, "lon": 34.5873, "type": "Train"},
    {"name": "Netivot (נתיבות)", "lat": 31.4085, "lon": 34.5833, "type": "Train"},
    {"name": "Ofakim (אופקים)", "lat": 31.3204, "lon": 34.6077, "type": "Train"},
    {"name": "Lehavim Rahat (להבים רהט)", "lat": 31.3667, "lon": 34.7950, "type": "Train"},
    {"name": "Beer Sheva North/Uni (באר שבע צפון/אונ')", "lat": 31.2618, "lon": 34.8123, "type": "Train"},
    {"name": "Beer Sheva Center (באר שבע מרכז)", "lat": 31.2431, "lon": 34.7978, "type": "Train"},
    {"name": "Dimona (דימונה)", "lat": 31.0664, "lon": 35.0116, "type": "Train"},

    # ==========================================
    # 🚌 תחנות מרכזיות וצמתים (Bus Hubs)
    # ==========================================

    # --- צפון ---
    {"name": "Kiryat Shmona Central (מרכזית קרית שמונה)", "lat": 33.2075, "lon": 35.5700, "type": "Bus Hub"},
    {"name": "Tiberias Central (מרכזית טבריה)", "lat": 32.7880, "lon": 35.5383, "type": "Bus Hub"},
    {"name": "Katzrin Central (מרכזית קצרין)", "lat": 32.9936, "lon": 35.6894, "type": "Bus Hub"},
    {"name": "Nazareth Central (מרכזית נצרת)", "lat": 32.7025, "lon": 35.2975, "type": "Bus Hub"},
    {"name": "Golani Junction (צומת גולני)", "lat": 32.7933, "lon": 35.4122, "type": "Bus Hub"},
    {"name": "Amiad Junction (צומת עמיעד)", "lat": 32.9308, "lon": 35.5433, "type": "Bus Hub"},
    {"name": "Hamovil Junction (צומת המוביל)", "lat": 32.7561, "lon": 35.2344, "type": "Bus Hub"},
    {"name": "Yagur Junction (צומת יגור)", "lat": 32.7420, "lon": 35.0760, "type": "Bus Hub"},
    {"name": "Alonim Junction (צומת אלונים)", "lat": 32.7160, "lon": 35.1320, "type": "Bus Hub"},
    {"name": "Megiddo Junction (צומת מגידו)", "lat": 32.5735, "lon": 35.1840, "type": "Bus Hub"},
    {"name": "Check Post Junction (צומת צ'ק פוסט)", "lat": 32.7950, "lon": 35.0350, "type": "Bus Hub"},
    
    # --- השרון והמרכז ---
    {"name": "Beit Lid Junction (צומת בית ליד/השרון)", "lat": 32.3240, "lon": 34.9090, "type": "Bus Hub"},
    {"name": "Poleg Junction (מחלף פולג)", "lat": 32.2745, "lon": 34.8460, "type": "Bus Hub"},
    {"name": "Netanya Central Bus (מרכזית נתניה)", "lat": 32.3275, "lon": 34.8617, "type": "Bus Hub"},
    {"name": "Hadera Central Bus (מרכזית חדרה)", "lat": 32.4361, "lon": 34.9133, "type": "Bus Hub"},
    {"name": "Olga Junction (מחלף אולגה)", "lat": 32.4330, "lon": 34.8930, "type": "Bus Hub"},
    {"name": "Kfar Yona Junction (צומת כפר יונה)", "lat": 32.3160, "lon": 34.9350, "type": "Bus Hub"},
    {"name": "Sira Junction (מחלף הסירה)", "lat": 32.1645, "lon": 34.8190, "type": "Bus Hub"},
    {"name": "Glilot Junction (צומת גלילות)", "lat": 32.1466, "lon": 34.8055, "type": "Bus Hub"},
    {"name": "Ra'anana Junction (צומת רעננה)", "lat": 32.1795, "lon": 34.8620, "type": "Bus Hub"},
    {"name": "Morasha Junction (מחלף מורשה)", "lat": 32.1333, "lon": 34.8417, "type": "Bus Hub"},
    
    # --- גוש דן רבתי ---
    {"name": "Tel Aviv Central Bus (תחנה מרכזית ת''א)", "lat": 32.0558, "lon": 34.7794, "type": "Bus Hub"},
    {"name": "Tel Aviv Savidor Terminal (מסוף 2000)", "lat": 32.0830, "lon": 34.7955, "type": "Bus Hub"},
    {"name": "Geha Junction (מחלף גהה)", "lat": 32.0911, "lon": 34.8458, "type": "Bus Hub"},
    {"name": "Aluf Sade Junction (מחלף אלוף שדה)", "lat": 32.0525, "lon": 34.8211, "type": "Bus Hub"},
    {"name": "Mesubim Junction (מחלף מסובים)", "lat": 32.0350, "lon": 34.8250, "type": "Bus Hub"},
    {"name": "Beit Dagan Junction (צומת בית דגן)", "lat": 31.9983, "lon": 34.8139, "type": "Bus Hub"},
    {"name": "Tzrifin / Assaf Harofeh (צריפין/אסף הרופא)", "lat": 31.9620, "lon": 34.8390, "type": "Bus Hub"},
    {"name": "El Al Junction (צומת אל על)", "lat": 32.0000, "lon": 34.8900, "type": "Bus Hub"},
    
    # --- ירושלים והשפלה ---
    {"name": "Jerusalem Central Bus (מרכזית ירושלים)", "lat": 31.7892, "lon": 35.2028, "type": "Bus Hub"},
    {"name": "Latrun Junction (מחלף לטרון)", "lat": 31.8385, "lon": 34.9780, "type": "Bus Hub"},
    {"name": "Shimshon Junction (צומת שמשון)", "lat": 31.7850, "lon": 34.9920, "type": "Bus Hub"},
    {"name": "Hemed Interchange (מחלף חמד)", "lat": 31.8028, "lon": 35.1278, "type": "Bus Hub"},
    {"name": "Shoresh Interchange (מחלף שורש)", "lat": 31.8089, "lon": 35.0847, "type": "Bus Hub"},
    {"name": "Bilu Junction (צומת בילו)", "lat": 31.8687, "lon": 34.8166, "type": "Bus Hub"},
    
    # --- דרום ---
    {"name": "Kastina Junction (צומת קסטינה)", "lat": 31.7303, "lon": 34.7578, "type": "Bus Hub"},
    {"name": "Silver Junction (צומת סילבר)", "lat": 31.6700, "lon": 34.6150, "type": "Bus Hub"},
    {"name": "Yad Mordechai Junction (צומת יד מרדכי)", "lat": 31.5875, "lon": 34.5565, "type": "Bus Hub"},
    {"name": "Plugot Junction (צומת פלוגות)", "lat": 31.6247, "lon": 34.7558, "type": "Bus Hub"},
    {"name": "Beit Kama Junction (צומת בית קמה)", "lat": 31.4464, "lon": 34.7619, "type": "Bus Hub"},
    {"name": "Gilat Junction (צומת גילת)", "lat": 31.3285, "lon": 34.6640, "type": "Bus Hub"},
    {"name": "Shoket Junction (צומת שוקת)", "lat": 31.2917, "lon": 34.8967, "type": "Bus Hub"},
    {"name": "Beer Sheva Central Bus (מרכזית באר שבע)", "lat": 31.2435, "lon": 34.7960, "type": "Bus Hub"},
    {"name": "City of Bahadim (עיר הבה''דים)", "lat": 31.1072, "lon": 34.7867, "type": "Bus Hub"},
    
    # --- איו"ש ---
    {"name": "Ariel Junction (צומת אריאל)", "lat": 32.1050, "lon": 35.1750, "type": "Bus Hub"},
    {"name": "Tapuah Junction (צומת תפוח)", "lat": 32.1122, "lon": 35.2600, "type": "Bus Hub"},
    {"name": "Gush Etzion Junction (צומת גוש עציון)", "lat": 31.6500, "lon": 35.1370, "type": "Bus Hub"},
    {"name": "Adam Junction (צומת חיזמא/אדם)", "lat": 31.8600, "lon": 35.2450, "type": "Bus Hub"},
    {"name": "Shilo Junction (צומת שילה)", "lat": 32.0544, "lon": 35.2869, "type": "Bus Hub"},
    {"name": "Sha'ar Binyamin (שער בנימין)", "lat": 31.8744, "lon": 35.2472, "type": "Bus Hub"},

    # --- ערבה ואילת ---
    {"name": "Eilat Central Bus (מרכזית אילת)", "lat": 29.5564, "lon": 34.9525, "type": "Bus Hub"},
    {"name": "Yotvata (יוטבתה)", "lat": 29.8950, "lon": 35.0617, "type": "Bus Hub"},
    {"name": "Ketura Junction (צומת קטורה)", "lat": 29.9678, "lon": 35.0650, "type": "Bus Hub"},
    {"name": "Ein Yahav (עין יהב)", "lat": 30.6631, "lon": 35.2464, "type": "Bus Hub"},
    {"name": "Arava Junction (צומת הערבה)", "lat": 31.0267, "lon": 35.1583, "type": "Bus Hub"}
]