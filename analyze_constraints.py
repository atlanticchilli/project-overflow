import pandas as pd
import re

# Load the data
df = pd.read_csv('ukpn-constraints-real-time-meter-readings.csv')
descriptions = df['constraint_description'].unique()

# Parse the descriptions to extract key components
constraint_locations = []

for desc in descriptions:
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

print('Constraint Location Analysis:')
print('=' * 50)
print(f'Total unique constraint descriptions: {len(descriptions)}')
print(f'Total unique main locations: {len(location_summary)}')
print()

print('Top 20 locations by constraint count:')
print('-' * 40)
for i, (location, row) in enumerate(location_summary.head(20).iterrows()):
    print(f'{i+1:2d}. {location:<25} ({row["constraint_count"]:2d} constraints)')
    print(f'    Voltages: {row["voltage_kv"]}')
    if row['route_codes']:
        print(f'    Routes: {row["route_codes"]}')
    print()

# Save detailed analysis
locations_df.to_csv('constraint_locations_parsed.csv', index=False)
location_summary.to_csv('constraint_locations_summary.csv')
print('Detailed analysis saved to constraint_locations_parsed.csv and constraint_locations_summary.csv')
