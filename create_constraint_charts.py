import pandas as pd
import matplotlib.pyplot as plt

# Set style
plt.style.use('default')

# Load the summary data
df = pd.read_csv('constraint_locations_summary.csv')

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('UKPN Constraint Analysis - Distribution by Location', fontsize=16, fontweight='bold')

# 1. Top 15 locations by constraint count
top_15 = df.head(15)
bars1 = ax1.barh(range(len(top_15)), top_15['constraint_count'], color='skyblue')
ax1.set_yticks(range(len(top_15)))
ax1.set_yticklabels([loc[:20] + '...' if len(loc) > 20 else loc for loc in top_15['main_location']])
ax1.set_xlabel('Number of Constraints')
ax1.set_title('Top 15 Locations by Constraint Count')
ax1.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, bar in enumerate(bars1):
    width = bar.get_width()
    ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, str(int(width)), 
             ha='left', va='center', fontweight='bold')

# 2. Voltage level distribution
voltage_counts = df['voltage_kv'].apply(lambda x: eval(x)[0] if x != '[]' else 'Unknown').value_counts()
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
bars2 = ax2.pie(voltage_counts.values, labels=voltage_counts.index, autopct='%1.1f%%', colors=colors[:len(voltage_counts)])
ax2.set_title('Distribution by Voltage Level')

# 3. Constraint count distribution (histogram)
ax3.hist(df['constraint_count'], bins=range(1, max(df['constraint_count'])+2), 
         edgecolor='black', alpha=0.7, color='lightgreen')
ax3.set_xlabel('Number of Constraints per Location')
ax3.set_ylabel('Number of Locations')
ax3.set_title('Distribution of Constraint Counts per Location')
ax3.grid(axis='y', alpha=0.3)

# 4. Top locations with route codes
has_routes = df[df['route_codes'].apply(lambda x: x != '[]')].head(10)
bars4 = ax4.barh(range(len(has_routes)), has_routes['constraint_count'], color='lightcoral')
ax4.set_yticks(range(len(has_routes)))
ax4.set_yticklabels([loc[:20] + '...' if len(loc) > 20 else loc for loc in has_routes['main_location']])
ax4.set_xlabel('Number of Constraints')
ax4.set_title('Top 10 Locations with Route Codes')
ax4.grid(axis='x', alpha=0.3)

# Add value labels on bars
for i, bar in enumerate(bars4):
    width = bar.get_width()
    ax4.text(width + 0.1, bar.get_y() + bar.get_height()/2, str(int(width)), 
             ha='left', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('constraint_analysis_charts.png', dpi=300, bbox_inches='tight')
print('Charts saved to constraint_analysis_charts.png')

# Create a summary table
print('\nConstraint Location Summary:')
print('=' * 50)
print(f'Total locations: {len(df)}')
print(f'Total constraints: {df["constraint_count"].sum()}')
print(f'Average constraints per location: {df["constraint_count"].mean():.1f}')
print(f'Locations with route codes: {len(df[df["route_codes"].apply(lambda x: x != "[]")])}')

print('\nTop 10 locations by constraint count:')
print('-' * 40)
for i, row in df.head(10).iterrows():
    print(f'{i+1:2d}. {row["main_location"]:<30} ({row["constraint_count"]:2d} constraints)')
