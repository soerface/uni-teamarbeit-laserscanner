#!/usr/bin/env python2

import os
from pprint import pprint
import re
import numpy as np


def get_data():
    current_path = os.path.realpath(__file__)
    current_directory = os.path.dirname(current_path)
    data_directory = os.path.join(current_directory, 'data')

    result = {}
    for filename in os.listdir(data_directory):
        match = re.match(r'^(\d*)_\d\.csv$', filename)
        if match:
            x = []
            y = []
            with open(os.path.join(data_directory, filename)) as f:
                    for line in f:
                        x_value, y_value = line.split(',')
                        try:
                            x_value = float(x_value)
                            y_value = float(y_value)
                        except ValueError:
                            continue
                        x.append(x_value)
                        y.append(y_value)
            sample = {
                'x': x,
                'y': y,
            }
            result.setdefault(match.group(1), []).append(sample)
    return result


if __name__ == '__main__':
    data = get_data()
    
    for name, samples in data.iteritems():
        pprint(name)
        pprint(samples)

        x = []
        y = []
        for sample in samples:
            x.append(sample['x'])
            y.append(sample['y'])
            
        for tupel in zip(*x):
            print np.mean(tupel)
            
        for tupel in zip(*y):
            print np.mean(tupel)    
