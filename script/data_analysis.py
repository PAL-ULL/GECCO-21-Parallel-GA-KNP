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
DP_PATH = '/home/amarrero/Proyectos/CEC-2021-Parallel-GA-KNP/results/DynamicProgramming'
GA_PATH = '/home/amarrero/Proyectos/CEC-2021-Parallel-GA-KNP/results/Preliminar/'
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
        ratio = avg[0] / avg[1]
        results[key] = [avg[0], avg[1], ratio]

    results[DYNAMIC] = [optimal, dp_time, dp_ratio]
    df = pd.DataFrame.from_dict(results, orient='index',
                                columns=[AVG_OBJS, AVG_TIME, RATIO])
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
    path = "/home/amarrero/Proyectos/CEC-2021-Parallel-GA-KNP/results/Preliminar/SpannerStronglyCorrelated/"
    patterns = ["SpannerStronglyCorrelated_N_50_R_100_0", "SpannerStronglyCorrelated_N_100_R_100_0",
                "SpannerStronglyCorrelated_N_500_R_100_0", "SpannerStronglyCorrelated_N_1000_R_100_0"]

    for pattern in patterns:
        df_results = parse_files(path, pattern)
        df_results.to_csv(f'{pattern}.csv')
        to_plot(df_results, pattern)
