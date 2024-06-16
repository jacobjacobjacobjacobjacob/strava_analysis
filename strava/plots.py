from strava.analysis import calculate_monthly_metrics, fetch_and_clean_strava_data
from strava.data_processing import add_cumsum_columns
import plotly.graph_objects as go
import plotly.io as pio
from config import current_month


# Constants
COLORS = ["#b2e061", "#7eb0d5"]
LINEWIDTH = 5
LINECOLOR = "black"
HEIGHT = 250
WIDTH = 300
BGCOLOR = "rgba(0,0,0,0)"


def prepare_data():
    df = fetch_and_clean_strava_data()
    month_2023 = calculate_monthly_metrics(df, year=2023)
    month_2024 = calculate_monthly_metrics(df, year=2024)
    add_cumsum_columns(month_2023)
    add_cumsum_columns(month_2024)
    return month_2023.iloc[:current_month], month_2024.iloc[:current_month]


def generate_plot(month_2023_slice, month_2024_slice, y_column, title):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=month_2023_slice.index,
            y=month_2023_slice[y_column],
            mode="lines",
            line=dict(color=COLORS[0], width=LINEWIDTH),
            name="2023",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=month_2024_slice.index,
            y=month_2024_slice[y_column],
            mode="lines",
            line=dict(color=COLORS[1], width=LINEWIDTH),
            name="2024",
        )
    )

    fig.update_layout(
        height=HEIGHT,
        width=WIDTH,
        title=title,
        xaxis_title="",
        yaxis_title="",
        legend=dict(font=dict(size=12), traceorder="normal", bgcolor=BGCOLOR),
        margin=dict(l=0, r=0, t=40, b=50),
        plot_bgcolor=BGCOLOR,
        xaxis=dict(showline=True, linecolor=LINECOLOR, linewidth=0.5),
        yaxis=dict(showline=True, linecolor=LINECOLOR, linewidth=0.5),
    )

    return pio.to_html(fig, full_html=False)


def generate_distance_plot(month_2023_slice, month_2024_slice):
    return generate_plot(
        month_2023_slice, month_2024_slice, "cumsum_total_distance", ""
    )


def generate_elevation_plot(month_2023_slice, month_2024_slice):
    return generate_plot(
        month_2023_slice, month_2024_slice, "cumsum_total_elevation", ""
    )


def generate_time_plot(month_2023_slice, month_2024_slice):
    return generate_plot(month_2023_slice, month_2024_slice, "cumsum_total_time", "")


def generate_rides_plot(month_2023_slice, month_2024_slice):
    return generate_plot(month_2023_slice, month_2024_slice, "cumsum_total_rides", "")


if __name__ == "__main__":
    month_2023_slice, month_2024_slice = prepare_data()
    distance_plot_html = generate_distance_plot(month_2023_slice, month_2024_slice)
    elevation_plot_html = generate_elevation_plot(month_2023_slice, month_2024_slice)
    time_plot_html = generate_time_plot(month_2023_slice, month_2024_slice)
    rides_plot_html = generate_rides_plot(month_2023_slice, month_2024_slice)
