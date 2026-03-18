import streamlit as st
import sqlite3
import plotly.graph_objects as go
import time

# ตั้งค่าหน้าจอ
st.set_page_config(page_title="OSF Monitoring", layout="wide")

def get_bio_data():
    conn = sqlite3.connect('osf_network.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT n.node_name, b.current_emotion_intensity 
        FROM nodes n JOIN bio_metrics b ON n.node_id = b.node_id
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def create_gauge(value, name):
    # ถ้าค่าอารมณ์สูงเกิน 0.8 (Trauma) ให้เข็มเป็นสีแดง ไม่งั้นเป็นสีฟ้า
    bar_color = "red" if value >= 0.8 else "royalblue"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': f"📡 {name}", 'font': {'size': 18}},
        gauge = {
            'axis': {'range': [0, 1]},
            'bar': {'color': bar_color},
            'steps': [
                {'range': [0, 0.8], 'color': "#e8f8f5"},
                {'range': [0.8, 1], 'color': "#f9ebea"}
            ],
            'threshold': {'line': {'color': "red", 'width': 4}, 'value': 0.8}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20))
    return fig

st.title("🌐 The Omnisync Fabric: Real-time Biometric Monitor")

# ใช้ st.empty() เพื่อสร้างพื้นที่อัปเดตข้อมูลทับที่เดิม
placeholder = st.empty()

with placeholder.container():
    data = get_bio_data()
    if data:
        cols = st.columns(5) # แบ่งเป็น 5 คอลัมน์สำหรับ 5 คน
        for i, (name, val) in enumerate(data):
            with cols[i]:
                st.plotly_chart(create_gauge(val, name), use_container_width=True)
                if val >= 0.8:
                    st.error(f"⚠️ {name}: Trauma Detected! [BLOCKED]")
                else:
                    st.success(f"✅ Status: Normal")

# สั่งให้ Streamlit รันโหลดหน้าเว็บใหม่ทุก 2 วินาที
time.sleep(2)
st.rerun()