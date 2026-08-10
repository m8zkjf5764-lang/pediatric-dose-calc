import streamlit as st

# ตั้งค่าหน้าตาของเว็บ
st.set_page_config(
    page_title="Pediatric Dose Calculator", page_icon="💊", layout="centered"
)

# ==========================================
# 1. ฐานข้อมูลยาเด็กครบทุกตัว (55 รายการ)
# ==========================================
medications = {
    # ----------------------------------------------------
    # Group 1: Analgesics & Antipyretics (ยาแก้ปวด ลดไข้)
    # ----------------------------------------------------
    "Acetaminophen (Paracetamol)": {
        "type": "weight_dose",
        "min_mg_kg": 10,
        "max_mg_kg": 15,
        "max_daily_mg_kg": 75,
        "freq": "ทุก 4-6 ชั่วโมง เวลาที่มีไข้หรือปวด",
    },
    "Ibuprofen": {
        "type": "weight_dose",
        "min_mg_kg": 5,
        "max_mg_kg": 10,
        "max_daily_mg_kg": 40,
        "freq": "ทุก 6-8 ชั่วโมง พร้อมหรือหลังอาหารทันที",
    },
    "Diclofenac": {
        "type": "weight_day",
        "min_mg_kg_day": 2,
        "max_mg_kg_day": 3,
        "max_daily_mg": 200,
        "default_doses": 3,
        "freq": "วันละ 2-4 ครั้ง หลังอาหารทันที",
    },
    # ----------------------------------------------------
    # Group 2: Antimicrobial agents (ยาฆ่าเชื้อ / ยาปฏิชีวนะ)
    # ----------------------------------------------------
    "Penicillin V (< 12 ปี)": {
        "type": "weight_day",
        "min_mg_kg_day": 25,
        "max_mg_kg_day": 50,
        "max_daily_mg": 3000,
        "default_doses": 4,
        "freq": "วันละ 3-4 ครั้ง ก่อนอาหาร 30 นาที",
    },
    "Amoxicillin (General Dose)": {
        "type": "weight_day",
        "min_mg_kg_day": 20,
        "max_mg_kg_day": 50,
        "max_single_mg": 500,
        "default_doses": 3,
        "freq": "วันละ 2-3 ครั้ง หลังอาหาร",
    },
    "Amoxicillin (High Dose - Otitis Media)": {
        "type": "weight_day",
        "min_mg_kg_day": 80,
        "max_mg_kg_day": 90,
        "max_single_mg": 500,
        "default_doses": 2,
        "freq": "วันละ 2 ครั้ง หลังอาหาร",
    },
    "Amoxicillin + Clavulanic acid": {
        "type": "weight_day",
        "min_mg_kg_day": 20,
        "max_mg_kg_day": 50,
        "max_single_mg": 500,
        "default_doses": 2,
        "freq": "วันละ 2 ครั้ง หลังอาหาร",
    },
    "Cloxacillin (> 1 เดือน)": {
        "type": "weight_day",
        "min_mg_kg_day": 50,
        "max_mg_kg_day": 100,
        "max_daily_mg": 4000,
        "default_doses": 4,
        "freq": "วันละ 3-4 ครั้ง ก่อนอาหาร 30 นาที",
    },
    "Dicloxacillin (General Dose)": {
        "type": "weight_day",
        "min_mg_kg_day": 25,
        "max_mg_kg_day": 50,
        "max_single_mg": 500,
        "default_doses": 4,
        "freq": "วันละ 3-4 ครั้ง ก่อนอาหาร 30 นาที",
    },
    "Dicloxacillin (High Dose)": {
        "type": "weight_day",
        "min_mg_kg_day": 50,
        "max_mg_kg_day": 100,
        "max_single_mg": 500,
        "default_doses": 4,
        "freq": "วันละ 3-4 ครั้ง ก่อนอาหาร 30 นาที",
    },
    "Cephalexin (General Dose)": {
        "type": "weight_day",
        "min_mg_kg_day": 25,
        "max_mg_kg_day": 50,
        "max_daily_mg": 2000,
        "default_doses": 3,
        "freq": "วันละ 2-4 ครั้ง หลังอาหาร",
    },
    "Cephalexin (High Dose)": {
        "type": "weight_day",
        "min_mg_kg_day": 75,
        "max_mg_kg_day": 100,
        "max_daily_mg": 4000,
        "default_doses": 4,
        "freq": "วันละ 3-4 ครั้ง หลังอาหาร",
    },
    "Cefuroxime (3 เดือน - 12 ปี)": {
        "type": "weight_day",
        "min_mg_kg_day": 20,
        "max_mg_kg_day": 30,
        "max_single_mg": 500,
        "default_doses": 2,
        "freq": "วันละ 2 ครั้ง หลังอาหาร",
    },
    "Cefaclor (> 1 เดือน)": {
        "type": "weight_day",
        "min_mg_kg_day": 20,
        "max_mg_kg_day": 40,
        "max_daily_mg": 1500,
        "default_doses": 3,
        "freq": "วันละ 2-3 ครั้ง หลังอาหาร",
    },
    "Cefdinir (6 เดือน - 12 ปี)": {
        "type": "weight_day",
        "min_mg_kg_day": 14,
        "max_mg_kg_day": 14,
        "max_daily_mg": 600,
        "default_doses": 2,
        "freq": "วันละ 1-2 ครั้ง หลังอาหาร",
    },
    "Cefixime (>= 6 เดือน)": {
        "type": "weight_day",
        "min_mg_kg_day": 8,
        "max_mg_kg_day": 20,
        "max_daily_mg": 400,
        "default_doses": 2,
        "freq": "วันละ 1-2 ครั้ง หลังอาหาร",
    },
    "Cefditoren pivoxil (>= 12 ปี)": {
        "type": "weight_day",
        "min_mg_kg_day": 10,
        "max_mg_kg_day": 20,
        "default_doses": 3,
        "freq": "วันละ 2-3 ครั้ง หลังอาหาร (หรือ 200-400 mg/dose bid)",
    },
    "Erythromycin Base/Estolate/Stearate": {
        "type": "weight_day",
        "min_mg_kg_day": 30,
        "max_mg_kg_day": 50,
        "max_daily_mg": 2000,
        "default_doses": 4,
        "freq": "วันละ 2-4 ครั้ง ก่อนอาหาร 1 ชม.",
    },
    "Erythromycin Ethylsuccinate": {
        "type": "weight_day",
        "min_mg_kg_day": 30,
        "max_mg_kg_day": 50,
        "max_daily_mg": 3200,
        "default_doses": 4,
        "freq": "วันละ 2-4 ครั้ง หลังอาหาร",
    },
    "Azithromycin (>= 6 เดือน - 3-day course)": {
        "type": "weight_day",
        "min_mg_kg_day": 5,
        "max_mg_kg_day": 12,
        "max_single_mg": 500,
        "default_doses": 1,
        "freq": "วันละ 1 ครั้ง ทานติดต่อกัน 3 วัน (ก่อน/หลังอาหาร)",
    },
    "Roxithromycin": {
        "type": "weight_day",
        "min_mg_kg_day": 5,
        "max_mg_kg_day": 8,
        "max_daily_mg": 300,
        "default_doses": 2,
        "freq": "วันละ 2 ครั้ง ก่อนอาหาร",
    },
    "Clarithromycin (>= 6 เดือน)": {
        "type": "weight_day",
        "min_mg_kg_day": 15,
        "max_mg_kg_day": 15,
        "max_daily_mg": 500,
        "default_doses": 2,
        "freq": "วันละ 2 ครั้ง หลังอาหาร",
    },
    "Co-trimoxazole (TMP+SMX)": {
        "type": "weight_day",
        "min_mg_kg_day": 8,
        "max_mg_kg_day": 8,
        "max_daily_mg": 320,
        "default_doses": 2,
        "note": "คิดตามขนาด Trimethoprim (TMP)",
        "freq": "วันละ 2 ครั้ง หลังอาหาร",
    },
    # ----------------------------------------------------
    # Group 3: Respiratory drugs (ยาทางเดินหายใจ / แก้ไอ / แก้แพ้)
    # ----------------------------------------------------
    "Brompheniramine maleate": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 0.125,
                "is_per_kg": True,
                "max_daily": 8,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 2.0,
                "is_per_kg": False,
                "max_daily": 16,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 4.0,
                "is_per_kg": False,
                "max_daily": 24,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
        ],
    },
    "Chlorpheniramine maleate (CPM)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 1.0,
                "is_per_kg": False,
                "max_daily": 8,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 2.0,
                "is_per_kg": False,
                "max_daily": 12,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 4.0,
                "is_per_kg": False,
                "max_daily": 24,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
        ],
    },
    "Diphenhydramine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 6.25,
                "is_per_kg": False,
                "max_daily": 75,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 12.5,
                "is_per_kg": False,
                "max_daily": 150,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 25.0,
                "is_per_kg": False,
                "max_daily": 300,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
        ],
    },
    "Hydroxyzine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 0,
                "max_m": 71,
                "mg": 12.5,
                "is_per_kg": False,
                "max_daily": 50,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 999,
                "mg": 12.5,
                "is_per_kg": False,
                "max_daily": 100,
                "freq": "ทุก 6-8 ชั่วโมง (ถ้าหนัก >40 kg ทาน 25-50 mg)",
            },
        ],
    },
    "Cetirizine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 11,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 2.5,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 12,
                "max_m": 23,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 5.0,
                "freq": "วันละ 1-2 ครั้ง",
            },
            {
                "min_m": 24,
                "max_m": 60,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 5.0,
                "freq": "วันละ 1-2 ครั้ง",
            },
            {
                "min_m": 61,
                "max_m": 144,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 10.0,
                "freq": "วันละ 1-2 ครั้ง",
            },
            {
                "min_m": 145,
                "max_m": 999,
                "mg": 10.0,
                "is_per_kg": False,
                "max_daily": 40.0,
                "freq": "วันละ 1 ครั้ง",
            },
        ],
    },
    "Levocetirizine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 60,
                "mg": 1.25,
                "is_per_kg": False,
                "max_daily": 1.25,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 61,
                "max_m": 144,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 2.5,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 145,
                "max_m": 999,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 20.0,
                "freq": "วันละ 1 ครั้ง",
            },
        ],
    },
    "Loratadine (>= 2 ปี)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 60,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 5.0,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 61,
                "max_m": 999,
                "mg": 10.0,
                "is_per_kg": False,
                "max_daily": 10.0,
                "freq": "วันละ 1 ครั้ง",
            },
        ],
    },
    "Desloratadine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 11,
                "mg": 1.0,
                "is_per_kg": False,
                "max_daily": 1.0,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 12,
                "max_m": 60,
                "mg": 1.25,
                "is_per_kg": False,
                "max_daily": 1.25,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 61,
                "max_m": 144,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 2.5,
                "freq": "วันละ 1 ครั้ง",
            },
            {
                "min_m": 145,
                "max_m": 999,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 20.0,
                "freq": "วันละ 1 ครั้ง",
            },
        ],
    },
    "Fexofenadine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 23,
                "mg": 15.0,
                "is_per_kg": False,
                "max_daily": 30,
                "freq": "วันละ 2 ครั้ง",
            },
            {
                "min_m": 24,
                "max_m": 143,
                "mg": 30.0,
                "is_per_kg": False,
                "max_daily": 60,
                "freq": "วันละ 2 ครั้ง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 60.0,
                "is_per_kg": False,
                "max_daily": 720,
                "freq": "วันละ 2 ครั้ง (หรือ 180 mg od)",
            },
        ],
    },
    "Ketotifen (>= 6 เดือน)": {
        "type": "weight_dose",
        "min_mg_kg": 0.25,
        "max_mg_kg": 0.25,
        "max_single_mg": 1,
        "freq": "วันละ 2 ครั้ง",
    },
    "Montelukast": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 60,
                "mg": 4.0,
                "is_per_kg": False,
                "max_daily": 4.0,
                "freq": "วันละ 1 ครั้ง ก่อนนอน",
            },
            {
                "min_m": 61,
                "max_m": 179,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 5.0,
                "freq": "วันละ 1 ครั้ง ก่อนนอน",
            },
            {
                "min_m": 180,
                "max_m": 999,
                "mg": 10.0,
                "is_per_kg": False,
                "max_daily": 10.0,
                "freq": "วันละ 1 ครั้ง ก่อนนอน",
            },
        ],
    },
    "Phenylephrine HCl": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 48,
                "max_m": 71,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 15,
                "freq": "ทุก 4 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 30,
                "freq": "ทุก 4 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 10.0,
                "is_per_kg": False,
                "max_daily": 60,
                "freq": "ทุก 4 ชั่วโมง",
            },
        ],
    },
    "Pseudoephedrine": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 15.0,
                "is_per_kg": False,
                "max_daily": 60,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 30.0,
                "is_per_kg": False,
                "max_daily": 120,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 60.0,
                "is_per_kg": False,
                "max_daily": 240,
                "freq": "ทุก 4-6 ชั่วโมง",
            },
        ],
    },
    "Glyceryl guaiacolate (Guaifenesin)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 50.0,
                "is_per_kg": False,
                "max_daily": 600,
                "freq": "ทุก 4 ชั่วโมง (วันละไม่เกิน 6 ครั้ง)",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 100.0,
                "is_per_kg": False,
                "max_daily": 1200,
                "freq": "ทุก 4 ชั่วโมง (วันละไม่เกิน 6 ครั้ง)",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 200.0,
                "is_per_kg": False,
                "max_daily": 2400,
                "freq": "ทุก 4 ชั่วโมง (วันละไม่เกิน 6 ครั้ง)",
            },
        ],
    },
    "Acetylcysteine": {
        "type": "weight_day",
        "min_mg_kg_day": 20,
        "max_mg_kg_day": 30,
        "max_daily_mg": 600,
        "default_doses": 3,
        "freq": "วันละ 2-3 ครั้ง หลังอาหาร",
    },
    "Ambroxol": {
        "type": "weight_day",
        "min_mg_kg_day": 1.2,
        "max_mg_kg_day": 1.6,
        "default_doses": 3,
        "freq": "วันละ 2-3 ครั้ง หลังอาหาร",
    },
    "Carbocysteine": {
        "type": "weight_day",
        "min_mg_kg_day": 15,
        "max_mg_kg_day": 20,
        "default_doses": 3,
        "freq": "วันละ 3 ครั้ง หลังอาหาร",
    },
    "Bromhexine": {
        "type": "weight_day",
        "min_mg_kg_day": 0.6,
        "max_mg_kg_day": 0.8,
        "max_daily_mg": 48,
        "default_doses": 3,
        "freq": "วันละ 3 ครั้ง หลังอาหาร",
    },
    "Dextromethorphan (>= 4 ปี)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 48,
                "max_m": 71,
                "mg": 2.5,
                "is_per_kg": False,
                "max_daily": 30,
                "freq": "ทุก 4 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 5.0,
                "is_per_kg": False,
                "max_daily": 60,
                "freq": "ทุก 4 ชั่วโมง",
            },
            {
                "min_m": 144,
                "max_m": 999,
                "mg": 20.0,
                "is_per_kg": False,
                "max_daily": 120,
                "freq": "ทุก 4 ชั่วโมง",
            },
        ],
    },
    "Salbutamol": {
        "type": "weight_dose",
        "min_mg_kg": 0.1,
        "max_mg_kg": 0.2,
        "max_daily_mg": 12,
        "freq": "วันละ 3 ครั้ง",
    },
    "Terbutaline sulfate": {
        "type": "weight_dose",
        "min_mg_kg": 0.05,
        "max_mg_kg": 0.05,
        "max_daily_mg": 15,
        "freq": "วันละ 3 ครั้ง",
    },
    "Procaterol (Meptin syr. 5 mcg/ml)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 0,
                "max_m": 11,
                "mg": 0.010,
                "is_per_kg": False,
                "max_daily": 0.030,
                "freq": "วันละ 2 ครั้ง (10-15 mcg/dose)",
            },
            {
                "min_m": 12,
                "max_m": 23,
                "mg": 0.015,
                "is_per_kg": False,
                "max_daily": 0.040,
                "freq": "วันละ 2 ครั้ง (15-20 mcg/dose)",
            },
            {
                "min_m": 24,
                "max_m": 59,
                "mg": 0.020,
                "is_per_kg": False,
                "max_daily": 0.050,
                "freq": "วันละ 2 ครั้ง (20-25 mcg/dose)",
            },
            {
                "min_m": 60,
                "max_m": 999,
                "mg": 0.025,
                "is_per_kg": False,
                "max_daily": 0.050,
                "freq": "วันละ 1-2 ครั้ง (25 mcg/dose)",
            },
        ],
    },
    # ----------------------------------------------------
    # Group 4: Gastrointestinal drugs (ยาทางเดินอาหาร)
    # ----------------------------------------------------
    "Dimenhydrinate (2-11 ปี)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 71,
                "mg": 15.0,
                "is_per_kg": False,
                "max_daily": 75,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
            {
                "min_m": 72,
                "max_m": 143,
                "mg": 25.0,
                "is_per_kg": False,
                "max_daily": 150,
                "freq": "ทุก 6-8 ชั่วโมง",
            },
        ],
    },
    "Domperidone (< 35 kg)": {
        "type": "weight_day",
        "min_mg_kg_day": 0.75,
        "max_mg_kg_day": 0.75,
        "max_daily_mg": 30,
        "default_doses": 3,
        "freq": "วันละ 3 ครั้ง ก่อนอาหาร 15-30 นาที",
    },
    "Dicyclomine (>= 6 เดือน)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 23,
                "mg": 5.0,
                "is_per_kg": False,
                "freq": "วันละ 3-4 ครั้ง ก่อนอาหาร",
            },
            {
                "min_m": 24,
                "max_m": 999,
                "mg": 10.0,
                "is_per_kg": False,
                "freq": "วันละ 3 ครั้ง ก่อนอาหาร",
            },
        ],
    },
    "Hyoscine (>= 6 เดือน)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 6,
                "max_m": 11,
                "mg": 5.0,
                "is_per_kg": False,
                "freq": "วันละ 3 ครั้ง",
            },
            {
                "min_m": 12,
                "max_m": 71,
                "mg": 5.0,
                "is_per_kg": False,
                "freq": "วันละ 3 ครั้ง",
            },
        ],
    },
    "Simethicone (< 2 ปี)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 0,
                "max_m": 23,
                "mg": 20.0,
                "is_per_kg": False,
                "max_daily": 500,
                "freq": "วันละ 3-4 ครั้ง หลังอาหารและก่อนนอน",
            },
            {
                "min_m": 24,
                "max_m": 143,
                "mg": 40.0,
                "is_per_kg": False,
                "max_daily": 500,
                "freq": "วันละ 3-4 ครั้ง หลังอาหารและก่อนนอน",
            },
        ],
    },
    "Al(OH)3 + Mg(OH)2 (Alum milk)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 0,
                "max_m": 1,
                "mg": 1.0,
                "is_per_kg": True,
                "freq": "ตามแพทย์สั่ง (ml/kg/dose)",
            },
            {
                "min_m": 2,
                "max_m": 11,
                "mg": 3.5,
                "is_per_kg": False,
                "freq": "หลังอาหาร 1-3 ชม. และก่อนนอน (2.5 - 5 ml/dose)",
            },
            {
                "min_m": 12,
                "max_m": 60,
                "mg": 10.0,
                "is_per_kg": False,
                "freq": "หลังอาหาร 1-3 ชม. และก่อนนอน (5 - 15 ml/dose)",
            },
            {
                "min_m": 61,
                "max_m": 144,
                "mg": 30.0,
                "is_per_kg": False,
                "freq": "หลังอาหาร 1-3 ชม. และก่อนนอน (15 - 45 ml/dose)",
            },
        ],
    },
    "Lactulose (Laevolac)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 1,
                "max_m": 71,
                "mg": 7.5,
                "is_per_kg": False,
                "freq": "วันละ 1 ครั้ง (5 - 10 ml/day)",
            },
            {
                "min_m": 72,
                "max_m": 168,
                "mg": 15.0,
                "is_per_kg": False,
                "freq": "วันละ 1 ครั้ง (15 ml/day)",
            },
            {
                "min_m": 169,
                "max_m": 999,
                "mg": 22.5,
                "is_per_kg": False,
                "freq": "วันละ 1 ครั้ง (15 - 30 ml/day)",
            },
        ],
    },
    "Metronidazole": {
        "type": "weight_day",
        "min_mg_kg_day": 35,
        "max_mg_kg_day": 50,
        "max_daily_mg": 2250,
        "default_doses": 3,
        "freq": "วันละ 3 ครั้ง หลังอาหาร",
    },
    "Albendazole (พยาธิเข็มหมุด/พยาธิไส้เดือน)": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 12,
                "max_m": 23,
                "mg": 200.0,
                "is_per_kg": False,
                "freq": "รับประทานครั้งเดียว (Single Dose)",
            },
            {
                "min_m": 24,
                "max_m": 999,
                "mg": 400.0,
                "is_per_kg": False,
                "freq": "รับประทานครั้งเดียว (Single Dose)",
            },
        ],
    },
    "Mebendazole": {
        "type": "age_fixed",
        "rules": [
            {
                "min_m": 24,
                "max_m": 999,
                "mg": 100.0,
                "is_per_kg": False,
                "freq": "วันละ 2 ครั้ง ติดต่อกัน 3 วัน (หรือ 500 mg Single Dose)",
            }
        ],
    },
}


def get_ml_and_tsp(mg_dose, conc_mg, conc_ml):
    conc_per_ml = conc_mg / conc_ml
    ml = mg_dose / conc_per_ml
    tsp = ml / 5.0
    return ml, tsp


# ==========================================
# 2. ส่วนแสดงผล UI ด้วย Streamlit
# ==========================================
st.title("💊 Pediatric Dose Calculator")
st.subheader("โปรแกรมคำนวณขนาดยาน้ำเด็กอภินันทนาการ")

# Dropdown เลือกยา
selected_med_name = st.selectbox(
    "เลือกรายการยาที่ต้องการคำนวณ:", list(medications.keys())
)
med = medications[selected_med_name]

st.divider()

# กรอกข้อมูลความเข้มข้นข้างขวด
st.markdown("### 1. ข้อมูลความเข้มข้นยาข้างขวด")
col1, col2 = st.columns(2)
with col1:
    conc_mg = st.number_input(
        "ปริมาณตัวยา (mg หรือ mcg)", value=120.0, step=10.0
    )
with col2:
    conc_ml = st.number_input("ปริมาตรยาน้ำ (mL)", value=5.0, step=1.0)

st.markdown("### 2. ข้อมูลผู้ป่วยเด็ก")

# แสดง Input ตามประเภทการคำนวณของยา
if med["type"] in ["weight_dose", "weight_day"]:
    weight = st.number_input(
        "น้ำหนักเด็ก (kg)", value=10.0, step=0.5, min_value=0.1
    )
    if med["type"] == "weight_day":
        doses_per_day = st.number_input(
            "จำนวนมื้อต่อวัน",
            value=int(med.get("default_doses", 3)),
            step=1,
            min_value=1,
        )

elif med["type"] == "age_fixed":
    age_months = st.number_input(
        "อายุเด็ก (จำนวนเดือน)", value=24.0, step=1.0, min_value=0.0
    )
    # เช็กว่ามีกฎที่ต้องใช้น้ำหนักด้วยหรือไม่
    needs_weight = any(r.get("is_per_kg", False) for r in med["rules"])
    if needs_weight:
        weight = st.number_input(
            "น้ำหนักเด็ก (kg)", value=10.0, step=0.5, min_value=0.1
        )

# ปุ่มคำนวณ
if st.button("🧮 คำนวณขนาดยา", type="primary"):
    st.divider()
    st.markdown("### 📊 ผลการคำนวณ")

    if med["type"] == "weight_dose":
        dose_min_mg = weight * med["min_mg_kg"]
        dose_max_mg = weight * med["max_mg_kg"]

        if "max_single_mg" in med and dose_max_mg > med["max_single_mg"]:
            dose_max_mg = med["max_single_mg"]

        ml_min, tsp_min = get_ml_and_tsp(dose_min_mg, conc_mg, conc_ml)
        ml_max, tsp_max = get_ml_and_tsp(dose_max_mg, conc_mg, conc_ml)

        st.info(f"**วิธีรับประทาน:** {med['freq']}")
        st.success(
            f"""
        - **ปริมาณตัวยาต่อครั้ง:** {dose_min_mg:.2f} - {dose_max_mg:.2f} mg/dose
        - **ปริมาตรยาน้ำ:** **{ml_min:.1f} - {ml_max:.1f} mL** ต่อครั้ง
        - **คิดเป็นช้อนชาประมาณ:** {tsp_min:.1f} - {tsp_max:.1f} ช้อนชา
        """
        )

    elif med["type"] == "weight_day":
        total_day_min = weight * med["min_mg_kg_day"]
        total_day_max = weight * med["max_mg_kg_day"]

        if "max_daily_mg" in med and total_day_max > med["max_daily_mg"]:
            total_day_max = med["max_daily_mg"]
            st.warning(
                f"⚠️ ปรับลดขนาดยารวมไม่ให้เกิน Limit สูงสุด {med['max_daily_mg']} mg/day"
            )

        dose_min_mg = total_day_min / doses_per_day
        dose_max_mg = total_day_max / doses_per_day

        if "max_single_mg" in med and dose_max_mg > med["max_single_mg"]:
            dose_max_mg = med["max_single_mg"]

        ml_min, tsp_min = get_ml_and_tsp(dose_min_mg, conc_mg, conc_ml)
        ml_max, tsp_max = get_ml_and_tsp(dose_max_mg, conc_mg, conc_ml)

        st.info(f"**วิธีรับประทาน:** {med['freq']}")
        st.success(
            f"""
        - **ยารวมทั้งวัน:** {total_day_min:.1f} - {total_day_max:.1f} mg/day
        - **ตัวยาต่อครั้ง (แบ่ง {doses_per_day} มื้อ):** {dose_min_mg:.1f} - {dose_max_mg:.1f} mg/dose
        - **ปริมาตรยาน้ำ:** **{ml_min:.1f} - {ml_max:.1f} mL** ต่อครั้ง
        - **คิดเป็นช้อนชาประมาณ:** {tsp_min:.1f} - {tsp_max:.1f} ช้อนชา
        """
        )

    elif med["type"] == "age_fixed":
        matched_rule = None
        for rule in med["rules"]:
            if rule["min_m"] <= age_months <= rule["max_m"]:
                matched_rule = rule
                break

        if matched_rule:
            if matched_rule.get("is_per_kg", False):
                mg_dose = weight * matched_rule["mg"]
            else:
                mg_dose = matched_rule["mg"]

            ml, tsp = get_ml_and_tsp(mg_dose, conc_mg, conc_ml)

            st.info(f"**วิธีรับประทาน:** {matched_rule['freq']}")
            st.success(
                f"""
            - **ปริมาณตัวยาต่อครั้ง:** {mg_dose:.2f} mg/dose
            - **ปริมาตรยาน้ำ:** **{ml:.1f} mL** ต่อครั้ง
            - **คิดเป็นช้อนชาประมาณ:** {tsp:.1f} ช้อนชา
            """
            )
        else:
            st.error("❌ ขออภัย ช่วงอายุนี้ไม่อยู่ในเกณฑ์การใช้ยาที่ระบุในตาราง")
