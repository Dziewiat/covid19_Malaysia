import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation


def plot_bar_map(df, column, title, output, reduction):
    '''Plot Malaysia map with animated bars showing a value.'''
    # Load data
    groups = df.groupby([df['date'].str[:7], df['state']])[column].last().unstack(1)

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
            label.set_text(val)

        # Update date
        date.set_text('date: '+data.name)

        return bars

    # Generate and save animation
    ani = FuncAnimation(fig=fig, func=update, frames=(len(groups)+4)//2, interval=300)
    ani.save(output, writer='imagemagick', dpi=300)


if __name__ == '__main__':

    filepath = '../data/cases_state.csv'

    df = pd.read_csv(filepath)

    plot_bar_map(df, 'cases_active', 'Active cases', '../figures/region_active_cases.gif', 500)