from flask import Flask, render_template
from strava.analysis import (
    calculate_yearly_totals,
    fetch_and_clean_strava_data,
    calculate_yearly_averages,
    calculate_monthly_metrics,
)
from strava.data_processing import add_cumsum_columns
from config import current_month
from strava.plots import generate_elevation_plot, generate_distance_plot

app = Flask(__name__)


@app.route("/")
def home():
    data = fetch_and_clean_strava_data()

    # Yearly totals
    last_year = 2023
    current_year = 2024
    all_time = None

    current_year_totals = calculate_yearly_totals(data, current_year)
    last_year_totals = calculate_yearly_totals(data, last_year)
    all_time_totals = calculate_yearly_totals(data, all_time)

    current_year_averages = calculate_yearly_averages(data, current_year)
    last_year_averages = calculate_yearly_averages(data, last_year)

    month_2023 = calculate_monthly_metrics(data, year=2023)
    month_2024 = calculate_monthly_metrics(data, year=2024)

    # Plots
    add_cumsum_columns(month_2023)
    add_cumsum_columns(month_2024)

    month_2023_slice = month_2023.iloc[:current_month]
    month_2024_slice = month_2024.iloc[:current_month]

    distance_plot_html = generate_distance_plot(month_2023_slice, month_2024_slice)
    elevation_plot_html = generate_elevation_plot(month_2023_slice, month_2024_slice)

    return render_template(
        "index.html",
        last_year=last_year,
        current_year=current_year,
        current_year_totals=current_year_totals,
        last_year_totals=last_year_totals,
        all_time_totals=all_time_totals,
        current_year_averages=current_year_averages,
        last_year_averages=last_year_averages,
        distance_plot_html=distance_plot_html,
        elevation_plot_html=elevation_plot_html,
    )


if __name__ == "__main__":
    app.run(debug=True)
