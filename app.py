import streamlit as st

st.set_page_config(page_title="โปรแกรมคำนวณยาสูตรเด็ก", page_icon="👶", layout="wide")

st.title("👶 โปรแกรมคำนวณขนาดยาสำหรับเด็ก")
st.caption("Pediatric Dose Calculator")

# --- Section 1: ข้อมูลผู้ป่วย ---
st.subheader("1. ข้อมูลผู้ป่วย")
col1, col2 = st.columns(2)

with col1:
    st.write("**อายุผู้ป่วย**")
    col_y, col_m = st.columns(2)
    with col_y:
        age_years = st.number_input("ปี (Years)", min_value=0, max_value=18, value=2, step=1)
    with col_m:
        age_months = st.number_input("เดือน (Months)", min_value=0, max_value=11, value=0, step=1)
    
    total_months = (age_years * 12) + age_months

with col2:
    st.write("**น้ำหนักผู้ป่วย**")
    weight_kg = st.number_input("น้ำหนัก (kg)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)

st.info(f"👤 **สรุปข้อมูล:** อายุ **{age_years} ปี {age_months} เดือน** ({total_months} เดือน) | น้ำหนัก **{weight_kg:.1f} kg**")
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

# --- Helper Functions สำหรับแปลงค่าและแสดงผลแบบอ่านง่ายบนมือถือ ---
def calc_dose_values(dose_val):
    if dose_val is None or conc_mg <= 0:
        return None
    if isinstance(dose_val, tuple):
        d_min, d_max = dose_val
        ml_min = (d_min * conc_ml) / conc_mg
        ml_max = (d_max * conc_ml) / conc_mg
        return {
            "mg": f"{d_min:.2f} - {d_max:.2f}",
            "ml": f"{ml_min:.2f} - {ml_max:.2f}",
            "tsp": f"{ml_min/5.0:.2f} - {ml_max/5.0:.2f}"
        }
    else:
        ml = (dose_val * conc_ml) / conc_mg
        return {
            "mg": f"{dose_val:.2f}",
            "ml": f"{ml:.2f}",
            "tsp": f"{ml/5.0:.2f}"
        }

def render_compact_result(title, dose_val, unit_name, frequency, max_dose=""):
    st.markdown(f"#### {title}")
    res = calc_dose_values(dose_val)
    if res:
        # ใช้ตารางกระจายตัวเลขขนาดกำลังพอดี ดูในมือถือแล้วเรียบสวย
        st.markdown(f"""
        | ปริมาณตัวยา | ปริมาตร (ml) | ช้อนชา (tsp) |
        | :---: | :---: | :---: |
        | **{res['mg']}** {unit_name} | **{res['ml']}** ml | **{res['tsp']}** ช้อนชา |
        """)
    
    st.markdown(f"⏱️ **วิธีรับประทาน/ความถี่:** {frequency}")
    if max_dose:
        st.caption(f"⚠️ **ขนาดยาสูงสุด (Max Dose):** {max_dose}")

# --- Section 3: ประมวลผลและแสดงผลลัพธ์ ---
st.subheader(f"3. ผลการคำนวณ: {selected_drug}")

age_dose_info = None
weight_dose_info = None
age_out_of_range = False
age_range_text = ""

# --- Logic คำนวณขนาดยา 55 ตัว ---
if selected_drug == "Brompheniramine maleate":
    if 24 <= total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (2-6 ปี)", 0.125 * weight_kg, "mg", "ทุก 6-8 ชม.", "8 mg/day")
    elif 72 < total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6-12 ปี)", (2, 4), "mg", "ทุก 6-8 ชม.", "16 mg/day")
    elif total_months > 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", (4, 8), "mg", "ทุก 6-8 ชม.", "24 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
    
    w_dose = (0.5 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (0.5 mg/kg/day)", w_dose, "mg", "แบ่งจ่ายทุก 6-8 ชม.", "")

elif selected_drug == "Chlorpheniramine maleate":
    if 24 <= total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (2-6 ปี)", 1, "mg", "ทุก 4-6 ชม.", "8 mg/day")
    elif 72 < total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6-12 ปี)", 2, "mg", "ทุก 4-6 ชม.", "12 mg/day")
    elif total_months > 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", 4, "mg", "ทุก 4-6 ชม.", "24 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
    
    w_dose = (0.35 * weight_kg) / 4
    weight_dose_info = ("คำนวณตามน้ำหนัก (0.35 mg/kg/day)", w_dose, "mg", "แบ่งจ่ายทุก 4-6 ชม.", "")

elif selected_drug == "Diphenhydramine":
    if 24 <= total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (2-6 ปี)", (6.25, 12.5), "mg", "ทุก 6-8 ชม.", "75 mg/day")
    elif 72 < total_months < 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6-12 ปี)", (12.5, 25), "mg", "ทุก 6-8 ชม.", "150 mg/day")
    elif total_months >= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", (25, 50), "mg", "ทุก 6-8 ชม.", "300 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป"
        
    if 24 <= total_months <= 144:
        w_dose = (5 * weight_kg) / 3
        weight_dose_info = ("คำนวณตามน้ำหนัก (5 mg/kg/day)", w_dose, "mg", "แบ่งจ่ายทุก 6-8 ชม.", "")

elif selected_drug == "Hydroxyzine":
    if total_months < 72:
        age_dose_info = ("ตามเกณฑ์อายุ (<6 ปี)", 12.5, "mg", "ทุก 6-8 ชม.", "")
    else:
        age_dose_info = ("ตามเกณฑ์อายุ (>=6 ปี)", (12.5, 25), "mg", "ทุก 6-8 ชม.", "")
        
    if weight_kg <= 40:
        w_dose = (2 * weight_kg) / 3
        weight_dose_info = ("คำนวณตามน้ำหนัก (2 mg/kg/day)", w_dose, "mg", "แบ่งจ่ายทุก 6-8 ชม.", "50 mg/day")
    else:
        weight_dose_info = ("คำนวณตามน้ำหนัก (>40 kg)", (25, 50), "mg", "วันละ 1-2 ครั้ง", "100 mg/day")

elif selected_drug == "Cetirizine":
    if 6 <= total_months <= 11:
        age_dose_info = ("ตามเกณฑ์อายุ (6-11 เดือน)", 2.5, "mg", "วันละ 1 ครั้ง", "")
    elif 12 <= total_months <= 23:
        age_dose_info = ("ตามเกณฑ์อายุ (12-23 เดือน)", 2.5, "mg", "วันละ 1-2 ครั้ง", "5 mg/day")
    elif 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2-5 ปี)", (2.5, 5), "mg", "วันละ 1-2 ครั้ง", "5 mg/day")
    elif 61 <= total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6-12 ปี)", (5, 10), "mg", "วันละ 1 ครั้ง", "10 mg/day")
    elif total_months > 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", 10, "mg", "วันละ 1 ครั้ง", "40 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"
        
    w_dose = 0.25 * weight_kg
    weight_dose_info = ("คำนวณตามน้ำหนัก (0.25 mg/kg/day)", w_dose, "mg", "วันละ 1-2 ครั้ง", "")

elif selected_drug == "Levocetirizine":
    if 6 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (6 เดือน - 5 ปี)", 1.25, "mg", "วันละ 1 ครั้ง", "1.25 mg/day")
    elif 61 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", 2.5, "mg", "วันละ 1 ครั้ง", "2.5 mg/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (2.5, 5), "mg", "วันละ 1 ครั้ง", "20 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"
        
    w_dose = min(0.125 * weight_kg, 5.0)
    weight_dose_info = ("คำนวณตามน้ำหนัก (0.125 mg/kg/day)", w_dose, "mg", "วันละ 1 ครั้ง", "5 mg/day")

elif selected_drug == "Loratadine":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", 5, "mg", "วันละ 1 ครั้ง", "10 mg/day")
    elif total_months >= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (>=6 ปี)", (5, 10), "mg", "วันละ 1-2 ครั้ง", "10 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"

elif selected_drug == "Desloratadine":
    if 6 <= total_months <= 11:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 เดือน)", 1, "mg", "วันละ 1 ครั้ง", "")
    elif 12 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (1 - 5 ปี)", 1.25, "mg", "วันละ 1 ครั้ง", "")
    elif 61 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", 2.5, "mg", "วันละ 1 ครั้ง", "")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", 5, "mg", "วันละ 1 ครั้ง", "20 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Fexofenadine":
    if 6 <= total_months < 24:
        d_val = 15 if weight_kg < 10.5 else 30
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 23 เดือน)", d_val, "mg", "วันละ 2 ครั้ง", "")
    elif 24 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 11 ปี)", 30, "mg", "วันละ 2 ครั้ง", "60 mg/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (60, 180), "mg", "วันละ 1-2 ครั้ง", "720 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Ketotifen":
    if total_months >= 72:
        w_dose = min(0.25 * weight_kg, 1.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (0.25 mg/kg/dose)", w_dose, "mg", "วันละ 2 ครั้ง", "1 mg/dose")
    else:
        age_out_of_range = True
        age_range_text = "72 เดือนขึ้นไป (6 ปีขึ้นไป)"

elif selected_drug == "Montelukast":
    if 6 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (6 เดือน - 5 ปี)", 4, "mg", "วันละ 1 ครั้ง", "4 mg/day")
    elif 61 <= total_months <= 168:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 14 ปี)", 5, "mg", "วันละ 1 ครั้ง", "5 mg/day")
    elif total_months >= 180:
        age_dose_info = ("ตามเกณฑ์อายุ (>=15 ปี)", 10, "mg", "วันละ 1 ครั้ง", "10 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Phenylephrine HCl":
    if 48 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (4 - 5 ปี)", 2.5, "mg", "ทุก 4 ชม.", "15 mg/day")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", 5, "mg", "ทุก 4 ชม.", "30 mg/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", 10, "mg", "ทุก 4 ชม.", "60 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "48 เดือนขึ้นไป (4 ปีขึ้นไป)"

elif selected_drug == "Pseudoephedrine":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", 15, "mg", "ทุก 4-6 ชม.", "60 mg/day")
        weight_dose_info = ("คำนวณตามน้ำหนัก (1 mg/kg/dose)", 1 * weight_kg, "mg", "ทุก 4-6 ชม.", "")
    elif 72 <= total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 12 ปี)", 30, "mg", "ทุก 4-6 ชม.", "120 mg/day")
    elif total_months > 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", 60, "mg", "ทุก 4-6 ชม.", "240 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", (50, 100), "mg", "ทุก 4 ชม.", "6 doses/day")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", (100, 200), "mg", "ทุก 4 ชม.", "6 doses/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (200, 400), "mg", "ทุก 4 ชม.", "6 doses/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
        
    w_dose = (12 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (12 mg/kg/day)", w_dose, "mg", "แบ่งจ่าย 3-4 ครั้ง/วัน", "")

elif selected_drug == "Acetylcysteine":
    if 24 <= total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 6 ปี)", (50, 100), "mg", "วันละ 2-4 ครั้ง", "")
    elif total_months > 72:
        age_dose_info = ("ตามเกณฑ์อายุ (>6 ปี)", (100, 200), "mg", "วันละ 3 ครั้ง", "600 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
        
    w_min = (20 * weight_kg) / 3
    w_max = (30 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (20-30 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย 2-3 ครั้ง/วัน", "")

elif selected_drug == "Ambroxol":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", (7.5, 15), "mg", "วันละ 3 ครั้ง", "")
    elif 72 <= total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 12 ปี)", (15, 30), "mg", "วันละ 2-3 ครั้ง", "")
    elif total_months > 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>12 ปี)", (20, 40), "mg", "วันละ 2-3 ครั้ง", "120 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
        
    w_min = (1.2 * weight_kg) / 3
    w_max = (1.6 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (1.2-1.6 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย 2-3 ครั้ง/วัน", "")

elif selected_drug == "Carbocysteine":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", (66, 166), "mg", "วันละ 2-3 ครั้ง", "")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", (100, 250), "mg", "วันละ 3 ครั้ง", "")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (250, 750), "mg", "วันละ 3 ครั้ง", "2.25 g/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"

    w_min = (15 * weight_kg) / 3
    w_max = (20 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (15-20 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย 3-4 ครั้ง", "")

elif selected_drug == "Bromhexine":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", (2, 4), "mg", "วันละ 2-3 ครั้ง", "8 mg/day")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", (4, 8), "mg", "วันละ 3 ครั้ง", "24 mg/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (8, 16), "mg", "วันละ 3 ครั้ง", "48 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"
        
    w_min = (0.6 * weight_kg) / 3
    w_max = (0.8 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (0.6-0.8 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย 3-4 ครั้ง", "")

elif selected_drug == "Dextromethorphan":
    if 48 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (4 - 5 ปี)", (2.5, 7.5), "mg", "ทุก 4-8 ชม.", "30 mg/day")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", (5, 10), "mg", "ทุก 4 ชม.", "60 mg/day")
    elif total_months >= 132:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", 20, "mg", "ทุก 4 ชม.", "120 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "48 เดือนขึ้นไป (4 ปีขึ้นไป)"

elif selected_drug == "Salbutamol":
    if 24 <= total_months <= 72:
        w_dose = 0.1 * weight_kg
        weight_dose_info = ("คำนวณตามน้ำหนัก (0.1 mg/kg/dose)", w_dose, "mg", "วันละ 3 ครั้ง", "12 mg/day")
    elif 84 <= total_months <= 168:
        age_dose_info = ("ตามเกณฑ์อายุ (7 - 14 ปี)", 2, "mg", "วันละ 3-4 ครั้ง", "24 mg/day")
    elif total_months >= 180:
        age_dose_info = ("ตามเกณฑ์อายุ (>=15 ปี)", (2, 4), "mg", "วันละ 3-4 ครั้ง", "32 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"

elif selected_drug == "Terbutaline sulfate":
    if total_months < 144:
        w_dose = 0.05 * weight_kg
        weight_dose_info = ("คำนวณตามน้ำหนัก (0.05 mg/kg/dose)", w_dose, "mg", "วันละ 3 ครั้ง", "5 mg/day")
    elif 144 <= total_months <= 168:
        age_dose_info = ("ตามเกณฑ์อายุ (12 - 14 ปี)", 2.5, "mg", "วันละ 3 ครั้ง", "7.5 mg/day")
    elif total_months >= 180:
        age_dose_info = ("ตามเกณฑ์อายุ (>=15 ปี)", 5, "mg", "วันละ 3-4 ครั้ง", "15 mg/day")

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    if total_months < 72:
        w_dose = 1.25 * weight_kg
        weight_dose_info = ("คำนวณตามน้ำหนัก (1.25 mcg/kg/dose)", w_dose, "mcg", "ทุก 12 ชม.", "")
        
    if total_months < 12:
        age_dose_info = ("ตามเกณฑ์อายุ (<1 ปี)", (10, 15), "mcg", "วันละ 2 ครั้ง", "30 mcg/day")
    elif 12 <= total_months <= 24:
        age_dose_info = ("ตามเกณฑ์อายุ (1 - 2 ปี)", (15, 20), "mcg", "วันละ 2 ครั้ง", "40 mcg/day")
    elif 36 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (3 - 5 ปี)", (20, 25), "mcg", "วันละ 2 ครั้ง", "50 mcg/day")
    elif 72 <= total_months <= 216:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 18 ปี)", 25, "mcg", "วันละ 1-2 ครั้ง", "50 mcg/day")

elif selected_drug == "Dimenhydrinate":
    if 24 <= total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 5 ปี)", (15, 25), "mg", "ทุก 6-8 ชม.", "75 mg/day")
    elif 72 <= total_months <= 131:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 11 ปี)", (25, 50), "mg", "ทุก 6-8 ชม.", "150 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "24 ถึง 131 เดือน (2 - 11 ปี)"

elif selected_drug == "Domperidone":
    if weight_kg < 35:
        w_dose = (0.75 * weight_kg) / 3
        weight_dose_info = ("คำนวณตามน้ำหนัก (0.75 mg/kg/day)", w_dose, "mg", "วันละ 3 ครั้งก่อนอาหาร", "30 mg/day")

elif selected_drug == "Dicyclomine":
    if 6 <= total_months <= 24:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 24 เดือน)", (5, 10), "mg", "วันละ 3-4 ครั้งก่อนอาหาร", "")
    elif total_months > 24:
        age_dose_info = ("ตามเกณฑ์อายุ (>2 ปี)", 10, "mg", "วันละ 3-4 ครั้งก่อนอาหาร", "")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Hyoscine":
    if 6 <= total_months <= 12:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 12 เดือน)", 5, "mg", "วันละ 3-4 ครั้ง", "")
    elif 12 < total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (1 - 6 ปี)", (5, 10), "mg", "วันละ 3-4 ครั้ง", "")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือน ถึง 6 ปี"

elif selected_drug == "Simethicone":
    if total_months < 24:
        age_dose_info = ("ตามเกณฑ์อายุ (<2 ปี)", 20, "mg", "วันละ 3-4 ครั้ง หลังอาหาร/ก่อนนอน", "500 mg/day")
    elif 24 <= total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (2 - 12 ปี)", 40, "mg", "วันละ 3-4 ครั้ง หลังอาหาร/ก่อนนอน", "500 mg/day")

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    if total_months <= 1:
        weight_dose_info = ("คำนวณตามน้ำหนัก (1 ml/kg/dose)", 1 * weight_kg, "ml", "วันละ 3-4 ครั้ง หลังอาหาร", "")
    elif 1 < total_months <= 12:
        age_dose_info = ("ตามเกณฑ์อายุ (1-12 เดือน)", (2, 5), "ml", "วันละ 3-4 ครั้ง หลังอาหาร", "")
    elif 12 < total_months <= 60:
        age_dose_info = ("ตามเกณฑ์อายุ (1-5 ปี)", (5, 15), "ml", "วันละ 3-4 ครั้ง หลังอาหาร", "")
    elif 72 <= total_months <= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (6-12 ปี)", (15, 45), "ml", "วันละ 3-4 ครั้ง หลังอาหาร", "")

elif selected_drug == "Lactulose (Laevolac)":
    if 1 <= total_months <= 72:
        age_dose_info = ("ตามเกณฑ์อายุ (1 เดือน - 6 ปี)", (5, 10), "ml", "วันละ 1 ครั้ง", "")
    elif 72 < total_months <= 168:
        age_dose_info = ("ตามเกณฑ์อายุ (6 - 14 ปี)", 15, "ml", "วันละ 1 ครั้ง", "")
    elif total_months > 168:
        age_dose_info = ("ตามเกณฑ์อายุ (>14 ปี)", (15, 30), "ml", "วันละ 1 ครั้ง", "")
    else:
        age_out_of_range = True
        age_range_text = "1 เดือนขึ้นไป"

elif selected_drug == "Metronidazole":
    w_dose = min((35 * weight_kg)/3, 750.0)
    weight_dose_info = ("คำนวณตามน้ำหนัก (Amebiasis: 35 mg/kg/day)", w_dose, "mg", "แบ่งจ่าย วันละ 3 ครั้ง", "")

elif selected_drug == "Albendazole":
    if 12 <= total_months <= 24:
        age_dose_info = ("ตามเกณฑ์อายุ (1 - 2 ปี)", 200, "mg", "รับประทานครั้งเดียว (Single dose)", "")
    elif total_months > 24:
        age_dose_info = ("ตามเกณฑ์อายุ (>2 ปี)", 400, "mg", "รับประทานครั้งเดียว หรือ วันละ 1 ครั้ง ตามชนิดพยาธิ", "")
    else:
        age_out_of_range = True
        age_range_text = "12 เดือนขึ้นไป (1 ปีขึ้นไป)"

elif selected_drug == "Mebendazole":
    if total_months >= 24:
        age_dose_info = ("ตามเกณฑ์อายุ (>=2 ปี)", 100, "mg", "รับประทานครั้งเดียว หรือ วันละ 2 ครั้ง x 3 วัน", "")
    else:
        age_out_of_range = True
        age_range_text = "24 เดือนขึ้นไป (2 ปีขึ้นไป)"

elif selected_drug == "Acetaminophen":
    w_min = 10 * weight_kg
    w_max = 15 * weight_kg
    weight_dose_info = ("คำนวณตามน้ำหนัก (10-15 mg/kg/dose)", (w_min, w_max), "mg", "ทุก 4-6 ชั่วโมง เวลาปวด/มีไข้", "75 mg/kg/day")

elif selected_drug == "Diclofenac":
    w_dose = (2 * weight_kg) / 3
    weight_dose_info = ("คำนวณตามน้ำหนัก (2 mg/kg/day)", w_dose, "mg", "แบ่งจ่าย 2-3 ครั้ง หลังอาหาร", "200 mg/day")

elif selected_drug == "Ibuprofen":
    w_min = 5 * weight_kg
    w_max = 10 * weight_kg
    weight_dose_info = ("คำนวณตามน้ำหนัก (5-10 mg/kg/dose)", (w_min, w_max), "mg", "ทุก 6-8 ชั่วโมง หลังอาหารทันที", "40 mg/kg/day")

elif selected_drug == "Penicillin V":
    if total_months < 144:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 750.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (25-50 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 3-4 ครั้ง", "3 g/day")
    else:
        age_out_of_range = True
        age_range_text = "น้อยกว่า 12 ปี"

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    if total_months < 3:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (20-30 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 2 ครั้ง", "")
    else:
        w_min = (20 * weight_kg) / 3
        w_max = min((50 * weight_kg) / 3, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (20-50 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 3 ครั้ง (High dose 80-90 mg/kg/day)", "")

elif selected_drug == "Cloxacillin":
    if total_months > 1:
        w_min = (50 * weight_kg) / 4
        w_max = min((100 * weight_kg) / 4, 1000.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (50-100 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 3-4 ครั้ง ก่อนอาหาร", "4 g/day")
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Dicloxacillin":
    if weight_kg < 40:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (25-50 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 4 ครั้ง ก่อนอาหาร", "")
    else:
        age_dose_info = ("น้ำหนัก >= 40 kg", (250, 500), "mg", "วันละ 4 ครั้ง ก่อนอาหาร", "")

elif selected_drug == "Cephalexin":
    if total_months > 12:
        w_min = (25 * weight_kg) / 4
        w_max = min((50 * weight_kg) / 4, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (25-50 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 4 ครั้ง", "4 g/day")
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 ปีขึ้นไป"

elif selected_drug == "Cefuroxime":
    if 3 <= total_months <= 144:
        w_min = (20 * weight_kg) / 2
        w_max = min((30 * weight_kg) / 2, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (20-30 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 2 ครั้ง หลังอาหาร", "500 mg/dose")
    else:
        age_out_of_range = True
        age_range_text = "3 เดือน ถึง 12 ปี"

elif selected_drug == "Cefaclor":
    if total_months > 1:
        w_min = (20 * weight_kg) / 3
        w_max = min((40 * weight_kg) / 3, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (20-40 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 3 ครั้ง", "1.5 g/day")
    else:
        age_out_of_range = True
        age_range_text = "มากกว่า 1 เดือนขึ้นไป"

elif selected_drug == "Cefdinir":
    if 6 <= total_months <= 144:
        w_dose = min(14 * weight_kg, 600.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (14 mg/kg/day)", w_dose, "mg", "วันละ 1-2 ครั้ง", "600 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือน ถึง 12 ปี"

elif selected_drug == "Cefixime":
    if total_months >= 6:
        w_min = 8 * weight_kg
        w_max = min(20 * weight_kg, 400.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (8-20 mg/kg/day)", (w_min, w_max), "mg", "วันละ 1-2 ครั้ง", "400 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Cefditoren pivoxil":
    if total_months >= 144:
        age_dose_info = ("ตามเกณฑ์อายุ (>=12 ปี)", (200, 400), "mg", "วันละ 2 ครั้ง หลังอาหาร", "")
    else:
        age_out_of_range = True
        age_range_text = "12 ปีขึ้นไป"

elif selected_drug == "Erythromycin":
    w_min = (30 * weight_kg) / 4
    w_max = min((50 * weight_kg) / 4, 500.0)
    weight_dose_info = ("คำนวณตามน้ำหนัก (30-50 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 4 ครั้ง", "2 g/day")

elif selected_drug == "Azithromycin":
    if total_months >= 6:
        w_dose = min(10 * weight_kg, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (10 mg/kg/day)", w_dose, "mg", "วันละ 1 ครั้ง ทานต่อเนื่อง 3-5 วัน", "500 mg/day")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Roxithromycin":
    w_min = (5 * weight_kg) / 2
    w_max = min((8 * weight_kg) / 2, 150.0)
    weight_dose_info = ("คำนวณตามน้ำหนัก (5-8 mg/kg/day)", (w_min, w_max), "mg", "แบ่งจ่าย วันละ 2 ครั้ง ก่อนอาหาร", "300 mg/day")

elif selected_drug == "Clarithromycin":
    if total_months >= 6:
        w_dose = min((15 * weight_kg) / 2, 500.0)
        weight_dose_info = ("คำนวณตามน้ำหนัก (15 mg/kg/day)", w_dose, "mg", "แบ่งจ่าย วันละ 2 ครั้ง", "500 mg/dose")
    else:
        age_out_of_range = True
        age_range_text = "6 เดือนขึ้นไป"

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    if total_months >= 2:
        w_tmp = min((8 * weight_kg) / 2, 160.0)
        weight_dose_info = ("คำนวณตาม TMP (8 mg/kg/day)", w_tmp, "mg TMP", "แบ่งจ่าย วันละ 2 ครั้ง", "")
    else:
        age_out_of_range = True
        age_range_text = "2 เดือนขึ้นไป"


# --- การแสดงผลสรุป ---
if age_out_of_range:
    st.error(f"⚠️ **ไม่อยู่ในเกณฑ์คำนวณอายุ:** ยา {selected_drug} เหมาะสำหรับเด็กอายุ **{age_range_text}** ขึ้นไป")

if age_dose_info:
    title, d_val, u_name, freq, m_dose = age_dose_info
    render_compact_result(f"📌 {title}", d_val, u_name, freq, m_dose)
    st.markdown("")

if weight_dose_info:
    title, d_val, u_name, freq, m_dose = weight_dose_info
    render_compact_result(f"⚖️ {title}", d_val, u_name, freq, m_dose)

if not age_dose_info and not weight_dose_info and not age_out_of_range:
    st.warning("⚠️ ไม่มีข้อมูลเกณฑ์คำนวณเฉพาะช่วงอายุน้ำหนักนี้ โปรดตรวจสอบเอกสารกำกับยาเพิ่มเติม")

st.markdown("---")
st.caption("⚠️ **หมายเหตุ:** โปรแกรมนี้ใช้สำหรับช่วยคำนวณเบื้องต้นเท่านั้น ควรตรวจสอบความถูกต้องและด่านการแพทย์ก่อนใช้จริง")

