#!/usr/bin/env python2

from datetime import datetime
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
                for i, line in enumerate(f):
                    try:
                        x_value, y_value = line.split(',')
                    except ValueError:
                        print 'Invalid line %d in file "%s": %s' % (i+1, filename, line)
                        if not line:
                            print 'remove trailing (empty) lines'
                        continue
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

def write_to_file(name, angle, velocity):
	timestamp = datetime.now().strftime('%Y-%m-%d')
	directory = os.path.join('results', timestamp)
	if not os.path.exists(directory):
		os.makedirs(directory)
	filename = '%s.csv' % name
	with open(os.path.join(directory, filename), 'w') as f:
		f.writelines([
		'winkel,geschwindigkeit\n',
		'%f,%f' % (angle, velocity)
		])

def mean_curve(samples):
    x = []
    y = []
    
    max_x_len = 0
    max_y_len = 0

    #copy samples in lists and determine max x and y list-length
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
    #calculate mean values
    for tupel in zip(*x):
        l = [xi for xi in tupel if xi is not None]
        x_result.append(np.mean(l))
        
    for tupel in zip(*y):
        l = [yi for yi in tupel if yi is not None]
        y_result.append(np.mean(l))

    return {'x': x_result, 'y': y_result}

if __name__ == '__main__':
    #get data from files
    data = get_data()
    
    #for each power calculate mean curve
    curves = {}
    for i, dat in enumerate(data.iteritems()):
        name, samples = dat
        curves[name] = mean_curve(samples)

    for name, curve in curves.iteritems():
        #calculate koefficients for each power
        koeff = np.polyfit(curve['x'], curve['y'], 2)
    
        #quadratic approximation
        p = np.poly1d(koeff)
        #derivative of p
        pd = p.deriv()

        distance = np.roots(p)[0]
        root = np.roots(p)[1]
        slope = pd(root)
        angle = np.arctan(slope)
        velocity = np.sqrt((distance * 9.81) / np.sin(2 * angle))

        print "%s:" % name
        #print "Nullstellen:", root
        #print "Steigung:   ", slope
        print "Winkel.:    ", angle
        print "Geschw.:    ", velocity
        print
        write_to_file(name, angle, velocity)
