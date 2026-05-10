import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="World Cup 2026 Predictor", page_icon="⚽")

# נתוני משחקים - שלב הבתים (חלקי - דוגמה למבנה המלא)
# הערה: במונדיאל 2026 יש 104 משחקים. כאן מופיעים משחקי הפתיחה המרכזיים.
games_data = [
    {"id": 1, "group": "A", "team1": "Mexico", "flag1": "🇲🇽", "team2": "TBD", "flag2": "❓", "date": "2026-06-11"},
    {"id": 2, "group": "A", "team1": "USA", "flag1": "🇺🇸", "team2": "TBD", "flag2": "❓", "date": "2026-06-12"},
    {"id": 3, "group": "B", "team1": "Canada", "flag1": "🇨🇦", "team2": "TBD", "flag2": "❓", "date": "2026-06-12"},
    {"id": 4, "group": "C", "team1": "Argentina", "flag1": "🇦🇷", "team2": "TBD", "flag2": "❓", "date": "2026-06-13"},
    {"id": 5, "group": "D", "team1": "Brazil", "flag1": "🇧🇷", "team2": "TBD", "flag2": "❓", "date": "2026-06-14"},
]

# ניהול מצב (Session State)
if 'user_predictions' not in st.session_state:
    st.session_state.user_predictions = {}
if 'actual_results' not in st.session_state:
    st.session_state.actual_results = {}

st.title("🏆 מנחש תוצאות מונדיאל 2026")

tabs = st.tabs(["🎯 הימורי משתמש", "📊 תוצאות אמת וניקוד"])

# --- טאב 1: הימורי משתמש ---
with tabs[0]:
    st.header("הזן את התחזית שלך")
    for game in games_data:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
        with col2:
            st.write(f"{game['flag1']} {game['team1']}")
        with col3:
            pred = st.text_input(f"תוצאה {game['id']}", placeholder="0-0", key=f"pred_{game['id']}")
            if pred:
                st.session_state.user_predictions[game['id']] = pred
        with col4:
            st.write(f"{game['team2']} {game['flag2']}")
    
    if st.button("שמור הימורים"):
        st.success("ההימורים נשמרו בהצלחה!")
        st.subheader("הסיכום שלך:")
        for g_id, score in st.session_state.user_predictions.items():
            game = next(g for g in games_data if g['id'] == g_id)
            st.write(f"משחק {g_id}: {game['team1']} {score} {game['team2']}")

# --- טאב 2: תוצאות אמת וניקוד ---
with tabs[1]:
    st.header("ניהול תוצאות אמת (מנהל)")
    
    for game in games_data:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"{game['team1']} נגד {game['team2']}")
        with col2:
            actual = st.text_input(f"תוצאה סופית {game['id']}", key=f"actual_{game['id']}")
            if actual:
                st.session_state.actual_results[game['id']] = actual

    st.divider()
    st.header("חישוב ניקוד")
    
    if st.button("חשב ניקוד עכשיו"):
        total_score = 0
        calculation_made = False
        
        for g_id, actual in st.session_state.actual_results.items():
            if g_id in st.session_state.user_predictions:
                prediction = st.session_state.user_predictions[g_id]
                # לוגיקת ניקוד בסיסית: פגיעה בול = 3 נקודות
                if prediction == actual:
                    total_score += 3
                calculation_made = True
        
        if calculation_made:
            st.balloons()
            st.metric("הניקוד הכולל שלך", f"{total_score} נקודות")
        else:
            st.warning("לא ניתן לחשב ניקוד: חסרים הימורים או תוצאות אמת.")
