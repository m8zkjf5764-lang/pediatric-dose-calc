import streamlit as st

st.set_page_config(page_title="โปรแกรมคำนวณยาสูตรเด็ก", page_icon="👶", layout="wide")

st.title("👶 โปรแกรมคำนวณขนาดขนาดยาสำหรับเด็ก (Pediatric Dose Calculator)")
st.caption("ระบบคำนวณขนาดยา ปริมาตร (ml) และช้อนชา พร้อมระบบตรวจเช็คเกณฑ์อายุ")

# --- Section 1: ข้อมูลผู้ป่วย ---
st.header("1. ข้อมูลผู้ป่วย")
col1, col2 = st.columns(2)

with col1:
    st.subheader("อายุผู้ป่วย")
    col_y, col_m = st.columns(2)
    with col_y:
        age_years = st.number_input("ปี (Years)", min_value=0, max_value=18, value=2, step=1)
    with col_m:
        age_months = st.number_input("เดือน (Months)", min_value=0, max_value=11, value=0, step=1)
    total_months = (age_years * 12) + age_months

with col2:
    st.subheader("น้ำหนักผู้ป่วย")
    weight_kg = st.number_input("น้ำหนัก (kg)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

st.write(f"👉 **สรุปข้อมูล:** อายุ **{age_years} ปี {age_months} เดือน** ({total_months} เดือน) | น้ำหนัก **{weight_kg:.1f} kg**")
st.markdown("---")

# --- Section 2: เลือกยาและความเข้มข้น ---
st.header("2. เลือกยาและความเข้มข้น")

drug_list = [
    # 1. Respiratory
    "Brompheniramine maleate", "Chlorpheniramine maleate", "Diphenhydramine", "Hydroxyzine",
    "Cetirizine", "Levocetirizine", "Loratadine", "Desloratadine", "Fexofenadine", "Ketotifen",
    "Montelukast", "Phenylephrine HCl", "Pseudoephedrine", "Glyceryl-guaiacolate (Guaifenesin)",
    "Acetylcysteine", "Ambroxol", "Carbocysteine", "Bromhexine", "Dextromethorphan",
    "Salbutamol", "Terbutaline sulfate", "Procaterol (Meptin syrup 5 mcg/ml)",
    # 2. GI
    "Dimenhydrinate", "Domperidone", "Dicyclomine", "Hyoscine", "Simethicone",
    "Al(OH)3 + Mg(OH)2 (Alum milk)", "Lactulose (Laevolac)", "Metronidazole",
    "Albendazole", "Mebendazole",
    # 3. Analgesic & Antipyretic
    "Acetaminophen", "Diclofenac", "Ibuprofen",
    # 4. Antimicrobial
    "Penicillin V", "Amoxicillin / Amoxicillin + Clavulanic acid", "Cloxacillin", "Dicloxacillin",
    "Cephalexin", "Cefuroxime", "Cefaclor", "Cefdinir", "Cefixime", "Cefditoren pivoxil",
    "Erythromycin", "Azithromycin", "Roxithromycin", "Clarithromycin", "Co-trimoxazole (TMP + SMX)"
]

selected_drug = st.selectbox("เลือกรายการยา:", drug_list)

col_conc1, col_conc2 = st.columns(2)
with col_conc1:
    conc_mg = st.number_input("ความเข้มข้นตัวยา (mg หรือ mcg):", min_value=0.0, value=125.0, step=0.5)
with col_conc2:
    conc_ml = st.number_input("ต่อปริมาตร (ml):", min_value=0.1, value=5.0, step=0.5)

st.markdown("---")

# --- Helper Functions สำหรับแปลงค่าและจัดฟอร์แมต ---
def calc_vol(dose_val):
    """แปลง mg/mcg เป็น ml และ ช้อนชา"""
    if dose_val is None or conc_mg <= 0:
        return "0", "0"
    if isinstance(dose_val, tuple):
        d_min, d_max = dose_val
        ml_min = (d_min * conc_ml) / conc_mg
        ml_max = (d_max * conc_ml) / conc_mg
        return f"{ml_min:.2f} - {ml_max:.2f}", f"{(ml_min/5):.2f} - {(ml_max/5):.2f}"
    else:
        ml = (dose_val * conc_ml) / conc_mg
        return f"{ml:.2f}", f"{(ml/5):.2f}"

def format_mg_str(dose_val, unit="mg"):
    if isinstance(dose_val, tuple):
        return f"{dose_val[0]:.2f} - {dose_val[1]:.2f} {unit}"
    return f"{dose_val:.2f} {unit}"

def render_compact_card(title, formula_ref, per_dose_val, freq_text, per_day_val=None, max_text="", unit="mg"):
    """ฟังก์ชันแสดงผลขนาดพอดีจอโทรศัพท์ ตัวอักษรไม่ใหญ่เกินไป"""
    st.markdown(f"#### {title}")
    st.markdown(f"📌 **สูตรที่ใช้คำนวณ:** `{formula_ref}`")
    
    # 1. แสดงขนาดยาต่อมื้อ (Per Dose)
    ml_dose, tsp_dose = calc_vol(per_dose_val)
    mg_dose_str = format_mg_str(per_dose_val, unit)
    
    st.info(f"""
    💊 **กินครั้งละ (Per dose):** **{mg_dose_str}**
    * 🧪 **ปริมาตร:** **{ml_dose} ml**
    * 🥄 **จำนวน:** **{tsp_dose} ช้อนชา**
    * ⏱️ **วิธีใช้/ความถี่:** {freq_text}
    """)
    
    # 2. แสดงขนาดยารวมต่อวัน (Per Day - ถ้ามี)
    if per_day_val is not None:
        ml_day, tsp_day = calc_vol(per_day_val)
        mg_day_str = format_mg_str(per_day_val, unit)
        st.success(f"🗓️ **ขนาดยารวมทั้งวัน (Per day):** **{mg_day_str}** ({ml_day} ml / {tsp_day} ช้อนชา)")
        
    if max_text:
        st.caption(f"⚠️ **ขนาดยาสูงสุด (Max dose):** {max_text}")

# --- Section 3: ประมวลผลและแสดงผลลัพธ์ ---
st.header(f"3. ผลการคำนวณ: {selected_drug}")

age_out_of_range = False
age_range_text = ""

# ==================== Logic การคำนวณยา 55 รายการ ====================

if selected_drug == "Acetaminophen":
    dose_min = 10 * weight_kg
    dose_max = 15 * weight_kg
    render_compact_card(
        title="⚖️ ผลการคำนวณตามน้ำหนัก (Weight-based dose)",
        formula_ref="10 - 15 mg/kg/dose ทุก 4-6 ชม.",
        per_dose_val=(dose_min, dose_max),
        freq_text="ทานทุก 4 - 6 ชั่วโมง เวลาปวดหรือมีไข้",
        max_text=f"ไม่เกิน 75 mg/kg/day (สูงสุดไม่เกิน {75*weight_kg:.1f} mg/วัน)"
    )

elif selected_drug == "Ibuprofen":
    dose_min = 5 * weight_kg
    dose_max = 10 * weight_kg
    render_compact_card(
        title="⚖️ ผลการคำนวณตามน้ำหนัก (Weight-based dose)",
        formula_ref="5 - 10 mg/kg/dose ทุก 6-8 ชม.",
        per_dose_val=(dose_min, dose_max),
        freq_text="ทานทุก 6 - 8 ชั่วโมง หลังอาหารทันที",
        max_text=f"ไม่เกิน 40 mg/kg/day (สูงสุดไม่เกิน {40*weight_kg:.1f} mg/วัน)"
    )

elif selected_drug == "Brompheniramine maleate":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", "0.125 mg/kg/dose ทุก 6-8 ชม.", 0.125 * weight_kg, "ทุก 6-8 ชม.", max_text="8 mg/day")
    elif 72 < total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "2 - 4 mg/dose ทุก 6-8 ชม.", (2, 4), "ทุก 6-8 ชม.", max_text="16 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", "4 - 8 mg/dose ทุก 6-8 ชม.", (4, 8), "ทุก 6-8 ชม.", max_text="24 mg/day")
    else:
        age_out_of_range, age_range_text = True, "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
    
    # mg/kg/day -> แบ่งทาน 3 ครั้ง (ทุก 8 ชม.)
    day_dose = 0.5 * weight_kg
    dose_per_meal = day_dose / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.5 mg/kg/day แบ่งทานวันละ 3 ครั้ง (ทุก 8 ชม.)", dose_per_meal, "ทานวันละ 3 ครั้ง (ทุก 8 ชม.)", per_day_val=day_dose)

elif selected_drug == "Chlorpheniramine maleate":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", "1 mg/dose ทุก 4-6 ชม.", 1.0, "ทุก 4-6 ชม.", max_text="8 mg/day")
    elif 72 < total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "2 mg/dose ทุก 4-6 ชม.", 2.0, "ทุก 4-6 ชม.", max_text="12 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", "4 mg/dose ทุก 4-6 ชม.", 4.0, "ทุก 4-6 ชม.", max_text="24 mg/day")
    else:
        age_out_of_range, age_range_text = True, "24 เดือนขึ้นไป"
    
    day_dose = 0.35 * weight_kg
    dose_per_meal = day_dose / 4 # คิดที่ 4 ครั้ง/วัน
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.35 mg/kg/day แบ่งทานวันละ 4 ครั้ง (ทุก 6 ชม.)", dose_per_meal, "ทานทุก 4-6 ชม. (เฉลี่ยวันละ 4 ครั้ง)", per_day_val=day_dose)

elif selected_drug == "Diphenhydramine":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", "6.25 - 12.5 mg ทุก 6-8 ชม.", (6.25, 12.5), "ทุก 6-8 ชม.", max_text="75 mg/day")
    elif 72 < total_months < 144:
        render_compact_card("📌 คำนวณตามอายุ", "12.5 - 25 mg ทุก 6-8 ชม.", (12.5, 25), "ทุก 6-8 ชม.", max_text="150 mg/day")
    elif total_months >= 144:
        render_compact_card("📌 คำนวณตามอายุ", "25 - 50 mg ทุก 6-8 ชม.", (25, 50), "ทุก 6-8 ชม.", max_text="300 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"
        
    day_dose = 5 * weight_kg
    dose_per_meal = day_dose / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "5 mg/kg/day แบ่งทานวันละ 3 ครั้ง (ทุก 8 ชม.)", dose_per_meal, "ทานทุก 6-8 ชม. (เฉลี่ยวันละ 3 ครั้ง)", per_day_val=day_dose)

elif selected_drug == "Hydroxyzine":
    if total_months < 72:
        render_compact_card("📌 คำนวณตามอายุ", "12.5 mg ทุก 6-8 ชม.", 12.5, "ทุก 6-8 ชม.")
    else:
        render_compact_card("📌 คำนวณตามอายุ", "12.5 - 25 mg ทุก 6-8 ชม.", (12.5, 25), "ทุก 6-8 ชม.")
        
    if weight_kg <= 40:
        day_dose = 2 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "2 mg/kg/day แบ่งทานวันละ 3 ครั้ง", day_dose / 3, "ทานวันละ 3 ครั้ง (ทุก 8 ชม.)", per_day_val=day_dose, max_text="50 mg/day")

elif selected_drug == "Cetirizine":
    if 6 <= total_months <= 11:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg วันละ 1 ครั้ง", 2.5, "วันละ 1 ครั้ง")
    elif 12 <= total_months <= 23:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg วันละ 1-2 ครั้ง", 2.5, "วันละ 1-2 ครั้ง", max_text="5 mg/day")
    elif 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 - 5 mg วันละ 1 ครั้ง", (2.5, 5.0), "วันละ 1 ครั้ง (หรือแบ่งทาน 2.5 mg เช้า-เย็น)", max_text="5 mg/day")
    elif 61 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "5 - 10 mg วันละ 1 ครั้ง", (5.0, 10.0), "วันละ 1 ครั้ง", max_text="10 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", "10 mg วันละ 1 ครั้ง", 10.0, "วันละ 1 ครั้ง", max_text="40 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"
        
    day_dose = 0.25 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.25 mg/kg/day วันละ 1 ครั้ง", day_dose, "วันละ 1 ครั้ง (หรือแบ่ง 2 มื้อ)", per_day_val=day_dose)

elif selected_drug == "Levocetirizine":
    if 6 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "1.25 mg วันละ 1 ครั้ง", 1.25, "วันละ 1 ครั้ง")
    elif 61 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg วันละ 1 ครั้ง", 2.5, "วันละ 1 ครั้ง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 - 5 mg วันละ 1 ครั้ง", (2.5, 5.0), "วันละ 1 ครั้ง", max_text="20 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Loratadine":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg วันละ 1 ครั้ง", 5.0, "วันละ 1 ครั้ง", max_text="10 mg/day")
    elif total_months >= 72:
        render_compact_card("📌 คำนวณตามอายุ", "10 mg วันละ 1 ครั้ง (หรือ 5 mg BID)", 10.0, "วันละ 1 ครั้ง หรือ 5 mg เช้า-เย็น", max_text="10 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"

elif selected_drug == "Desloratadine":
    if 6 <= total_months <= 11:
        render_compact_card("📌 คำนวณตามอายุ", "1 mg วันละ 1 ครั้ง", 1.0, "วันละ 1 ครั้ง")
    elif 12 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "1.25 mg วันละ 1 ครั้ง", 1.25, "วันละ 1 ครั้ง")
    elif 61 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg วันละ 1 ครั้ง", 2.5, "วันละ 1 ครั้ง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg วันละ 1 ครั้ง", 5.0, "วันละ 1 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Fexofenadine":
    if 6 <= total_months < 24:
        dose = 15.0 if weight_kg < 10.5 else 30.0
        render_compact_card("📌 คำนวณตามอายุ/น้ำหนัก", f"{dose} mg วันละ 2 ครั้ง", dose, "วันละ 2 ครั้ง (เช้า-เย็น)")
    elif 24 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "30 mg วันละ 2 ครั้ง", 30.0, "วันละ 2 ครั้ง (เช้า-เย็น)", max_text="60 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "60 mg วันละ 2 ครั้ง", 60.0, "วันละ 2 ครั้ง (เช้า-เย็น)", max_text="720 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Ketotifen":
    if total_months >= 72:
        p_dose = min(0.25 * weight_kg, 1.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.25 mg/kg/dose วันละ 2 ครั้ง", p_dose, "วันละ 2 ครั้ง (เช้า-เย็น)", max_text="1 mg/dose")
    else:
        age_out_of_range, age_range_text = True, "6 ปีขึ้นไป"

elif selected_drug == "Montelukast":
    if 6 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "4 mg วันละ 1 ครั้ง", 4.0, "วันละ 1 ครั้ง (ก่อนนอน)")
    elif 61 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg วันละ 1 ครั้ง", 5.0, "วันละ 1 ครั้ง (ก่อนนอน)")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", "10 mg วันละ 1 ครั้ง", 10.0, "วันละ 1 ครั้ง (ก่อนนอน)")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Phenylephrine HCl":
    if 48 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg ทุก 4 ชม.", 2.5, "ทุก 4 ชั่วโมง", max_text="15 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg ทุก 4 ชม.", 5.0, "ทุก 4 ชั่วโมง", max_text="30 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "10 mg ทุก 4 ชม.", 10.0, "ทุก 4 ชั่วโมง", max_text="60 mg/day")
    else:
        age_out_of_range, age_range_text = True, "4 ปีขึ้นไป"

elif selected_drug == "Pseudoephedrine":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "15 mg ทุก 4-6 ชม.", 15.0, "ทุก 4-6 ชม.", max_text="60 mg/day")
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "1 mg/kg/dose ทุก 4-6 ชม.", 1 * weight_kg, "ทุก 4-6 ชม.")
    elif 72 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "30 mg ทุก 4-6 ชม.", 30.0, "ทุก 4-6 ชม.", max_text="120 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", "60 mg ทุก 4-6 ชม.", 60.0, "ทุก 4-6 ชม.", max_text="240 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "50 - 100 mg ทุก 4 ชม.", (50, 100), "ทุก 4 ชั่วโมง")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "100 - 200 mg ทุก 4 ชม.", (100, 200), "ทุก 4 ชั่วโมง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "200 - 400 mg ทุก 4 ชม.", (200, 400), "ทุก 4 ชั่วโมง")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"
        
    day_dose = 12 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "12 mg/kg/day แบ่งทาน 3-4 ครั้ง/วัน", day_dose / 3, "ทานวันละ 3-4 ครั้ง", per_day_val=day_dose)

elif selected_drug == "Acetylcysteine":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", "50 - 100 mg วันละ 2-4 ครั้ง", (50, 100), "วันละ 2-4 ครั้ง")
    elif total_months > 72:
        render_compact_card("📌 คำนวณตามอายุ", "100 - 200 mg วันละ 3 ครั้ง", (100, 200), "วันละ 3 ครั้ง", max_text="600 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"
        
    day_min = 20 * weight_kg
    day_max = 30 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "20 - 30 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทานวันละ 3 ครั้ง", per_day_val=(day_min, day_max))

elif selected_drug == "Ambroxol":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "7.5 - 15 mg วันละ 3 ครั้ง", (7.5, 15.0), "วันละ 3 ครั้ง หลังอาหาร")
    elif 72 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "15 - 30 mg วันละ 2-3 ครั้ง", (15.0, 30.0), "วันละ 2-3 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "2 ถึง 12 ปี"
        
    day_min = 1.2 * weight_kg
    day_max = 1.6 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "1.2 - 1.6 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทานวันละ 3 ครั้ง", per_day_val=(day_min, day_max))

elif selected_drug == "Carbocysteine":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "200 - 500 mg/day แบ่งทาน 2-3 ครั้ง", (200/3, 500/3), "ทานวันละ 2-3 ครั้ง", per_day_val=(200, 500))
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "300 - 750 mg/day แบ่งทาน 3 ครั้ง", (300/3, 750/3), "ทานวันละ 3 ครั้ง", per_day_val=(300, 750))
    else:
        age_out_of_range, age_range_text = True, "2 ถึง 11 ปี"
        
    day_min = 15 * weight_kg
    day_max = 20 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "15 - 20 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทานวันละ 3 ครั้ง", per_day_val=(day_min, day_max))

elif selected_drug == "Bromhexine":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "2 mg วันละ 3 ครั้ง", 2.0, "วันละ 3 ครั้ง", max_text="8 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "4 - 8 mg วันละ 3 ครั้ง", (4.0, 8.0), "วันละ 3 ครั้ง", max_text="24 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "8 - 16 mg วันละ 3 ครั้ง", (8.0, 16.0), "วันละ 3 ครั้ง", max_text="48 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"
        
    day_min = 0.6 * weight_kg
    day_max = 0.8 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.6 - 0.8 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทานวันละ 3 ครั้ง", per_day_val=(day_min, day_max))

elif selected_drug == "Dextromethorphan":
    if 48 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 - 7.5 mg ทุก 4-8 ชม.", (2.5, 7.5), "ทุก 4-8 ชม.", max_text="30 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "5 - 10 mg ทุก 4 ชม.", (5.0, 10.0), "ทุก 4 ชม.", max_text="60 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", "20 mg ทุก 4 ชม.", 20.0, "ทุก 4 ชม.", max_text="120 mg/day")
    else:
        age_out_of_range, age_range_text = True, "4 ปีขึ้นไป"

elif selected_drug == "Salbutamol":
    if 24 <= total_months <= 72:
        p_dose = 0.1 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.1 - 0.2 mg/kg/dose วันละ 3 ครั้ง", p_dose, "วันละ 3 ครั้ง", max_text="12 mg/day")
    elif 84 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", "2 mg วันละ 3-4 ครั้ง", 2.0, "วันละ 3-4 ครั้ง", max_text="24 mg/day")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", "2 - 4 mg วันละ 3-4 ครั้ง", (2.0, 4.0), "วันละ 3-4 ครั้ง", max_text="32 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"

elif selected_drug == "Terbutaline sulfate":
    if total_months < 144:
        p_dose = 0.05 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.05 mg/kg/dose วันละ 3 ครั้ง", p_dose, "วันละ 3 ครั้ง", max_text="5 mg/day")
    elif 144 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", "2.5 mg วันละ 3 ครั้ง", 2.5, "วันละ 3 ครั้ง", max_text="7.5 mg/day")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg วันละ 3-4 ครั้ง", 5.0, "วันละ 3-4 ครั้ง", max_text="15 mg/day")

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    if total_months < 12:
        render_compact_card("📌 คำนวณตามอายุ", "10 - 15 mcg/dose วันละ 2 ครั้ง", (10.0, 15.0), "วันละ 2 ครั้ง (เช้า-ก่อนนอน)", max_text="30 mcg/day", unit="mcg")
    elif 12 <= total_months <= 24:
        render_compact_card("📌 คำนวณตามอายุ", "15 - 20 mcg/dose วันละ 2 ครั้ง", (15.0, 20.0), "วันละ 2 ครั้ง", max_text="40 mcg/day", unit="mcg")
    elif 36 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "20 - 25 mcg/dose วันละ 2 ครั้ง", (20.0, 25.0), "วันละ 2 ครั้ง", max_text="50 mcg/day", unit="mcg")
    elif 72 <= total_months <= 216:
        render_compact_card("📌 คำนวณตามอายุ", "25 mcg/dose วันละ 1-2 ครั้ง", 25.0, "วันละ 1-2 ครั้ง", max_text="50 mcg/day", unit="mcg")
    
    if total_months < 72:
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "1.25 mcg/kg/dose ทุก 12 ชม.", 1.25 * weight_kg, "ทุก 12 ชั่วโมง", unit="mcg")

elif selected_drug == "Dimenhydrinate":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", "15 - 25 mg ทุก 6-8 ชม.", (15.0, 25.0), "ทุก 6-8 ชม.", max_text="75 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", "25 - 50 mg ทุก 6-8 ชม.", (25.0, 50.0), "ทุก 6-8 ชม.", max_text="150 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ถึง 11 ปี"

elif selected_drug == "Domperidone":
    if weight_kg < 35:
        day_dose = min(0.75 * weight_kg, 30.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "0.75 mg/kg/day แบ่งทานวันละ 3 ครั้งก่อนอาหาร", day_dose / 3, "วันละ 3 ครั้ง ก่อนอาหาร 15-30 นาที", per_day_val=day_dose, max_text="30 mg/day")
    else:
        st.warning("น้ำหนักตั้งแต่ 35 kg ขึ้นไป แนะนำให้ใช้ขนาดยาผู้ใหญ่ (10 mg วันละ 3 ครั้งก่อนอาหาร)")

elif selected_drug == "Dicyclomine":
    if 6 <= total_months <= 24:
        render_compact_card("📌 คำนวณตามอายุ", "5 - 10 mg วันละ 3-4 ครั้งก่อนอาหาร", (5.0, 10.0), "วันละ 3-4 ครั้ง ก่อนอาหาร")
    elif total_months > 24:
        render_compact_card("📌 คำนวณตามอายุ", "10 mg วันละ 3-4 ครั้งก่อนอาหาร", 10.0, "วันละ 3-4 ครั้ง ก่อนอาหาร")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Hyoscine":
    if 6 <= total_months <= 12:
        render_compact_card("📌 คำนวณตามอายุ", "5 mg วันละ 3-4 ครั้ง", 5.0, "วันละ 3-4 ครั้ง")
    elif 12 < total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", "5 - 10 mg วันละ 3-4 ครั้ง", (5.0, 10.0), "วันละ 3-4 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "6 เดือน ถึง 6 ปี"

elif selected_drug == "Simethicone":
    if total_months < 24:
        render_compact_card("📌 คำนวณตามอายุ", "20 mg วันละ 3-4 ครั้งหลังอาหาร/ก่อนนอน", 20.0, "วันละ 3-4 ครั้ง", max_text="500 mg/day")
    elif 24 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", "40 mg วันละ 3-4 ครั้งหลังอาหาร/ก่อนนอน", 40.0, "วันละ 3-4 ครั้ง", max_text="500 mg/day")

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    if total_months <= 1:
        ml = 1 * weight_kg
        st.info(f"📌 **สูตร:** 1 ml/kg/dose -> **ทานครั้งละ {ml:.2f} ml ({(ml/5):.2f} ช้อนชา)**")
    elif 1 < total_months <= 12:
        st.info("📌 **สูตร:** 2 - 5 ml/dose วันละ 4 ครั้งหลังอาหาร 1 ชม. และก่อนนอน")
    elif 12 < total_months <= 60:
        st.info("📌 **สูตร:** 5 - 15 ml/dose วันละ 4 ครั้งหลังอาหาร 1 ชม. และก่อนนอน")
    elif 72 <= total_months <= 144:
        st.info("📌 **สูตร:** 15 - 45 ml/dose วันละ 4 ครั้งหลังอาหาร 1 ชม. และก่อนนอน")

elif selected_drug == "Lactulose (Laevolac)":
    if 1 <= total_months <= 72:
        st.info("📌 **ตามอายุ:** 5 - 10 ml/day วันละ 1 ครั้ง มื้อเช้า")
        day_dose = 1.5 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "1 - 2 g/kg/day วันละ 1 ครั้ง", day_dose, "วันละ 1 ครั้ง หลังอาหารเช้า", per_day_val=day_dose)
    elif 72 < total_months <= 168:
        st.info("📌 **ตามอายุ:** 15 ml/day วันละ 1 ครั้ง มื้อเช้า")
    elif total_months > 168:
        st.info("📌 **ตามอายุ:** 15 - 30 ml/day วันละ 1 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "1 เดือนขึ้นไป"

elif selected_drug == "Metronidazole":
    day_ameba = min(35 * weight_kg, 2250.0)
    day_anaerobic = min(15 * weight_kg, 750.0)
    render_compact_card("⚖️ Amebiasis", "35 - 50 mg/kg/day แบ่งทานวันละ 3 ครั้ง", day_ameba / 3, "ทานวันละ 3 ครั้ง หลังอาหาร", per_day_val=day_ameba)
    render_compact_card("⚖️ Anaerobic Infections", "15 - 50 mg/kg/day แบ่งทานวันละ 3 ครั้ง", day_anaerobic / 3, "ทานวันละ 3 ครั้ง หลังอาหาร", per_day_val=day_anaerobic)

elif selected_drug == "Albendazole":
    if 12 <= total_months <= 24:
        render_compact_card("📌 คำนวณตามอายุ", "200 mg กินครั้งเดียว (Single dose)", 200.0, "รับประทานครั้งเดียว หลังอาหาร")
    elif total_months > 24:
        render_compact_card("📌 คำนวณตามอายุ", "400 mg Single dose", 400.0, "รับประทานครั้งเดียว หลังอาหาร")
    else:
        age_out_of_range, age_range_text = True, "1 ปีขึ้นไป"

elif selected_drug == "Mebendazole":
    if total_months >= 24:
        render_compact_card("📌 คำนวณตามอายุ", "100 mg กินครั้งเดียว (พยาธิเข็มหมุด)", 100.0, "รับประทานครั้งเดียว (หากพยาธิอื่นทาน 100 mg เช้า-เย็น x 3 วัน)")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"

elif selected_drug == "Diclofenac":
    day_dose = (2 * weight_kg)
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "2 - 3 mg/kg/day แบ่งทานวันละ 3 ครั้งหลังอาหาร", day_dose / 3, "ทานวันละ 3 ครั้ง หลังอาหารทันที", per_day_val=day_dose, max_text="200 mg/day")

elif selected_drug == "Penicillin V":
    if total_months < 144:
        day_min = 25 * weight_kg
        day_max = min(50 * weight_kg, 3000.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "25 - 50 mg/kg/day แบ่งทานวันละ 4 ครั้ง (ทุก 6 ชม.)", (day_min/4, day_max/4), "ทานทุก 6 ชม. ก่อนอาหาร 1 ชม.", per_day_val=(day_min, day_max), max_text="3 g/day")
    else:
        age_out_of_range, age_range_text = True, "น้อยกว่า 12 ปี"

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    if total_months < 3:
        day_min = 20 * weight_kg
        day_max = min(30 * weight_kg, 500.0)
        render_compact_card("⚖️ ขนาดปกติ (เด็ก < 3 เดือน)", "20 - 30 mg/kg/day แบ่งทานวันละ 2 ครั้ง", (day_min/2, day_max/2), "ทุก 12 ชั่วโมง", per_day_val=(day_min, day_max))
    else:
        day_min = 20 * weight_kg
        day_max = min(50 * weight_kg, 500.0)
        day_high = min(80 * weight_kg, 1000.0)
        render_compact_card("⚖️ ขนาดปกติ (Standard dose)", "20 - 50 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทุก 8 ชั่วโมง", per_day_val=(day_min, day_max))
        render_compact_card("⚖️ ขนาดสูง (High dose - AOM/Pneumonia)", "80 - 90 mg/kg/day แบ่งทานวันละ 2 ครั้ง", day_high / 2, "ทุก 12 ชั่วโมง", per_day_val=day_high)

elif selected_drug == "Cloxacillin":
    if total_months > 1:
        day_min = 50 * weight_kg
        day_max = min(100 * weight_kg, 4000.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "50 - 100 mg/kg/day แบ่งทานวันละ 4 ครั้ง", (day_min/4, day_max/4), "ทุก 6 ชั่วโมง ก่อนอาหาร 1 ชม.", per_day_val=(day_min, day_max), max_text="4 g/day")
    else:
        age_out_of_range, age_range_text = True, "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Dicloxacillin":
    if weight_kg < 40:
        day_min = 25 * weight_kg
        day_max = min(50 * weight_kg, 500.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "25 - 50 mg/kg/day แบ่งทานวันละ 4 ครั้ง", (day_min/4, day_max/4), "ทุก 6 ชั่วโมง ก่อนอาหาร 1 ชม.", per_day_val=(day_min, day_max))
    else:
        st.info("น้ำหนักตั้งแต่ 40 kg ขึ้นไป แนะนำขนาดผู้ใหญ่: 250 - 500 mg วันละ 4 ครั้ง ก่อนอาหาร")

elif selected_drug == "Cephalexin":
    if total_months > 12:
        day_min = 25 * weight_kg
        day_max = min(50 * weight_kg, 2000.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "25 - 50 mg/kg/day แบ่งทานวันละ 4 ครั้ง", (day_min/4, day_max/4), "ทุก 6 ชั่วโมง", per_day_val=(day_min, day_max), max_text="2-4 g/day")
    else:
        age_out_of_range, age_range_text = True, "1 ปีขึ้นไป"

elif selected_drug == "Cefuroxime":
    if 3 <= total_months <= 144:
        day_min = 20 * weight_kg
        day_max = min(30 * weight_kg, 500.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "20 - 30 mg/kg/day แบ่งทานวันละ 2 ครั้ง", (day_min/2, day_max/2), "ทุก 12 ชั่วโมง หลังอาหารทันที", per_day_val=(day_min, day_max), max_text="500 mg/dose")
    else:
        age_out_of_range, age_range_text = True, "3 เดือน ถึง 12 ปี"

elif selected_drug == "Cefaclor":
    if total_months > 1:
        day_min = 20 * weight_kg
        day_max = min(40 * weight_kg, 1500.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "20 - 40 mg/kg/day แบ่งทานวันละ 3 ครั้ง", (day_min/3, day_max/3), "ทุก 8 ชั่วโมง", per_day_val=(day_min, day_max), max_text="1.5 g/day")
    else:
        age_out_of_range, age_range_text = True, "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Cefdinir":
    if 6 <= total_months <= 144:
        day_dose = min(14 * weight_kg, 600.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "14 mg/kg/day วันละ 1-2 ครั้ง", day_dose / 2, "ทานวันละ 2 ครั้ง (หรือทานครั้งเดียวตอนเช้า)", per_day_val=day_dose, max_text="600 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือน ถึง 12 ปี"

elif selected_drug == "Cefixime":
    if total_months >= 6:
        day_min = 8 * weight_kg
        day_max = min(20 * weight_kg, 400.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "8 - 20 mg/kg/day วันละ 1-2 ครั้ง", (day_min/2, day_max/2), "ทานวันละ 2 ครั้ง (ทุก 12 ชม.)", per_day_val=(day_min, day_max), max_text="400 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Cefditoren pivoxil":
    if total_months >= 144:
        day_min = 10 * weight_kg
        day_max = 20 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "10 - 20 mg/kg/day แบ่งทานวันละ 2 ครั้ง", (day_min/2, day_max/2), "ทุก 12 ชั่วโมง หลังอาหาร", per_day_val=(day_min, day_max))
    else:
        age_out_of_range, age_range_text = True, "12 ปีขึ้นไป"

elif selected_drug == "Erythromycin":
    day_min = 30 * weight_kg
    day_max = min(50 * weight_kg, 2000.0)
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "30 - 50 mg/kg/day แบ่งทานวันละ 4 ครั้ง", (day_min/4, day_max/4), "ทุก 6 ชั่วโมง ก่อนอาหาร", per_day_val=(day_min, day_max))

elif selected_drug == "Azithromycin":
    if total_months >= 6:
        day_dose = min(10 * weight_kg, 500.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "10 mg/kg/day วันละ 1 ครั้ง x 3 วัน", day_dose, "ทานวันละ 1 ครั้ง ก่อนอาหาร 1 ชม. (กินติดต่อกัน 3 วัน)", per_day_val=day_dose, max_text="500 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Roxithromycin":
    day_min = 5 * weight_kg
    day_max = min(8 * weight_kg, 300.0)
    render_compact_card("⚖️ คำนวณตามน้ำหนัก", "5 - 8 mg/kg/day แบ่งทานวันละ 2 ครั้ง", (day_min/2, day_max/2), "ทุก 12 ชั่วโมง ก่อนอาหาร", per_day_val=(day_min, day_max), max_text="300 mg/day")

elif selected_drug == "Clarithromycin":
    if total_months >= 6:
        day_dose = min(15 * weight_kg, 1000.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก", "15 mg/kg/day แบ่งทานวันละ 2 ครั้ง", day_dose / 2, "ทุก 12 ชั่วโมง พร้อมอาหาร", per_day_val=day_dose, max_text="500 mg/dose")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    if total_months >= 2:
        day_tmp = min(8 * weight_kg, 320.0)
        day_smx = min(40 * weight_kg, 1600.0)
        st.info(f"""
        ⚖️ **สูตรคำนวณ:** TMP 8 mg/kg/day + SMX 40 mg/kg/day แบ่งทานวันละ 2 ครั้ง
        * 💊 **ต่อมื้อ (ทุก 12 ชม.):** TMP **{day_tmp/2:.2f} mg** + SMX **{day_smx/2:.2f} mg**
        * 🗓️ **รวมทั้งวัน:** TMP **{day_tmp:.2f} mg** + SMX **{day_smx:.2f} mg**
        """)
    else:
        age_out_of_range, age_range_text = True, "2 เดือนขึ้นไป"


# --- แสดงเตือนกรณีอายุนอกเกณฑ์ ---
if age_out_of_range:
    st.error(f"⚠️ **แจ้งเตือน:** อายุของผู้ป่วย ({age_years} ปี {age_months} เดือน) **ไม่อยู่ในช่วงเกณฑ์อายุที่รองรับ** สำหรับยา {selected_drug}\n\n*(ช่วงอายุที่แนะนำ: **{age_range_text}**)*")

st.markdown("---")
st.caption("⚠️ **หมายเหตุ:** โปรแกรมนี้ใช้สำหรับช่วยคำนวณเบื้องต้นเท่านั้น ควรตรวจสอบความถูกต้องกับเอกสารกำกับยาอีกครั้งก่อนจ่ายยา")
