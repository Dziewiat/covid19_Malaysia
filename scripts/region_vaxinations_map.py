import pandas as pd
from mikolaj_utils import plot_bar_map

if __name__ == '__main__':
    filepath = '../data/vax_state.csv'

    df = pd.read_csv(filepath)

    plot_bar_map(df, 'daily', 'COVID vaxinations', '../figures/region_vaxinations_map.gif', 15000, thousands=True)
    