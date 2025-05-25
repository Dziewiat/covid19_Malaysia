import imageio
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time

start = time.time()


#import data
main_folder = Path.cwd().parent.parent

data_folder = main_folder / 'data/Norbert'
plots_folder = main_folder / 'Plots/Norbert'
nat_folder = main_folder / 'Plots/Norbert/nat'
scripts_folder = main_folder / 'scripts/Norbert'

# Clear the output folder before generating new plots
for file in nat_folder.glob("*"):
    if file.is_file():
        file.unlink()


nat_temp = pd.read_csv(data_folder/'vax_demog_nationality.csv', parse_dates = ['date'])
cols_to_drop = [col for col in nat_temp.columns if 'missing' in col]
cols_to_drop.append('state')
cols_to_drop.append('district')
nat_temp.drop(columns = cols_to_drop, inplace = True)
countries = ['malaysia', 'indonesia', 'bangladesh', 'myanmar', 'philippines']

cols_to_keep = ['date'] + [col for col in nat_temp.columns if any(f'full_{country}' in col for country in countries)]
nat_temp = nat_temp[cols_to_keep]
nat_temp = nat_temp.set_index('date')

#count values for each day
nat_grouped = nat_temp.groupby('date').sum()

#count cumulative sum
nat = nat_grouped.cumsum()

#divide all values by 1_000_000
nat = nat / 1_000_000
total_population = 35 #in millions


color_palette = plt.get_cmap('tab10')
base_colors = {}

loop_counter = 0
max_ylimit = nat.max().max()
for idx in nat.index:
    row_data = nat.loc[idx]

    country_keys = {country: [k for k in row_data.index if f'_{country}' in k] for country in countries}
    country_values = {country : row_data[keys].values for country, keys in country_keys.items()}



    spacing=0.3
    countries_x = {
        country: (np.arange(len(keys)) + offset) * spacing
        for offset, (country, keys) in enumerate(country_values.items())}

    x_all = np.concatenate(list(countries_x.values()))
    y_all = np.concatenate(list(country_values.values()))
    # labels = list(country_keys.values()) + list(country_values.values())
    labels = [label for keys in country_keys.values() for label in keys]

    base_names = [label.replace('full_', '') for label in labels]
    unique_bases = sorted(set(base_names))
    color_palette = plt.get_cmap('tab10')
    base_colors = {base: color_palette(i) for i, base in enumerate(unique_bases)}
    bar_colors = [base_colors[base] for base in base_names]

    plt.figure(figsize = (10, 5))
    plt.ylim(0, max_ylimit*1.1)
    plt.bar(x_all, y_all, width=0.25, color = bar_colors)
    for x, y in zip(x_all, y_all):
        percentage = ((y)/total_population) * 100
        plt.text(x, y+max_ylimit * 0.01, f'{percentage:.1f}%', ha='center', va='bottom', fontsize = 8)

    plt.xticks(ticks = x_all, labels = labels, rotation = 45)
    plt.ylabel('People in millions')
    plt.title(f'Vaccination by nationality in {idx.year}-{idx.month:02d}-{idx.day:02d}')
    plt.tight_layout()

    filename = f'vaccination_nat_{idx.year}-{idx.month:02d}-{idx.day:02d}.png'
    plt.savefig(nat_folder / filename)

    plt.close()
    end = time.time()
    print(f'{loop_counter}th loop. Time since program start: {end - start:.2f} seconds')
    loop_counter += 1

image_files = sorted(nat_folder.glob("vaccination_nat_*.png"))

resized_images = [np.array(Image.open(img).resize((800, 400))) for img in image_files]
imageio.mimsave(plots_folder/'vaccination_nat.gif', resized_images, duration=0.5)
