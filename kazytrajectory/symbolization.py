import numpy as np
import pandas as pd
import sys
import glob
import os.path

class Symbolization(object):
    def __init__(self):
        pass

    def symbolize(self,dataframe,column_names,thresholds):
        """
        columns_names = ['hoge','fuga']

        thresholds = [[-3,0,2,3.5],[2,10]] :  sorted list!!!

        return ['1:3:4','3:3:1','1:1:2',.....]
        """

        sequence = []

        for index, row in dataframe.iterrows():
            is_first = True
            item = ''
            for i, j in zip(column_names, thresholds):
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

    # def symbolize_trajectories(self,trajectories_path, save_path):
    #     """
    #     trajectories_path = 'hoge/trajectories/'

    #     save_path = 'hoge/maps/'
    #     """

    #     files = glob.glob(trajectories_path + '*')

    #     # for all data
    #     for i in files:
    #         print(i)
    #         file_extension = i.split('.')[-1] 
    #         # load data
    #         if file_extension == 'tsv':
    #             # delete all rows which has NaN
    #             df = pd.read_table(i,header=1)
    #             df = df.loc[:,[self.lat_name,self.long_name]].dropna()
    #         elif file_extension == 'csv':
    #             # delete all rows which has NaN
    #             df = pd.read_csv(i,header=1)
    #             df = df.loc[:,[self.lat_name,self.long_name]].dropna()
    #         else:
    #             continue
            
    #         save_for = save_path + os.path.splitext(i.split('/')[-1])[0] + '.html'
    #         self.drow_map([df[self.lat_name], df[self.long_name]], save_for)
