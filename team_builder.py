
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Team Auto-Assignment", layout="wide")

st.title("ระบบจัดทีมอัตโนมัติ (แบบ Snake Draft)")

sheet_url = st.text_input("🔗 วางลิงก์ Google Sheets (.csv format)", 
    value="https://docs.google.com/spreadsheets/d/1jNPyTl3R9rg7TEaYxcLpN2Ae-QUs3Are/export?format=csv&gid=869418635")

if st.button("🚀 Load & Generate Teams"):
    try:
        df = pd.read_csv(sheet_url)

        # รวมชื่อ
        df['ชื่อเต็ม'] = df['First Name'].astype(str) + " " + df['Last Name'].astype(str) + " (" + df['Nickname'].astype(str) + ")"
        df = df.sort_values(by='Total', ascending=False).reset_index(drop=True)

        # Snake draft
        teams = []
        direction = 1
        for i in range(0, len(df), 50):
            block = list(range(50)) if direction == 1 else list(reversed(range(50)))
            teams.extend(block[:min(50, len(df) - i)])
            direction *= -1
        df['ทีมที่'] = [f"ทีม {i+1}" for i in teams]
        df['สาย'] = [chr(65 + (i // 5)) for i in teams]  # A–J

        # สรุปข้อมูล
        st.success("จัดทีมเรียบร้อยแล้ว")
        grouped = df.groupby('ทีมที่')[['Total']].count().rename(columns={'Total': 'จำนวนสมาชิก'})
        st.dataframe(grouped)

        st.subheader("📋 รายชื่อสมาชิกแต่ละทีม")
        for team in sorted(df['ทีมที่'].unique(), key=lambda x: int(x.split()[1])):
            team_df = df[df['ทีมที่'] == team][['ชื่อเต็ม', 'Total']]
            st.markdown(f"### {team}")
            st.dataframe(team_df.reset_index(drop=True), use_container_width=True)

        # ดาวน์โหลดผลลัพธ์
        output = df[['ชื่อเต็ม', 'Total', 'ทีมที่', 'สาย']]
        csv = output.to_csv(index=False).encode('utf-8-sig')
        st.download_button("⬇️ ดาวน์โหลดผลลัพธ์ (CSV)", data=csv, file_name="ทีมที่จัดแล้ว.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
