#!/usr/bin/env python2

import os
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
    
    #for each power
    for name, samples in data.iteritems():
        #list of lists
        x = []
        y = []
        
        max_x_len = 0
        max_y_len = 0
        #for each shot
        for sample in samples:
            x.append(sample['x'])
            max_x_len = max(len(sample['x']), max_x_len)
            y.append(sample['y'])
            max_y_len = max(len(sample['y']), max_y_len)
            
        #bring lists in x,y to same length
        for sample in x:
            a = [None] * (max_x_len - len(sample))
            sample.extend(a)
            
        for sample in y:
            a = [None] * (max_y_len - len(sample))
            sample.extend(a)
        
        x_result = []
        y_result = []
        #match first, second, ... to one list
        for tupel in zip(*x):
            l = [x for x in tupel if x is not None]
            x_result.append(np.mean(l))
            
        for tupel in zip(*y):
            l = [y for y in tupel if y is not None]
            y_result.append(np.mean(l))
        
        #print result for each power  
        print '%s, x: %s' % (name, x_result)
        print '%s, y: %s' % (name, y_result)
            
            
            
            
            
            
            
            
            
            
            
            
            
