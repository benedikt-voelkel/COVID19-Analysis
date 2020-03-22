import argparse
from os.path import join, exists

from numpy import diff as npdiff
import matplotlib.pyplot as plt

from covid19_analysis.data_utils import collect_data
from covid19_analysis.plot_utils import plot_1d, plot_2d, plot_3d_bubbles

def run_analysis(data_path):
    
    # Make full path where data is assumed to be

    
    data_path = join(data_path, "csse_covid_19_data/csse_covid_19_daily_reports")
    if not exists(data_path):
        print(f"Path to data does apparently not exist: {data_path}")
        return

    # Prepare data
    countries = ("Germany", "Italy", "China", "Iran", "South Korea", "Spain", "France", "Switzerland")
    countries_aliases = {"China": ["China", "Mainland China"], "South Korea": ["Korea, South", "South Korea"]}
    metrics = ("Confirmed", "Deaths")
    dates, data = collect_data(data_path, "Country/Region", countries, metrics, group_aliases=countries_aliases)


    # Used to scale things
    inhabitants = {"Germany": 83000000,
                   "Italy": 60000000,
                   "China": 1401000000,
                   "Iran": 83000000,
                   "South Korea": 52000000,
                   "Spain": 47000000,
                   "France": 67000000,
                   "Brazil": 211000000,
                   "Switzerland": 9000000}
    inv_inhabitants = {key: 100000. / value for key, value in inhabitants.items()}

    # Make a new figure, everything normalised to countries' inhabitants
    fig, axes = plt.subplots(2, 3, figsize=(50, 25))

    plot_1d(axes[0][0], data, "Confirmed", 500, inv_inhabitants, log_y=True,
            x_label="days since # Confirmed > 500",
            y_label="# Confirmed / 100,000 inhabitants (log scale)")
    plot_1d(axes[0][1], data, "Deaths", 50, inv_inhabitants, log_y=True,
            x_label="days since # Deaths > 50",
            y_label="# Deaths / 100,000 inhabitants (log scale)")
    plot_2d(axes[0][2], data, "Confirmed", "Deaths",
            scale_x=inv_inhabitants, scale_y=inv_inhabitants,
            x_label="# Confirmed / 100,000 inhabitants", y_label="# Deaths / 100,000 inhabitants")
    plot_1d(axes[1][0], data, "Confirmed", 500, inv_inhabitants, transform=npdiff,
            x_label="days since # Confirmed > 500",
            y_label="# Delta Confirmed / 100,000 inhabitants")
    plot_1d(axes[1][1], data, "Deaths", 50, inv_inhabitants, transform=npdiff,
            x_label="days since # Deaths > 50", y_label="# Delta Deaths / 100,000 inhabitants")

    # Prepare for a more fancy plot
    hospital_beds = {"Germany": 8.00,
                     "Italy": 3.18,
                     "China": 4.34,
                     "South Korea": 12.27,
                     "Spain": 2.97,
                     "France": 5.98,
                     "Switzerland": 4.53}

    # Median ages of population in different countries
    median_age = {"Germany": 47.1,
                   "Italy": 45.5,
                   "China": 37.4,
                   "South Korea": 41.8,
                   "Spain": 42.7,
                   "France": 41.4,
                   "Switzerland": 42.4}

    last_confirmed = {key: values["Confirmed"][-1] * inv_inhabitants[key] for key, values in data.items()}
    tuple_dict = {key: (hospital_beds[key], median_age[key], last_confirmed[key]) for key in hospital_beds.keys()}

    # Funny "bubble" plot
    plot_3d_bubbles(axes[1][2], tuple_dict,
                    x_label="# hospital beds / 1,000 inhabitants",
                    y_label="population's median age", title="# Confirmed cases / 100,000 inhabitants")

    fig.tight_layout()
    fig.savefig("plot.png")
    plt.close(fig)


def main():
    """
    This is used as the entry point for ml-analysis.
    Read optional command line arguments and launch the analysis.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("data_path",
                        help="top directory of WHO data", default="./COVID-19/")
    args = parser.parse_args()


    run_analysis(args.data_path)    
