import pandas as pd
import numpy as np
from faker import Faker
import random

# 1. 加载真实光纤覆盖率数据
def load_coverage_data():
    # 读取Excel文件，跳过前两行（标题和单位行）
    df_coverage = pd.read_excel('Glasfaser.xlsx', sheet_name='Sheet1', skiprows=2)
    
    # 清理列名（去除空格和特殊字符）
    df_coverage.columns = [
        'ags', 'region', 'admin_level', 
        'fttb_h_1000', 'fttc_16', 'fttc_30', 'fttc_50', 'fttc_100', 'fttc_200',
        'hfc_16', 'hfc_30', 'hfc_50', 'hfc_100', 'hfc_200', 'hfc_400', 'hfc_1000'
    ]
    
    # 提取关键指标：FTTH覆盖率（≥1000Mbit/s）
    df_coverage['ftth_coverage'] = df_coverage['fttb_h_1000']
    return df_coverage[['ags', 'region', 'ftth_coverage']]

# 2. 生成模拟客户数据（与真实覆盖率关联）
def generate_customer_data(num_customers=1000):
    fake = Faker('de_DE')
    np.random.seed(42)
    
    # 加载真实覆盖率数据
    df_coverage = load_coverage_data()
    regions = df_coverage['region'].tolist()
    coverage_rates = df_coverage['ftth_coverage'].tolist()
    
    # 生成模拟数据
    data = []
    for _ in range(num_customers):
        # 随机选择一个地区（根据覆盖率加权）
        region_idx = random.choices(
            range(len(regions)), 
            weights=coverage_rates,  # 覆盖率高的地区生成更多客户
            k=1
        )[0]
        region = regions[region_idx]
        region_coverage = coverage_rates[region_idx]
        
        # 生成客户特征
        age = np.random.randint(18, 70)
        occupation = np.random.choice(
            ['Freelancer', 'KMU Owner', 'Corporate Employee', 'Retired'], 
            p=[0.3, 0.2, 0.4, 0.1]  # 假设企业员工占比更高
        )
        is_remote_worker = 1 if occupation in ['Freelancer', 'KMU Owner'] else 0
        
        # 根据地区和职业生成互联网使用量
        if 'Urban' in region:
            usage_gb = np.random.lognormal(mean=3.5, sigma=0.4)
        else:
            usage_gb = np.random.lognormal(mean=2.8, sigma=0.6)
        
        # 根据覆盖率生成是否使用光纤
        has_fiber = np.random.choice(
            [True, False], 
            p=[region_coverage/100, 1-region_coverage/100]  # 转换为概率
        )
        
        data.append({
            'customer_id': fake.unique.random_number(5),
            'postal_code': fake.postcode(),
            'region': region,
            'age': age,
            'occupation': occupation,
            'is_remote_worker': is_remote_worker,
            'internet_usage_gb': np.round(usage_gb, 1),
            'current_provider': np.random.choice(
                ['Telekom', 'Vodafone', 'O2', 'Deutsche Glasfaser', 'Other'],
                p=[0.4, 0.3, 0.2, 0.05, 0.05]  # 模拟当前市场份额
            ),
            'monthly_spend_eur': np.round(np.random.uniform(20, 80), 2),
            'has_fiber': has_fiber,
            'coverage_rate': region_coverage
        })
    
    return pd.DataFrame(data)

# 3. 保存模拟数据
df_customers = generate_customer_data()
df_customers.to_csv('simulated_customers_with_coverage.csv', index=False)

# 4. 分析示例：按地区统计光纤使用情况
def analyze_coverage(df):
    # 按地区分组统计
    df_region = df.groupby('region').agg({
        'customer_id': 'count',
        'has_fiber': 'mean',
        'coverage_rate': 'first',
        'monthly_spend_eur': 'mean'
    }).rename(columns={
        'customer_id': 'customer_count',
        'has_fiber': 'actual_fiber_adoption'
    })
    
    # 计算覆盖率与实际使用率的差距
    df_region['coverage_gap'] = df_region['coverage_rate']/100 - df_region['actual_fiber_adoption']
    
    # 按差距排序
    return df_region.sort_values('coverage_gap', ascending=False)

# 运行分析
analysis_result = analyze_coverage(df_customers)
print(analysis_result.head())

# 5. 可视化（需要matplotlib或plotly）
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
analysis_result['coverage_gap'].plot(kind='barh')
plt.title('Fiber Coverage Gap by Region (Coverage Rate - Actual Adoption)')
plt.xlabel('Gap Percentage')
plt.ylabel('Region')
plt.tight_layout()
plt.savefig('coverage_gap_analysis.png')
plt.show()