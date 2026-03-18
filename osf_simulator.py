import sqlite3
import random
import time

def simulate_emotions():
    print("🚀 OSF Biometric Simulator Started...")
    while True:
        try:
            # เชื่อมต่อกับไฟล์ฐานข้อมูลของคุณ (แก้ชื่อไฟล์ให้ตรงถ้าตั้งชื่ออื่น)
            conn = sqlite3.connect('osf_network.db')
            cursor = conn.cursor()
            
            # สุ่มอัปเดตค่าอารมณ์ให้คนทั้ง 5 คน (ช่วง 0.1 ถึง 0.95)
            for node_id in range(1, 6):
                new_intensity = round(random.uniform(0.1, 0.95), 2)
                cursor.execute("""
                    UPDATE bio_metrics 
                    SET current_emotion_intensity = ?, last_update = CURRENT_TIMESTAMP 
                    WHERE node_id = ?
                """, (new_intensity, node_id))
            
            conn.commit()
            print(f"📊 Updated Biometrics at {time.strftime('%H:%M:%S')}")
            conn.close()
            
            time.sleep(2) # หน่วงเวลาอัปเดตทุก 2 วินาที
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    simulate_emotions()