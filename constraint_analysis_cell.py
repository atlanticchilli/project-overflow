# 8) Constraint Location Analysis
print("\n" + "=" * 60)
print("CONSTRAINT LOCATION ANALYSIS")
print("=" * 60)

# Load the real-time constraints data
rt_constraints = pd.read_csv(RT_CONSTRAINTS_PATH)
print(f"Loaded {len(rt_constraints)} real-time constraint readings")

# Extract unique constraint descriptions
unique_descriptions = rt_constraints['constraint_description'].unique()
print(f"Found {len(unique_descriptions)} unique constraint descriptions")

# Parse constraint descriptions to extract key components
constraint_locations = []

for desc in unique_descriptions:
    # Extract voltage level
    voltage_match = re.search(r'(\d+)kV', desc)
    voltage = voltage_match.group(1) if voltage_match else 'Unknown'
    
    # Extract main location (before first dash)
    location_match = re.search(r'^([^-]+)', desc)
    location = location_match.group(1).strip() if location_match else 'Unknown'
    
    # Extract route codes in parentheses
    route_codes = re.findall(r'\(([^)]+)\)', desc)
    
    constraint_locations.append({
        'description': desc,
        'main_location': location,
        'voltage_kv': voltage,
        'route_codes': route_codes
    })

# Create DataFrame and analyze
locations_df = pd.DataFrame(constraint_locations)

# Group by main location
location_summary = locations_df.groupby('main_location').agg({
    'voltage_kv': lambda x: list(set(x)),
    'route_codes': lambda x: list(set([code for codes in x for code in codes if codes])),
    'description': 'count'
}).rename(columns={'description': 'constraint_count'})

# Sort by constraint count
location_summary = location_summary.sort_values('constraint_count', ascending=False)

print(f"\nTotal unique main locations: {len(location_summary)}")
print(f"Total constraints: {location_summary['constraint_count'].sum()}")

# Display top 20 locations
print("\nTop 20 locations by constraint count:")
print("-" * 50)
for i, (location, row) in enumerate(location_summary.head(20).iterrows()):
    print(f'{i+1:2d}. {location:<30} ({row["constraint_count"]:2d} constraints)')
    print(f'    Voltages: {row["voltage_kv"]}')
    if row['route_codes']:
        print(f'    Routes: {row["route_codes"]}')
    print()

# Save detailed analysis
locations_df.to_csv('outputs/constraint_locations_parsed.csv', index=False)
location_summary.to_csv('outputs/constraint_locations_summary.csv')
print('Detailed analysis saved to outputs/constraint_locations_parsed.csv and outputs/constraint_locations_summary.csv')

# Create visualizations
try:
    import matplotlib.pyplot as plt
    
    # Create figure with subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('UKPN Constraint Analysis - Distribution by Location', fontsize=16, fontweight='bold')

    # 1. Top 15 locations by constraint count
    top_15 = location_summary.head(15)
    bars1 = ax1.barh(range(len(top_15)), top_15['constraint_count'], color='skyblue')
    ax1.set_yticks(range(len(top_15)))
    ax1.set_yticklabels([loc[:20] + '...' if len(loc) > 20 else loc for loc in top_15.index])
    ax1.set_xlabel('Number of Constraints')
    ax1.set_title('Top 15 Locations by Constraint Count')
    ax1.grid(axis='x', alpha=0.3)

    # Add value labels on bars
    for i, bar in enumerate(bars1):
        width = bar.get_width()
        ax1.text(width + 0.1, bar.get_y() + bar.get_height()/2, str(int(width)), 
                 ha='left', va='center', fontweight='bold')

    # 2. Voltage level distribution
    voltage_counts = location_summary['voltage_kv'].apply(lambda x: x[0] if x else 'Unknown').value_counts()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    ax2.pie(voltage_counts.values, labels=voltage_counts.index, autopct='%1.1f%%', colors=colors[:len(voltage_counts)])
    ax2.set_title('Distribution by Voltage Level')

    # 3. Constraint count distribution (histogram)
    ax3.hist(location_summary['constraint_count'], bins=range(1, max(location_summary['constraint_count'])+2), 
             edgecolor='black', alpha=0.7, color='lightgreen')
    ax3.set_xlabel('Number of Constraints per Location')
    ax3.set_ylabel('Number of Locations')
    ax3.set_title('Distribution of Constraint Counts per Location')
    ax3.grid(axis='y', alpha=0.3)

    # 4. Top locations with route codes
    has_routes = location_summary[location_summary['route_codes'].apply(lambda x: len(x) > 0)].head(10)
    if len(has_routes) > 0:
        bars4 = ax4.barh(range(len(has_routes)), has_routes['constraint_count'], color='lightcoral')
        ax4.set_yticks(range(len(has_routes)))
        ax4.set_yticklabels([loc[:20] + '...' if len(loc) > 20 else loc for loc in has_routes.index])
        ax4.set_xlabel('Number of Constraints')
        ax4.set_title('Top 10 Locations with Route Codes')
        ax4.grid(axis='x', alpha=0.3)

        # Add value labels on bars
        for i, bar in enumerate(bars4):
            width = bar.get_width()
            ax4.text(width + 0.1, bar.get_y() + bar.get_height()/2, str(int(width)), 
                     ha='left', va='center', fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No locations with route codes', ha='center', va='center', transform=ax4.transAxes)
        ax4.set_title('Top 10 Locations with Route Codes')

    plt.tight_layout()
    plt.savefig('outputs/constraint_analysis_charts.png', dpi=300, bbox_inches='tight')
    print('Charts saved to outputs/constraint_analysis_charts.png')
    
except ImportError:
    print("Matplotlib not available - skipping charts")

# Summary statistics
print("\n" + "=" * 50)
print("CONSTRAINT LOCATION SUMMARY")
print("=" * 50)
print(f'Total locations: {len(location_summary)}')
print(f'Total constraints: {location_summary["constraint_count"].sum()}')
print(f'Average constraints per location: {location_summary["constraint_count"].mean():.1f}')
print(f'Locations with route codes: {len(location_summary[location_summary["route_codes"].apply(lambda x: len(x) > 0)])}')

print('\nTop 10 locations by constraint count:')
print('-' * 40)
for i, (location, row) in enumerate(location_summary.head(10).iterrows()):
    print(f'{i+1:2d}. {location:<30} ({row["constraint_count"]:2d} constraints)')
