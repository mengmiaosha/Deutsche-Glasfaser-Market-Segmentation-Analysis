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

## 📌 核心分析步骤
## 1. 数据准备与清洗
## 模拟数据生成：基于德国真实光纤覆盖率数据，合成1000条客户记录（地域、职业、消费等）

## 数据清洗：处理缺失值，标记高潜力客户（potential_upsell=1）

```python
# 标记高价值客户标准：
# 1. 月使用量 > 50GB
# 2. 月消费 < 50欧元
df['potential_upsell'] = np.where(
    (df['usage_gb'] > 50) & 
    (df['spend_eur'] < 50), 
    1, 
    0
)
```
## 2. 探索性分析（EDA）
## 关键图表（精选3张最具业务价值的图）：

图表名称	分析结论	可视化
光纤采用率地域差异	农村地区采用率比城市低40%	地域差异
客户聚类结果	识别出4类价值群体，Cluster 3为最优潜力客群	聚类
覆盖率差距TOP5地区	萨克森-安哈尔特未开发潜力最大	差距分析
## 3. RFM模型与K-Means聚类
## 客户分群：基于消费额（Monetary）、使用量（Frequency）、客户稳定性（Recency）

## 聚类中心解读：

```python
# 聚类中心分析结果：
print("Cluster Centers:")
print(f"{'':<10} {'Recency':<8} {'Frequency':<10} {'Monetary':<8}")
print(f"Cluster 0 {52.1:<8.1f} {62.3:<10.1f} {45.2:<8.1f} # 低价值老年群体")
print(f"Cluster 3 {38.5:<8.1f} {155.6:<10.1f} {55.8:<8.1f} # 高潜力升级客群")
```
## 🎯 业务应用建议
精准营销策略
客户群	特征	行动方案
Cluster 3	高使用量但低消费	推送"商务套餐限时折扣"，强调性价比
农村KMUs	覆盖率差距>20%	联合地方政府开展"光纤下乡"补贴活动
自动化工具设计
触发式邮件：当客户搜索"网速慢"时，自动发送免费体验邀约

动态定价模型：基于使用量弹性调整农村套餐价格

## 🚀 快速复现
克隆仓库：

```bash
# 克隆仓库
git clone https://github.com/mengmiaosha/ClientAnalysis.git

# 安装Python依赖
pip install \
    pandas \
    scikit-learn \
    matplotlib

# 运行分析流水线
python scripts/1.data_generation.py && \
python scripts/4.RFM_KMeans.py
```
## ❓ 常见问题
## Q: 能否使用真实数据替换模拟数据？
## A: 可以！只需将data/simulated_customers_with_coverage.csv替换为包含相同字段的真实数据。

## Q: 如何调整客户分群数量？
## A: 修改4.RFM_KMeans.py中的n_clusters参数，并通过轮廓系数评估最佳分群数。
