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
    
    # คำนวณอายุรวมเป็นเดือนเพื่อใช้ประมวลผล Logic
    total_months = (age_years * 12) + age_months

with col2:
    st.subheader("น้ำหนักผู้ป่วย")
    weight_kg = st.number_input("น้ำหนัก (kg)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

st.write(f"👉 **สรุปข้อมูล:** อายุ **{age_years} ปี {age_months} เดือน** ({total_months} เดือน) | น้ำหนัก **{weight_kg:.1f} kg**")
st.markdown("---")

# --- Section 2: เลือกยาและความเข้มข้น ---
st.header("2. เลือกยาและความเข้มข้น")

# รายชื่อยาทั้งหมด 55 ตัว
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

# --- Function คำนวณแปลง mg/mcg เป็น ml และ ช้อนชา ---
def format_volume_result(dose_val, unit="mg"):
    if dose_val is None or conc_mg <= 0:
        return "N/A"
    if isinstance(dose_val, tuple): # กรณีช่วงขนาดยา (min, max)
        d_min, d_max = dose_val
        ml_min = (d_min * conc_ml) / conc_mg
        ml_max = (d_max * conc_ml) / conc_mg
        tsp_min = ml_min / 5.0
        tsp_max = ml_max / 5.0
        return f"{d_min:.2f} - {d_max:.2f} {unit} ({ml_min:.2f} - {ml_max:.2f} ml / {tsp_min:.2f} - {tsp_max:.2f} ช้อนชา)"
    else: # กรณีขนาดยาค่าเดียว
        ml = (dose_val * conc_ml) / conc_mg
        tsp = ml / 5.0
        return f"{dose_val:.2f} {unit} ({ml:.2f} ml / {tsp:.2f} ช้อนชา)"

# --- Section 3: ประมวลผลและแสดงผลลัพธ์ ---
st.header(f"3. ผลการคำนวณ: {selected_drug}")

age_dose_info = None
weight_dose_info = None
age_out_of_range = False
age_range_text = ""

# Logic การคำนวณแยกตามรายยา (55 รายการ)
if selected_drug == "Brompheniramine maleate":
    if 24 <= total_months <= 72:
        age_dose_info = "0.125 mg/kg/dose ทุก 6-8 ชม. (Max 8 mg/day)"
    elif 72 < total_months <= 144:
        age_dose_info = f"2 - 4 mg ทุก 6-8 ชม. (Max 16 mg/day) -> {format_volume_result((2, 4))}"
    elif total_months > 144:
        age_dose_info = f"4 - 8 mg ทุก 6-8 ชม. (Max 24 mg/day) -> {format_volume_result((4, 8))}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่าหรือเท่ากับ 2 ปี (24 เดือนขึ้นไป)"
    
    w_dose = (0.5 * weight_kg) / 3 # แบ่งจ่ายทุก 6-8 ชม. (3 ครั้ง/วัน)
    weight_dose_info = f"0.5 mg/kg/day แบ่งจ่ายทุก 6-8 ชม. (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"

elif selected_drug == "Chlorpheniramine maleate":
    if 24 <= total_months <= 72:
        age_dose_info = f"1 mg ทุก 4-6 ชม. (Max 8 mg/day) -> {format_volume_result(1)}"
    elif 72 < total_months <= 144:
        age_dose_info = f"2 mg ทุก 4-6 ชม. (Max 12 mg/day) -> {format_volume_result(2)}"
    elif total_months > 144:
        age_dose_info = f"4 mg ทุก 4-6 ชม. (Max 24 mg/day) -> {format_volume_result(4)}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่าหรือเท่ากับ 2 ปี (24 เดือนขึ้นไป)"
    
    w_dose = (0.35 * weight_kg) / 4 # แบ่งจ่ายทุก 4-6 ชม.
    weight_dose_info = f"0.35 mg/kg/day แบ่งจ่ายทุก 4-6 ชม. (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"

elif selected_drug == "Diphenhydramine":
    if 24 <= total_months <= 72:
        age_dose_info = f"6.25 - 12.5 mg ทุก 6-8 ชม. (Max 75 mg/day) -> {format_volume_result((6.25, 12.5))}"
    elif 72 < total_months < 144:
        age_dose_info = f"12.5 - 25 mg ทุก 6-8 ชม. (Max 150 mg/day) -> {format_volume_result((12.5, 25))}"
    elif total_months >= 144:
        age_dose_info = f"25 - 50 mg ทุก 6-8 ชม. (Max 300 mg/day) -> {format_volume_result((25, 50))}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่าหรือเท่ากับ 2 ปีขึ้นไป"
        
    if 24 <= total_months <= 144:
        w_dose = (5 * weight_kg) / 3
        weight_dose_info = f"5 mg/kg/day แบ่งจ่ายทุก 6-8 ชม. (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"

elif selected_drug == "Hydroxyzine":
    if total_months < 72:
        age_dose_info = f"12.5 mg/dose ทุก 6-8 ชม. -> {format_volume_result(12.5)}"
    else:
        age_dose_info = f"12.5 - 25 mg/dose ทุก 6-8 ชม. -> {format_volume_result((12.5, 25))}"
        
    if weight_kg <= 40:
        w_dose = (2 * weight_kg) / 3
        weight_dose_info = f"2 mg/kg/day แบ่งจ่ายทุก 6-8 ชม. (Max 50 mg/day) (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"
    else:
        weight_dose_info = f"25 - 50 mg/dose วันละ 1-2 ครั้ง (Max 100 mg/day) -> {format_volume_result((25, 50))}"

elif selected_drug == "Cetirizine":
    if 6 <= total_months <= 11:
        age_dose_info = f"2.5 mg วันละ 1 ครั้ง -> {format_volume_result(2.5)}"
    elif 12 <= total_months <= 23:
        age_dose_info = f"2.5 mg วันละ 1-2 ครั้ง (Max 5 mg/day) -> {format_volume_result(2.5)}"
    elif 24 <= total_months <= 60:
        age_dose_info = f"2.5 mg วันละ 1-2 ครั้ง หรือ 5 mg วันละ 1 ครั้ง (Max 5 mg/day) -> {format_volume_result(2.5)} ถึง {format_volume_result(5)}"
    elif 61 <= total_months <= 144:
        age_dose_info = f"5 - 10 mg วันละ 1 ครั้ง (Max 10 mg/day) -> {format_volume_result((5, 10))}"
    elif total_months > 144:
        age_dose_info = f"10 mg วันละ 1 ครั้ง (Max 40 mg/day) -> {format_volume_result(10)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"
        
    w_dose = 0.25 * weight_kg
    weight_dose_info = f"0.25 mg/kg/day วันละ 1-2 ครั้ง (~{w_dose:.2f} mg/day) -> {format_volume_result(w_dose)}"

elif selected_drug == "Levocetirizine":
    if 6 <= total_months <= 60:
        age_dose_info = f"1.25 mg วันละ 1 ครั้ง (Max 1.25 mg/day) -> {format_volume_result(1.25)}"
    elif 61 <= total_months <= 131:
        age_dose_info = f"2.5 mg วันละ 1 ครั้ง (Max 2.5 mg/day) -> {format_volume_result(2.5)}"
    elif total_months >= 132:
        age_dose_info = f"2.5 - 5 mg วันละ 1 ครั้ง (Max 20 mg/day) -> {format_volume_result((2.5, 5))}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"
        
    w_dose = min(0.125 * weight_kg, 5.0)
    weight_dose_info = f"0.125 mg/kg/day วันละ 1 ครั้ง (Max 5 mg/day) (~{w_dose:.2f} mg/day) -> {format_volume_result(w_dose)}"

elif selected_drug == "Loratadine":
    if 24 <= total_months <= 60:
        age_dose_info = f"5 mg วันละ 1 ครั้ง (Max 10 mg/day) -> {format_volume_result(5)}"
    elif total_months >= 72:
        age_dose_info = f"5 mg วันละ 2 ครั้ง หรือ 10 mg วันละ 1 ครั้ง (Max 10 mg/day) -> {format_volume_result(5)} หรือ {format_volume_result(10)}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Desloratadine":
    if 6 <= total_months <= 11:
        age_dose_info = f"1 mg วันละ 1 ครั้ง -> {format_volume_result(1)}"
    elif 12 <= total_months <= 60:
        age_dose_info = f"1.25 mg วันละ 1 ครั้ง -> {format_volume_result(1.25)}"
    elif 61 <= total_months <= 131:
        age_dose_info = f"2.5 mg วันละ 1 ครั้ง -> {format_volume_result(2.5)}"
    elif total_months >= 132:
        age_dose_info = f"5 mg วันละ 1 ครั้ง (Max 20 mg/day) -> {format_volume_result(5)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Fexofenadine":
    if 6 <= total_months < 24:
        if weight_kg < 10.5:
            age_dose_info = f"15 mg/dose วันละ 2 ครั้ง -> {format_volume_result(15)}"
        else:
            age_dose_info = f"30 mg/dose วันละ 2 ครั้ง -> {format_volume_result(30)}"
    elif 24 <= total_months <= 131:
        age_dose_info = f"30 mg/dose วันละ 2 ครั้ง (Max 60 mg/day) -> {format_volume_result(30)}"
    elif total_months >= 132:
        age_dose_info = f"60 mg/dose วันละ 2 ครั้ง หรือ 180 mg วันละ 1 ครั้ง (Max 720 mg/day) -> {format_volume_result(60)} หรือ {format_volume_result(180)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Ketotifen":
    if total_months >= 72:
        age_dose_info = f"0.25 mg/kg/dose วันละ 2 ครั้ง (Max 1 mg/dose)"
        w_dose = min(0.25 * weight_kg, 1.0)
        weight_dose_info = f"0.25 mg/kg/dose (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"
    else:
        age_out_of_range = True
        age_range_text = "6 ปีขึ้นไป (72 เดือนขึ้นไป)"

elif selected_drug == "Montelukast":
    if 6 <= total_months <= 60:
        age_dose_info = f"4 mg วันละ 1 ครั้ง (Max 4 mg/day) -> {format_volume_result(4)}"
    elif 61 <= total_months <= 168:
        age_dose_info = f"5 mg วันละ 1 ครั้ง (Max 5 mg/day) -> {format_volume_result(5)}"
    elif total_months >= 180:
        age_dose_info = f"10 mg วันละ 1 ครั้ง (Max 10 mg/day) -> {format_volume_result(10)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Phenylephrine HCl":
    if 48 <= total_months <= 60:
        age_dose_info = f"2.5 mg/dose ทุก 4 ชม. (Max 15 mg/day) -> {format_volume_result(2.5)}"
    elif 72 <= total_months <= 131:
        age_dose_info = f"5 mg/dose ทุก 4 ชม. (Max 30 mg/day) -> {format_volume_result(5)}"
    elif total_months >= 132:
        age_dose_info = f"10 mg/dose ทุก 4 ชม. (Max 60 mg/day) -> {format_volume_result(10)}"
    else:
        age_out_of_range = True
        age_range_text = "4 ปีขึ้นไป (48 เดือนขึ้นไป)"

elif selected_drug == "Pseudoephedrine":
    if 24 <= total_months <= 60:
        age_dose_info = f"15 mg/dose ทุก 4-6 ชม. (Max 60 mg/day) -> {format_volume_result(15)}"
        w_dose = 1 * weight_kg
        weight_dose_info = f"1 mg/kg/dose ทุก 4-6 ชม. (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"
    elif 72 <= total_months <= 144:
        age_dose_info = f"30 mg/dose ทุก 4-6 ชม. (Max 120 mg/day) -> {format_volume_result(30)}"
    elif total_months > 144:
        age_dose_info = f"60 mg/dose ทุก 4-6 ชม. หรือ SR 120-240 mg/day (Max 240 mg/day) -> {format_volume_result(60)}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    if 24 <= total_months <= 60:
        age_dose_info = f"50 - 100 mg ทุก 4 ชม. (Max 6 doses/day) -> {format_volume_result((50, 100))}"
    elif 72 <= total_months <= 131:
        age_dose_info = f"100 - 200 mg ทุก 4 ชม. (Max 6 doses/day) -> {format_volume_result((100, 200))}"
    elif total_months >= 132:
        age_dose_info = f"200 - 400 mg ทุก 4 ชม. (Max 6 doses/day) -> {format_volume_result((200, 400))}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose = (12 * weight_kg) / 3
    weight_dose_info = f"12 mg/kg/day แบ่งจ่าย 3-4 ครั้ง/วัน (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"

elif selected_drug == "Acetylcysteine":
    if 24 <= total_months <= 72:
        age_dose_info = f"50 - 100 mg วันละ 2-4 ครั้ง -> {format_volume_result((50, 100))}"
    elif total_months > 72:
        age_dose_info = f"100 - 200 mg วันละ 3 ครั้ง หรือ 600 mg วันละ 1 ครั้ง (Max 600 mg/day) -> {format_volume_result((100, 200))}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (20 * weight_kg) / 3
    w_dose_max = (30 * weight_kg) / 3
    weight_dose_info = f"20-30 mg/kg/day แบ่งจ่าย 2-3 ครั้ง/วัน (~{w_dose_min:.2f} - {w_dose_max:.2f} mg/dose) -> {format_volume_result((w_dose_min, w_dose_max))}"

elif selected_drug == "Ambroxol":
    if 24 <= total_months <= 60:
        age_dose_info = f"7.5 - 15 mg/dose วันละ 3 ครั้ง -> {format_volume_result((7.5, 15))}"
    elif 72 <= total_months <= 144:
        age_dose_info = f"15 - 30 mg/dose วันละ 2-3 ครั้ง -> {format_volume_result((15, 30))}"
    elif total_months > 144:
        age_dose_info = f"60 - 120 mg/day วันละ 2-3 ครั้ง"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (1.2 * weight_kg) / 3
    w_dose_max = (1.6 * weight_kg) / 3
    weight_dose_info = f"1.2-1.6 mg/kg/day แบ่งจ่าย 2-3 ครั้ง/วัน (~{w_dose_min:.2f} - {w_dose_max:.2f} mg/dose) -> {format_volume_result((w_dose_min, w_dose_max))}"

elif selected_drug == "Carbocysteine":
    if total_months > 24:
        w_dose_min = (15 * weight_kg) / 3
        w_dose_max = (20 * weight_kg) / 3
        weight_dose_info = f"15-20 mg/kg/day แบ่งจ่าย 3-4 ครั้ง (~{w_dose_min:.2f} - {w_dose_max:.2f} mg/dose) -> {format_volume_result((w_dose_min, w_dose_max))}"

    if 24 <= total_months <= 60:
        age_dose_info = f"200 - 500 mg/day วันละ 2-3 ครั้ง"
    elif 72 <= total_months <= 131:
        age_dose_info = f"300 - 750 mg/day วันละ 3 ครั้ง"
    elif 132 <= total_months <= 179:
        age_dose_info = f"300 mg - 2.25 g/day วันละ 3 ครั้ง"
    elif total_months >= 180:
        age_dose_info = f"750 mg - 2.25 g/day วันละ 3 ครั้ง"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Bromhexine":
    if 24 <= total_months <= 60:
        age_dose_info = f"2 mg/dose วันละ 3 ครั้ง หรือ 4 mg/dose วันละ 2 ครั้ง (Max 8 mg/day) -> {format_volume_result(2)} หรือ {format_volume_result(4)}"
    elif 72 <= total_months <= 131:
        age_dose_info = f"4 - 8 mg/dose วันละ 3 ครั้ง (Max 24 mg/day) -> {format_volume_result((4, 8))}"
    elif total_months >= 132:
        age_dose_info = f"8 - 16 mg/dose วันละ 3 ครั้ง (Max 48 mg/day) -> {format_volume_result((8, 16))}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (0.6 * weight_kg) / 3
    w_dose_max = (0.8 * weight_kg) / 3
    weight_dose_info = f"0.6-0.8 mg/kg/day แบ่งจ่าย 3-4 ครั้ง (~{w_dose_min:.2f} - {w_dose_max:.2f} mg/dose) -> {format_volume_result((w_dose_min, w_dose_max))}"

elif selected_drug == "Dextromethorphan":
    if 48 <= total_months <= 60:
        age_dose_info = f"2.5 - 7.5 mg ทุก 4-8 ชม. (Max 30 mg/day) -> {format_volume_result((2.5, 7.5))}"
    elif 72 <= total_months <= 131:
        age_dose_info = f"5 - 10 mg ทุก 4 ชม. (Max 60 mg/day) -> {format_volume_result((5, 10))}"
    elif total_months >= 132:
        age_dose_info = f"20 mg ทุก 4 ชม. (Max 120 mg/day) -> {format_volume_result(20)}"
    else:
        age_out_of_range = True
        age_range_text = "4 ปีขึ้นไป (48 เดือนขึ้นไป)"

elif selected_drug == "Salbutamol":
    if 24 <= total_months <= 72:
        w_dose = 0.1 * weight_kg
        age_dose_info = f"0.1 - 0.2 mg/kg/dose วันละ 3 ครั้ง (Max 12 mg/day)"
        weight_dose_info = f"คำนวณตามน้ำหนัก (0.1 mg/kg/dose): ~{w_dose:.2f} mg/dose -> {format_volume_result(w_dose)}"
    elif 84 <= total_months <= 168:
        age_dose_info = f"2 mg/dose วันละ 3-4 ครั้ง (Max 24 mg/day) -> {format_volume_result(2)}"
    elif total_months >= 180:
        age_dose_info = f"2 - 4 mg/dose วันละ 3-4 ครั้ง (Max 32 mg/day) -> {format_volume_result((2, 4))}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Terbutaline sulfate":
    if total_months < 144:
        w_dose = 0.05 * weight_kg
        age_dose_info = f"0.05 mg/kg/dose วันละ 3 ครั้ง (Max 5 mg/day)"
        weight_dose_info = f"คำนวณตามน้ำหนัก (0.05 mg/kg/dose): ~{w_dose:.2f} mg/dose -> {format_volume_result(w_dose)}"
    elif 144 <= total_months <= 168:
        age_dose_info = f"2.5 mg/dose วันละ 3 ครั้ง (Max 7.5 mg/day) -> {format_volume_result(2.5)}"
    elif total_months >= 180:
        age_dose_info = f"5 mg/dose วันละ 3-4 ครั้ง (Max 15 mg/day) -> {format_volume_result(5)}"

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    if total_months < 72:
        w_dose = 1.25 * weight_kg
        weight_dose_info = f"1.25 mcg/kg/dose ทุก 12 ชม. (~{w_dose:.2f} mcg/dose) -> {format_volume_result(w_dose, unit='mcg')}"
        
    if total_months < 12:
        age_dose_info = f"10 - 15 mcg/dose วันละ 2 ครั้ง (Max 30 mcg/day) -> {format_volume_result((10, 15), unit='mcg')}"
    elif 12 <= total_months <= 24:
        age_dose_info = f"15 - 20 mcg/dose วันละ 2 ครั้ง (Max 40 mcg/day) -> {format_volume_result((15, 20), unit='mcg')}"
    elif 36 <= total_months <= 60:
        age_dose_info = f"20 - 25 mcg/dose วันละ 2 ครั้ง (Max 50 mcg/day) -> {format_volume_result((20, 25), unit='mcg')}"
    elif 72 <= total_months <= 216:
        age_dose_info = f"25 mcg/dose วันละ 1-2 ครั้ง (Max 50 mcg/day) -> {format_volume_result(25, unit='mcg')}"

elif selected_drug == "Dimenhydrinate":
    if 24 <= total_months <= 60:
        age_dose_info = f"15 - 25 mg ทุก 6-8 ชม. (Max 75 mg/day) -> {format_volume_result((15, 25))}"
    elif 72 <= total_months <= 131:
        age_dose_info = f"25 - 50 mg ทุก 6-8 ชม. (Max 150 mg/day) -> {format_volume_result((25, 50))}"
    else:
        age_out_of_range = True
        age_range_text = "2 ถึง 11 ปี (24 ถึง 131 เดือน)"

elif selected_drug == "Domperidone":
    if weight_kg < 35:
        w_dose_day = min(0.75 * weight_kg, 30.0)
        w_dose_single = (0.2 * weight_kg, 0.4 * weight_kg)
        weight_dose_info = f"0.75 mg/kg/day วันละ 3 ครั้งก่อนอาหาร (~{w_dose_day/3:.2f} mg/dose) -> {format_volume_result(w_dose_day/3)} หรือ 0.2-0.4 mg/kg/dose -> {format_volume_result(w_dose_single)}"
    else:
        weight_dose_info = "น้ำหนักเกิน 35 kg พิจารณาขนาดยาผู้ใหญ่ (Max 30 mg/day)"

elif selected_drug == "Dicyclomine":
    if 6 <= total_months <= 24:
        age_dose_info = f"5 - 10 mg วันละ 3-4 ครั้งก่อนอาหาร -> {format_volume_result((5, 10))}"
    elif total_months > 24:
        age_dose_info = f"10 mg วันละ 3-4 ครั้ง -> {format_volume_result(10)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Hyoscine":
    if 6 <= total_months <= 12:
        age_dose_info = f"5 mg/dose วันละ 3-4 ครั้ง -> {format_volume_result(5)}"
    elif 12 < total_months <= 72:
        age_dose_info = f"5 - 10 mg วันละ 3-4 ครั้ง -> {format_volume_result((5, 10))}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือน ถึง 6 ปี"

elif selected_drug == "Simethicone":
    if total_months < 24:
        age_dose_info = f"20 mg/dose วันละ 3-4 ครั้ง (Max 500 mg/day) -> {format_volume_result(20)}"
    elif 24 <= total_months <= 144:
        age_dose_info = f"40 mg/dose วันละ 3-4 ครั้ง (Max 500 mg/day) -> {format_volume_result(40)}"

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    if total_months <= 1:
        age_dose_info = f"1 ml/kg/dose -> {1 * weight_kg:.2f} ml"
    elif 1 < total_months <= 12:
        age_dose_info = "2 - 5 ml/dose"
    elif 12 < total_months <= 60:
        age_dose_info = "5 - 15 ml/dose"
    elif 72 <= total_months <= 144:
        age_dose_info = "15 - 45 ml/dose"

elif selected_drug == "Lactulose (Laevolac)":
    if 1 <= total_months <= 72:
        age_dose_info = f"5 - 10 ml/day วันละ 1 ครั้ง"
        w_dose = 1.5 * weight_kg # ค่าเฉลี่ย 1-2 g/kg/day (Laevolac 10g/15ml)
        weight_dose_info = f"1 - 2 g/kg/day"
    elif 72 < total_months <= 168:
        age_dose_info = f"15 ml/day วันละ 1 ครั้ง"
        weight_dose_info = f"1.5 - 3 ml/kg/day วันละ 1-2 ครั้ง"
    elif total_months > 168:
        age_dose_info = f"15 - 30 ml/day"
    else:
        age_out_of_range = True
        age_range_text = "1 เดือนขึ้นไป"

elif selected_drug == "Metronidazole":
    w_dose_ameba = min((35 * weight_kg)/3, 2250/3)
    w_dose_anaerobic = min((15 * weight_kg)/3, 750)
    weight_dose_info = f"Amebiasis: 35-50 mg/kg/day แบ่งจ่าย 3 ครั้ง (~{w_dose_ameba:.2f} mg/dose) -> {format_volume_result(w_dose_ameba)} | Anaerobic/Trichomoniasis: 15-50 mg/kg/day (~{w_dose_anaerobic:.2f} mg/dose) -> {format_volume_result(w_dose_anaerobic)}"

elif selected_drug == "Albendazole":
    if 12 <= total_months <= 24:
        age_dose_info = f"Roundworm/Pinworm/Hookworm: 200 mg กินครั้งเดียว (Single dose) -> {format_volume_result(200)}"
    elif total_months > 24:
        age_dose_info = f"Roundworm/Pinworm/Hookworm: 400 mg Single dose | Whipworm: 400 mg OD x 3 วัน | Strongyloides: 400 mg BID x 7 วัน -> {format_volume_result(400)}"
        w_tape = min(7.5 * weight_kg, 400.0)
        w_fluke = min(10 * weight_kg, 800.0)
        weight_dose_info = f"Tapeworm: 7.5 mg/kg/dose BID (~{w_tape:.2f} mg) -> {format_volume_result(w_tape)} | Liver flukes: 10 mg/kg/dose OD (~{w_fluke:.2f} mg) -> {format_volume_result(w_fluke)}"
    else:
        age_out_of_range = True
        age_range_text = "1 ปีขึ้นไป (12 เดือนขึ้นไป)"

elif selected_drug == "Mebendazole":
    if total_months >= 24:
        age_dose_info = f"Pinworm: 100 mg Single dose | Roundworm/Whipworm/Hookworm: 100 mg BID x 3 วัน หรือ 500 mg Single dose | Capillariasis: 200 mg OD x 20 วัน -> {format_volume_result(100)}"
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Acetaminophen":
    w_min = 10 * weight_kg
    w_max = 15 * weight_kg
    weight_dose_info = f"10 - 15 mg/kg/dose ทุก 4-6 ชม. (Max 75 mg/kg/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"

elif selected_drug == "Diclofenac":
    w_dose = (2 * weight_kg) / 3
    weight_dose_info = f"2 - 3 mg/kg/day แบ่งจ่าย 2-4 ครั้ง หลังอาหาร (Max 200 mg/day) (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"

elif selected_drug == "Ibuprofen":
    w_min = 5 * weight_kg
    w_max = 10 * weight_kg
    weight_dose_info = f"5 - 10 mg/kg/dose ทุก 6-8 ชม. หลังอาหาร (Max 40 mg/kg/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"

elif selected_drug == "Penicillin V":
    if total_months < 144:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 3000 / 4)
        weight_dose_info = f"25 - 50 mg/kg/day แบ่งจ่าย 3-4 ครั้ง (Max 3 g/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "น้อยกว่า 12 ปี"

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    if total_months < 3:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        weight_dose_info = f"20 - 30 mg/kg/day แบ่งจ่าย 2 ครั้ง (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        w_min = (20 * weight_kg) / 3
        w_max = min((50 * weight_kg) / 3, 500.0)
        w_high = min((80 * weight_kg) / 2, 1000.0)
        weight_dose_info = f"ปกติ: 20-50 mg/kg/day (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))} | High dose: 80-90 mg/kg/day (~{w_high:.2f} mg/dose) -> {format_volume_result(w_high)}"

elif selected_drug == "Cloxacillin":
    if total_months > 1:
        w_min = (50 * weight_kg) / 4
        w_max = min((100 * weight_kg) / 4, 4000 / 4)
        weight_dose_info = f"50 - 100 mg/kg/day แบ่งจ่าย 3-4 ครั้ง (Max 4 g/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Dicloxacillin":
    if weight_kg < 40:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 500.0)
        w_high = (100 * weight_kg) / 4
        weight_dose_info = f"ปกติ: 25-50 mg/kg/day (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))} | High dose: 50-100 mg/kg/day (~{w_high:.2f} mg/dose) -> {format_volume_result(w_high)}"
    else:
        weight_dose_info = "น้ำหนักตั้งแต่ 40 kg ขึ้นไป แนะนำขนาดผู้ใหญ่ 250 - 500 mg/dose"

elif selected_drug == "Cephalexin":
    if total_months > 12:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 2000 / 4)
        w_high = min((100 * weight_kg) / 4, 4000 / 4)
        weight_dose_info = f"ปกติ: 25-50 mg/kg/day (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))} | High dose: 75-100 mg/kg/day (~{w_high:.2f} mg/dose) -> {format_volume_result(w_high)}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 ปีขึ้นไป (12 เดือนขึ้นไป)"

elif selected_drug == "Cefuroxime":
    if 3 <= total_months <= 144:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        weight_dose_info = f"20 - 30 mg/kg/day แบ่งจ่าย 2 ครั้ง (Max 500 mg/dose) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "3 เดือน ถึง 12 ปี"

elif selected_drug == "Cefaclor":
    if total_months > 1:
        w_min = (20 * weight_kg) / 3
        w_max = min((40 * weight_kg) / 3, 1500 / 3)
        weight_dose_info = f"20 - 40 mg/kg/day แบ่งจ่าย 2-3 ครั้ง (Max 1.5 g/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Cefdinir":
    if 6 <= total_months <= 144:
        w_dose = min(14 * weight_kg, 600.0)
        weight_dose_info = f"14 mg/kg/day วันละ 1-2 ครั้ง (Max 600 mg/day) (~{w_dose:.2f} mg/day) -> {format_volume_result(w_dose)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือน ถึง 12 ปี"

elif selected_drug == "Cefixime":
    if total_months >= 6:
        w_min = 8 * weight_kg
        w_max = min(20 * weight_kg, 400.0)
        weight_dose_info = f"8 - 20 mg/kg/day วันละ 1-2 ครั้ง (Max 400 mg/day) (~{w_min:.2f} - {w_max:.2f} mg/day) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Cefditoren pivoxil":
    if total_months >= 144:
        w_min = (10 * weight_kg) / 2
        w_max = (20 * weight_kg) / 2
        age_dose_info = f"200 - 400 mg วันละ 2 ครั้ง หลังอาหาร -> {format_volume_result((200, 400))}"
        weight_dose_info = f"10 - 20 mg/kg/day แบ่งจ่าย 2-3 ครั้ง (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"
    else:
        age_out_of_range = True
        age_range_text = "12 ปีขึ้นไป (144 เดือนขึ้นไป)"

elif selected_drug == "Erythromycin":
    w_base = (30 * weight_kg) / 4
    w_max_base = min((50 * weight_kg) / 4, 2000 / 4)
    weight_dose_info = f"Base/Estolate/Stearate: 30-50 mg/kg/day (~{w_base:.2f} - {w_max_base:.2f} mg/dose) -> {format_volume_result((w_base, w_max_base))} | Ethylsuccinate: Max 3.2 g/day"

elif selected_drug == "Azithromycin":
    if total_months >= 6:
        w_dose = min(10 * weight_kg, 500.0)
        weight_dose_info = f"5-12 mg/kg/day OD x 3 วัน OR 10-12 mg/kg Day 1 แล้ว 5-6 mg/kg Day 2-5 (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Roxithromycin":
    w_min = (5 * weight_kg) / 2
    w_max = min((8 * weight_kg) / 2, 300 / 2)
    weight_dose_info = f"5 - 8 mg/kg/day แบ่งจ่าย วันละ 2 ครั้ง (Max 300 mg/day) (~{w_min:.2f} - {w_max:.2f} mg/dose) -> {format_volume_result((w_min, w_max))}"

elif selected_drug == "Clarithromycin":
    if total_months >= 6:
        w_dose = min((15 * weight_kg) / 2, 500.0)
        weight_dose_info = f"15 mg/kg/day แบ่งจ่าย วันละ 2 ครั้ง (Max 500 mg/dose) (~{w_dose:.2f} mg/dose) -> {format_volume_result(w_dose)}"
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    if total_months >= 2:
        w_tmp = min((8 * weight_kg) / 2, 160.0)
        w_smx = min((40 * weight_kg) / 2, 800.0)
        weight_dose_info = f"TMP 8 mg/kg/day + SMX 40 mg/kg/day แบ่งจ่าย 2 ครั้ง (~TMP {w_tmp:.2f} mg + SMX {w_smx:.2f} mg/dose)"
    else:
        age_out_of_range = True
        age_range_text = "2 เดือนขึ้นไป"


# --- แสดงผลการเตือนและคำนวณ ---

# 1. แสดงเตือนกรณีอายุนอกเกณฑ์
if age_out_of_range:
    st.error(f"⚠️ **แจ้งเตือน:** อายุของผู้ป่วย ({age_years} ปี {age_months} เดือน) **ไม่อยู่ในช่วงเกณฑ์อายุที่ใช้คำนวณ** ของยา {selected_drug}\n\n*(ช่วงอายุที่รองรับสำหรับยาตัวนี้คือ: **{age_range_text}**)*")

# 2. แสดงผลตามเกณฑ์อายุ (ถ้ามี)
if age_dose_info:
    st.info(f"📌 **ขนาดยาคำนวณตามอายุ (Age-based dose):**\n\n{age_dose_info}")

# 3. แสดงผลตามเกณฑ์น้ำหนัก (ถ้ามี)
if weight_dose_info:
    st.success(f"⚖️ **ขนาดยาคำนวณตามน้ำหนัก (Weight-based dose):**\n\n{weight_dose_info}")

# กรณีไม่มีข้อมูลทั้งสองทาง
if not age_dose_info and not weight_dose_info and not age_out_of_range:
    st.warning("⚠️ ไม่มีข้อมูลเกณฑ์คำนวณเฉพาะช่วงอายุน้ำหนักนี้ โปรดตรวจสอบเอกสารกำกับยาเพิ่มเติม")

st.markdown("---")
st.caption("⚠️ **หมายเหตุ:** โปรแกรมนี้ใช้สำหรับช่วยคำนวณเบื้องต้นเท่านั้น ควรตรวจสอบความถูกต้องและด่านการแพทย์ก่อนใช้จริง")

