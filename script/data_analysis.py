#!/usr/bin/python3

from os import listdir
import numpy as np
import argparse
import re
import json
from pprint import pprint as pp
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing


DYNAMIC = 'Dynamic'
DP = ".DP"
JSON = ".json"
DP_PATH = ''
DIFF = 'Avg. difference with optimal'
RATIO = 'Ratio Avg Objective / Avg Elapsed Time'
AVG_TIME = 'Average Elapsed Time (s)'
AVG_OBJS = 'Average Objective'
CONFIG = 'Configuration'


def parse_files(path, pattern, verbose=True):
    # Parseamos cada fichero de resultados
    dp_file = f'{DP_PATH}/{pattern}{DP}'
    optimal = 0
    dp_time = 0
    with open(dp_file) as file:
        optimal = float(file.readline())
        dp_time = float(file.readline())
        print(f'Optimal = {optimal} in {dp_time}s')

    dp_ratio = optimal / dp_time

    inst_regex = rf'.*{pattern}\.kp\w+{JSON}'
    configs = {}
    for file in listdir(path):
        # Buscamos todos los ficheros de resultados para la instancia concreta
        if re.match(inst_regex, file):
            key = file[:file.find('Inst') - 1]
            group = configs.get(key, [])
            with open(f'{path}/{file}') as f:
                j_file = json.load(f)
            objectives = j_file['Results']['Objectives']
            elapsed_time = j_file['Name']['Elapsed Time']
            # Nos quedamos con el mejor resultado obtenido
            group.append((max(objectives), elapsed_time))
            configs[key] = group

    results = {}
    for key in configs:
        avg = np.average(configs[key], axis=0)
        diff_with_optimal = optimal - avg[0]
        results[key] = [avg[0], avg[1], diff_with_optimal]

    results[DYNAMIC] = [optimal, dp_time, dp_ratio]
    df = pd.DataFrame.from_dict(results, orient='index',
                                columns=[AVG_OBJS, AVG_TIME, DIFF])
    df.index.name = CONFIG
    print(df)
    return df


def to_plot(results, title):
    min_max_scaler = preprocessing.MinMaxScaler()
    ratio_scaled = min_max_scaler.fit_transform(results[[RATIO]])
    results['norm_ratio'] = ratio_scaled
    results.plot(kind='bar', y='norm_ratio')
    print(results['norm_ratio'])
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data analysis')
    parser.add_argument(
        'path', type=str, help='Path to find the .json result files')
    parser.add_argument('dp_path', type=str,
                        help='Path to find the DP results')
    parser.add_argument('-p', '--patterns', nargs='+',
                        help='<Required> Instance patterns', required=True)

    args = parser.parse_args()
    path = args.path
    DP_PATH = args.dp_path
    patterns = args.patterns
    for pattern in patterns:
        df_results = parse_files(path, pattern)
        df_results.to_csv(f'{pattern}.csv')
        #to_plot(df_results, pattern)
