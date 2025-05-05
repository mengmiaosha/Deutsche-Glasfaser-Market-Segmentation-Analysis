# Deutsche Glasfaser Market Segmentation Analysis  

<!-- 项目概述：用简短有力的语言说明核心目标 -->
*A data-driven approach to identify high-potential customer segments for fiber optic expansion*  

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-orange)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.0+-green)
<!-- 技术徽章增加专业感 -->

## 📌 Project Overview  
**Objective**:  
Analyze simulated customer data to:  
- Prioritize target segments using RFM + K-Means clustering  
- Identify regional gaps between fiber coverage and adoption  
- Generate actionable marketing strategies  

**Key Features**:  
✔️ 1000+ simulated customer records with geo-tagging  
✔️ Automated data cleaning pipeline  
✔️ Interactive Power BI dashboard (see `outputs/dashboard.pbix`)  

## 📂 File Structure  
```bash
├── data/
│   ├── simulated_customers_with_coverage.csv    # 主数据集
│   └── Glasfaser.xlsx                           # 原始覆盖率数据
├── scripts/
│   ├── 1.simulated_customers_with_coverage.py   # 数据生成脚本
│   ├── 2.data_cleansing.py                      # 数据清洗
│   ├── 3.EDA.py                                 # 探索性分析
│   └── 4.RFM_KMeans.py                          # 客户分群模型
├── outputs/                                     # 生成的图表
│   ├── fiber_adoption_by_region.png          
│   ├── customer_clusters.png                 
│   └── top5_gap_regions.png                  
└── README.md


---

## 📊 核心分析步骤

### 1. 数据准备与清洗  
**模拟数据生成**：基于德国真实光纤覆盖率数据，合成1000条客户记录（地域、职业、消费等）  
**数据清洗**：处理缺失值，标记高潜力客户（`potential_upsell = 1`）

```python
# 示例代码：标记高价值客户
df['potential_upsell'] = np.where((df['usage_gb'] > 50) & (df['spend_eur'] < 50), 1, 0)

