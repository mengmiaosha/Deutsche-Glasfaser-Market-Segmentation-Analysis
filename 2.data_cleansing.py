import pandas as pd
import numpy as np

# 加载模拟数据
df = pd.read_csv('simulated_customers_with_coverage.csv')

# 处理缺失值（如有）
df.dropna(subset=['monthly_spend_eur', 'internet_usage_gb'], inplace=True)

# 添加衍生特征
df['potential_upsell'] = np.where(
    (df['internet_usage_gb'] > 50) & (df['monthly_spend_eur'] < 50),
    1, 0  # 标记高使用量低消费客户
)

# 保存清洗后数据
df.to_csv('cleaned_customer_data.csv', index=False)
