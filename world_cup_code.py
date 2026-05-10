import streamlit as st
import json
import os

# הגדרות דף
st.set_page_config(page_title="2026 World Cup Predictor", page_icon="⚽", layout="wide")

# נתיבים לקבצי שמירה מקומיים
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

# טעינת נתונים
if 'predictions' not in st.session_state:
    st.session_state.predictions = load_data(PREDICTIONS_FILE)
if 'actual_results' not in st.session_state:
    st.session_state.actual_results = load_data(ACTUAL_RESULTS_FILE)

# מילון דגלים מעודכן
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

# רשימת המשחקים המעודכנת (לפי הלינק)
games_data = [
    {"id": "1", "t1": "Mexico", "t2": "South Africa"},
    {"id": "2", "t1": "South Korea", "t2": "Czechia"},
    {"id": "3", "t1": "Canada", "t2": "Bosnia and Herzegovina"},
    {"id": "4", "t1": "USA", "t2": "Paraguay"},
    {"id": "5", "t1": "Haiti", "t2": "Scotland"},
    {"id": "6", "t1": "Australia", "t2": "Türkiye"},
    {"id": "7", "t1": "Brazil", "t2": "Morocco"},
    {"id": "8", "t1": "Qatar", "t2": "Switzerland"},
]

st.title("⚽ אפליקציית מונדיאל 2026")

tab1, tab2, tab3 = st.tabs(["🎯 הימורי משתמש", "📊 לוח ניקוד", "⚙️ ניהול תוצאות"])

# --- טאב 1: הימורי משתמש ---
with tab1:
    st.header("הזן את התחזית שלך")
    for g in games_data:
        g_id = g['id']
        # פירוק התוצאה הקיימת לערכים עבור ה-number_input
        current_pred = st.session_state.predictions.get(g_id, "0-0").split('-')
        v1, v2 = int(current_pred[0]), int(current_pred[1])

        col1, col2, col3, col4, col5 = st.columns([2, 1, 0.5, 1, 2])
        with col1:
            st.write(f"{flags.get(g['t1'], '')} {g['t1']}")
        with col2:
            s1 = st.number_input("", min_value=0, value=v1, key=f"user_s1_{g_id}", label_visibility="collapsed")
        with col3:
            st.write("—")
        with col4:
            s2 = st.number_input("", min_value=0, value=v2, key=f"user_s2_{g_id}", label_visibility="collapsed")
        with col5:
            st.write(f"{g['t2']} {flags.get(g['t2'], '')}")
        
        # שמירה אוטומטית בפורמט X-X
        st.session_state.predictions[g_id] = f"{s1}-{s2}"
    
    if st.button("שמור את כל ההימורים"):
        save_data(st.session_state.predictions, PREDICTIONS_FILE)
        st.success("ההימורים נשמרו!")

# --- טאב 2: לוח ניקוד ---
with tab2:
    st.header("תוצאות וניקוד")
    
    # בדיקה אם הוזנה תוצאת אמת כלשהי
    if not st.session_state.actual_results:
        st.info("הניקוד יוצג רק לאחר שיוזנו תוצאות משחקים בפועל על ידי המנהל.")
    else:
        total_score = 0
        summary = []
        
        for g in games_data:
            g_id = g['id']
            pred = st.session_state.predictions.get(g_id)
            actual = st.session_state.actual_results.get(g_id)
            
            if actual:
                # שיטת הניקוד המקורית: פגיעה בול בתוצאה
                if pred == actual:
                    total_score += 3
                    status = "✅ פגיעה בול (3 נק')"
                else:
                    status = "❌ לא קלעת"
                
                summary.append({
                    "משחק": f"{g['t1']} - {g['t2']}",
                    "הימור שלך": pred,
                    "תוצאה סופית": actual,
                    "מצב": status
                })
        
        if summary:
            st.table(summary)
            st.metric("ניקוד כולל", f"{total_score} נקודות")
        else:
            st.write("ממתינים לעדכון תוצאות המשחקים שהימרת עליהם.")

# --- טאב 3: ניהול תוצאות אמת ---
with tab3:
    st.header("הזנת תוצאות אמת (מנהל)")
    st.write("הזן תוצאה כדי להפעיל את חישוב הניקוד")
    
    for g in games_data:
        g_id = g['id']
        current_actual = st.session_state.actual_results.get(g_id, "NONE-NONE").split('-')
        
        # מאתחל ל-0 רק אם כבר הוזן פעם אחת, אחרת משאיר ריק להחלטת מנהל
        a_v1 = int(current_actual[0]) if current_actual[0] != "NONE" else 0
        a_v2 = int(current_actual[1]) if current_actual[1] != "NONE" else 0

        c1, c2, c3, c4 = st.columns([3, 1, 0.5, 1])
        with c1:
            st.write(f"{g['t1']} נגד {g['t2']}")
        with c2:
            as1 = st.number_input("T1", min_value=0, value=a_v1, key=f"adm_s1_{g_id}", label_visibility="collapsed")
        with c3:
            st.write(":")
        with c4:
            as2 = st.number_input("T2", min_value=0, value=as_v2 if 'as_v2' in locals() else a_v2, key=f"adm_s2_{g_id}", label_visibility="collapsed")
        
        # כפתור עדכון ספציפי למשחק או שמירה גורפת
        if st.button(f"עדכן תוצאה למשחק {g_id}", key=f"btn_{g_id}"):
            st.session_state.actual_results[g_id] = f"{as1}-{as2}"
            save_data(st.session_state.actual_results, ACTUAL_RESULTS_FILE)
            st.success(f"תוצאת משחק {g_id} עודכנה!")
            st.rerun()
