#!/usr/bin/python3
import os
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


def parse_files(rootdir, verbose=True):
    configs = {}
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if not file.endswith('_AVG_.json'):
                continue

            config_name = file.split('_Inst_')[0]
            config_name = config_name[: config_name.rfind('0_')]
            config_cores = configs.get(config_name, {})
            print(f'Configuration: {config_name}')
            cores = 1
            # En caso de ser una instancia secuencial
            if(file.find('SEQ') != -1):
                cores = 1
            else:
                key = file[file.find('OMP') + 4: file.find('Inst') - 1]
                cores = int(key)

            # Los resultados de la configuracion para el numero de cores especifico
            filename = os.path.join(subdir, file)
            with open(filename) as f:
                j_file = json.load(f)
                elapsed_time = j_file['Average Elapsed Time (s)']
                config_cores[cores] = elapsed_time
                configs[config_name] = config_cores

    df = pd.DataFrame.from_dict(configs, orient='index')
    df = df.reindex(sorted(df.columns), axis=1)
    print(df)
    return df


def to_speed_up_plot(df_results, instance):
    for index, row in df_results.iterrows():
        seq_time = row[1]
        for column in df_results:
            df_results.loc[index, column] = seq_time / \
                df_results.loc[index, column]

    print(df_results)
    plt.figure(figsize=(12, 8))
    ticks = df_results.columns.values.tolist()
    for index, _ in df_results.iterrows():
        data = df_results.loc[index].values.tolist()
        plt.plot(ticks, data, linestyle='-.', marker='o', label=index)

    plt.title(f'Speed-up for N-1000 {instance}')
    plt.ylabel('Speed-up')
    plt.xticks(ticks)
    plt.legend()
    plt.savefig(f'Speed-up_{instance}.png')
    plt.clf()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Scalability')
    parser.add_argument(
        'path', type=str, help='Path to find the .json result files')

    args = parser.parse_args()
    rootdir = args.path
    for subdir, dirs, _ in os.walk(rootdir):
        for directory in dirs:
            full_path = os.path.join(subdir, directory)
            print(f'Directory {full_path}')
            df_results = parse_files(full_path)
            df_results.to_csv(f'Scalability_{directory}.csv')
            to_speed_up_plot(df_results, directory)
