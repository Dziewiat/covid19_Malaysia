import pandas as pd
from mikolaj_utils import plot_interactive_piechart

if __name__ == '__main__':

    filepath = '../data/vax_state.csv'

    df = pd.read_csv(filepath)

    plot_interactive_piechart(df, 'daily', '../figures/region_vaxinations_piechart.html', 'New COVID vaxinations')
    