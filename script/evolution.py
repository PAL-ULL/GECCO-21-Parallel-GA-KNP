#!/usr/bin/python3

from os import listdir
import numpy as np
import argparse
import re
import json
from pprint import pprint as pp
import matplotlib.pyplot as plt
import pandas as pd

JSON = ".json"
GA_PATH = '/home/amarrero/Proyectos/CEC-2021-Parallel-GA-KNP/results/Preliminar/'
EVOLUTION = 'Evolution'
CORES = 'num_of_cores'
SPEEDUP = 'speedup'


def parse_files(path, verbose=True):
    configs = {}
    for file in listdir(path):
        key = file.split('_')[8]
        group = configs.get(key, [])
        with open(f'{path}/{file}') as f:
            j_file = json.load(f)
            evolution = j_file[EVOLUTION]
            group.append(evolution)
            configs[key] = group

    results = {}
    # Aprovechamos para calcular el speedup
    for key in configs:
        avg_evolution = np.average(configs[key], axis=0)
        results[key] = [avg_evolution]

    df = pd.DataFrame.from_dict(results, orient='index',
                                columns=['avg_evolution'])
    df.index.name = 'Config'
    #unpacked_df = pd.DataFrame(df['avg_evolution'].to_list(), index=df.index)
    #print(unpacked_df)
    return df

def to_evolution_plot(df_results, size):
    xs = np.arange(0, 342)
    xs = np.interp(xs, (xs.min(), xs.max()), (0, 500000))
    for index, row in df_results.iterrows():
        plt.plot(xs, row['avg_evolution'], label=index)
    plt.title(f'Avg. Objective Evolution N={size} instances')
    plt.ylabel('Avg. Objective')
    plt.xlabel('Evaluations')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    sizes = [50, 100, 500, 1000]
    path = "/home/amarrero"
    types = [
        'InverserCorrelated',
        'SpannerStronglyCorrelated',
        'StronglyCorrelated',
        'Uncorrelated',
        'SubsetSum'
        ]
    for size in sizes:
        directory = f'{path}/{size}/'
        df_results = parse_files(directory)
        df_results.to_csv(f'Evolution_{size}.csv')
        to_evolution_plot(df_results, size)