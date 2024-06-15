from strava.analysis import calculate_monthly_metrics, fetch_and_clean_strava_data
from strava.data_processing import add_cumsum_columns
import matplotlib.pyplot as plt
from config import current_month

""" MONTH ON MONTH PROGRESS YEARS"""
df = fetch_and_clean_strava_data()
month_2023 = calculate_monthly_metrics(df, year=2023)
month_2024 = calculate_monthly_metrics(df, year=2024)

# Add cumsum columns
add_cumsum_columns(month_2023)
add_cumsum_columns(month_2024)

# Slice for year-to-date (YTD)
month_2023_slice = month_2023.iloc[:current_month]  # Sliced for first 6 months
month_2024_slice = month_2024.iloc[:current_month]  # Sliced for first 6 months

# Plot styling parameters
linestyle = "-"
colors_1 = ['#65aeb9', '#d77e76', '#66b0da']
colors_2 = ['#1e4a76', '#66b5c0', '#f1a556']
linewidth = 3
marker = "o"
fontsize = "small"

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 6))

# Plotting data on ax1
ax.plot(month_2023_slice.index, month_2023_slice["cumsum_total_time"], linestyle=linestyle, color=colors_1[2], linewidth=linewidth, marker=marker, label='2023')
ax.plot(month_2024_slice.index, month_2024_slice["cumsum_total_time"], linestyle=linestyle, color=colors_2[0], linewidth=linewidth, marker=marker, label='2024')

# Title and labels
ax.set_title('Time(h)', fontsize=25)

# Customize spines (axis lines)
for spine in ax.spines.values():
    spine.set_linewidth(0.7)

# Ticks and grid
ax.grid(True)

# Legend
legend = ax.legend(fontsize=16)
legend.get_frame().set_edgecolor('black')
legend.get_frame().set_linewidth(0.5)

# Axis line colors
ax.spines['bottom'].set_color('black')
ax.spines['left'].set_color('black')
ax.spines['top'].set_color('black')
ax.spines['right'].set_color('black')

plt.tight_layout()
plt.show()
