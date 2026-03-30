# bot/config.py

# --- ACCOUNT SETUP ---
IG_USERNAME = "Penguin.3918654"
IG_PASSWORD = "ใส่รหัสผ่านตรงนี้"

# --- PATH SETUP ---
TARGET_FACE = "../target.jpg"
INPUT_IMAGE = "../following.jpg"
REPORT_FILE = "../data/report.json"
TEMP_DIR = "temp_img"

# --- SYSTEM LIMITS (กันโดนแบนและเครื่องค้าง) ---
SLEEP_BETWEEN_USERS = 30  # พัก 30 วินาทีต่อคน (กัน IG แบน)
SIMILARITY_SCORE = 0.85   # ความแม่นยำ AI (85%)

