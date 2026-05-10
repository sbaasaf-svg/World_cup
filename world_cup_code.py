import streamlit as st
import pandas as pd

st.set_page_config(page_title="מונדיאל - אפליקציית הימורים", layout="wide")

st.title("⚽ אפליקציית הימורים על המונדיאל")

# -----------------------------
# משחקי שלב הבתים
# -----------------------------
matches = [
    {"id": 1, "team1": "Brazil", "team2": "France"},
    {"id": 2, "team1": "Argentina", "team2": "Germany"},
    {"id": 3, "team1": "Spain", "team2": "England"},
    {"id": 4, "team1": "Portugal", "team2": "Italy"},
]

# -----------------------------
# תוצאות אמת (אפשר לעדכן אחר כך)
# -----------------------------
real_results = {
    1: (2, 1),
    2: (1, 1),
    3: (0, 2),
    4: (3, 0),
}

# -----------------------------
# פונקציית ניקוד
# -----------------------------
def calculate_points(pred1, pred2, real1, real2):
    # תוצאה מדויקת
    if pred1 == real1 and pred2 == real2:
        return 10

    # פגיעה במנצחת/תיקו
    pred_diff = pred1 - pred2
    real_diff = real1 - real2

    if (
        (pred_diff > 0 and real_diff > 0)
        or (pred_diff < 0 and real_diff < 0)
        or (pred_diff == 0 and real_diff == 0)
    ):
        return 5

    # פגיעה רק בכמות שערים של קבוצה אחת
    if pred1 == real1 or pred2 == real2:
        return 2

    return 0


# -----------------------------
# טופס משתמש
# -----------------------------
st.header("🎯 הכנס את ההימורים שלך")

username = st.text_input("שם המשתתף")

predictions = {}

for match in matches:
    st.subheader(f"{match['team1']} 🇧🇷 vs 🇫🇷 {match['team2']}")

    col1, col2 = st.columns(2)

    with col1:
        score1 = st.number_input(
            f"שערים {match['team1']}",
            min_value=0,
            max_value=20,
            key=f"{match['id']}_1",
        )

    with col2:
        score2 = st.number_input(
            f"שערים {match['team2']}",
            min_value=0,
            max_value=20,
            key=f"{match['id']}_2",
        )

    predictions[match["id"]] = (score1, score2)

# -----------------------------
# חישוב ניקוד
# -----------------------------
if st.button("חשב ניקוד"):
    total_points = 0
    rows = []

    for match in matches:
        match_id = match["id"]

        pred1, pred2 = predictions[match_id]
        real1, real2 = real_results[match_id]

        points = calculate_points(pred1, pred2, real1, real2)
        total_points += points

        rows.append({
            "משחק": f"{match['team1']} - {match['team2']}",
            "ניחוש": f"{pred1}:{pred2}",
            "תוצאה אמיתית": f"{real1}:{real2}",
            "נקודות": points
        })

    st.success(f"🏆 {username} קיבל {total_points} נקודות!")

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

# -----------------------------
# חוקי הניקוד
# -----------------------------
st.sidebar.title("📜 חוקי הניקוד")

st.sidebar.write("""
### שיטת הניקוד:
- ✅ תוצאה מדויקת → 10 נקודות
- ✅ פגיעה במנצחת/תיקו → 5 נקודות
- ✅ פגיעה בשערים של קבוצה אחת → 2 נקודות
- ❌ טעות מלאה → 0 נקודות
""")