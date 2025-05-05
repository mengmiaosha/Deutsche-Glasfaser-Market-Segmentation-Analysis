import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv('cleaned_customer_data.csv')

# 1. 光纤使用率分析
plt.figure(figsize=(10, 6))
fiber_adoption = df.groupby('region')['has_fiber'].mean().sort_values()
fiber_adoption.plot(kind='barh', title='Fiber Adoption Rate by Region')
plt.tight_layout()
plt.savefig('fiber_adoption_by_region.png')

# 2. 客户特征分布
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(df['age'], bins=20, ax=axes[0])
sns.boxplot(x='has_fiber', y='monthly_spend_eur', data=df, ax=axes[1])
plt.savefig('customer_distributions.png')

# 3. 相关性分析
corr_matrix = df[['age', 'monthly_spend_eur', 'internet_usage_gb', 'coverage_rate']].corr()
sns.heatmap(corr_matrix, annot=True)
plt.savefig('correlation_analysis.png')
