# Author: Shyamanth Lingampally

# Generates 4 charts for the README.
# Each one shows a key finding from the analysis.

import pandas as pd
import matplotlib.pyplot as plt


# basic styling
plt.rcParams['font.size'] = 10
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False


# load data
df = pd.read_csv('/Users/shyamanthlingampally/Desktop/energy_clean.csv')
df['date'] = pd.to_datetime(df['date'])


# ---------- chart 1: hourly load profile ----------
# shows when during the day the plant uses the most energy

hourly = df.groupby('hour')['Usage_kWh'].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(hourly['hour'], hourly['Usage_kWh'], alpha=0.2, color='#C62828')
ax.plot(hourly['hour'], hourly['Usage_kWh'], color='#C62828',
        linewidth=2.5, marker='o', markersize=4)

# annotate the peak
peak_row = hourly.loc[hourly['Usage_kWh'].idxmax()]
peak_hour = int(peak_row['hour'])
peak_value = peak_row['Usage_kWh']

ax.annotate(f'Peak: {peak_value:.0f} kWh at hour {peak_hour}',
            xy=(peak_hour, peak_value),
            xytext=(peak_hour + 2, peak_value + 5),
            fontsize=10, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#333'))

ax.set_xlabel('Hour of Day')
ax.set_ylabel('Avg Energy Usage (kWh)')
ax.set_xticks(range(0, 24, 2))
ax.set_title('Daily load profile - peak concentrates in business hours',
             fontweight='bold', loc='left', pad=15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/shyamanthlingampally/Desktop/hourly_profile.png', dpi=150, bbox_inches='tight')
plt.close()


# ---------- chart 2: load type breakdown ----------
# compares how much TIME is spent in each load type vs how much ENERGY
# goes to each - shows that Maximum Load is a small % of time but most of the cost

load = df.groupby('Load_Type').agg(
    intervals=('Usage_kWh', 'count'),
    total_kwh=('Usage_kWh', 'sum'),
).reset_index()

load['pct_time'] = load['intervals'] / load['intervals'].sum() * 100
load['pct_energy'] = load['total_kwh'] / load['total_kwh'].sum() * 100

# sort them Light -> Medium -> Maximum for readability
load_order = ['Light Load', 'Medium Load', 'Maximum Load']
load['Load_Type'] = pd.Categorical(load['Load_Type'], categories=load_order, ordered=True)
load = load.sort_values('Load_Type').reset_index(drop=True)

fig, ax = plt.subplots(figsize=(10, 5))

x_positions = range(len(load))
bar_width = 0.35

ax.bar([x - bar_width/2 for x in x_positions], load['pct_time'],
       width=bar_width, label='% of Time', color='#90CAF9', edgecolor='white')
ax.bar([x + bar_width/2 for x in x_positions], load['pct_energy'],
       width=bar_width, label='% of Energy', color='#C62828', edgecolor='white')

# add value labels on top of each bar
for i in range(len(load)):
    t = load['pct_time'].iloc[i]
    e = load['pct_energy'].iloc[i]
    ax.text(i - bar_width/2, t + 1, f'{t:.0f}%', ha='center',
            fontweight='bold', fontsize=9)
    ax.text(i + bar_width/2, e + 1, f'{e:.0f}%', ha='center',
            fontweight='bold', fontsize=9)

ax.set_xticks(x_positions)
ax.set_xticklabels(load['Load_Type'])
ax.set_ylabel('Percent')
ax.set_title('Maximum Load - small share of time, outsized share of energy',
             fontweight='bold', loc='left', pad=15)
ax.legend()

plt.tight_layout()
plt.savefig('/Users/shyamanthlingampally/Desktop/load_type.png', dpi=150, bbox_inches='tight')
plt.close()


# ---------- chart 3: weekday vs weekend ----------
# shows the baseload difference

ws = df.groupby('WeekStatus')['Usage_kWh'].agg(['mean', 'sum']).reset_index()

fig, ax = plt.subplots(figsize=(8, 5))

# use different colors for weekday vs weekend
bar_colors = []
for status in ws['WeekStatus']:
    if status == 'Weekday':
        bar_colors.append('#1565C0')
    else:
        bar_colors.append('#F57C00')

bars = ax.bar(ws['WeekStatus'], ws['mean'],
              color=bar_colors, width=0.5, edgecolor='white')

# label the bars
for bar, value in zip(bars, ws['mean']):
    ax.text(bar.get_x() + bar.get_width()/2, value + 1,
            f'{value:.1f} kWh',
            ha='center', fontweight='bold', fontsize=11)

ax.set_ylabel('Avg Energy Usage (kWh per 15-min interval)')
ax.set_title('Weekend baseload is non-zero - potential dead-load waste',
             fontweight='bold', loc='left', pad=15)

plt.tight_layout()
plt.savefig('/Users/shyamanthlingampally/Desktop/weekday_weekend.png', dpi=150, bbox_inches='tight')
plt.close()


# ---------- chart 4: monthly trend ----------
# shows consumption across the year to identify maintenance windows

monthly = df.groupby(['month', 'month_name'])['Usage_kWh'].sum().reset_index()
monthly = monthly.sort_values('month')

fig, ax = plt.subplots(figsize=(11, 5))

# plot in MWh for readability
ax.plot(monthly['month_name'], monthly['Usage_kWh']/1000,
        marker='o', linewidth=2.5, color='#1565C0', markersize=8)
ax.fill_between(monthly['month_name'], monthly['Usage_kWh']/1000,
                alpha=0.15, color='#1565C0')

# annotate each month's value
for i in range(len(monthly)):
    month = monthly['month_name'].iloc[i]
    value = monthly['Usage_kWh'].iloc[i] / 1000
    ax.annotate(f'{value:.0f}',
                xy=(month, value),
                textcoords='offset points',
                xytext=(0, 10), ha='center', fontsize=9)

ax.set_ylabel('Total Energy (MWh)')
ax.set_title('Monthly consumption pattern - identifies maintenance windows',
             fontweight='bold', loc='left', pad=15)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('/Users/shyamanthlingampally/Desktop/monthly_trend.png', dpi=150, bbox_inches='tight')
plt.close()


print('4 charts saved to charts/ folder')
