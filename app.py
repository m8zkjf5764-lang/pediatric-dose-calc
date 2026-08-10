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

# --- Helper Functions สำหรับคำนวณและแสดงผลแบบ UI Card ---

def calc_dose_val(dose_val, unit="mg"):
    """คำนวณแปลง mg/mcg เป็น ml และช้อนชา คืนค่าเป็น dict"""
    if dose_val is None or conc_mg <= 0:
        return None
    if isinstance(dose_val, tuple):
        d_min, d_max = dose_val
        ml_min = (d_min * conc_ml) / conc_mg
        ml_max = (d_max * conc_ml) / conc_mg
        tsp_min = ml_min / 5.0
        tsp_max = ml_max / 5.0
        return {
            "dose_str": f"{d_min:.2f} - {d_max:.2f} {unit}",
            "ml_str": f"{ml_min:.2f} - {ml_max:.2f} ml",
            "tsp_str": f"{tsp_min:.2f} - {tsp_max:.2f} ช้อนชา"
        }
    else:
        ml = (dose_val * conc_ml) / conc_mg
        tsp = ml / 5.0
        return {
            "dose_str": f"{dose_val:.2f} {unit}",
            "ml_str": f"{ml:.2f} ml",
            "tsp_str": f"{tsp:.2f} ช้อนชา"
        }

def render_dose_card(card_title, calc_data, frequency_info="", max_dose_info="", note=""):
    """ฟังก์ชั่นวาด Card แสดงผลตัวเลขใหญ่สไตล์ Dashboard"""
    st.markdown(f"### {card_title}")
    if calc_data:
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("💊 ขนาดยา (Dose)", calc_data["dose_str"])
        col_m2.metric("🧪 ปริมาตร (Volume)", calc_data["ml_str"])
        col_m3.metric("🥄 ปริมาณ (Teaspoon)", calc_data["tsp_str"])
    
    if frequency_info:
        st.markdown(f"⏱️ **วิธีใช้ / ความถี่:** {frequency_info}")
    if max_dose_info:
        st.caption(f"⚠️ **ขนาดยาสูงสุด (Max Dose):** {max_dose_info}")
    if note:
        st.info(f"💡 **ข้อแนะนำเพิ่มเติม:** {note}")

# --- Section 3: ประมวลผลและแสดงผลลัพธ์ ---
st.header(f"3. ผลการคำนวณ: {selected_drug}")

age_out_of_range = False
age_range_text = ""

# Logic ยา 55 ตัว
if selected_drug == "Acetaminophen":
    w_min = 10 * weight_kg
    w_max = 15 * weight_kg
    calc_res = calc_dose_val((w_min, w_max))
    
    render_dose_card(
        card_title="⚖️ ขนาดยาคำนวณตามน้ำหนัก (Weight-based dose)",
        calc_data=calc_res,
        frequency_info="ทานทุก 4 - 6 ชั่วโมง เวลาปวดหรือมีไข้",
        max_dose_info="ไม่เกิน 75 mg/kg/day"
    )

elif selected_drug == "Brompheniramine maleate":
    if 24 <= total_months <= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", None, "ทุก 6 - 8 ชม.", "8 mg/day", "คำนวณ 0.125 mg/kg/dose")
    elif 72 < total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((2, 4)), "ทุก 6 - 8 ชม.", "16 mg/day")
    elif total_months > 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((4, 8)), "ทุก 6 - 8 ชม.", "24 mg/day")
    else:
        age_out_of_range, age_range_text = True, "24 เดือน (2 ปี) ขึ้นไป"

    w_dose = (0.5 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่ายทุก 6 - 8 ชม.", note="อ้างอิงจาก 0.5 mg/kg/day")

elif selected_drug == "Chlorpheniramine maleate":
    if 24 <= total_months <= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(1), "ทุก 4 - 6 ชม.", "8 mg/day")
    elif 72 < total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2), "ทุก 4 - 6 ชม.", "12 mg/day")
    elif total_months > 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(4), "ทุก 4 - 6 ชม.", "24 mg/day")
    else:
        age_out_of_range, age_range_text = True, "24 เดือน (2 ปี) ขึ้นไป"

    w_dose = (0.35 * weight_kg) / 4
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่ายทุก 4 - 6 ชม.", note="อ้างอิงจาก 0.35 mg/kg/day")

elif selected_drug == "Diphenhydramine":
    if 24 <= total_months <= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((6.25, 12.5)), "ทุก 6 - 8 ชม.", "75 mg/day")
    elif 72 < total_months < 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((12.5, 25)), "ทุก 6 - 8 ชม.", "150 mg/day")
    elif total_months >= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((25, 50)), "ทุก 6 - 8 ชม.", "300 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป"

    if 24 <= total_months <= 144:
        w_dose = (5 * weight_kg) / 3
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่ายทุก 6 - 8 ชม.", note="อ้างอิงจาก 5 mg/kg/day")

elif selected_drug == "Hydroxyzine":
    if total_months < 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(12.5), "ทุก 6 - 8 ชม.")
    else:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((12.5, 25)), "ทุก 6 - 8 ชม.")

    if weight_kg <= 40:
        w_dose = (2 * weight_kg) / 3
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่ายทุก 6 - 8 ชม.", "50 mg/day", "อ้างอิงจาก 2 mg/kg/day")
    else:
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((25, 50)), "วันละ 1 - 2 ครั้ง", "100 mg/day")

elif selected_drug == "Cetirizine":
    if 6 <= total_months <= 11:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 1 ครั้ง")
    elif 12 <= total_months <= 23:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 1 - 2 ครั้ง", "5 mg/day")
    elif 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 1 - 2 ครั้ง (หรือ 5 mg วันละ 1 ครั้ง)", "5 mg/day")
    elif 61 <= total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((5, 10)), "วันละ 1 ครั้ง", "10 mg/day")
    elif total_months > 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(10), "วันละ 1 ครั้ง", "40 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

    w_dose = 0.25 * weight_kg
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 1 - 2 ครั้ง", note="อ้างอิงจาก 0.25 mg/kg/day")

elif selected_drug == "Levocetirizine":
    if 6 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(1.25), "วันละ 1 ครั้ง", "1.25 mg/day")
    elif 61 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 1 ครั้ง", "2.5 mg/day")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((2.5, 5)), "วันละ 1 ครั้ง", "20 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

    w_dose = min(0.125 * weight_kg, 5.0)
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 1 ครั้ง", "5 mg/day", "อ้างอิงจาก 0.125 mg/kg/day")

elif selected_drug == "Loratadine":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "วันละ 1 ครั้ง", "10 mg/day")
    elif total_months >= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(10), "วันละ 1 ครั้ง (หรือ 5 mg วันละ 2 ครั้ง)", "10 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Desloratadine":
    if 6 <= total_months <= 11:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(1), "วันละ 1 ครั้ง")
    elif 12 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(1.25), "วันละ 1 ครั้ง")
    elif 61 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 1 ครั้ง")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "วันละ 1 ครั้ง", "20 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Fexofenadine":
    if 6 <= total_months < 24:
        d_val = 15 if weight_kg < 10.5 else 30
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(d_val), "วันละ 2 ครั้ง")
    elif 24 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(30), "วันละ 2 ครั้ง", "60 mg/day")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(60), "วันละ 2 ครั้ง (หรือ 180 mg วันละ 1 ครั้ง)", "720 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Ketotifen":
    if total_months >= 72:
        w_dose = min(0.25 * weight_kg, 1.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 2 ครั้ง", "1 mg/dose", "คำนวณจาก 0.25 mg/kg/dose")
    else:
        age_out_of_range, age_range_text = True, "6 ปีขึ้นไป (72 เดือนขึ้นไป)"

elif selected_drug == "Montelukast":
    if 6 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(4), "วันละ 1 ครั้ง", "4 mg/day")
    elif 61 <= total_months <= 168:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "วันละ 1 ครั้ง", "5 mg/day")
    elif total_months >= 180:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(10), "วันละ 1 ครั้ง", "10 mg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Phenylephrine HCl":
    if 48 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "ทุก 4 ชม.", "15 mg/day")
    elif 72 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "ทุก 4 ชม.", "30 mg/day")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(10), "ทุก 4 ชม.", "60 mg/day")
    else:
        age_out_of_range, age_range_text = True, "4 ปีขึ้นไป (48 เดือนขึ้นไป)"

elif selected_drug == "Pseudoephedrine":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(15), "ทุก 4 - 6 ชม.", "60 mg/day")
        w_dose = 1 * weight_kg
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "ทุก 4 - 6 ชม.", note="อ้างอิงจาก 1 mg/kg/dose")
    elif 72 <= total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(30), "ทุก 4 - 6 ชม.", "120 mg/day")
    elif total_months > 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(60), "ทุก 4 - 6 ชม.", "240 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((50, 100)), "ทุก 4 ชม. (ไม่เกิน 6 ครั้ง/วัน)")
    elif 72 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((100, 200)), "ทุก 4 ชม. (ไม่เกิน 6 ครั้ง/วัน)")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((200, 400)), "ทุก 4 ชม. (ไม่เกิน 6 ครั้ง/วัน)")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose = (12 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่าย 3 - 4 ครั้ง/วัน", note="อ้างอิงจาก 12 mg/kg/day")

elif selected_drug == "Acetylcysteine":
    if 24 <= total_months <= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((50, 100)), "วันละ 2 - 4 ครั้ง")
    elif total_months > 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((100, 200)), "วันละ 3 ครั้ง", "600 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (20 * weight_kg) / 3
    w_dose_max = (30 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_dose_min, w_dose_max)), "แบ่งจ่าย 2 - 3 ครั้ง/วัน", note="อ้างอิงจาก 20-30 mg/kg/day")

elif selected_drug == "Ambroxol":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((7.5, 15)), "วันละ 3 ครั้ง")
    elif 72 <= total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((15, 30)), "วันละ 2 - 3 ครั้ง")
    elif total_months > 144:
        st.info("📌 **ขนาดยาตามอายุ:** 60 - 120 mg/day แบ่งวันละ 2 - 3 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (1.2 * weight_kg) / 3
    w_dose_max = (1.6 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_dose_min, w_dose_max)), "แบ่งจ่าย 2 - 3 ครั้ง/วัน", note="อ้างอิงจาก 1.2-1.6 mg/kg/day")

elif selected_drug == "Carbocysteine":
    if 24 <= total_months <= 60:
        st.info("📌 **ขนาดยาตามอายุ:** 200 - 500 mg/day แบ่งวันละ 2 - 3 ครั้ง")
    elif 72 <= total_months <= 131:
        st.info("📌 **ขนาดยาตามอายุ:** 300 - 750 mg/day แบ่งวันละ 3 ครั้ง")
    elif 132 <= total_months <= 179:
        st.info("📌 **ขนาดยาตามอายุ:** 300 mg - 2.25 g/day แบ่งวันละ 3 ครั้ง")
    elif total_months >= 180:
        st.info("📌 **ขนาดยาตามอายุ:** 750 mg - 2.25 g/day แบ่งวันละ 3 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

    if total_months > 24:
        w_dose_min = (15 * weight_kg) / 3
        w_dose_max = (20 * weight_kg) / 3
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_dose_min, w_dose_max)), "แบ่งจ่าย 3 - 4 ครั้ง/วัน", note="อ้างอิงจาก 15-20 mg/kg/day")

elif selected_drug == "Bromhexine":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2), "วันละ 3 ครั้ง (หรือ 4 mg วันละ 2 ครั้ง)", "8 mg/day")
    elif 72 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((4, 8)), "วันละ 3 ครั้ง", "24 mg/day")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((8, 16)), "วันละ 3 ครั้ง", "48 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"
        
    w_dose_min = (0.6 * weight_kg) / 3
    w_dose_max = (0.8 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_dose_min, w_dose_max)), "แบ่งจ่าย 3 - 4 ครั้ง/วัน", note="อ้างอิงจาก 0.6-0.8 mg/kg/day")

elif selected_drug == "Dextromethorphan":
    if 48 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((2.5, 7.5)), "ทุก 4 - 8 ชม.", "30 mg/day")
    elif 72 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((5, 10)), "ทุก 4 ชม.", "60 mg/day")
    elif total_months >= 132:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(20), "ทุก 4 ชม.", "120 mg/day")
    else:
        age_out_of_range, age_range_text = True, "4 ปีขึ้นไป (48 เดือนขึ้นไป)"

elif selected_drug == "Salbutamol":
    if 24 <= total_months <= 72:
        w_dose = 0.1 * weight_kg
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 3 ครั้ง", "12 mg/day", "คำนวณจาก 0.1 mg/kg/dose")
    elif 84 <= total_months <= 168:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2), "วันละ 3 - 4 ครั้ง", "24 mg/day")
    elif total_months >= 180:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((2, 4)), "วันละ 3 - 4 ครั้ง", "32 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Terbutaline sulfate":
    if total_months < 144:
        w_dose = 0.05 * weight_kg
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 3 ครั้ง", "5 mg/day", "คำนวณจาก 0.05 mg/kg/dose")
    elif 144 <= total_months <= 168:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(2.5), "วันละ 3 ครั้ง", "7.5 mg/day")
    elif total_months >= 180:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "วันละ 3 - 4 ครั้ง", "15 mg/day")

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    if total_months < 72:
        w_dose = 1.25 * weight_kg
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose, unit="mcg"), "ทุก 12 ชม.", note="คำนวณจาก 1.25 mcg/kg/dose")
        
    if total_months < 12:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((10, 15), unit="mcg"), "วันละ 2 ครั้ง", "30 mcg/day")
    elif 12 <= total_months <= 24:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((15, 20), unit="mcg"), "วันละ 2 ครั้ง", "40 mcg/day")
    elif 36 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((20, 25), unit="mcg"), "วันละ 2 ครั้ง", "50 mcg/day")
    elif 72 <= total_months <= 216:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(25, unit="mcg"), "วันละ 1 - 2 ครั้ง", "50 mcg/day")

elif selected_drug == "Dimenhydrinate":
    if 24 <= total_months <= 60:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((15, 25)), "ทุก 6 - 8 ชม.", "75 mg/day")
    elif 72 <= total_months <= 131:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((25, 50)), "ทุก 6 - 8 ชม.", "150 mg/day")
    else:
        age_out_of_range, age_range_text = True, "2 ถึง 11 ปี (24 ถึง 131 เดือน)"

elif selected_drug == "Domperidone":
    if weight_kg < 35:
        w_dose_day = min(0.75 * weight_kg, 30.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose_day/3), "วันละ 3 ครั้งก่อนอาหาร", "30 mg/day", "อ้างอิงจาก 0.75 mg/kg/day")
    else:
        st.warning("⚠️ น้ำหนักเกิน 35 kg พิจารณาขนาดยาผู้ใหญ่ (Max 30 mg/day)")

elif selected_drug == "Dicyclomine":
    if 6 <= total_months <= 24:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((5, 10)), "วันละ 3 - 4 ครั้งก่อนอาหาร")
    elif total_months > 24:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(10), "วันละ 3 - 4 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Hyoscine":
    if 6 <= total_months <= 12:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(5), "วันละ 3 - 4 ครั้ง")
    elif 12 < total_months <= 72:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((5, 10)), "วันละ 3 - 4 ครั้ง")
    else:
        age_out_of_range, age_range_text = True, "6 เดือน ถึง 6 ปี"

elif selected_drug == "Simethicone":
    if total_months < 24:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(20), "วันละ 3 - 4 ครั้ง", "500 mg/day")
    elif 24 <= total_months <= 144:
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val(40), "วันละ 3 - 4 ครั้ง", "500 mg/day")

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    if total_months <= 1:
        st.info(f"📌 **ขนาดยาคำนวณ:** {1 * weight_kg:.2f} ml/dose (1 ml/kg/dose)")
    elif 1 < total_months <= 12:
        st.info("📌 **ขนาดยาตามอายุ:** 2 - 5 ml/dose")
    elif 12 < total_months <= 60:
        st.info("📌 **ขนาดยาตามอายุ:** 5 - 15 ml/dose")
    elif 72 <= total_months <= 144:
        st.info("📌 **ขนาดยาตามอายุ:** 15 - 45 ml/dose")

elif selected_drug == "Lactulose (Laevolac)":
    if 1 <= total_months <= 72:
        st.info("📌 **ขนาดยาตามอายุ:** 5 - 10 ml/day วันละ 1 ครั้ง")
        w_dose = 1.5 * weight_kg
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 1 ครั้ง", note="อ้างอิงจาก 1-2 g/kg/day")
    elif 72 < total_months <= 168:
        st.info("📌 **ขนาดยาตามอายุ:** 15 ml/day วันละ 1 ครั้ง")
    elif total_months > 168:
        st.info("📌 **ขนาดยาตามอายุ:** 15 - 30 ml/day")
    else:
        age_out_of_range, age_range_text = True, "1 เดือนขึ้นไป"

elif selected_drug == "Metronidazole":
    w_ameba = min((35 * weight_kg)/3, 2250/3)
    w_anaerobic = min((15 * weight_kg)/3, 750)
    render_dose_card("⚖️ ขนาดยา Amebiasis (35-50 mg/kg/day)", calc_dose_val(w_ameba), "แบ่งจ่ายวันละ 3 ครั้ง")
    render_dose_card("⚖️ ขนาดยา Anaerobic (15-50 mg/kg/day)", calc_dose_val(w_anaerobic), "แบ่งจ่ายวันละ 3 ครั้ง")

elif selected_drug == "Albendazole":
    if 12 <= total_months <= 24:
        render_dose_card("📌 Roundworm/Pinworm/Hookworm", calc_dose_val(200), "ทานครั้งเดียว (Single dose)")
    elif total_months > 24:
        render_dose_card("📌 Roundworm/Pinworm/Hookworm", calc_dose_val(400), "ทานครั้งเดียว (Single dose)")
        st.caption("Whipworm: 400 mg OD x 3 วัน | Strongyloides: 400 mg BID x 7 วัน")
        w_tape = min(7.5 * weight_kg, 400.0)
        w_fluke = min(10 * weight_kg, 800.0)
        render_dose_card("⚖️ Tapeworm (7.5 mg/kg/dose)", calc_dose_val(w_tape), "วันละ 2 ครั้ง (BID)")
        render_dose_card("⚖️ Liver flukes (10 mg/kg/dose)", calc_dose_val(w_fluke), "วันละ 1 ครั้ง (OD)")
    else:
        age_out_of_range, age_range_text = True, "1 ปีขึ้นไป (12 เดือนขึ้นไป)"

elif selected_drug == "Mebendazole":
    if total_months >= 24:
        render_dose_card("📌 Pinworm", calc_dose_val(100), "ทานครั้งเดียว (Single dose)")
        st.caption("Roundworm/Whipworm/Hookworm: 100 mg BID x 3 วัน หรือ 500 mg Single dose")
    else:
        age_out_of_range, age_range_text = True, "2 ปีขึ้นไป (24 เดือนขึ้นไป)"

elif selected_drug == "Diclofenac":
    w_dose = (2 * weight_kg) / 3
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่าย 2 - 4 ครั้ง หลังอาหาร", "200 mg/day", "อ้างอิงจาก 2-3 mg/kg/day")

elif selected_drug == "Ibuprofen":
    w_min = 5 * weight_kg
    w_max = 10 * weight_kg
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "ทุก 6 - 8 ชม. หลังอาหาร", "40 mg/kg/day", "อ้างอิงจาก 5-10 mg/kg/dose")

elif selected_drug == "Penicillin V":
    if total_months < 144:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 3000 / 4)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 3 - 4 ครั้ง", "3 g/day", "อ้างอิงจาก 25-50 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "น้อยกว่า 12 ปี"

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    if total_months < 3:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 2 ครั้ง", note="อ้างอิงจาก 20-30 mg/kg/day")
    else:
        w_min = (20 * weight_kg) / 3
        w_max = min((50 * weight_kg) / 3, 500.0)
        w_high = min((80 * weight_kg) / 2, 1000.0)
        render_dose_card("⚖️ ขนาดยาปกติ (20-50 mg/kg/day)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 3 ครั้ง")
        render_dose_card("⚖️ ขนาดยา High dose (80-90 mg/kg/day)", calc_dose_val(w_high), "แบ่งจ่าย 2 ครั้ง")

elif selected_drug == "Cloxacillin":
    if total_months > 1:
        w_min = (50 * weight_kg) / 4
        w_max = min((100 * weight_kg) / 4, 4000 / 4)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 3 - 4 ครั้ง", "4 g/day", "อ้างอิงจาก 50-100 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Dicloxacillin":
    if weight_kg < 40:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 500.0)
        w_high = (100 * weight_kg) / 4
        render_dose_card("⚖️ ขนาดยาปกติ (25-50 mg/kg/day)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 4 ครั้ง")
        render_dose_card("⚖️ ขนาดยา High dose (50-100 mg/kg/day)", calc_dose_val(w_high), "แบ่งจ่าย 4 ครั้ง")
    else:
        st.warning("⚠️ น้ำหนักตั้งแต่ 40 kg ขึ้นไป แนะนำขนาดผู้ใหญ่ 250 - 500 mg/dose")

elif selected_drug == "Cephalexin":
    if total_months > 12:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 2000 / 4)
        w_high = min((100 * weight_kg) / 4, 4000 / 4)
        render_dose_card("⚖️ ขนาดยาปกติ (25-50 mg/kg/day)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 4 ครั้ง", "2 g/day")
        render_dose_card("⚖️ ขนาดยา High dose (75-100 mg/kg/day)", calc_dose_val(w_high), "แบ่งจ่าย 4 ครั้ง", "4 g/day")
    else:
        age_out_of_range, age_range_text = True, "มากกว่า 1 ปีขึ้นไป (12 เดือนขึ้นไป)"

elif selected_drug == "Cefuroxime":
    if 3 <= total_months <= 144:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 2 ครั้ง", "500 mg/dose", "อ้างอิงจาก 20-30 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "3 เดือน ถึง 12 ปี"

elif selected_drug == "Cefaclor":
    if total_months > 1:
        w_min = (20 * weight_kg) / 3
        w_max = min((40 * weight_kg) / 3, 1500 / 3)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 2 - 3 ครั้ง", "1.5 g/day", "อ้างอิงจาก 20-40 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Cefdinir":
    if 6 <= total_months <= 144:
        w_dose = min(14 * weight_kg, 600.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 1 - 2 ครั้ง", "600 mg/day", "อ้างอิงจาก 14 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือน ถึง 12 ปี"

elif selected_drug == "Cefixime":
    if total_months >= 6:
        w_min = 8 * weight_kg
        w_max = min(20 * weight_kg, 400.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "วันละ 1 - 2 ครั้ง", "400 mg/day", "อ้างอิงจาก 8-20 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Cefditoren pivoxil":
    if total_months >= 144:
        w_min = (10 * weight_kg) / 2
        w_max = (20 * weight_kg) / 2
        render_dose_card("📌 ขนาดยาตามอายุ (Age-based)", calc_dose_val((200, 400)), "วันละ 2 ครั้ง หลังอาหาร")
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่าย 2 - 3 ครั้ง", note="อ้างอิงจาก 10-20 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "12 ปีขึ้นไป (144 เดือนขึ้นไป)"

elif selected_drug == "Erythromycin":
    w_base = (30 * weight_kg) / 4
    w_max_base = min((50 * weight_kg) / 4, 2000 / 4)
    render_dose_card("⚖️ Base/Estolate/Stearate (30-50 mg/kg/day)", calc_dose_val((w_base, w_max_base)), "แบ่งจ่าย 4 ครั้ง", "2 g/day")

elif selected_drug == "Azithromycin":
    if total_months >= 6:
        w_dose = min(10 * weight_kg, 500.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "วันละ 1 ครั้ง x 3 วัน", "500 mg/day", "อ้างอิงจาก 5-12 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Roxithromycin":
    w_min = (5 * weight_kg) / 2
    w_max = min((8 * weight_kg) / 2, 300 / 2)
    render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val((w_min, w_max)), "แบ่งจ่ายวันละ 2 ครั้ง", "300 mg/day", "อ้างอิงจาก 5-8 mg/kg/day")

elif selected_drug == "Clarithromycin":
    if total_months >= 6:
        w_dose = min((15 * weight_kg) / 2, 500.0)
        render_dose_card("⚖️ ขนาดยาตามน้ำหนัก (Weight-based)", calc_dose_val(w_dose), "แบ่งจ่ายวันละ 2 ครั้ง", "500 mg/dose", "อ้างอิงจาก 15 mg/kg/day")
    else:
        age_out_of_range, age_range_text = True, "6 เดือนขึ้นไป"

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    if total_months >= 2:
        w_tmp = min((8 * weight_kg) / 2, 160.0)
        st.info(f"⚖️ **ขนาดยาคำนวณ:** TMP {w_tmp:.2f} mg / dose (อ้างอิงจาก TMP 8 mg/kg/day + SMX 40 mg/kg/day แบ่งจ่าย 2 ครั้ง)")
    else:
        age_out_of_range, age_range_text = True, "2 เดือนขึ้นไป"

# --- แสดงเตือนกรณีอายุนอกเกณฑ์ ---
if age_out_of_range:
    st.error(f"⚠️ **แจ้งเตือน:** อายุของผู้ป่วย ({age_years} ปี {age_months} เดือน) **ไม่อยู่ในช่วงเกณฑ์อายุที่ใช้คำนวณ** ของยา {selected_drug}\n\n*(ช่วงอายุที่รองรับสำหรับยาตัวนี้คือ: **{age_range_text}**)*")

st.markdown("---")
st.caption("⚠️ **หมายเหตุ:** โปรแกรมนี้ใช้สำหรับช่วยคำนวณเบื้องต้นเท่านั้น ควรตรวจสอบความถูกต้องและด่านการแพทย์ก่อนใช้จริง")

