import imageio
import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import time


#import data
main_folder = Path.cwd().parent.parent

data_folder = main_folder / 'data/Norbert'
plots_folder = main_folder / 'Plots/Norbert'
sex_folder = main_folder / 'Plots/Norbert/sex'
scripts_folder = main_folder / 'scripts/Norbert'

# Clear the output folder before generating new plots
for file in sex_folder.glob("*"):
    if file.is_file():
        file.unlink()

sex_temp = pd.read_csv(data_folder / 'vax_demog_sex.csv', parse_dates = ['date'])
sex_temp.drop(columns = ['state', 'district', 'partial_missing', 'full_missing', 'booster_missing', 'booster2_missing'], inplace = True)
sex_temp = sex_temp.set_index('date')

#count values for each day
sex = sex_temp.groupby('date').sum()
sex = sex.cumsum()



#divide all values by 1_000_000
sex = sex / 1_000_000
total_population = 35 #in millions


color_palette = plt.get_cmap('tab10')
base_colors = {}

start = time.time()
loop_counter = 0
max_ylimit = sex.max().max()
for idx in sex.index:
    row_data = sex.loc[idx]

    male_keys = [k for k in row_data.index if '_male' in k]
    female_keys = [k for k in row_data.index if '_female' in k]

    base_names = [k.replace("_female", "").replace("_male", '') for k in female_keys]

    for i, base in enumerate(base_names):
        base_colors[base] = color_palette(i)

    male_values = row_data[male_keys].values
    female_values = row_data[female_keys].values

    spacing=0.3
    male_x = np.arange(len(male_keys)) * spacing
    female_x = (np.arange(len(female_keys)) + len(male_keys) + 1) * spacing

    x_all = np.concatenate([male_x, female_x])
    y_all = np.concatenate([male_values, female_values])
    labels = male_keys + female_keys

    bar_colors = []
    for key in male_keys + female_keys:
        base = key.replace('_female', '').replace('_male', '')
        bar_colors.append(base_colors[base])

    plt.figure(figsize = (10, 5))
    plt.ylim(0, max_ylimit*1.1)
    plt.bar(x_all, y_all, width=0.25, color = bar_colors)
    for x, y in zip(x_all, y_all):
        percentage = ((y)/total_population) * 100
        plt.text(x, y+max_ylimit * 0.01, f'{percentage:.1f}%', ha='center', va='bottom', fontsize = 8)

    plt.xticks(ticks = x_all, labels = labels, rotation = 45)
    plt.ylabel('People in millions')
    plt.title(f'Vaccination by sex in {idx.year}-{idx.month:02d}-{idx.day:02d}')
    plt.tight_layout()

    filename = f'vaccination_sex_{idx.year}-{idx.month:02d}-{idx.day:02d}.png'
    plt.savefig(sex_folder / filename)
    end = time.time()
    print(f'{loop_counter}th loop. Time since program start: {end - start:.2f} seconds')
    loop_counter += 1
    plt.close()


image_files = sorted(sex_folder.glob("vaccination_sex_*.png"))

resized_images = [np.array(Image.open(img).resize((800, 400))) for img in image_files]
imageio.mimsave(plots_folder/'vaccination_sex.gif', resized_images, duration=0.5)

