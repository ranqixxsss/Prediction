import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 或者 'Microsoft YaHei'
matplotlib.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 读取数据
df = pd.read_csv('C:/Python/py_Code/Prediction/csv_cleaned_output/diabetes_with_CHD_cleaned.csv')

# 1. 缺失值可视化
plt.figure(figsize=(10, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title("缺失值热力图")
plt.tight_layout()
plt.show()

# 2. 数值型变量分布可视化 - 直方图
plt.figure(figsize=(10, 6))
sns.histplot(df['C-反应蛋白（CRP）'], kde=True)
plt.title("C-反应蛋白（CRP）分布")
plt.tight_layout()
plt.show()

# 3. 数值型变量分布可视化 - 箱型图
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['C-反应蛋白（CRP）'])
plt.title("C-反应蛋白（CRP）箱型图")
plt.tight_layout()
plt.show()

# 4. 相关性热力图
# 只选择数值型列进行相关性分析
numeric_df = df.select_dtypes(include=['number'])

# 计算相关性矩阵
correlation_matrix = numeric_df.corr()

# 绘制相关性热力图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("特征相关性热力图")
plt.tight_layout()
plt.show()

# 5. 目标变量与特征的关系 - 散点图
plt.figure(figsize=(10, 6))
sns.scatterplot(x=df['BMI（公式：体重/身高/身高）'], y=df['C-反应蛋白（CRP）'])
plt.title("BMI与C-反应蛋白（CRP）关系散点图")
plt.tight_layout()
plt.show()

# 6. 目标变量与特征的关系 - Pairplot (多个变量)
sns.pairplot(df[['C-反应蛋白（CRP）', '白介素-6（IL-6）', '肿瘤坏死因子（TNF）']])
plt.title("C-反应蛋白（CRP）、白介素-6（IL-6）与肿瘤坏死因子（TNF）关系的Pairplot")
plt.tight_layout()
plt.show()

# 7. 分类变量与目标变量的关系 - 性别与CRP的关系
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['性别'], y=df['C-反应蛋白（CRP）'])
plt.title("性别与C-反应蛋白（CRP）关系箱型图")
plt.tight_layout()
plt.show()

# 8. 分类变量与目标变量的关系 - 吸烟史与CRP的关系
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['吸烟史（0：无；1：有)'], y=df['C-反应蛋白（CRP）'])
plt.title("吸烟史与C-反应蛋白（CRP）关系箱型图")
plt.tight_layout()
plt.show()

# 9. 时间序列分析 - 假设数据中有病程与炎性指标（例如 CRP）
plt.figure(figsize=(10, 6))
sns.lineplot(x=df['病程（天）'], y=df['C-反应蛋白（CRP）'])
plt.title("病程与C-反应蛋白（CRP）的时间序列分析")
plt.tight_layout()
plt.show()

# 10. 多变量可视化 - 使用FacetGrid来查看不同变量的关系
g = sns.FacetGrid(df, col="性别", height=5)
g.map(sns.scatterplot, "BMI（公式：体重/身高/身高）", "C-反应蛋白（CRP）")
plt.title("性别与BMI、C-反应蛋白（CRP）关系的多变量可视化")
plt.tight_layout()
plt.show()
