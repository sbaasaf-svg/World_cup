import streamlit as st

# הגדרות דף
st.set_page_config(page_title="2026 World Cup Predictor", page_icon="⚽", layout="wide")

# מילון דגלים למדינות המשתתפות (לפי הנתונים מהלינק)
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

# נתוני המשחקים המדויקים מהמקור שסופק
games_data = [
    {"id": 1, "date": "11-Jun-26", "t1": "Mexico", "t2": "South Africa", "grp": "A"},
    {"id": 2, "date": "11-Jun-26", "t1": "South Korea", "t2": "Czechia", "grp": "A"},
    {"id": 3, "date": "12-Jun-26", "t1": "Canada", "t2": "Bosnia and Herzegovina", "grp": "B"},
    {"id": 4, "date": "12-Jun-26", "t1": "USA", "t2": "Paraguay", "grp": "D"},
    {"id": 5, "date": "13-Jun-26", "t1": "Haiti", "t2": "Scotland", "grp": "C"},
    {"id": 6, "date": "13-Jun-26", "t1": "Australia", "t2": "Türkiye", "grp": "D"},
    {"id": 7, "date": "13-Jun-26", "t1": "Brazil", "t2": "Morocco", "grp": "C"},
    {"id": 8, "date": "13-Jun-26", "t1": "Qatar", "t2": "Switzerland", "grp": "B"},
    {"id": 9, "date": "14-Jun-26", "t1": "Ivory Coast", "t2": "Ecuador", "grp": "E"},
    {"id": 10, "date": "14-Jun-26", "t1": "Germany", "t2": "Curaçao", "grp": "E"},
    {"id": 11, "date": "14-Jun-26", "t1": "Netherlands", "t2": "Japan", "grp": "F"},
    {"id": 12, "date": "14-Jun-26", "t1": "Sweden", "t2": "Tunisia", "grp": "F"},
]

# ניהול מצב (Session State) לשמירת הנתונים
if 'predictions' not in st.session_state:
    st.session_state.predictions = {}
if 'actual_results' not in st.session_state:
    st.session_state.actual_results = {}

st.title("🏆 מנהל הימורי מונדיאל 2026")

tab1, tab2, tab3 = st.tabs(["📝 הזנת הימורים", "📋 ההימורים שלי", "⚙️ טאב מנהל: תוצאות אמת"])

# --- טאב 1: הזנת הימורים ---
with tab1:
    st.header("הזן את התחזית שלך לשלב הבתים")
    for g in games_data:
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 1])
        with col2:
            st.write(f"{flags.get(g['t1'], '🏳️')} {g['t1']}")
        with col3:
            # הזנת תוצאה בפורמט X-X
            score = st.text_input(f"תוצאה {g['id']}", key=f"in_{g['id']}", placeholder="0-0")
            if score:
                st.session_state.predictions[g['id']] = score
        with col4:
            st.write(f"{g['t2']} {flags.get(g['t2'], '🏳️')}")
    st.info("התוצאות נשמרות אוטומטית בעת ההקלדה.")

# --- טאב 2: הצגת הימורים וניקוד ---
with tab2:
    st.header("סיכום ההימורים שלך וניקוד")
    if not st.session_state.predictions:
        st.warning("טרם הזנת הימורים.")
    else:
        total_points = 0
        results_list = []
        
        for g in games_data:
            g_id = g['id']
            user_pred = st.session_state.predictions.get(g_id, "לא הוזן")
            actual = st.session_state.actual_results.get(g_id, None)
            
            points = 0
            status = "ממתין לתוצאה"
            
            if actual:
                if user_pred == actual:
                    points = 3
                    status = "✅ פגיעה בול! (3 נק')"
                else:
                    status = f"❌ טעות (התוצאה: {actual})"
                total_points += points
            
            results_list.append({
                "משחק": f"{g['t1']} vs {g['t2']}",
                "הימור שלך": user_pred,
                "תוצאת אמת": actual if actual else "טרם עודכן",
                "סטטוס": status
            })
        
        st.table(results_list)
        
        if st.session_state.actual_results:
            st.metric("ניקוד כולל", f"{total_points} נקודות")
        else:
            st.info("הניקוד יוצג לאחר שיוזנו תוצאות אמת בטאב המנהל.")

# --- טאב 3: הזנת תוצאות אמת (למנהל) ---
with tab3:
    st.header("עדכון תוצאות מהשטח")
    st.write("הזן כאן את תוצאות המשחקים כפי שהסתיימו בפועל:")
    for g in games_data:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.write(f"משחק {g['id']}: {g['t1']} נגד {g['t2']}")
        with c2:
            act_score = st.text_input(f"תוצאה סופית {g['id']}", key=f"act_{g['id']}")
            if act_score:
                st.session_state.actual_results[g['id']] = act_score
