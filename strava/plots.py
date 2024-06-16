from strava.analysis import calculate_monthly_metrics, fetch_and_clean_strava_data
from strava.data_processing import add_cumsum_columns
import matplotlib.pyplot as plt
from config import current_month
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio


""" MONTH ON MONTH PROGRESS YEARS"""
df = fetch_and_clean_strava_data()
month_2023 = calculate_monthly_metrics(df, year=2023)
month_2024 = calculate_monthly_metrics(df, year=2024)

# Add cumsum columns
add_cumsum_columns(month_2023)
add_cumsum_columns(month_2024)

# Slice data to get year-to-date (YTD)
month_2023_slice = month_2023.iloc[:current_month]
month_2024_slice = month_2024.iloc[:current_month]


# Common plot parameters
colors = ["#b2e061", "#7eb0d5"]
linewidth = 5
linecolor = "black"
height = 250
width = 300
bgcolor = "rgba(0,0,0,0)"


def generate_distance_plot(month_2023_slice, month_2024_slice):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=month_2023_slice.index,
            y=month_2023_slice["cumsum_total_distance"],
            mode="lines",
            line=dict(color=colors[0], width=linewidth),
            name="2023",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=month_2024_slice.index,
            y=month_2024_slice["cumsum_total_distance"],
            mode="lines",
            line=dict(color=colors[1], width=linewidth),
            name="2024",
        )
    )

    fig.update_layout(
        height=height,
        width=width,
        title="",
        xaxis_title="",
        yaxis_title="",
        legend=dict(font=dict(size=12), traceorder="normal", bgcolor=bgcolor),
        margin=dict(l=0, r=0, t=40, b=50),
        plot_bgcolor=bgcolor,
        xaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
        yaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
    )

    graph_html = pio.to_html(fig, full_html=False)
    return graph_html


def generate_elevation_plot(month_2023_slice, month_2024_slice):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=month_2023_slice.index,
            y=month_2023_slice["cumsum_total_elevation"],
            mode="lines",
            line=dict(color=colors[0], width=linewidth),
            name="2023",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=month_2024_slice.index,
            y=month_2024_slice["cumsum_total_elevation"],
            mode="lines",
            line=dict(color=colors[1], width=linewidth),
            name="2024",
        )
    )

    fig.update_layout(
        height=height,
        width=width,
        title="",
        xaxis_title="",
        yaxis_title="",
        legend=dict(font=dict(size=12), traceorder="normal", bgcolor=bgcolor),
        margin=dict(l=0, r=0, t=20, b=20),
        plot_bgcolor=bgcolor,
        xaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
        yaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
    )

    graph_html = pio.to_html(fig, full_html=False)
    return graph_html

"""
# Parameters that apply to all plots
colors = ["#b2e061", "#7eb0d5"]
linewidth = 5
linecolor = "black"
fig = go.Figure()
height = 250
width = 350
bgcolor = "rgba(0,0,0,0)"


fig.add_trace(
    go.Scatter(
        x=month_2023_slice.index,
        y=month_2023_slice["cumsum_total_distance"],
        mode="lines",
        line=dict(color=colors[0], width=linewidth),
        name="2023",
    )
)

# Plotting data for 2024
fig.add_trace(
    go.Scatter(
        x=month_2024_slice.index,
        y=month_2024_slice["cumsum_total_distance"],
        mode="lines",
        line=dict(color=colors[1], width=linewidth),
        name="2024",
    )
)

# Update layout with title and axis labels
fig.update_layout(
    height=height,
    width=width,
    title="",
    xaxis_title="",
    yaxis_title="",
    legend=dict(font=dict(size=1), traceorder="normal", bgcolor=bgcolor),
    margin=dict(l=0, r=0, t=40, b=50),
    plot_bgcolor=bgcolor,
    xaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
    yaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
)

# Customize the legend frame
fig.update_traces(showlegend=True, selector=dict(type="scatter"))
fig.update_layout(legend=dict(font=dict(size=16), traceorder="normal", bgcolor=bgcolor))

# Convert figure to HTML
graph_html = pio.to_html(fig, full_html=False)


fig.add_trace(
    go.Scatter(
        x=month_2023_slice.index,
        y=month_2023_slice["cumsum_total_elevation"],
        mode="lines",
        line=dict(color=colors[0], width=linewidth),
        name="2023",
    )
)

# Plotting data for 2024
fig.add_trace(
    go.Scatter(
        x=month_2024_slice.index,
        y=month_2024_slice["cumsum_total_elevation"],
        mode="lines",
        line=dict(color=colors[1], width=linewidth),
        name="2024",
    )
)

# Update layout with title and axis labels
fig.update_layout(
    height=height,
    width=width,
    title="",
    xaxis_title="",
    yaxis_title="",
    legend=dict(font=dict(size=1), traceorder="normal", bgcolor=bgcolor),
    margin=dict(l=0, r=0, t=40, b=50),
    plot_bgcolor=bgcolor,
    xaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
    yaxis=dict(showline=True, linecolor=linecolor, linewidth=0.5),
)

# Customize the legend frame
fig.update_traces(showlegend=True, selector=dict(type="scatter"))
fig.update_layout(legend=dict(font=dict(size=16), traceorder="normal", bgcolor=bgcolor))

# Convert figure to HTML
graph_html = pio.to_html(fig, full_html=False)



def ytd_line_chart(metric, title):
    # Plot styling parameters
    linestyle = "-"
    colors_1 = ["#65aeb9", "#d77e76", "#66b0da"]
    colors_2 = ["#1e4a76", "#66b5c0", "#f1a556"]
    linewidth = 3
    marker = ""

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(6, 4))

    # Plotting data on ax1
    ax.plot(month_2023_slice.index, month_2023_slice[metric], linestyle=linestyle, color=colors_1[2], linewidth=linewidth, marker=marker, label='2023')
    ax.plot(month_2024_slice.index, month_2024_slice[metric], linestyle=linestyle, color=colors_2[0], linewidth=linewidth, marker=marker, label='2024')

    # Title and labels
    ax.set_title(title, fontsize=18)

    # Customize spines (axis lines)
    for spine in ax.spines.values():
        spine.set_linewidth(0.7)

    # Ticks and grid
        ax.grid(False)
        ax.tick_params(axis='both', which='major', labelsize=12)
        ax.tick_params(axis='both', which='minor', labelsize=12)


    # Legend
    legend = ax.legend(fontsize=10)
    legend.get_frame().set_edgecolor('black')
    legend.get_frame().set_linewidth(0.5)

    # Axis line colors
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')

    plt.tight_layout()
    plt.show()


ytd_line_chart('cumsum_total_rides', "Total Rides")


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Assuming you have month_2023 and month_2024 DataFrames already defined

# Get current month
current_month = 6  # Example value, adjust as per your actual data

# Slice data to get YTD values for time, distance, and elevation
month_2023_slice_time = month_2023.iloc[:current_month]
month_2024_slice_time = month_2024.iloc[:current_month]
month_2023_slice_dist = month_2023.iloc[:current_month]
month_2024_slice_dist = month_2024.iloc[:current_month]
month_2023_slice_elev = month_2023.iloc[:current_month]
month_2024_slice_elev = month_2024.iloc[:current_month]

colors = ['#b2e061', '#7eb0d5']
linewidth = 3

# Create subplots with three rows (for time, distance, and elevation) and one column
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                    subplot_titles=['Time (h)', 'Distance (km)', 'Elevation (m)'])

# Plotting data for 2023 and 2024 for Time
fig.add_trace(go.Scatter(x=month_2023_slice_time.index, y=month_2023_slice_time["cumsum_total_time"],
                         mode='lines',
                         line=dict(color=colors[0], width=linewidth),
                         name='2023'), row=1, col=1)

fig.add_trace(go.Scatter(x=month_2024_slice_time.index, y=month_2024_slice_time["cumsum_total_time"],
                         mode='lines',
                         line=dict(color=colors[1], width=linewidth),
                         name='2024'), row=1, col=1)

# Plotting data for 2023 and 2024 for Distance
fig.add_trace(go.Scatter(x=month_2023_slice_dist.index, y=month_2023_slice_dist["cumsum_total_rides"],
                         mode='lines',
                         line=dict(color=colors[0], width=linewidth),
                         showlegend=False), row=2, col=1)

fig.add_trace(go.Scatter(x=month_2024_slice_dist.index, y=month_2024_slice_dist["cumsum_total_rides"],
                         mode='lines',
                         line=dict(color=colors[1], width=linewidth),
                         showlegend=False), row=2, col=1)

# Plotting data for 2023 and 2024 for Elevation
fig.add_trace(go.Scatter(x=month_2023_slice_elev.index, y=month_2023_slice_elev["cumsum_total_elevation"],
                         mode='lines',
                         line=dict(color=colors[0], width=linewidth),
                         showlegend=False), row=3, col=1)

fig.add_trace(go.Scatter(x=month_2024_slice_elev.index, y=month_2024_slice_elev["cumsum_total_elevation"],
                         mode='lines',
                         line=dict(color=colors[1], width=linewidth),
                         showlegend=False), row=3, col=1)

# Update layout for entire figure
fig.update_layout(
    height=900,  # Adjust height as needed
    width=600,   # Adjust width as needed
    showlegend=True,
    legend=dict(font=dict(size=12), traceorder='normal', bgcolor='rgba(0,0,0,0)',
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=50, r=50, t=70, b=70),  # Adjust margins as needed
    plot_bgcolor='rgba(0,0,0,0)',
)

# Update subplot titles, x-axis, and y-axis labels
fig.update_xaxes(title_text='Month', row=3, col=1, showline=True, linecolor='black', linewidth=0.5)
fig.update_yaxes(title_text='Cumulative Time (h)', row=1, col=1, showline=True, linecolor='black', linewidth=0.5,
                 gridcolor='lightgray', gridwidth=0.5)
fig.update_yaxes(title_text='Cumulative Distance (km)', row=2, col=1, showline=True, linecolor='black', linewidth=0.5,
                 gridcolor='lightgray', gridwidth=0.5)
fig.update_yaxes(title_text='Cumulative Elevation (m)', row=3, col=1, showline=True, linecolor='black', linewidth=0.5,
                 gridcolor='lightgray', gridwidth=0.5)

# Update x-axis gridlines for all subplots
fig.update_xaxes(showgrid=True, gridcolor='lightgray', gridwidth=0.5)

# Show the plot
fig.show()
"""
