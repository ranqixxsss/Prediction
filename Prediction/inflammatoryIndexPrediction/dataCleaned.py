import pandas as pd
import os

# 映射中文列名到英文简写
columns_mapping = {
    '编号': 'ID', '姓名': 'Name', '性别': 'Gender', '年龄': 'Age', '具体诊断': 'Diagnosis',
    '病程（天）': 'Disease_Duration', '吸烟史（0：无；1：有)': 'Smoking_History', '每日吸烟支数': 'Smoking_Pack_Amount',
    '吸烟年数': 'Smoking_Years', '吸烟指数': 'Smoking_Index', '体重（Kg）': 'Weight', '身高（m）': 'Height',
    'BMI（公式：体重/身高/身高）': 'BMI', '腰围（cm）': 'Waist_Circumference', '收缩压（mmHg）': 'Systolic_BP',
    '舒张压（mmHg）': 'Diastolic_BP', '空腹血糖（mmol/L）': 'Fasting_Glucose', '餐后2h血糖（mmol/L）': 'Postmeal_2h_Glucose',
    '空腹C肽': 'Fasting_C_Peptide', '餐后2hC肽': 'Postmeal_2h_C_Peptide', '空腹胰岛素': 'Fasting_Insulin',
    '餐后2h胰岛素': 'Postmeal_2h_Insulin', '糖化血红蛋白(HbA1C)': 'HbA1C', '载脂蛋白-A1（APO-A1）': 'ApoA1',
    '载脂蛋白-B（APO-B）': 'ApoB', '颈动脉彩超（0=无斑块 1=有斑块）': 'Carotid_Artery', '淋巴细胞绝对值（LYMPH#）': 'Lymphocyte_Absolute',
    '单核细胞绝对值（MONO#）': 'Monocyte_Absolute', '中性分叶核粒细胞绝对值（NEUT#）': 'Neutrophil_Absolute',
    '血小板计数（PLT）': 'Platelet_Count', 'LMR(淋巴细胞绝对值/单核细胞绝对值)': 'LMR', 'NLR(中性分叶核粒细胞绝对值/淋巴细胞绝对值)': 'NLR',
    'PLR（血小板计数/淋巴细胞绝对值）': 'PLR', '全身免疫炎症指数': 'Immune_Inflammation_Index', '单核细胞计数 / 高密度脂蛋白胆固醇比值': 'MHR',
    '血清纤维蛋白原/白蛋白比值(FAR)': 'FAR', '血沉（ESR）': 'ESR', 'C-反应蛋白（CRP）': 'CRP', '降钙素原（PCT）': 'PCT',
    '白介素-6（IL-6）': 'IL6', '肿瘤坏死因子（TNF）': 'TNF', '同型半胱氨酸（Hcy）': 'Hcy', '24小时尿量（L/24h）': 'Urine_24h_Volume',
    '24h尿蛋白量（g/24h）': 'Urine_24h_Protein', '尿蛋白/尿肌酐（g/mmol Cr）': 'Urine_Protein_Creatinine', '红细胞计数（10`12/L）': 'RBC_Count',
    '血红蛋白（g/L）': 'Hemoglobin', '红细胞压积（L/L）': 'Hematocrit', '平均红细胞体积（fL）': 'MCV', '平均红细胞HGB含量（pg）': 'MCH',
    '平均红细胞HGB浓度（g/L）': 'MCHC', 'RBC分布宽度CV（%）': 'RDW_CV', 'RBC分布宽度SD（fL）': 'RDW_SD', '血小板计数（10`9/L）': 'Platelet_Count_10_9',
    '白细胞计数（10`9/L）': 'WBC_Count', '中性分叶核粒细胞百分率（%）': 'Neutrophil_Percentage', '淋巴细胞百分率（%）': 'Lymphocyte_Percentage',
    '单核细胞百分率（%）': 'Monocyte_Percentage', '嗜酸性粒细胞百分率（%）': 'Eosinophil_Percentage', '嗜碱性粒细胞百分率（%）': 'Basophil_Percentage',
    '原始细胞百分率（%）': 'Blast_Cell_Percentage', '中性分叶核粒细胞绝对值（10`9/L）': 'Neutrophil_Absolute_10_9', '淋巴细胞绝对值（10`9/L）': 'Lymphocyte_Absolute_10_9',
    '单核细胞绝对值（10`9/L）': 'Monocyte_Absolute_10_9', '嗜酸细胞绝对值（10`9/L）': 'Eosinophil_Absolute_10_9', '嗜碱细胞绝对值（10`9/L）': 'Basophil_Absolute_10_9',
    '晚幼红细胞（/100个细胞）': 'Reticulocyte_Late', '总胆红素（umol/L）': 'Total_Bilirubin', '直接胆红素（umol/L）': 'Direct_Bilirubin',
    '丙氨酸氨基转移酶（IU/L）': 'ALT', '间接胆红素（umol/L）': 'Indirect_Bilirubin', '总蛋白（g/L）': 'Total_Protein', '白蛋白（g/L）': 'Albumin',
    '球蛋白（g/L）': 'Globulin', '白球比例': 'Albumin_Globulin_Ratio', '肌酐（umol/L）': 'Creatinine', '尿酸（umol/L）': 'Uric_Acid', 'AST/ALT': 'AST_ALT_Ratio',
    '葡萄糖（mmol/L）': 'Glucose', '门冬氨酸氨基转移酶（IU/L）': 'AST', '碱性磷酸酶（IU/L）': 'ALP', '肌酸激酶（IU/L）': 'CK', '谷氨酰转肽酶（IU/L）': 'GGT',
    '乳酸脱氢酶（IU/L）': 'LDH', '羟丁酸脱氢酶（IU/L）': 'HBDH', '甘油三酯（mmol/L）': 'Triglycerides', '尿素（mmol/L）': 'Urea', '胆固醇（mmol/L）': 'Cholesterol',
    '钙（mmol/L）': 'Calcium', '镁（mmol/L）': 'Magnesium', '血清无机磷（mmol/L）': 'Inorganic_Phosphate', '高密度脂蛋白（mmol/L）': 'HDL', '低密度脂蛋白（mmol/L）': 'LDL',
    '总胆汁酸（umol/L）': 'Total_Bile_Acid', '钠（mmol/L）': 'Sodium', '钾（mmol/L）': 'Potassium', '氯（mmol/L）': 'Chloride', '二氧化碳结合力（mmol/L）': 'CO2_Binding',
    '阴离子间隙（mmol/L）': 'Anion_Gap', '血清胱抑素C测定（mg/L）': 'Cystatin_C', '血清β羟基丁酸测定（mmol/L）': 'Beta_Hydroxybutyrate', '估算肾小球滤过率（ml/min/1.73㎡）': 'eGFR',
    '颜色': 'Urine_Color', '浊度': 'Turbidity', '比重': 'Specific_Gravity', '酸碱度': 'pH', '隐血（Cell/μL）': 'Hemoglobin_Cells', '白细胞（Cell/μl）': 'WBC_Cells',
    '尿蛋白定性（g/L）': 'Urine_Protein_Qualitative', '尿葡萄糖（mmol/L）': 'Urine_Glucose'
}

def clean_data(file_path, output_dir):
    if not os.path.exists(file_path):
        print(f"⚠️ 文件未找到: {file_path}")
        return

    try:
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='gb18030')

        df.columns = df.columns.str.strip().str.replace("\n", "")
    except Exception as e:
        print(f"❌ 读取 CSV 失败: {e}")
        return

    print("🔍 现有列名：", df.columns.tolist())

    # 计算 NLR（中性分叶核粒细胞绝对值 / 淋巴细胞绝对值）
    if '中性分叶核粒细胞绝对值（10`9/L）' in df.columns and '淋巴细胞绝对值（10`9/L）' in df.columns:
        df['NLR'] = df['中性分叶核粒细胞绝对值（10`9/L）'] / df['淋巴细胞绝对值（10`9/L）']
        df['NLR'] = df['NLR'].replace([float('inf'), -float('inf')], None)  # 替换无穷大值
        df['NLR'] = df['NLR'].fillna(0)  # 处理 NaN 值
    else:
        print("⚠️ 关键列缺失，请检查列名！")
        return

    # 统一列名为英文（如果需要）
    #df = df.rename(columns=columns_mapping)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = os.path.join(output_dir, os.path.basename(file_path).replace(".csv", "_cleaned.csv"))
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"✅ 数据清洗完成，已保存至 {output_path}")

# 设置文件夹路径
#input_file = 'C:/Python/py_Code/Prediction/csv_output/diabetes_with_CHD.csv'
#output_directory = 'C:/Python/py_Code/Prediction/csv_cleaned_output'

# 运行数据清洗
clean_data('C:/Python/py_Code/Prediction/csv_output/diabetes_with_CHD.csv', 'C:/Python/py_Code/Prediction/csv_cleaned_output')
clean_data('C:/Python/py_Code/Prediction/csv_output/diabetes_no_CHD.csv', 'C:/Python/py_Code/Prediction/csv_cleaned_output')
clean_data('C:/Python/py_Code/Prediction/csv_output/hypertension_no_CHD.csv', 'C:/Python/py_Code/Prediction/csv_cleaned_output')
clean_data('C:/Python/py_Code/Prediction/csv_output/hypertension_with_CHD.csv', 'C:/Python/py_Code/Prediction/csv_cleaned_output')