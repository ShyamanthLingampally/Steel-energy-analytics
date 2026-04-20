# Author: Shyamanth Lingampally

# Steel plant energy analysis
# Looks at 15-min interval data for a full year and pulls out the key findings:
# when the plant peaks, how much is wasted on weekends, power factor issues,
# and what peak-shaving could save.

import pandas as pd
import json


# assumptions
KWH_RATE = 0.10             # $/kWh industrial rate (KEPCO 2018 avg)
DEMAND_CHARGE_SHARE = 0.30  # demand charges typically ~30% of industrial bill
PEAK_SHAVING_PCT = 0.15     # target 15% reduction on peak periods


# load cleaned data
df = pd.read_csv('/Users/shyamanthlingampally/Desktop/energy_clean.csv')
df['date'] = pd.to_datetime(df['date'])

findings = {}


# ---------- 1. annual footprint ----------
print('\n1. annual energy footprint')
print('-' * 40)

total_kwh = df['Usage_kWh'].sum()
total_cost = total_kwh * KWH_RATE
total_co2 = df['CO2tCO2'].sum()

print(f'total energy used: {total_kwh:,.0f} kWh')
print(f'estimated cost:    ${total_cost:,.0f}')
print(f'total CO2:         {total_co2:,.1f} tons')

findings['footprint'] = {
    'total_kwh': round(total_kwh, 0),
    'estimated_cost_usd': round(total_cost, 0),
    'total_co2_tons': round(total_co2, 1),
}


# ---------- 2. peak hours ----------
print('\n2. peak vs off-peak')
print('-' * 40)

hourly = df.groupby('hour')['Usage_kWh'].mean()
hourly = hourly.round(1)

peak_hour = hourly.idxmax()
peak_avg = hourly.max()
off_peak_avg = hourly.min()

# how much bigger is peak vs off-peak
peak_multiple = peak_avg / off_peak_avg

print(f'peak hour:          {peak_hour}:00')
print(f'peak avg:           {peak_avg:.0f} kWh')
print(f'off-peak minimum:   {off_peak_avg:.0f} kWh')
print(f'peak is {peak_multiple:.1f}x off-peak')

findings['peak'] = {
    'peak_hour': int(peak_hour),
    'peak_avg_kwh': round(peak_avg, 1),
    'off_peak_avg_kwh': round(off_peak_avg, 1),
    'peak_multiple': round(peak_multiple, 1),
}

hourly.to_csv('/Users/shyamanthlingampally/Desktop/hourly_profile.csv')


# ---------- 3. weekday vs weekend ----------
print('\n3. weekday vs weekend baseload')
print('-' * 40)

status = df.groupby('WeekStatus')['Usage_kWh'].agg(['mean', 'sum'])
print(status.round(1))

# handle case where data might not span a weekend
if 'Weekend' in status.index and 'Weekday' in status.index:
    weekend_avg = status.loc['Weekend', 'mean']
    weekday_avg = status.loc['Weekday', 'mean']
    weekend_total = status.loc['Weekend', 'sum']

    weekend_pct = (weekend_avg / weekday_avg) * 100
    weekend_cost = weekend_total * KWH_RATE

    print(f'\nweekend avg is {weekend_pct:.0f}% of weekday avg')
    print(f'total weekend consumption cost: ${weekend_cost:,.0f}')

    findings['weekend'] = {
        'weekend_avg_kwh': round(weekend_avg, 1),
        'weekday_avg_kwh': round(weekday_avg, 1),
        'weekend_as_pct_of_weekday': round(weekend_pct, 1),
        'weekend_annual_cost_usd': round(weekend_cost, 0),
    }
else:
    print('(need both weekday and weekend data for this section)')


# ---------- 4. load type breakdown ----------
print('\n4. load type profile')
print('-' * 40)

load_summary = df.groupby('Load_Type').agg(
    intervals=('Usage_kWh', 'count'),
    avg_kwh=('Usage_kWh', 'mean'),
    total_kwh=('Usage_kWh', 'sum'),
)
load_summary = load_summary.round(1)

# add some derived columns
total_intervals = len(df)
load_summary['pct_time'] = (load_summary['intervals'] / total_intervals * 100).round(1)
load_summary['pct_energy'] = (load_summary['total_kwh'] / total_kwh * 100).round(1)
load_summary['cost_usd'] = (load_summary['total_kwh'] * KWH_RATE).round(0)

print(load_summary)

# specifically track the max load since that's the cost driver
if 'Maximum Load' in load_summary.index:
    max_pct_time = load_summary.loc['Maximum Load', 'pct_time']
    max_pct_energy = load_summary.loc['Maximum Load', 'pct_energy']
    findings['load_distribution'] = {
        'max_load_pct_time': float(max_pct_time),
        'max_load_pct_energy': float(max_pct_energy),
    }

load_summary.to_csv('/Users/shyamanthlingampally/Desktop/load_type_profile.csv')


# ---------- 5. power factor efficiency ----------
print('\n5. power factor')
print('-' * 40)

# utilities penalize industrial customers when power factor drops below 90%
avg_lag_pf = df['Lagging_Current_Power_Factor'].mean()
avg_lead_pf = df['Leading_Current_Power_Factor'].mean()

below_90 = df[df['Lagging_Current_Power_Factor'] < 90]
pct_below_90 = len(below_90) / len(df) * 100

print(f'avg lagging power factor:  {avg_lag_pf:.1f}%')
print(f'avg leading power factor:  {avg_lead_pf:.1f}%')
print(f'intervals below 90% PF:    {pct_below_90:.1f}%')

findings['power_factor'] = {
    'avg_lagging_pct': round(avg_lag_pf, 1),
    'pct_intervals_below_90': round(pct_below_90, 1),
}


# ---------- 6. monthly pattern ----------
print('\n6. monthly consumption')
print('-' * 40)

monthly = df.groupby(['month', 'month_name'])['Usage_kWh'].agg(['sum', 'mean'])
monthly = monthly.round(1).reset_index()
monthly.columns = ['month', 'month_name', 'total_kwh', 'avg_kwh']
print(monthly.to_string(index=False))

# lowest-usage month is the best window for scheduled maintenance
lowest_row = monthly.loc[monthly['total_kwh'].idxmin()]
highest_row = monthly.loc[monthly['total_kwh'].idxmax()]

print(f'\nlowest month: {lowest_row["month_name"]} (best for maintenance)')
print(f'highest month: {highest_row["month_name"]}')

findings['seasonal'] = {
    'lowest_month': lowest_row['month_name'],
    'highest_month': highest_row['month_name'],
}

monthly.to_csv('/Users/shyamanthlingampally/Desktop/monthly_pattern.csv', index=False)


# ---------- 7. savings opportunity ----------
print('\n7. peak shaving opportunity')
print('-' * 40)

# industrial bills have two parts: energy consumption + demand charges
# demand charges scale with peak load, so shifting peak reduces them
demand_charges = total_cost * DEMAND_CHARGE_SHARE
potential_savings = demand_charges * PEAK_SHAVING_PCT

print(f'estimated demand charges: ${demand_charges:,.0f}')
print(f'if we shave 15% off peak: ${potential_savings:,.0f} saved per year')

findings['savings_opportunity'] = {
    'current_demand_charges_usd': round(demand_charges, 0),
    'potential_savings_usd': round(potential_savings, 0),
}


# save all findings to a json
with open('/Users/shyamanthlingampally/Desktop/findings.json', 'w') as f:
    json.dump(findings, f, indent=2)


# headline summary
print('\n\nHEADLINE FINDINGS')
print('=' * 50)
print(f'1. Plant uses {total_kwh/1e6:.2f}M kWh/yr (~${total_cost/1e6:.2f}M)')
print(f'2. Peak load is {peak_multiple:.1f}x off-peak, concentrated at hour {peak_hour}')
if 'weekend' in findings:
    wpct = findings['weekend']['weekend_as_pct_of_weekday']
    print(f'3. Weekend baseload is {wpct:.0f}% of weekday avg')
print(f'4. {pct_below_90:.0f}% of intervals have sub-90% power factor')
print(f'5. 15% peak shaving could save ~${potential_savings/1000:.0f}K/yr')
