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
            print(f'File: {file}')
            config_name = file.split('_Inst_')[0]
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
            cc_results = config_cores.get(cores, [])
            filename = os.path.join(subdir, file)
            with open(filename) as f:
                j_file = json.load(f)
                elapsed_time = j_file['Algorithm']['Elapsed Time']
                cc_results.append(elapsed_time)
                config_cores[cores] = cc_results
                configs[config_name] = config_cores

        pp(configs)

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
    df_results = parse_files(path)
    df_results.to_csv(f'Scalability_{size}.csv')
    to_speed_up_plot(df_results, size)
