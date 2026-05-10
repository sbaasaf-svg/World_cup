import streamlit as st
import json
import os

# הגדרות דף
st.set_page_config(page_title="2026 World Cup Predictor", page_icon="⚽", layout="wide")

# נתיבים לקבצי שמירה מקומיים (כדי שהנתונים לא יימחקו ברענון)
PREDICTIONS_FILE = "user_predictions.json"
ACTUAL_RESULTS_FILE = "actual_results.json"

def save_data(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

# טעינת נתונים ראשונית
if 'predictions' not in st.session_state:
    st.session_state.predictions = load_data(PREDICTIONS_FILE)
if 'actual_results' not in st.session_state:
    st.session_state.actual_results = load_data(ACTUAL_RESULTS_FILE)

# מילון דגלים
flags = {
    "Mexico": "🇲🇽", "South Africa": "🇿🇦", "South Korea": "🇰🇷", "Czechia": "🇨🇿",
    "Canada": "🇨🇦", "Bosnia and Herzegovina": "🇧🇦", "USA": "🇺🇸", "Paraguay": "🇵🇾",
    "Haiti": "🇭🇹", "Scotland": "󠁧󠁢󠁳󠁣󠁴󠁿", "Australia": "🇦🇺", "Türkiye": "🇹🇷",
    "Brazil": "🇧🇷", "Morocco": "🇲🇦", "Qatar": "🇶🇦", "Switzerland": "🇨🇭",
    "Ivory Coast": "🇨🇮", "Ecuador": "🇪🇨", "Germany": "🇩🇪", "Curaçao": "🇨🇼",
    "Netherlands": "🇳🇱", "Japan": "🇯🇵", "Sweden": "🇸🇪", "Tunisia": "🇹🇳",
    "Saudi Arabia": "🇸🇦", "Uruguay": "🇺🇾", "Spain": "🇪🇸", "Cape Verde": "🇨🇻",
    "Iran": "🇮🇷", "New Zealand": "🇳🇿", "Belgium": "🇧🇪", "Egypt": "🇪🇬",
    "France": "🇫🇷", "Senegal": "🇸🇳", "Iraq": "🇮🇶", "Norway": "🇳🇴",
    "Argentina": "🇦🇷", "Algeria": "🇩🇿", "Austria": "🇦🇹", "Jordan": "🇯🇴"
}

games_data = [
    {"id": "1", "date": "11-Jun-26", "t1": "Mexico", "t2": "South Africa"},
    {"id": "2", "date": "11-Jun-26", "t1": "South Korea", "t2": "Czechia"},
    {"id": "3", "date": "12-Jun-26", "t1": "Canada", "t2": "Bosnia and Herzegovina"},
    {"id": "4", "date": "12-Jun-26", "t1": "USA", "t2": "Paraguay"},
]

st.title("🏆 אפליקציית מונדיאל 2026 - גרסה יציבה")

tab1, tab2, tab3 = st.tabs(["🎯 הימורים", "📊 הניקוד שלי", "🛠️ תוצאות אמת"])

# --- טאב 1: הימורים עם חיצים ---
with tab1:
    st.header("הזן את התחזית שלך")
    st.caption("השתמש בחיצים כדי לקבוע את כמות השערים")
    
    for g in games_data:
        g_id = g['id']
        # טעינת ערכים קיימים אם ישנם
        existing_pred = st.session_state.predictions.get(g_id, "0-0").split('-')
        val1 = int(existing_pred[0]) if len(existing_pred) == 2 else 0
        val2 = int(existing_pred[1]) if len(existing_pred) == 2 else 0

        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
        
        with col1:
            st.write(f"{flags.get(g['t1'], '')} {g['t1']}")
        with col2:
            s1 = st.number_input("", min_value=0, max_value=20, value=val1, key=f"s1_{g_id}", label_visibility="collapsed")
        with col3:
            st.write("—")
        with col4:
            s2 = st.number_input("", min_value=0, max_value=20, value=val2, key=f"s2_{g_id}", label_visibility="collapsed")
        with col5:
            st.write(f"{g['t2']} {flags.get(g['t2'], '')}")
        
        # עדכון ושמירה אוטומטית לקובץ
        new_pred = f"{s1}-{s2}"
        if new_pred != st.session_state.predictions.get(g_id):
            st.session_state.predictions[g_id] = new_pred
            save_data(st.session_state.predictions, PREDICTIONS_FILE)

# --- טאב 2: ניקוד ---
with tab2:
    st.header("מצב הניקוד")
    points = 0
    for g in games_data:
        g_id = g['id']
        pred = st.session_state.predictions.get(g_id)
        actual = st.session_state.actual_results.get(g_id)
        
        if actual:
            if pred == actual:
                points += 3
                st.success(f"{g['t1']} vs {g['t2']}: הימרת {pred}, תוצאה {actual} 🎯 (+3 נק')")
            else:
                st.error(f"{g['t1']} vs {g['t2']}: הימרת {pred}, תוצאה {actual} ❌")
        else:
            st.info(f"{g['t1']} vs {g['t2']}: הימרת {pred}. מחכים לתוצאת אמת...")
    
    st.metric("סה\"כ ניקוד", f"{points} נקודות")

# --- טאב 3: תוצאות אמת (עדכון מיידי) ---
with tab3:
    st.header("ניהול תוצאות אמת")
    for g in games_data:
        g_id = g['id']
        existing_actual = st.session_state.actual_results.get(g_id, "0-0").split('-')
        act_val1 = int(existing_actual[0]) if len(existing_actual) == 2 else 0
        act_val2 = int(existing_actual[1]) if len(existing_actual) == 2 else 0

        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        with c1:
            st.write(f"תוצאה סופית: {g['t1']} - {g['t2']}")
        with c2:
            a1 = st.number_input("T1", min_value=0, value=act_val1, key=f"a1_{g_id}", label_visibility="collapsed")
        with c3:
            a2 = st.number_input("T2", min_value=0, value=act_val2, key=f"a2_{g_id}", label_visibility="collapsed")
        
        # שמירה אוטומטית ברגע שהמנהל משנה ערך
        new_actual = f"{a1}-{a2}"
        if new_actual != st.session_state.actual_results.get(g_id):
            st.session_state.actual_results[g_id] = new_actual
            save_data(st.session_state.actual_results, ACTUAL_RESULTS_FILE)
            st.rerun() # מרענן את האפליקציה כדי לעדכן ניקוד בטאבים אחרים מיידית
