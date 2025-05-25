import pandas as pd
from mikolaj_utils import plot_interactive_piechart

if __name__ == '__main__':

    filepath = '../data/cases_state.csv'

    df = pd.read_csv(filepath)

    plot_interactive_piechart(df, 'cases_active', '../figures/region_active_cases_piechart.html', 'Active COVID cases')