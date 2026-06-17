import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)


# ── Load Data ────────────────────────────────────────────────
base = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(base, '..', 'data', 'healthcare_data.csv'))

print(f"Shape: {df.shape}")
print(df.head())


# ── Basic Info ───────────────────────────────────────────────
print(df.dtypes)
print(df.isnull().sum())
print(df.duplicated().sum())


# ── Clean & Prepare ──────────────────────────────────────────
df['Admission_Date']  = pd.to_datetime(df['Admission_Date'])
df['Discharge_Date']  = pd.to_datetime(df['Discharge_Date'])

df['Month']     = df['Admission_Date'].dt.month_name()
df['Month_Num'] = df['Admission_Date'].dt.month
df['Quarter']   = df['Admission_Date'].dt.quarter

bins   = [0, 30, 45, 60, 75, 100]
labels = ['18-30', '31-45', '46-60', '61-75', '75+']
df['Age_Group'] = pd.cut(df['Age'], bins=bins, labels=labels)

print(df.head(10))


# ── Descriptive Stats ────────────────────────────────────────
print(df.describe().round(2))
print(df['Medical_Condition'].value_counts())
print(df['Hospital'].value_counts())


# ── Statistics ───────────────────────────────────────────────
print(f"\nMean Billing  : ${df['Billing_Amount'].mean():,.2f}")
print(f"Median Billing: ${df['Billing_Amount'].median():,.2f}")
print(f"Std Dev       : ${df['Billing_Amount'].std():,.2f}")
print(f"Mode Condition: {df['Medical_Condition'].mode()[0]}")
print(f"Mode Hospital : {df['Hospital'].mode()[0]}")

print("\nStats by Condition:")
print(
    df.groupby('Medical_Condition')['Billing_Amount']
    .agg(Mean='mean', Median='median', Std=('std'), Min='min', Max='max')
    .round(2)
)


# ── Charts ───────────────────────────────────────────────────
out = os.path.join(base, '..', 'screenshots')
os.makedirs(out, exist_ok=True)


# Chart 1 — Revenue by Medical Condition
rev_cond = (
    df.groupby('Medical_Condition')['Billing_Amount']
    .sum().sort_values(ascending=False).reset_index()
)
fig, ax = plt.subplots()
sns.barplot(data=rev_cond, x='Medical_Condition', y='Billing_Amount',
            palette='Blues_d', ax=ax)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000,
            f"${bar.get_height():,.0f}", ha='center', fontsize=9, fontweight='bold')
ax.set_title('Total Revenue by Medical Condition (2023)', fontsize=13, fontweight='bold')
ax.set_xlabel('Medical Condition')
ax.set_ylabel('Total Revenue (USD)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart1_revenue_by_condition.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 2 — Revenue by Hospital
rev_hosp = (
    df.groupby('Hospital')['Billing_Amount']
    .sum().sort_values(ascending=True).reset_index()
)
fig, ax = plt.subplots()
sns.barplot(data=rev_hosp, x='Billing_Amount', y='Hospital',
            palette='Greens_d', ax=ax)
for bar in ax.patches:
    ax.text(bar.get_width() + 20000, bar.get_y() + bar.get_height()/2,
            f"${bar.get_width():,.0f}", ha='left', va='center', fontsize=9, fontweight='bold')
ax.set_title('Total Revenue by Hospital (2023)', fontsize=13, fontweight='bold')
ax.set_xlabel('Total Revenue (USD)')
ax.set_ylabel('Hospital')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart2_revenue_by_hospital.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 3 — Revenue by Gender
rev_gen = df.groupby('Gender')['Billing_Amount'].sum().reset_index()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(rev_gen['Billing_Amount'], labels=rev_gen['Gender'],
       autopct='%1.1f%%', startangle=90, explode=[0.05, 0.05],
       colors=['#4C72B0', '#DD8452'], textprops={'fontsize': 12})
ax.set_title('Revenue Distribution by Gender (2023)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart3_revenue_by_gender.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 4 — Age Distribution
fig, ax = plt.subplots()
sns.histplot(data=df, x='Age', bins=20, kde=True,
             color='#4C72B0', edgecolor='white', ax=ax)
ax.axvline(df['Age'].mean(), color='red', linestyle='--', linewidth=1.5,
           label=f"Mean Age: {df['Age'].mean():.1f}")
ax.set_title('Age Distribution of Patients (2023)', fontsize=13, fontweight='bold')
ax.set_xlabel('Patient Age (Years)')
ax.set_ylabel('Number of Patients')
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart4_age_distribution.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 5 — Monthly Revenue Trend
monthly = (
    df.groupby(['Month_Num', 'Month'])['Billing_Amount']
    .sum().reset_index().sort_values('Month_Num')
)
fig, ax = plt.subplots()
ax.plot(monthly['Month'], monthly['Billing_Amount'],
        marker='o', linewidth=2.5, markersize=8, color='#2196F3')
ax.fill_between(monthly['Month'], monthly['Billing_Amount'], alpha=0.15, color='#2196F3')
for _, row in monthly.iterrows():
    ax.annotate(f"${row['Billing_Amount']:,.0f}",
                xy=(row['Month'], row['Billing_Amount']),
                xytext=(0, 10), textcoords='offset points',
                ha='center', fontsize=8)
ax.set_title('Monthly Revenue Trend — 2023', fontsize=13, fontweight='bold')
ax.set_xlabel('Month')
ax.set_ylabel('Total Revenue (USD)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart5_monthly_revenue_trend.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 6 — Avg Billing by Age Group
avg_age = (
    df.groupby('Age_Group', observed=True)['Billing_Amount']
    .mean().reset_index()
)
fig, ax = plt.subplots()
sns.barplot(data=avg_age, x='Age_Group', y='Billing_Amount', palette='OrRd', ax=ax)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
            f"${bar.get_height():,.0f}", ha='center', fontsize=10, fontweight='bold')
ax.set_title('Average Billing by Age Group (2023)', fontsize=13, fontweight='bold')
ax.set_xlabel('Age Group')
ax.set_ylabel('Avg Billing (USD)')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart6_avg_billing_by_age_group.png'), dpi=150, bbox_inches='tight')
plt.close()


# Chart 7 — Avg Stay by Condition
avg_stay = (
    df.groupby('Medical_Condition')['Stay_Days']
    .mean().sort_values(ascending=False).reset_index()
)
fig, ax = plt.subplots()
sns.barplot(data=avg_stay, x='Medical_Condition', y='Stay_Days', palette='Purples_d', ax=ax)
for bar in ax.patches:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{bar.get_height():.1f}d", ha='center', fontsize=10, fontweight='bold')
ax.set_title('Average Stay Days by Medical Condition (2023)', fontsize=13, fontweight='bold')
ax.set_xlabel('Medical Condition')
ax.set_ylabel('Avg Stay (Days)')
plt.tight_layout()
plt.savefig(os.path.join(out, 'chart7_avg_stay_by_condition.png'), dpi=150, bbox_inches='tight')
plt.close()


# ── Summary ──────────────────────────────────────────────────
print("\n========== PROJECT SUMMARY ==========")
print(f"Total Patients : {len(df)}")
print(f"Total Revenue  : ${df['Billing_Amount'].sum():,.2f}")
print(f"Avg Billing    : ${df['Billing_Amount'].mean():,.2f}")
print(f"Median Billing : ${df['Billing_Amount'].median():,.2f}")
print(f"Avg Stay       : {df['Stay_Days'].mean():.1f} days")
print(f"Top Condition  : {df.groupby('Medical_Condition')['Billing_Amount'].sum().idxmax()}")
print(f"Top Hospital   : {df.groupby('Hospital')['Billing_Amount'].sum().idxmax()}")
print("=====================================")
print("Charts saved to screenshots/")
