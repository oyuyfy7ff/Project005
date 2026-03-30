# bot/main.py
import os
import time
import json
import gc
import pytesseract
from PIL import Image
from instagrapi import Client
from deepface import DeepFace
import config

# สร้างโฟลเดอร์ Temp ถ้ายังไม่มี
if not os.path.exists(config.TEMP_DIR):
    os.makedirs(config.TEMP_DIR)

def log(msg):
    time_str = time.strftime("%H:%M:%S")
    print(f"[{time_str}] {msg}")

def get_names_from_image():
    log("[*] เริ่มอ่านรายชื่อจากรูป (OCR)...")
    if not os.path.exists(config.INPUT_IMAGE):
        log("[!] ไม่พบไฟล์รูป following.jpg")
        return []
    try:
        text = pytesseract.image_to_string(Image.open(config.INPUT_IMAGE))
        lines = [line.strip() for line in text.split('\n') if line.strip() and " " not in line]
        log(f"[+] ได้รายชื่อมา {len(lines)} บัญชี")
        return lines
    except Exception as e:
        log(f"[!] OCR พัง: {e}")
        return []

def scan_user(cl, username):
    log(f"[*] เจาะข้อมูล: @{username}")
    try:
        user_info = cl.user_info_by_username(username)
        data = {
            "username": username,
            "full_name": user_info.full_name,
            "bio": user_info.biography,
            "is_private": user_info.is_private,
            "pk": user_info.pk,
            "matches": []
        }
        
        # ถ้าเปิด Public ให้ส่อง Story ทันที
        if not user_info.is_private:
            stories = cl.user_stories(user_info.pk)
            for story in stories:
                if story.media_type == 1: # ถ้าเป็นรูปภาพ
                    img_path = cl.photo_download(story.pk, folder=config.TEMP_DIR)
                    try:
                        # สแกนหน้า (enforce_detection=False เพื่อกัน AI error ถ้าไม่มีหน้าคน)
                        result = DeepFace.verify(config.TARGET_FACE, img_path, enforce_detection=False)
                        if result["verified"]:
                            data["matches"].append(story.thumbnail_url)
                            log(f"[!!!] เจอเป้าหมายในสตอรี่ของ @{username}")
                    except Exception as ai_err:
                        pass # ข้ามไปถ้า AI ประมวลผลรูปนี้ไม่ได้
                    finally:
                        # ลบรูปทิ้งทันที คืนพื้นที่ RAM และ Storage
                        if os.path.exists(img_path):
                            os.remove(img_path)
            
        return data
    except Exception as e:
        log(f"[!] ข้าม @{username} (Error: {e})")
        return None

def main():
    names = get_names_from_image()
    if not names: return

    cl = Client()
    try:
        log("[*] ล็อกอินเข้า Instagram...")
        cl.login(config.IG_USERNAME, config.IG_PASSWORD)
    except Exception as e:
        log(f"[!] ล็อกอินล้มเหลว: {e}")
        return

    report = []
    for user in names:
        result = scan_user(cl, user)
        if result:
            report.append(result)
            # Save ข้อมูลทุกครั้งที่สแกนเสร็จ 1 คน (กันระบบล่มกลางคัน)
            with open(config.REPORT_FILE, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=4)
        
        # คืน Memory ให้ระบบ
        gc.collect() 
        
        log(f"[*] พัก {config.SLEEP_BETWEEN_USERS} วิ หลบเรดาร์ IG...")
        time.sleep(config.SLEEP_BETWEEN_USERS)

    log("[+] ภารกิจเสร็จสิ้น ข้อมูลปลอดภัย!")

if __name__ == "__main__":
    main()
