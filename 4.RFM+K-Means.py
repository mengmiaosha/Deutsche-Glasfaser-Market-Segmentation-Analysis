import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 加载数据
try:
    df = pd.read_csv('cleaned_customer_data.csv')
except FileNotFoundError:
    df = pd.read_csv('simulated_customers_with_coverage.csv')

# RFM 计算
df_rfm = df.groupby('customer_id').agg({
    'monthly_spend_eur': 'mean',
    'internet_usage_gb': 'sum',
    'age': 'last'
}).rename(columns={
    'monthly_spend_eur': 'monetary',
    'internet_usage_gb': 'frequency',
    'age': 'recency'
})

# 标准化数据
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_rfm)

# K-Means聚类
kmeans = KMeans(n_clusters=4, random_state=42)
df_rfm['cluster'] = kmeans.fit_predict(X_scaled)

# 合并回原始数据
df = pd.merge(df, df_rfm[['cluster']], left_on='customer_id', right_index=True)

# 可视化聚类结果
import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.scatter(df_rfm['frequency'], df_rfm['monetary'], c=df_rfm['cluster'], cmap='viridis')
plt.xlabel('Frequency')
plt.ylabel('Monetary')
plt.title('Customer Segments by RFM')
plt.colorbar(label='Cluster')
plt.show()

# 分析聚类中心
cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
centers_df = pd.DataFrame(cluster_centers, columns=df_rfm.columns[:-1])
print("Cluster Centers:")
print(centers_df)

# 计算各州理论vs实际光纤使用差距
gap_analysis = df.groupby('region').agg({
    'coverage_rate': 'mean',
    'has_fiber': 'mean',
    'customer_id': 'count'
}).rename(columns={
    'customer_id': 'customer_count',
    'has_fiber': 'actual_adoption'
})

gap_analysis['gap'] = gap_analysis['coverage_rate']/100 - gap_analysis['actual_adoption']
gap_analysis.sort_values('gap', ascending=False, inplace=True)

# 可视化差距TOP5
plt.figure(figsize=(12,8))
gap_analysis.head(5).plot(kind='bar', y=['coverage_rate', 'actual_adoption'])
plt.title('Top 5 Regions with Fiber Coverage-Adoption Gap')
plt.ylabel('Percentage')
plt.tight_layout()
plt.savefig('top5_gap_regions.png', dpi=300)

# 示例：月度自动化报告生成
def generate_monthly_report():
    # 1. 更新数据
    new_data = pd.read_csv('new_customers.csv')
    
    # 2. 重新运行分析
    gap_analysis = calculate_coverage_gap(new_data)
    
    # 3. 生成PDF报告
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Monthly Fiber Adoption Report", ln=1)
    pdf.output("monthly_report.pdf")

# 设置定时任务（如cron job）
