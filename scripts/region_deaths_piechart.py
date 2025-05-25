import pandas as pd
from mikolaj_utils import plot_interactive_piechart

if __name__ == '__main__':

    filepath = '../data/deaths_state.csv'

    df = pd.read_csv(filepath)

    plot_interactive_piechart(df, 'deaths_new', '../figures/region_deaths_piechart.html', 'Deaths caused by COVID')