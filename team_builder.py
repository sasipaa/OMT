import streamlit as st
import pandas as pd

st.set_page_config(page_title="Team Auto-Assignment", layout="wide")
st.title("ระบบจัดทีมอัตโนมัติ (แบบ Snake Draft)")

sheet_url = st.text_input("🔗 วางลิงก์ Google Sheets (.csv format)", 
    value="https://docs.google.com/spreadsheets/d/1jNPyTl3R9rg7TEaYxcLpN2Ae-QUs3Are/export?format=csv&gid=869418635")

num_lines = 10  # สาย A–J
line_labels = [chr(65 + i) for i in range(num_lines)]  # ['A', 'B', ..., 'J']

if st.button("🚀 Load & Generate Teams"):
    try:
        df = pd.read_csv(sheet_url)

        # รวมชื่อ
        df['ชื่อเต็ม'] = df['First Name'].astype(str) + " " + df['Last Name'].astype(str) + " (" + df['Nickname'].astype(str) + ")"
        df = df.sort_values(by='Total', ascending=False).reset_index(drop=True)

        # สร้าง Snake Draft ที่กระจายตามสายแบบ A1, B1, ..., J1, A2, ...
        teams = []
        direction = 1
        team_round = 1
        while len(teams) < len(df):
            batch = line_labels if direction == 1 else list(reversed(line_labels))
            for line in batch:
                if len(teams) >= len(df):
                    break
                teams.append(f"{line}{team_round}")
            team_round += 1
            direction *= -1

        df['ทีม'] = teams
        df['สาย'] = df['ทีม'].str[0]

        # สรุปข้อมูล
        st.success("✅ จัดทีมเรียบร้อยแล้ว")
        grouped = df['ทีม'].value_counts().sort_index()
        st.dataframe(grouped.rename("จำนวนสมาชิก"))

        st.subheader("📋 รายชื่อสมาชิกแต่ละทีม")
        for team in sorted(df['ทีม'].unique(), key=lambda x: (x[0], int(x[1:]))):
            team_df = df[df['ทีม'] == team][['ชื่อเต็ม', 'Total']]
            st.markdown(f"### ทีม {team} | สาย {team[0]}")
            st.dataframe(team_df.reset_index(drop=True), use_container_width=True)

        # ดาวน์โหลดผลลัพธ์
        output = df[['ชื่อเต็ม', 'Total', 'ทีม', 'สาย']]
        csv = output.to_csv(index=False).encode('utf-8-sig')
        st.download_button("⬇️ ดาวน์โหลดผลลัพธ์ (CSV)", data=csv, file_name="ทีมที่จัดแล้ว.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
