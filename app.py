import streamlit as st

st.set_page_config(page_title="โปรแกรมคำนวณยาสูตรเด็ก", page_icon="👶", layout="wide")

st.title("👶 โปรแกรมคำนวณขนาดขนาดยาสำหรับเด็ก")
st.caption("ระบบคำนวณขนาดยา ปริมาตร (ml) และช้อนชา สำหรับใช้งานบนมือถือและคอมพิวเตอร์")

# --- Section 1: ข้อมูลผู้ป่วย ---
st.subheader("1. ข้อมูลผู้ป่วย")
col1, col2 = st.columns(2)

with col1:
    col_y, col_m = st.columns(2)
    with col_y:
        age_years = st.number_input("อายุ (ปี)", min_value=0, max_value=18, value=2, step=1)
    with col_m:
        age_months = st.number_input("อายุ (เดือน)", min_value=0, max_value=11, value=0, step=1)
    total_months = (age_years * 12) + age_months

with col2:
    weight_kg = st.number_input("น้ำหนัก (kg)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

st.info(f"👤 **ผู้ป่วย:** อายุ **{age_years} ปี {age_months} เดือน** ({total_months} เดือน) | น้ำหนัก **{weight_kg:.1f} kg**")
st.markdown("---")

# --- Section 2: เลือกยาและความเข้มข้น ---
st.subheader("2. เลือกยาและความเข้มข้น")

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

# --- Helper Functions ---
def calc_ml_tsp(mg_val):
    """แปลง mg เป็น ml และ ช้อนชา"""
    if mg_val is None or conc_mg <= 0:
        return 0.0, 0.0
    ml = (mg_val * conc_ml) / conc_mg
    tsp = ml / 5.0
    return ml, tsp

def render_compact_card(title, mg_single, freq_str, note="", unit="mg"):
    """แสดงผลลัพธ์แบบการ์ดขนาดพอดีมือถือ ตัวหนังสือไม่ใหญ่เกินไป"""
    st.markdown(f"##### {title}")
    
    if isinstance(mg_single, tuple):
        m_min, m_max = mg_single
        ml_min, tsp_min = calc_ml_tsp(m_min)
        ml_max, tsp_max = calc_ml_tsp(m_max)
        mg_display = f"{m_min:.2f} - {m_max:.2f} {unit}"
        ml_display = f"{ml_min:.2f} - {ml_max:.2f} ml"
        tsp_display = f"{tsp_min:.2f} - {tsp_max:.2f} ช้อนชา"
    else:
        ml, tsp = calc_ml_tsp(mg_single)
        mg_display = f"{mg_single:.2f} {unit}"
        ml_display = f"{ml:.2f} ml"
        tsp_display = f"{tsp:.2f} ช้อนชา"

    # HTML/CSS แต่งการ์ดให้อ่านง่าย กระทัดรัด
    card_html = f"""
    <div style="background-color: #f0f2f6; border-left: 5px solid #007bff; padding: 12px; border-radius: 6px; margin-bottom: 10px; color: #1f2937;">
        <div style="font-size: 15px; font-weight: bold; margin-bottom: 6px;">👉 ทานครั้งละ: <span style="color: #d9534f;">{ml_display}</span> ({tsp_display})</div>
        <div style="font-size: 13px; color: #4b5563;">• คิดเป็นตัวยา: {mg_display} / ครั้ง</div>
        <div style="font-size: 13px; color: #4b5563;">• ความถี่: {freq_str}</div>
        {"<div style='font-size: 12px; color: #856404; margin-top: 4px;'>⚠️ " + note + "</div>" if note else ""}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# --- Section 3: ประมวลผลและแสดงผลลัพธ์ ---
st.subheader(f"3. ผลการคำนวณ: {selected_drug}")

age_out_of_range = False
age_range_text = ""

# --- LOGIC คำนวณรายยา (55 รายการ) ---

if selected_drug == "Acetaminophen":
    # 10-15 mg/kg/dose ทุก 4-6 ชม.
    single_min = 10 * weight_kg
    single_max = 15 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (Weight-based)", (single_min, single_max), "ทุก 4 - 6 ชั่วโมง เวลาปวดหรือมีไข้", f"Max {75 * weight_kg:.1f} mg/day")

elif selected_drug == "Ibuprofen":
    # 5-10 mg/kg/dose ทุก 6-8 ชม.
    single_min = 5 * weight_kg
    single_max = 10 * weight_kg
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (Weight-based)", (single_min, single_max), "ทุก 6 - 8 ชั่วโมง หลังอาหาร", f"Max {40 * weight_kg:.1f} mg/day")

elif selected_drug == "Diclofenac":
    # 2-3 mg/kg/day แบ่งจ่าย 3 ครั้ง (ทุก 8 ชม.)
    single_dose = (2 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่งจ่าย 3 ครั้ง/วัน)", single_dose, "วันละ 3 ครั้ง หลังอาหาร (ทุก 8 ชม.)", "Max 200 mg/day")

elif selected_drug == "Brompheniramine maleate":
    if 24 <= total_months <= 72:
        single_dose = 0.125 * weight_kg
        render_compact_card("📌 คำนวณตามอายุ/น้ำหนัก", single_dose, "ทุก 6 - 8 ชั่วโมง (วันละ 3-4 ครั้ง)", "Max 8 mg/day")
    elif 72 < total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", (2, 4), "ทุก 6 - 8 ชั่วโมง", "Max 16 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", (4, 8), "ทุก 6 - 8 ชั่วโมง", "Max 24 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Chlorpheniramine maleate":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", 1.0, "ทุก 4 - 6 ชั่วโมง", "Max 8 mg/day")
    elif 72 < total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", 2.0, "ทุก 4 - 6 ชั่วโมง", "Max 12 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", 4.0, "ทุก 4 - 6 ชั่วโมง", "Max 24 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Diphenhydramine":
    if 24 <= total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", (6.25, 12.5), "ทุก 6 - 8 ชั่วโมง", "Max 75 mg/day")
    elif 72 < total_months < 144:
        render_compact_card("📌 คำนวณตามอายุ", (12.5, 25.0), "ทุก 6 - 8 ชั่วโมง", "Max 150 mg/day")
    elif total_months >= 144:
        render_compact_card("📌 คำนวณตามอายุ", (25.0, 50.0), "ทุก 6 - 8 ชั่วโมง", "Max 300 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Hydroxyzine":
    # 2 mg/kg/day แบ่ง 3 ครั้ง
    single_dose = (2 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่งจ่าย 3 ครั้ง/วัน)", single_dose, "ทุก 6 - 8 ชั่วโมง (วันละ 3 ครั้ง)", "Max 50 mg/day")

elif selected_drug == "Cetirizine":
    if 6 <= total_months <= 23:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "วันละ 1 ครั้ง")
    elif 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "วันละ 1 - 2 ครั้ง", "Max 5 mg/day")
    elif 61 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", (5.0, 10.0), "วันละ 1 ครั้ง", "Max 10 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", 10.0, "วันละ 1 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Levocetirizine":
    if 6 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 1.25, "วันละ 1 ครั้ง")
    elif 61 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "วันละ 1 ครั้ง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", (2.5, 5.0), "วันละ 1 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Loratadine":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "วันละ 1 ครั้ง")
    elif total_months >= 72:
        render_compact_card("📌 คำนวณตามอายุ", 10.0, "วันละ 1 ครั้ง (หรือแบ่งทาน 5 mg วันละ 2 ครั้ง)")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Desloratadine":
    if 6 <= total_months <= 11:
        render_compact_card("📌 คำนวณตามอายุ", 1.0, "วันละ 1 ครั้ง")
    elif 12 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 1.25, "วันละ 1 ครั้ง")
    elif 61 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "วันละ 1 ครั้ง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "วันละ 1 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Fexofenadine":
    if 6 <= total_months < 24:
        dose = 15.0 if weight_kg < 10.5 else 30.0
        render_compact_card("📌 คำนวณตามอายุ/น้ำหนัก", dose, "วันละ 2 ครั้ง (ทุก 12 ชม.)")
    elif 24 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", 30.0, "วันละ 2 ครั้ง (ทุก 12 ชม.)")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", 60.0, "วันละ 2 ครั้ง (ทุก 12 ชม.)")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Ketotifen":
    if total_months >= 72:
        single_dose = min(0.25 * weight_kg, 1.0)
        render_compact_card("⚖️ คำนวณตามน้ำหนัก (0.25 mg/kg/dose)", single_dose, "วันละ 2 ครั้ง (ทุก 12 ชม.)", "Max 1 mg/dose")
    else:
        age_out_of_range = True
        age_range_text = "6 ปีขึ้นไป"

elif selected_drug == "Montelukast":
    if 6 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 4.0, "วันละ 1 ครั้ง ก่อนนอน")
    elif 61 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "วันละ 1 ครั้ง ก่อนนอน")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", 10.0, "วันละ 1 ครั้ง ก่อนนอน")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Phenylephrine HCl":
    if 48 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "ทุก 4 ชั่วโมง", "Max 15 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "ทุก 4 ชั่วโมง", "Max 30 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", 10.0, "ทุก 4 ชั่วโมง", "Max 60 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "4 ปีขึ้นไป"

elif selected_drug == "Pseudoephedrine":
    if 24 <= total_months <= 60:
        # 1 mg/kg/dose ทุก 4-6 ชม. (คิดเฉลี่ยวันละ 4 ครั้ง)
        single_dose = 1.0 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก (1 mg/kg/dose)", single_dose, "ทุก 4 - 6 ชั่วโมง", "Max 60 mg/day")
    elif 72 <= total_months <= 144:
        render_compact_card("📌 คำนวณตามอายุ", 30.0, "ทุก 4 - 6 ชั่วโมง", "Max 120 mg/day")
    elif total_months > 144:
        render_compact_card("📌 คำนวณตามอายุ", 60.0, "ทุก 4 - 6 ชั่วโมง", "Max 240 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    # 12 mg/kg/day แบ่ง 3 ครั้ง
    single_w = (12 * weight_kg) / 3
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ/น้ำหนัก", (50.0, 100.0), "ทุก 4 ชั่วโมง (วันละ 4-6 ครั้ง)")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", (100.0, 200.0), "ทุก 4 ชั่วโมง")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", (200.0, 400.0), "ทุก 4 ชั่วโมง")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Acetylcysteine":
    # 20-30 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (20 * weight_kg) / 3
    single_max = (30 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "วันละ 3 ครั้ง (ทุก 8 ชม.)")

elif selected_drug == "Ambroxol":
    # 1.2 - 1.6 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (1.2 * weight_kg) / 3
    single_max = (1.6 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "วันละ 3 ครั้ง (ทุก 8 ชม.)")

elif selected_drug == "Carbocysteine":
    # 15-20 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (15 * weight_kg) / 3
    single_max = (20 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "วันละ 3 ครั้ง (ทุก 8 ชม.)")

elif selected_drug == "Bromhexine":
    # 0.6 - 0.8 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (0.6 * weight_kg) / 3
    single_max = (0.8 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "วันละ 3 ครั้ง (ทุก 8 ชม.)")

elif selected_drug == "Dextromethorphan":
    if 48 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", (2.5, 7.5), "ทุก 4 - 8 ชั่วโมง", "Max 30 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", (5.0, 10.0), "ทุก 4 ชั่วโมง", "Max 60 mg/day")
    elif total_months >= 132:
        render_compact_card("📌 คำนวณตามอายุ", 20.0, "ทุก 4 ชั่วโมง", "Max 120 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "4 ปีขึ้นไป"

elif selected_drug == "Salbutamol":
    if 24 <= total_months <= 72:
        single_dose = 0.1 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก (0.1 mg/kg/dose)", single_dose, "วันละ 3 ครั้ง (ทุก 8 ชม.)")
    elif 84 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", 2.0, "วันละ 3 - 4 ครั้ง")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", (2.0, 4.0), "วันละ 3 - 4 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Terbutaline sulfate":
    if total_months < 144:
        single_dose = 0.05 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก (0.05 mg/kg/dose)", single_dose, "วันละ 3 ครั้ง (ทุก 8 ชม.)")
    elif 144 <= total_months <= 168:
        render_compact_card("📌 คำนวณตามอายุ", 2.5, "วันละ 3 ครั้ง")
    elif total_months >= 180:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "วันละ 3 - 4 ครั้ง")

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    if total_months < 72:
        single_dose = 1.25 * weight_kg
        render_compact_card("⚖️ คำนวณตามน้ำหนัก (1.25 mcg/kg/dose)", single_dose, "วันละ 2 ครั้ง (ทุก 12 ชม.)", unit="mcg")
    else:
        render_compact_card("📌 คำนวณตามอายุ", 25.0, "วันละ 1 - 2 ครั้ง", unit="mcg")

elif selected_drug == "Dimenhydrinate":
    if 24 <= total_months <= 60:
        render_compact_card("📌 คำนวณตามอายุ", (15.0, 25.0), "ทุก 6 - 8 ชั่วโมง", "Max 75 mg/day")
    elif 72 <= total_months <= 131:
        render_compact_card("📌 คำนวณตามอายุ", (25.0, 50.0), "ทุก 6 - 8 ชั่วโมง", "Max 150 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "2 ถึง 11 ปี"

elif selected_drug == "Domperidone":
    # 0.75 mg/kg/day แบ่ง 3 ครั้งก่อนอาหาร
    single_dose = (0.75 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", single_dose, "วันละ 3 ครั้ง ก่อนอาหาร 15-30 นาที", "Max 30 mg/day")

elif selected_drug == "Dicyclomine":
    if 6 <= total_months <= 24:
        render_compact_card("📌 คำนวณตามอายุ", (5.0, 10.0), "วันละ 3 - 4 ครั้ง ก่อนอาหาร")
    elif total_months > 24:
        render_compact_card("📌 คำนวณตามอายุ", 10.0, "วันละ 3 - 4 ครั้ง ก่อนอาหาร")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Hyoscine":
    if 6 <= total_months <= 12:
        render_compact_card("📌 คำนวณตามอายุ", 5.0, "วันละ 3 - 4 ครั้ง")
    elif 12 < total_months <= 72:
        render_compact_card("📌 คำนวณตามอายุ", (5.0, 10.0), "วันละ 3 - 4 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือน ถึง 6 ปี"

elif selected_drug == "Simethicone":
    if total_months < 24:
        render_compact_card("📌 คำนวณตามอายุ", 20.0, "วันละ 3 - 4 ครั้ง หลังอาหาร/ก่อนนอน")
    else:
        render_compact_card("📌 คำนวณตามอายุ", 40.0, "วันละ 3 - 4 ครั้ง หลังอาหาร/ก่อนนอน")

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    if total_months <= 1:
        single_ml = 1.0 * weight_kg
        st.write(f"👉 ทานครั้งละ **{single_ml:.1f} ml** (1 ml/kg/dose)")
    elif 1 < total_months <= 12:
        st.write("👉 ทานครั้งละ **2 - 5 ml** วันละ 3-4 ครั้ง หลังอาหาร 1 ชม.")
    elif 12 < total_months <= 60:
        st.write("👉 ทานครั้งละ **5 - 15 ml** วันละ 3-4 ครั้ง หลังอาหาร 1 ชม.")
    elif 72 <= total_months <= 144:
        st.write("👉 ทานครั้งละ **15 - 45 ml** วันละ 3-4 ครั้ง หลังอาหาร 1 ชม.")

elif selected_drug == "Lactulose (Laevolac)":
    if 1 <= total_months <= 72:
        st.write("👉 ทาน **5 - 10 ml/day** วันละ 1 ครั้ง")
    elif 72 < total_months <= 168:
        st.write("👉 ทาน **15 ml/day** วันละ 1 ครั้ง")
    elif total_months > 168:
        st.write("👉 ทาน **15 - 30 ml/day** วันละ 1 ครั้ง")
    else:
        age_out_of_range = True
        age_range_text = "1 เดือนขึ้นไป"

elif selected_drug == "Metronidazole":
    # Amebiasis: 35-50 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (35 * weight_kg) / 3
    single_max = (50 * weight_kg) / 3
    render_compact_card("⚖️ Amebiasis (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "วันละ 3 ครั้ง (ทุก 8 ชม.)")

elif selected_drug == "Albendazole":
    if 12 <= total_months <= 24:
        render_compact_card("📌 คำนวณตามอายุ", 200.0, "ทานครั้งเดียว (Single dose)")
    elif total_months > 24:
        render_compact_card("📌 คำนวณตามอายุ", 400.0, "ทานครั้งเดียว ( Single dose ) หรือ วันละ 1 ครั้ง ติดต่อกัน 3 วัน")
    else:
        age_out_of_range = True
        age_range_text = "1 ปีขึ้นไป"

elif selected_drug == "Mebendazole":
    if total_months >= 24:
        render_compact_card("📌 คำนวณตามอายุ", 100.0, "ทานครั้งเดียว หรือ วันละ 2 ครั้ง ติดต่อกัน 3 วัน")
    else:
        age_out_of_range = True
        age_range_text = "2 ปีขึ้นไป"

elif selected_drug == "Penicillin V":
    # 25-50 mg/kg/day แบ่ง 4 ครั้ง
    single_min = (25 * weight_kg) / 4
    single_max = (50 * weight_kg) / 4
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 4 ครั้ง/วัน)", (single_min, single_max), "ทุก 6 ชั่วโมง ก่อนอาหาร", "Max 3,000 mg/day")

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    if total_months < 3:
        # 20-30 mg/kg/day แบ่ง 2 ครั้ง
        s_min = (20 * weight_kg) / 2
        s_max = (30 * weight_kg) / 2
        render_compact_card("⚖️ สำหรับเด็ก < 3 เดือน (แบ่ง 2 ครั้ง/วัน)", (s_min, s_max), "ทุก 12 ชั่วโมง")
    else:
        # ปกติ 20-50 mg/kg/day แบ่ง 3 ครั้ง
        s_min = (20 * weight_kg) / 3
        s_max = (50 * weight_kg) / 3
        s_high = (80 * weight_kg) / 2 # High dose แบ่ง 2 ครั้ง
        render_compact_card("⚖️ ขนาดปกติ (แบ่ง 3 ครั้ง/วัน)", (s_min, s_max), "ทุก 8 ชั่วโมง")
        render_compact_card("⚖️ High dose (แบ่ง 2 ครั้ง/วัน)", s_high, "ทุก 12 ชั่วโมง")

elif selected_drug == "Cloxacillin":
    # 50-100 mg/kg/day แบ่ง 4 ครั้ง
    single_min = (50 * weight_kg) / 4
    single_max = (100 * weight_kg) / 4
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 4 ครั้ง/วัน)", (single_min, single_max), "ทุก 6 ชั่วโมง ก่อนอาหาร", "Max 4,000 mg/day")

elif selected_drug == "Dicloxacillin":
    # 25-50 mg/kg/day แบ่ง 4 ครั้ง
    single_min = (25 * weight_kg) / 4
    single_max = (50 * weight_kg) / 4
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 4 ครั้ง/วัน)", (single_min, single_max), "ทุก 6 ชั่วโมง ก่อนอาหาร")

elif selected_drug == "Cephalexin":
    # 25-50 mg/kg/day แบ่ง 4 ครั้ง
    single_min = (25 * weight_kg) / 4
    single_max = (50 * weight_kg) / 4
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 4 ครั้ง/วัน)", (single_min, single_max), "ทุก 6 ชั่วโมง", "Max 2,000 mg/day")

elif selected_drug == "Cefuroxime":
    # 20-30 mg/kg/day แบ่ง 2 ครั้ง
    single_min = (20 * weight_kg) / 2
    single_max = (30 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", (single_min, single_max), "ทุก 12 ชั่วโมง หลังอาหาร", "Max 500 mg/dose")

elif selected_drug == "Cefaclor":
    # 20-40 mg/kg/day แบ่ง 3 ครั้ง
    single_min = (20 * weight_kg) / 3
    single_max = (40 * weight_kg) / 3
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 3 ครั้ง/วัน)", (single_min, single_max), "ทุก 8 ชั่วโมง", "Max 1,500 mg/day")

elif selected_drug == "Cefdinir":
    # 14 mg/kg/day แบ่ง 2 ครั้ง
    single_dose = (14 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", single_dose, "ทุก 12 ชั่วโมง", "Max 600 mg/day")

elif selected_drug == "Cefixime":
    # 8 mg/kg/day วันละ 1-2 ครั้ง (กรณีแบ่ง 2 ครั้ง)
    single_dose = (8 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", single_dose, "ทุก 12 ชั่วโมง (หรือทานครั้งเดียวต่อวัน)", "Max 400 mg/day")

elif selected_drug == "Cefditoren pivoxil":
    # 10-20 mg/kg/day แบ่ง 2 ครั้ง
    single_min = (10 * weight_kg) / 2
    single_max = (20 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", (single_min, single_max), "ทุก 12 ชั่วโมง หลังอาหาร")

elif selected_drug == "Erythromycin":
    # 30-50 mg/kg/day แบ่ง 4 ครั้ง
    single_min = (30 * weight_kg) / 4
    single_max = (50 * weight_kg) / 4
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 4 ครั้ง/วัน)", (single_min, single_max), "ทุก 6 ชั่วโมง")

elif selected_drug == "Azithromycin":
    # 10 mg/kg/day วันละ 1 ครั้ง
    single_dose = min(10 * weight_kg, 500.0)
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (วันละ 1 ครั้ง)", single_dose, "วันละ 1 ครั้ง ติดต่อกัน 3 - 5 วัน", "Max 500 mg/day")

elif selected_drug == "Roxithromycin":
    # 5-8 mg/kg/day แบ่ง 2 ครั้ง
    single_min = (5 * weight_kg) / 2
    single_max = (8 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", (single_min, single_max), "ทุก 12 ชั่วโมง ก่อนอาหาร", "Max 300 mg/day")

elif selected_drug == "Clarithromycin":
    # 15 mg/kg/day แบ่ง 2 ครั้ง
    single_dose = (15 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", single_dose, "ทุก 12 ชั่วโมง", "Max 500 mg/dose")

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    # TMP 8 mg/kg/day แบ่ง 2 ครั้ง
    single_tmp = (8 * weight_kg) / 2
    render_compact_card("⚖️ คำนวณตามน้ำหนัก (แบ่ง 2 ครั้ง/วัน)", single_tmp, "ทุก 12 ชั่วโมง", "อ้างอิงขนาดยาตามตัวยา TMP")

# --- แสดงเตือนอายุนอกเกณฑ์ ---
if age_out_of_range:
    st.error(f"⚠️ **แจ้งเตือน:** อายุของผู้ป่วย ({age_years} ปี {age_months} เดือน) **ไม่อยู่ในช่วงเกณฑ์อายุที่รองรับ** ของยา {selected_drug}\n\n*(เกณฑ์อายุที่ใช้ได้: **{age_range_text}**)*")

st.markdown("---")
st.caption("⚠️ **หมายเหตุ:** ใช้สำหรับช่วยคำนวณเบื้องต้นเท่านั้น ควรตรวจสอบความถูกต้องก่อนใช้จริง")

