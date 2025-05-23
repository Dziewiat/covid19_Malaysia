import pandas as pd
from scripts.mikolaj_utils import plot_bar_map

if __name__ == '__main__':
    filepath = '../data/cases_state.csv'

    df = pd.read_csv(filepath)

    plot_bar_map(df, 'cases_active', 'Active COVID cases', '../figures/region_active_cases_map.gif', 500)