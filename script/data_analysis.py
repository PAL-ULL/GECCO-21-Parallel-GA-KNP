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
EVOLUTION = 'evolution'
TIME = 'average_elapsed_time'
OBJECTIVES = 'average_best_objective'
DIFF = 'diff_with_optimal'
CHECKPOINTS = 'checkpoints'


def parse_files(path, pattern, verbose=True):
    # Parseamos cada fichero de resultados
    dp_file = f'{DP_PATH}/{pattern}{DP}'
    optimal = 0
    dp_time = 0
    if(verbose):
        print(f'Openning DP results: {dp_file}')
    with open(dp_file) as file:
        optimal = float(file.readline())
        dp_time = float(file.readline())
        print(f'Optimal = {optimal} in {dp_time}s')

    inst_regex = rf'.*{pattern}\.kp_AVG_{JSON}'
    configs = {}
    configs[DYNAMIC] = {
        TIME: dp_time,
        OBJECTIVES: optimal,
        DIFF: 0
    }
    for file in listdir(path):
        # Buscamos todos los ficheros de resultados para la instancia concreta
        if re.match(inst_regex, file):
            key = file[:file.find('Inst') - 1]
            with open(f'{path}/{file}') as f:
                j_file = json.load(f)

            avg_objectives = j_file['Average Objective']
            avg_elapsed_time = j_file["Average Elapsed Time (s)"]
            avg_evolution = np.asarray(j_file['Average Evolution'])
            checkpoints, avg_evolution = avg_evolution.T

            diff_with_optimal = optimal - avg_objectives
            # Nos quedamos con el mejor resultado obtenido
            configs[key] = {
                EVOLUTION: avg_evolution,
                CHECKPOINTS: checkpoints,
                TIME: avg_elapsed_time,
                OBJECTIVES: avg_objectives,
                DIFF: diff_with_optimal
            }
            if(verbose):
                print(f'Resume of {key}\n')
                print(f'\t-Avg. objective: {configs[key][OBJECTIVES]}')
                print(f'\t-Avg. elapsed time: {configs[key][TIME]}')
                print(f'\t-Avg. diff with optimal: {configs[key][DIFF]}\n\n')

    return configs


def plot_objs_evolution(configs, title, machine):
    plt.figure(figsize=(12, 8))
    plt.title(title)
    for key in configs.keys():
        if key != DYNAMIC and 'OMP' not in key:
            plt.plot(configs[key][CHECKPOINTS],
                     configs[key][EVOLUTION], label=key)

    plt.ylabel(OBJECTIVES)
    plt.xlabel(CHECKPOINTS)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'{title}_{machine}.png')
    plt.clf()


def to_csv(configs, pattern, machine):
    header = f'{CONFIG},{OBJECTIVES},{TIME},{DIFF}\n'
    with open(f'{pattern}_{machine}.csv', 'w') as csv_file:
        csv_file.write(header)
        for key in configs.keys():
            line = f'{key},{configs[key][OBJECTIVES]},{configs[key][TIME]},{configs[key][DIFF]}\n'
            csv_file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Data analysis')
    parser.add_argument(
        'path', type=str, help='Path to find the .json result files')
    parser.add_argument('dp_path', type=str,
                        help='Path to find the DP results')
    parser.add_argument('machine', type=str,
                        help='Computer where the experiment was executed')
    parser.add_argument('-p', '--patterns', nargs='+',
                        help='<Required> Instance patterns', required=True)

    args = parser.parse_args()
    path = args.path
    DP_PATH = args.dp_path
    patterns = args.patterns
    for pattern in patterns:
        configs = parse_files(path, pattern)
        plot_objs_evolution(configs, pattern, args.machine)
        to_csv(configs, pattern, args.machine)
