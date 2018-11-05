import numpy as np
import pandas as pd
import sys
import glob
import os.path
import csv
import datetime

class Symbolization(object):
    def __init__(self, column_names,thresholds,label):
        """
        column_names = ['hoge','huga'] : columns using process

        thresholds = [[-3,0,2,3.5],[2,10]] :  sorted list!!!

        label = -1

        """
        self.columns = column_names
        self.thresholds = thresholds
        self.label = label

    def symbolize(self,dataframe):
        """
        return ['1:3:4','3:3:1','1:1:2',.....]
        """

        sequence = []

        for _index, row in dataframe.iterrows():
            is_first = True
            item = ''
            if not(self.label == False):
                sequence.append(str(self.label))
            for i, j in zip(self.columns, self.thresholds):
                symbol = 0
                for k in j:
                    if row[i] < k:
                        if is_first:
                            item += str(symbol)
                            is_first = False
                        else:
                            item += ':' + str(symbol)
                        break
                    else:
                        symbol += 1
                else:
                    if is_first:
                        item += str(symbol)
                        is_first = False
                    else:
                        item += ':' + str(symbol)
            else:
                sequence.append(item)

        return sequence

    def symbolize_trajectories(self,trajectories_path, save_path):
        """
        trajectories_path = 'hoge/trajectories/'

        save_path = 'hoge/maps/'
        """

        files = glob.glob(trajectories_path + '*')
        files.sort()
        save_for = save_path + 'sequence_' + '{0:%y%m%d%H%M}'.format(datetime.datetime.now()) + '.csv'

        sequences = []
        # for all data
        for i in files:
            print(i)
            file_extension = i.split('.')[-1]
            # load data
            if file_extension == 'tsv':
                # delete all rows which has NaN
                df = pd.read_table(i)
                df = df.loc[:,self.columns].dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i)
                df = df.loc[:,self.columns].dropna()
            else:
                continue
            sequences.append(self.symbolize(df))
        
        # save for csv file
        f = open(save_for, 'w')
        writer = csv.writer(f,delimiter=' ',lineterminator='\n')
        writer.writerows(sequences)
        f.close()
