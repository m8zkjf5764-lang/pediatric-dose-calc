import streamlit as st

st.set_page_config(page_title="Pediatric Dose Calculator", page_icon="💊", layout="wide")

st.title("💊 โปรแกรมคำนวณขนาดยาในเด็ก (Pediatric Dose Calculator)")
st.caption("ระบบคำนวณขนาดยาอ้างอิงตามเกณฑ์อายุและน้ำหนักตัว พร้อมระบบแจ้งเตือนช่วงอายุ")

st.sidebar.header("📌 กรอกข้อมูลผู้ป่วย")

# 1. รับค่าอายุเป็น ปี และ เดือน
col_y, col_m = st.sidebar.columns(2)
with col_y:
    age_years = st.number_input("อายุ (ปี)", min_value=0, max_value=18, value=3)
with col_m:
    age_months_input = st.number_input("อายุ (เดือน)", min_value=0, max_value=11, value=0)

# คำนวณอายุมวลรวม
total_months = (age_years * 12) + age_months_input
total_years = total_months / 12.0

# 2. รับค่าน้ำหนัก
weight = st.sidebar.number_input("น้ำหนัก (kg)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)

st.sidebar.info(f"📊 **ประมวลผล:** อายุ {age_years} ปี {age_months_input} เดือน ({total_months} เดือน) | น้ำหนัก {weight} kg")

st.subheader("💊 เลือกรายการยาที่ต้องการคำนวณ")

# รายการยา 55 ตัว
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
    "Penicillin V", "Amoxicillin / Amoxicillin + Clavulanic acid", "Cloxacillin",
    "Dicloxacillin", "Cephalexin", "Cefuroxime", "Cefaclor", "Cefdinir", "Cefixime",
    "Cefditoren pivoxil", "Erythromycin", "Azithromycin", "Roxithromycin", "Clarithromycin",
    "Co-trimoxazole (TMP + SMX)"
]

selected_drug = st.selectbox("พิมพ์ชื่อยาหรือเลือกจากรายการ:", drug_list)

st.write("---")

# ฟังก์ชันแสดงผล 2 คอลัมน์สำหรับ Dual Calculation
def render_dual_results(age_res, wt_res):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📅 คำนวณตามเกณฑ์อายุ")
        if age_res["valid"]:
            st.success(f"**ขนาดยา:** {age_res['dose']}")
            if age_res.get("max"):
                st.caption(f"🛑 ขนาดยาสูงสุด: {age_res['max']}")
        else:
            st.warning(f"⚠️ **ไม่อยู่ในช่วงอายุที่คำนวณได้:** {age_res['msg']}")
            
    with col2:
        st.markdown("### ⚖️ คำนวณตามเกณฑ์น้ำหนัก")
        if wt_res["valid"]:
            st.info(f"**ขนาดยาที่คำนวณได้:** {wt_res['dose']}")
            if wt_res.get("max"):
                st.caption(f"🛑 ขนาดยาสูงสุด: {wt_res['max']}")
        else:
            st.warning(f"⚠️ **ไม่อยู่ในช่วงน้ำหนัก/เกณฑ์ที่คำนวณได้:** {wt_res['msg']}")

# ฟังก์ชันแสดงผลเดี่ยว
def render_single_result(res_dict, calc_type="น้ำหนัก/อายุ"):
    if res_dict["valid"]:
        st.success(f"**ขนาดยาแนะนำ ({calc_type}):**\n\n{res_dict['dose']}")
        if res_dict.get("max"):
            st.caption(f"🛑 ขนาดยาสูงสุด: {res_dict['max']}")
    else:
        st.warning(f"⚠️ **ไม่อยู่ในช่วงที่รองรับ:** {res_dict['msg']}")

# LOGIC การคำนวณยาทั้งหมด
if selected_drug == "Brompheniramine maleate":
    # อายุ
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "ยาชนิดนี้รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years < 6:
        age_res = {"valid": True, "dose": f"0.125 mg/kg/dose = {0.125*weight:.2f} mg/dose ทุก 6-8 ชม.", "max": "8 mg/day"}
    elif 6 <= total_years <= 12:
        age_res = {"valid": True, "dose": "2 - 4 mg ทุก 6-8 ชม.", "max": "16 mg/day"}
    else:
        age_res = {"valid": True, "dose": "4 - 8 mg ทุก 6-8 ชม.", "max": "24 mg/day"}
    
    # น้ำหนัก
    wt_res = {"valid": True, "dose": f"0.5 mg/kg/day = {0.5*weight:.2f} mg/day (แบ่งให้ทุก 6-8 ชม.)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Chlorpheniramine maleate":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years < 6:
        age_res = {"valid": True, "dose": "1 mg ทุก 4-6 ชม.", "max": "8 mg/day"}
    elif 6 <= total_years <= 12:
        age_res = {"valid": True, "dose": "2 mg ทุก 4-6 ชม.", "max": "12 mg/day"}
    else:
        age_res = {"valid": True, "dose": "4 mg ทุก 4-6 ชม.", "max": "24 mg/day"}
        
    wt_res = {"valid": True, "dose": f"0.35 mg/kg/day = {0.35*weight:.2f} mg/day (แบ่งให้ทุก 4-6 ชม.)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Diphenhydramine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years < 6:
        age_res = {"valid": True, "dose": "6.25 - 12.5 mg ทุก 6-8 ชม.", "max": "75 mg/day"}
    elif 6 <= total_years < 12:
        age_res = {"valid": True, "dose": "12.5 - 25 mg ทุก 6-8 ชม.", "max": "150 mg/day"}
    else:
        age_res = {"valid": True, "dose": "25 - 50 mg ทุก 6-8 ชม.", "max": "300 mg/day"}
        
    wt_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if 2 <= total_years <= 12:
        wt_res = {"valid": True, "dose": f"5 mg/kg/day = {5*weight:.2f} mg/day (แบ่งให้ทุก 6-8 ชม.)", "max": "-"}
    else:
        wt_res["msg"] = "เกณฑ์คำนวณตามน้ำหนักใช้เฉพาะอายุ 2-12 ปี"
    render_dual_results(age_res, wt_res)

elif selected_drug == "Hydroxyzine":
    age_res = {"valid": True, "dose": "12.5 mg/dose ทุก 6-8 ชม." if total_years < 6 else "12.5 - 25 mg/dose ทุก 6-8 ชม."}
    if weight <= 40:
        wt_res = {"valid": True, "dose": f"2 mg/kg/day = {2*weight:.2f} mg/day (แบ่งให้ทุก 6-8 ชม.)", "max": "50 mg/day"}
    else:
        wt_res = {"valid": True, "dose": "25 - 50 mg/dose วันละ 1-2 ครั้ง", "max": "100 mg/day"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Cetirizine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months <= 11:
        age_res = {"valid": True, "dose": "2.5 mg วันละ 1 ครั้ง", "max": "-"}
    elif 12 <= total_months <= 23:
        age_res = {"valid": True, "dose": "2.5 mg วันละ 1-2 ครั้ง", "max": "5 mg/day"}
    elif 2 <= total_years <= 5:
        age_res = {"valid": True, "dose": "2.5 mg วันละ 1-2 ครั้ง หรือ 5 mg วันละ 1 ครั้ง", "max": "5 mg/day"}
    elif 6 <= total_years <= 12:
        age_res = {"valid": True, "dose": "5 - 10 mg วันละ 1 ครั้ง", "max": "10 mg/day"}
    else:
        age_res = {"valid": True, "dose": "10 mg วันละ 1 ครั้ง", "max": "40 mg/day"}
        
    wt_res = {"valid": True, "dose": f"0.25 mg/kg/day = {0.25*weight:.2f} mg/day (วันละ 1-2 ครั้ง)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Levocetirizine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months and total_years <= 5:
        age_res = {"valid": True, "dose": "1.25 mg วันละ 1 ครั้ง", "max": "1.25 mg/day"}
    elif 6 <= total_years <= 11:
        age_res = {"valid": True, "dose": "2.5 mg วันละ 1 ครั้ง", "max": "2.5 mg/day"}
    else:
        age_res = {"valid": True, "dose": "2.5 - 5 mg วันละ 1 ครั้ง", "max": "20 mg/day"}
        
    wt_res = {"valid": True, "dose": f"0.125 mg/kg/day = {0.125*weight:.2f} mg/day (วันละ 1 ครั้ง)", "max": "5 mg/day"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Loratadine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        res = {"valid": True, "dose": "5 mg วันละ 1 ครั้ง", "max": "10 mg/day"}
    else:
        res = {"valid": True, "dose": "5 mg/dose วันละ 2 ครั้ง หรือ 10 mg วันละ 1 ครั้ง", "max": "10 mg/day"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Desloratadine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months <= 11:
        res = {"valid": True, "dose": "1 mg วันละ 1 ครั้ง", "max": "-"}
    elif 12 <= total_months and total_years <= 5:
        res = {"valid": True, "dose": "1.25 mg วันละ 1 ครั้ง", "max": "-"}
    elif 6 <= total_years <= 11:
        res = {"valid": True, "dose": "2.5 mg วันละ 1 ครั้ง", "max": "-"}
    else:
        res = {"valid": True, "dose": "5 mg วันละ 1 ครั้ง", "max": "20 mg/day"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Fexofenadine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months and total_years <= 2:
        d = "15 mg/dose วันละ 2 ครั้ง" if weight < 10.5 else "30 mg/dose วันละ 2 ครั้ง"
        res = {"valid": True, "dose": d, "max": "-"}
    elif 2 < total_years <= 11:
        res = {"valid": True, "dose": "30 mg/dose วันละ 2 ครั้ง", "max": "60 mg/day"}
    else:
        res = {"valid": True, "dose": "60 mg/dose วันละ 2 ครั้ง หรือ 180 mg วันละ 1 ครั้ง", "max": "720 mg/day"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Ketotifen":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 ปีขึ้นไป"
    else:
        d_val = 0.25 * weight
        res = {"valid": True, "dose": f"0.25 mg/kg/dose = {d_val:.2f} mg/dose วันละ 2 ครั้ง", "max": "1 mg/dose"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Montelukast":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months and total_years <= 5:
        res = {"valid": True, "dose": "4 mg วันละ 1 ครั้ง", "max": "4 mg/day"}
    elif 6 <= total_years <= 14:
        res = {"valid": True, "dose": "5 mg วันละ 1 ครั้ง", "max": "5 mg/day"}
    else:
        res = {"valid": True, "dose": "10 mg วันละ 1 ครั้ง", "max": "10 mg/day"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Phenylephrine HCl":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 4:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 4 ปีขึ้นไป"
    elif 4 <= total_years <= 5:
        res = {"valid": True, "dose": "2.5 mg/dose ทุก 4 ชม.", "max": "15 mg/day"}
    elif 6 <= total_years <= 11:
        res = {"valid": True, "dose": "5 mg/dose ทุก 4 ชม.", "max": "30 mg/day"}
    else:
        res = {"valid": True, "dose": "10 mg/dose ทุก 4 ชม.", "max": "60 mg/day"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Pseudoephedrine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        res = {"valid": True, "dose": f"15 mg/dose ทุก 4-6 ชม. หรือ 1 mg/kg/dose = {1*weight:.2f} mg/dose ทุก 4-6 ชม.", "max": "60 mg/day"}
    elif 6 <= total_years <= 12:
        res = {"valid": True, "dose": "30 mg/dose ทุก 4-6 ชม.", "max": "120 mg/day"}
    else:
        res = {"valid": True, "dose": "60 mg/dose ทุก 4-6 ชม. (หรือ SR tab: 120 mg วันละ 1-2 ครั้ง / 240 mg วันละ 1 ครั้ง)", "max": "240 mg/day"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Glyceryl-guaiacolate (Guaifenesin)":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        age_res = {"valid": True, "dose": "50 - 100 mg ทุก 4 ชม.", "max": "6 doses/day"}
    elif 6 <= total_years <= 11:
        age_res = {"valid": True, "dose": "100 - 200 mg ทุก 4 ชม.", "max": "6 doses/day"}
    else:
        age_res = {"valid": True, "dose": "200 - 400 mg ทุก 4 ชม.", "max": "6 doses/day"}
        
    wt_res = {"valid": True, "dose": f"12 mg/kg/day = {12*weight:.2f} mg/day (แบ่งให้วันละ 3-4 ครั้ง)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Acetylcysteine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 6:
        age_res = {"valid": True, "dose": "50 - 100 mg วันละ 2-4 ครั้ง", "max": "-"}
    else:
        age_res = {"valid": True, "dose": "100 - 200 mg วันละ 3 ครั้ง หรือ 600 mg วันละ 1 ครั้ง", "max": "600 mg/day"}
        
    wt_res = {"valid": True, "dose": f"20 - 30 mg/kg/day = {20*weight:.2f} - {30*weight:.2f} mg/day (แบ่งให้วันละ 2-3 ครั้ง)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Ambroxol":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        age_res = {"valid": True, "dose": "7.5 - 15 mg/dose วันละ 3 ครั้ง", "max": "-"}
    elif 6 <= total_years <= 12:
        age_res = {"valid": True, "dose": "15 - 30 mg/dose วันละ 2-3 ครั้ง", "max": "-"}
    else:
        age_res = {"valid": True, "dose": "60 - 120 mg/day แบ่งวันละ 2-3 ครั้ง", "max": "-"}
        
    wt_res = {"valid": True, "dose": f"1.2 - 1.6 mg/kg/day = {1.2*weight:.2f} - {1.6*weight:.2f} mg/day (แบ่งให้วันละ 2-3 ครั้ง)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Carbocysteine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        age_res = {"valid": True, "dose": "200 - 500 mg/day แบ่งวันละ 2-3 ครั้ง", "max": "-"}
    elif 6 <= total_years <= 11:
        age_res = {"valid": True, "dose": "300 - 750 mg/day แบ่งวันละ 3 ครั้ง", "max": "-"}
    elif 12 <= total_years < 15:
        age_res = {"valid": True, "dose": "300 mg - 2.25 g/day แบ่งวันละ 3 ครั้ง", "max": "2.25 g/day"}
    else:
        age_res = {"valid": True, "dose": "750 mg - 2.25 g/day แบ่งวันละ 3 ครั้ง", "max": "2.25 g/day"}
        
    wt_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years >= 2:
        wt_res = {"valid": True, "dose": f"15 - 20 mg/kg/day = {15*weight:.2f} - {20*weight:.2f} mg/day (แบ่งให้วันละ 3-4 ครั้ง)", "max": "-"}
    else:
        wt_res["msg"] = "คำนวณตามน้ำหนักใช้ในเด็กอายุ > 2 ปี"
    render_dual_results(age_res, wt_res)

elif selected_drug == "Bromhexine":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        age_res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        age_res = {"valid": True, "dose": "2 mg/dose วันละ 3 ครั้ง หรือ 4 mg/dose วันละ 2 ครั้ง", "max": "8 mg/day"}
    elif 6 <= total_years <= 11:
        age_res = {"valid": True, "dose": "4 - 8 mg/dose วันละ 3 ครั้ง", "max": "24 mg/day"}
    else:
        age_res = {"valid": True, "dose": "8 - 16 mg/dose วันละ 3 ครั้ง", "max": "48 mg/day"}
        
    wt_res = {"valid": True, "dose": f"0.6 - 0.8 mg/kg/day = {0.6*weight:.2f} - {0.8*weight:.2f} mg/day (แบ่งให้วันละ 3-4 ครั้ง)", "max": "-"}
    render_dual_results(age_res, wt_res)

elif selected_drug == "Dextromethorphan":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 4:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 4 ปีขึ้นไป"
    elif 4 <= total_years <= 5:
        res = {"valid": True, "dose": "2.5 - 7.5 mg ทุก 4-8 ชม.", "max": "30 mg/day"}
    elif 6 <= total_years <= 11:
        res = {"valid": True, "dose": "5 - 10 mg ทุก 4 ชม.", "max": "60 mg/day"}
    else:
        res = {"valid": True, "dose": "20 mg ทุก 4 ชม.", "max": "120 mg/day"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Salbutamol":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 6:
        d1, d2 = 0.1 * weight, 0.2 * weight
        res = {"valid": True, "dose": f"0.1 - 0.2 mg/kg/dose = {d1:.2f} - {d2:.2f} mg/dose วันละ 3 ครั้ง", "max": "12 mg/day"}
    elif 7 <= total_years <= 14:
        res = {"valid": True, "dose": "2 mg/dose วันละ 3-4 ครั้ง", "max": "24 mg/day"}
    else:
        res = {"valid": True, "dose": "2 - 4 mg/dose วันละ 3-4 ครั้ง", "max": "32 mg/day"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Terbutaline sulfate":
    res = {"valid": True, "dose": "", "max": ""}
    if total_years < 12:
        d_val = 0.05 * weight
        res = {"valid": True, "dose": f"0.05 mg/kg/dose = {d_val:.2f} mg/dose วันละ 3 ครั้ง", "max": "5 mg/day"}
    elif 12 <= total_years <= 14:
        res = {"valid": True, "dose": "2.5 mg/dose วันละ 3 ครั้ง", "max": "7.5 mg/day"}
    else:
        res = {"valid": True, "dose": "5 mg/dose วันละ 3-4 ครั้ง", "max": "15 mg/day"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Procaterol (Meptin syrup 5 mcg/ml)":
    age_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 1:
        age_res = {"valid": True, "dose": "10 - 15 mcg/dose วันละ 2 ครั้ง", "max": "30 mcg/day"}
    elif 1 <= total_years <= 2:
        age_res = {"valid": True, "dose": "15 - 20 mcg/dose วันละ 2 ครั้ง", "max": "40 mcg/day"}
    elif 3 <= total_years <= 5:
        age_res = {"valid": True, "dose": "20 - 25 mcg/dose วันละ 2 ครั้ง", "max": "50 mcg/day"}
    else:
        age_res = {"valid": True, "dose": "25 mcg/dose วันละ 1-2 ครั้ง", "max": "50 mcg/day"}
        
    wt_res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 6:
        d_val = 1.25 * weight
        wt_res = {"valid": True, "dose": f"1.25 mcg/kg/dose = {d_val:.2f} mcg/dose ทุก 12 ชม.", "max": "-"}
    else:
        wt_res["msg"] = "คำนวณตามน้ำหนักใช้ในเด็กอายุ < 6 ปี"
    render_dual_results(age_res, wt_res)

elif selected_drug == "Dimenhydrinate":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    elif 2 <= total_years <= 5:
        res = {"valid": True, "dose": "15 - 25 mg ทุก 6-8 ชม.", "max": "75 mg/day"}
    elif 6 <= total_years <= 11:
        res = {"valid": True, "dose": "25 - 50 mg ทุก 6-8 ชม.", "max": "150 mg/day"}
    else:
        res["msg"] = "โปรดใช้อัตราขนาดยาของผู้ใหญ่"
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Domperidone":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if weight < 35:
        d1 = 0.75 * weight
        d2_min, d2_max = 0.2 * weight, 0.4 * weight
        res = {"valid": True, "dose": f"• 0.75 mg/kg/day = {d1:.2f} mg/day (แบ่งวันละ 3 ครั้ง ก่อนอาหาร)\n• หรือ 0.2 - 0.4 mg/kg/dose = {d2_min:.2f} - {d2_max:.2f} mg/dose ทุก 6-8 ชม. ก่อนอาหาร", "max": "30 mg/day"}
    else:
        res["msg"] = "น้ำหนักตัว >= 35 kg โปรดใช้เกณฑ์ขนาดยาผู้ใหญ่"
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Dicyclomine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months and total_years < 2:
        res = {"valid": True, "dose": "5 - 10 mg วันละ 3-4 ครั้ง ก่อนอาหาร", "max": "-"}
    else:
        res = {"valid": True, "dose": "10 mg วันละ 3-4 ครั้ง", "max": "-"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Hyoscine":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    elif 6 <= total_months and total_years < 1:
        res = {"valid": True, "dose": "5 mg/dose วันละ 3-4 ครั้ง", "max": "-"}
    elif 1 <= total_years <= 6:
        res = {"valid": True, "dose": "5 - 10 mg วันละ 3-4 ครั้ง", "max": "-"}
    else:
        res["msg"] = "โปรดใช้อัตราขนาดยาของผู้ใหญ่"
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Simethicone":
    res = {"valid": True, "dose": "", "max": "500 mg/day"}
    if total_years < 2:
        res["dose"] = "20 mg/dose วันละ 3-4 ครั้ง"
    elif 2 <= total_years <= 12:
        res["dose"] = "40 mg/dose วันละ 3-4 ครั้ง"
    else:
        res["dose"] = "40 - 125 mg วันละ 3-4 ครั้ง (เกณฑ์ผู้ใหญ่)"
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Al(OH)3 + Mg(OH)2 (Alum milk)":
    res = {"valid": True, "dose": "", "max": "-"}
    if total_months <= 1:
        res["dose"] = f"1 ml/kg/dose = {1*weight:.2f} ml/dose"
    elif 1 < total_months <= 12:
        res["dose"] = "2 - 5 ml/dose"
    elif 1 < total_years <= 5:
        res["dose"] = "5 - 15 ml/dose"
    elif 6 <= total_years <= 12:
        res["dose"] = "15 - 45 ml/dose"
    else:
        res["dose"] = "15 - 45 ml/dose"
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Lactulose (Laevolac)":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 1:
        res["msg"] = "รองรับในทารกอายุตั้งแต่ 1 เดือนขึ้นไป"
    elif 1 <= total_months and total_years <= 6:
        d_wt = 1 * weight
        d_wt2 = 2 * weight
        res = {"valid": True, "dose": f"• 5 - 10 ml/day วันละ 1 ครั้ง\n• หรือ 1 - 2 g/kg/day = {d_wt:.2f} - {d_wt2:.2f} g/day", "max": "-"}
    elif 6 < total_years <= 14:
        d_wt = 1.5 * weight
        d_wt2 = 3 * weight
        res = {"valid": True, "dose": f"• 15 ml/day วันละ 1 ครั้ง\n• หรือ 1.5 - 3 ml/kg/day = {d_wt:.2f} - {d_wt2:.2f} ml/day (แบ่งวันละ 1-2 ครั้ง)", "max": "-"}
    else:
        res = {"valid": True, "dose": "15 - 30 ml/day", "max": "-"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Metronidazole":
    d1_min, d1_max = 35 * weight, 50 * weight
    d2_min, d2_max = 15 * weight, 50 * weight
    res = {"valid": True, "dose": f"• Amebiasis: 35 - 50 mg/kg/day = {d1_min:.2f} - {d1_max:.2f} mg/day (แบ่งวันละ 3 ครั้ง, สูงสุด 2.25 g/day)\n• Anaerobic infection / Trichomoniasis: 15 - 50 mg/kg/day = {d2_min:.2f} - {d2_max:.2f} mg/day (แบ่งวันละ 3 ครั้ง, สูงสุด 750 mg/dose)", "max": "ตามที่ระบุ"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Albendazole":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 1:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 1 ปีขึ้นไป"
    else:
        txt = ""
        if 1 <= total_years < 2:
            txt += "• Intestinal roundworm, Pinworm, Hookworm: 200 mg กินครั้งเดียว (Single Dose)\n"
        else:
            txt += "• Intestinal roundworm, Pinworm, Hookworm: 400 mg กินครั้งเดียว (Single Dose)\n"
            txt += "• Whipworm: 400 mg วันละ 1 ครั้ง นาน 3 วัน\n"
            txt += "• Strongyloidiasis: 400 mg วันละ 2 ครั้ง นาน 7 วัน\n"
            txt += "• Capillariasis: 400 mg วันละ 1 ครั้ง นาน 10 วัน\n"
            txt += f"• Tapeworm: 7.5 mg/kg/dose = {7.5*weight:.2f} mg/dose วันละ 2 ครั้ง (สูงสุด 800 mg/day)\n"
            txt += f"• Liver flukes: 10 mg/kg/dose = {10*weight:.2f} mg/dose วันละ 1 ครั้ง นาน 7 วัน"
        res = {"valid": True, "dose": txt, "max": "800 mg/day"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Mebendazole":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 ปีขึ้นไป"
    else:
        txt = "• Intestinal roundworm, Whipworm, Hookworm: 100 mg วันละ 2 ครั้ง นาน 3 วัน (หรือ 500 mg ครั้งเดียว)\n"
        txt += "• Pinworm: 100 mg กินครั้งเดียว (Single Dose)\n"
        txt += "• Capillariasis: 200 mg วันละ 1 ครั้ง นาน 20 วัน"
        res = {"valid": True, "dose": txt, "max": "-"}
    render_single_result(res, "ตามอายุ")

elif selected_drug == "Acetaminophen":
    d_min, d_max = 10 * weight, 15 * weight
    max_d = 75 * weight
    res = {"valid": True, "dose": f"10 - 15 mg/kg/dose = {d_min:.2f} - {d_max:.2f} mg/dose ทุก 4-6 ชม. หลังอาหาร", "max": f"75 mg/kg/day ({max_d:.2f} mg/day)"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Diclofenac":
    d_min, d_max = 2 * weight, 3 * weight
    res = {"valid": True, "dose": f"2 - 3 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-4 ครั้ง หลังอาหาร)", "max": "200 mg/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Ibuprofen":
    d_min, d_max = 5 * weight, 10 * weight
    max_d = 40 * weight
    res = {"valid": True, "dose": f"5 - 10 mg/kg/dose = {d_min:.2f} - {d_max:.2f} mg/dose ทุก 6-8 ชม. หลังอาหาร", "max": f"40 mg/kg/day ({max_d:.2f} mg/day)"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Penicillin V":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 12:
        d_min, d_max = 25 * weight, 50 * weight
        res = {"valid": True, "dose": f"25 - 50 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง ก่อนอาหาร)", "max": "3 g/day"}
    else:
        res["msg"] = "อายุ >= 12 ปี โปรดใช้อัตราขนาดยาของผู้ใหญ่"
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Amoxicillin / Amoxicillin + Clavulanic acid":
    res = {"valid": True, "dose": "", "max": "500 mg/dose"}
    if total_months < 3:
        d_min, d_max = 20 * weight, 30 * weight
        res["dose"] = f"• Normal Dose: 20 - 30 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2 ครั้ง หลังอาหาร)"
    else:
        d_min, d_max = 20 * weight, 50 * weight
        d_hi = 80 * weight
        d_hi2 = 90 * weight
        res["dose"] = f"• Normal Dose: 20 - 50 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-3 ครั้ง หลังอาหาร)\n• High Dose (Acute otitis media/Severe infection): 80 - 90 mg/kg/day = {d_hi:.2f} - {d_hi2:.2f} mg/day (แบ่งวันละ 2 ครั้ง หลังอาหาร)"
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cloxacillin":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months <= 1:
        res["msg"] = "รองรับในทารกอายุตั้งแต่ 1 เดือนขึ้นไป"
    else:
        d_min, d_max = 50 * weight, 100 * weight
        res = {"valid": True, "dose": f"50 - 100 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง ก่อนอาหาร)", "max": "4 g/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Dicloxacillin":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if weight < 40:
        d_min, d_max = 25 * weight, 50 * weight
        d_hi1, d_hi2 = 50 * weight, 100 * weight
        txt = f"• Normal Dose: 25 - 50 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง ก่อนอาหาร)\n"
        txt += f"• High Dose (Osteomyelitis): 50 - 100 mg/kg/day = {d_hi1:.2f} - {d_hi2:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง ก่อนอาหาร)"
        res = {"valid": True, "dose": txt, "max": "500 mg/dose"}
    else:
        res["msg"] = "น้ำหนัก >= 40 kg โปรดใช้เกณฑ์ขนาดยาผู้ใหญ่"
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cephalexin":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 1:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 1 ปีขึ้นไป"
    else:
        d_min, d_max = 25 * weight, 50 * weight
        d_hi1, d_hi2 = 75 * weight, 100 * weight
        txt = f"• Normal Dose: 25 - 50 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-4 ครั้ง หลังอาหาร, Max 2 g/day)\n"
        txt += f"• High Dose (Severe infection): 75 - 100 mg/kg/day = {d_hi1:.2f} - {d_hi2:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง หลังอาหาร, Max 4 g/day)"
        res = {"valid": True, "dose": txt, "max": "ตามที่ระบุ"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cefuroxime":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 3 or total_years > 12:
        res["msg"] = "รองรับในเด็กช่วงอายุ 3 เดือน ถึง 12 ปี"
    else:
        d_min, d_max = 20 * weight, 30 * weight
        res = {"valid": True, "dose": f"20 - 30 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2 ครั้ง หลังอาหาร)", "max": "500 mg/dose"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cefaclor":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months <= 1:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 1 เดือนขึ้นไป"
    else:
        d_min, d_max = 20 * weight, 40 * weight
        res = {"valid": True, "dose": f"20 - 40 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-3 ครั้ง หลังอาหาร)", "max": "1.5 g/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cefdinir":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6 or total_years > 12:
        res["msg"] = "รองรับในเด็กช่วงอายุ 6 เดือน ถึง 12 ปี"
    else:
        d_val = 14 * weight
        res = {"valid": True, "dose": f"14 mg/kg/day = {d_val:.2f} mg/day (แบ่งวันละ 1-2 ครั้ง หลังอาหาร)", "max": "600 mg/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cefixime":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    else:
        d_min, d_max = 8 * weight, 20 * weight
        res = {"valid": True, "dose": f"8 - 20 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 1-2 ครั้ง หลังอาหาร)", "max": "400 mg/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Cefditoren pivoxil":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_years < 12:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 12 ปีขึ้นไป"
    else:
        d_min, d_max = 10 * weight, 20 * weight
        res = {"valid": True, "dose": f"• 10 - 20 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-3 ครั้ง หลังอาหาร)\n• หรือ 200 - 400 mg วันละ 2 ครั้ง หลังอาหาร", "max": "-"}
    render_single_result(res, "ตามอายุ/น้ำหนัก")

elif selected_drug == "Erythromycin":
    d_min, d_max = 30 * weight, 50 * weight
    txt = f"• Base, Estolate, Stearate: {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-4 ครั้ง ก่อนอาหาร, Max 2 g/day)\n"
    txt += f"• Ethylsuccinate: {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2-4 ครั้ง หลังอาหาร, Max 3.2 g/day)\n"
    txt += f"• High dose (Chlamydial conjunctivitis/Pneumonia): {d_min*2:.2f} - {d_max*2:.2f} mg/day (แบ่งวันละ 2-4 ครั้ง, Max 4 g/day)"
    res = {"valid": True, "dose": txt, "max": "ตามชนิดยา"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Azithromycin":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    else:
        d1_min, d1_max = 5 * weight, 12 * weight
        d2_d1 = 10 * weight
        d2_d2 = 5 * weight
        d3 = 30 * weight
        txt = f"• Regimen 1: 5 - 12 mg/kg/day = {d1_min:.2f} - {d1_max:.2f} mg/day วันละ 1 ครั้ง ก่อนอาหาร นาน 3 วัน (Max 500 mg/dose)\n"
        txt += f"• Regimen 2: วันที่ 1 ให้ {d2_d1:.2f} mg (10-12 mg/kg), วันที่ 2-5 ให้ {d2_d2:.2f} mg/day (5-6 mg/kg)\n"
        txt += f"• Regimen 3 (Single Dose): {d3:.2f} mg (30 mg/kg) ก่อนอาหาร ครั้งเดียว (Max 1500 mg/dose)"
        res = {"valid": True, "dose": txt, "max": "ตาม Regimen"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Roxithromycin":
    d_min, d_max = 5 * weight, 8 * weight
    res = {"valid": True, "dose": f"5 - 8 mg/kg/day = {d_min:.2f} - {d_max:.2f} mg/day (แบ่งวันละ 2 ครั้ง ก่อนอาหาร)", "max": "300 mg/day"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Clarithromycin":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 6:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 6 เดือนขึ้นไป"
    else:
        d_val = 15 * weight
        res = {"valid": True, "dose": f"15 mg/kg/day = {d_val:.2f} mg/day (แบ่งวันละ 2 ครั้ง หลังอาหาร)", "max": "500 mg/dose"}
    render_single_result(res, "ตามน้ำหนัก")

elif selected_drug == "Co-trimoxazole (TMP + SMX)":
    res = {"valid": False, "dose": "", "max": "", "msg": ""}
    if total_months < 2:
        res["msg"] = "รองรับในเด็กอายุตั้งแต่ 2 เดือนขึ้นไป"
    else:
        tmp_norm, smx_norm = 8 * weight, 40 * weight
        tmp_hi1, tmp_hi2 = 15 * weight, 20 * weight
        smx_hi1, smx_hi2 = 75 * weight, 100 * weight
        txt = f"• Normal Dose: TMP {tmp_norm:.2f} mg/day + SMX {smx_norm:.2f} mg/day (แบ่งวันละ 2 ครั้ง หลังอาหาร) [Max TMP 320 mg/day, SMX 1600 mg/day]\n"
        txt += f"• High Dose (PCP/Meningitis): TMP {tmp_hi1:.2f}-{tmp_hi2:.2f} mg/day + SMX {smx_hi1:.2f}-{smx_hi2:.2f} mg/day (แบ่งวันละ 3-4 ครั้ง หลังอาหาร)"
        res = {"valid": True, "dose": txt, "max": "ตามที่ระบุ"}
    render_single_result(res, "ตามน้ำหนัก")
