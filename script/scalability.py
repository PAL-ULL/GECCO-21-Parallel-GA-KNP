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
AVG_TIME = 'Average Elapsed Time (s)'
CORES = 'num_of_cores'
SPEEDUP = 'speedup'


def parse_files(path, verbose=True):
    configs = {}
    for file in listdir(path):
        cores = 1
        # En caso de ser una instancia secuencial
        if(file.find('SEQ') != -1):
            cores = 1
        else:
            key = file[file.find('OMP') + 4: file.find('Inst') - 1]
            cores = int(key)
        group = configs.get(cores, [])
        with open(f'{path}/{file}') as f:
            j_file = json.load(f)
            elapsed_time = j_file['Algorithm']['Elapsed Time']
            group.append(elapsed_time)
            configs[cores] = group

    results = {}
    avg_seq_time = np.average(configs[1], axis=0)
    # Aprovechamos para calcular el speedup
    for cores in configs:
        if cores == 1:
            results[cores] = [avg_seq_time, 1]
        else:
            avg = np.average(configs[cores], axis=0)
            cores_speedup = avg_seq_time / avg
            results[cores] = [avg, cores_speedup]

    df = pd.DataFrame.from_dict(results, orient='index',
                                columns=[AVG_TIME, SPEEDUP])
    df.index.name = CORES
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)
    print(df)
    return df


def to_speed_up_plot(df_results, size):
    df_results[SPEEDUP].plot(style='.-')
    plt.title(f'Speed-up for N={size} instances')
    plt.ylabel('Speed-up')
    plt.savefig(f'Speed-up_{size}.png')
    plt.clf()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scalability')
    parser.add_argument(
        'path', type=str, help='Path to find the .json result files')

    args = parser.parse_args()
    path = args.path
    sizes = [50, 100, 500, 1000]
    for size in sizes:
        directory = f'{path}/{size}'
        df_results = parse_files(directory)
        df_results.to_csv(f'Scalability_{size}.csv')
        to_speed_up_plot(df_results, size)
