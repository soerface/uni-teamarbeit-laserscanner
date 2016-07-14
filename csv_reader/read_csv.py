#!/usr/bin/env python2

import os
import re
import numpy as np
from matplotlib import pyplot as plt


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


def mean_curve(samples):
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
        
        #plt.plot(sample['x'], sample['y'])
        
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
        l = [xi for xi in tupel if xi is not None]
        x_result.append(np.mean(l))
        
    for tupel in zip(*y):
        l = [yi for yi in tupel if yi is not None]
        y_result.append(np.mean(l))
    
    #print result for each power  
    #print '%s, x: %s' % (name, x_result)
    #print '%s, y: %s' % (name, y_result)
    
    return {'x': x_result, 'y': y_result}
    

#plot for power
def plot_curves(samples, curve, name):
    
    plt.subplot(len(data), 1, i+1)
    plt.xlabel('width')
    plt.ylabel('height')
    plt.title(name)
    
    for sample in samples:
        plt.plot(sample['x'], sample['y'])
        
    plt.scatter(curve['x'], curve['y'])
    
    plt.tight_layout()
    plt.show()
    
def interpolate(curve):
    koeff = np.polyfit(curve['x'], curve['y'], 2)
    return koeff

if __name__ == '__main__':
    data = get_data()
    
    #for each power
    curves = {}
    for i, dat in enumerate(data.iteritems()):
        name, samples = dat
        
        curves[name] = mean_curve(samples)
        
        #plot current power
        plot_curves(samples, curves[name], name)

    #for each curve calculate initial angle and velocity
    interps = {}
    for name, curve in curves.iteritems():
        interps[name] = interpolate(curve)
        
    k2, k1, k0 = interps['1500']
    x_values = np.linspace(0, 9, 20)
    y_values = map(lambda x: k2*x**2 + k1*x + k0, x_values)
    plt.plot(x_values, y_values)