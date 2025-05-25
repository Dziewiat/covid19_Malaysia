import pandas as pd
from mikolaj_utils import plot_bar_map

if __name__ == '__main__':
    filepath = '../data/deaths_state.csv'

    df = pd.read_csv(filepath)

    plot_bar_map(df, 'deaths_new', 'New deaths caused by COVID', '../figures/region_deaths_map.gif', 10)
