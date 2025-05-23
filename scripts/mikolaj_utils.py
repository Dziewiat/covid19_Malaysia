import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation

import plotly.graph_objs as go
from plotly.subplots import make_subplots


def plot_bar_map(df, column, title, output, reduction, thousands=False):
    '''Plot Malaysia map with animated bars showing a value.'''
    # Load data
    groups = df.groupby([df['date'].str[:7], df['state']])[column].sum().unstack(1)

    fig, ax = plt.subplots(1,1)
    fig.set_tight_layout(True)
    
    # Load and crop image
    map = mpimg.imread('../data/map.jpg', format='jpg')
    map = map[map[:,0,0] != 0]

    ax.imshow(map)
    ax.set_axis_off()
    ax.set_title(f'{title} through the years 2020-2022', weight='bold', va='bottom')

    regions = ['Johor','Melaka','Negeri Sembilan','W.P. Putrajaya',
               'Selangor','Perak','Pulau Pinang','Kedah','Perlis',
               'Kelantan','Terengganu','Pahang','Sarawak','Sabah']

    region_locs = [
        (350,420),  # Johor
        (260,395),  # Melaka
        (240,360),  # Negeri sembilan
        (210,355),  # Putrajaya
        (195,310),  # Selangor
        (160,220),  # Perak
        (100,150),  # Pulau Pinang
        (135,115),  # Kedah
        (105,55),   # Perlis
        (240,160),  # Kelantan
        (335,190),  # Terengganu
        (280,280),  # Pahang
        (740,240),  # Sarawak
        (905,100)   # Sabah
    ]

    # Add bars
    bars = []
    for region, loc in zip(regions, region_locs):
        bar = Rectangle(loc, 10, 50, linewidth=0.5, edgecolor='0', facecolor='0.5', angle=180)
        ax.add_patch(bar)
        bars.append(bar)

    # Add date
    date = ax.text(500, 120, '', size=8, weight='bold')

    # Country labels
    labels = [ax.text(bar.get_x() - bar.get_width() / 2,
                      50, region, ha='center',
                      va='bottom', fontsize=5,
                      weight='bold') for bar, region in zip(bars, regions)]

    # Update frame function
    def update(frame):
        data = groups.iloc[frame]

        # Update bar heights
        for bar, region, label in zip(bars, regions, labels):
            val = data[region]
            bar.set_height(val / reduction)

            label.set_y(bar.get_y() - val / reduction - 10)
            txt = f'{val//1000}k' if thousands else val
            label.set_text(txt)

        # Update date
        date.set_text('date: '+data.name)

        return bars

    # Generate and save animation
    ani = FuncAnimation(fig=fig, func=update, frames=(len(groups)+4)//2, interval=300)
    ani.save(output, writer='imagemagick', dpi=300)


def plot_interactive_piechart(df, column, output, title):
    ''''''
    groups = df.groupby([df['date'].str[:7], df['state']])[column].sum().reset_index()

    # Create pie chart data for each month
    fig = go.Figure()

    months = groups.date.unique()

    for i, month in enumerate(months):
        month_data = groups[groups['date'] == month]
        fig.add_trace(go.Pie(
            labels=month_data['state'],
            values=month_data[column],
            name=month,
            visible=(i == 0)  # Only the first month's pie is visible initially
        ))

    # Slider steps
    steps = []
    for i, month in enumerate(months):
        step = dict(
            method='update',
            args=[
                {'visible': [j == i for j in range(len(months))]},
                {'title': {
                    'text': f'{title} for {month} (n_total = {groups[groups["date"] == month][column].sum()})',
                    'x': 0.1,
                    'y': 0.9,
                    'xanchor': 'left'
                }}
            ],
            label=month
        )
        steps.append(step)

    # Slider layout
    sliders = [dict(
        active=0,
        pad={"t": 50},
        steps=steps
    )]

    fig.update_layout(
        title={
            'text': f'{title} for 2020-01\nn_total = ...',
            'x': 0.1,
            'y': 0.9,
            'xanchor': 'left'
        },
        sliders=sliders
    )

    fig.write_html(output)


if __name__ == '__main__':

    filepath = '../data/cases_state.csv'

    df = pd.read_csv(filepath)

    plot_interactive_piechart(df, 'cases_active', '../figures/test.html', 'test')