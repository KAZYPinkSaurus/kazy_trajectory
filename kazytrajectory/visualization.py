import folium
import numpy as np
import pandas as pd
import sys
sys.path.append('..')
import glob
import os.path
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from kazytrajectory import symbolization


class Visualization(object):
    def __init__(self,name_lat_long=['latitude','longitude'],overlay= False):
        """
        name_lat_long = ['lat', 'long']

        I reference dataframe with name_lat_long

        (e.g. df['lat'], df['long'])

        overlay = false

        Whether all trajectories plot same map

        """
        self.lat_name = name_lat_long[0]
        self.long_name = name_lat_long[1]
        self.overlay = overlay

    def drow_map(self, location, save_path):
        """
        location = [df_lat, df_long]

        save_path = 'hoge/hogehoge.html'
        """

        location_list = np.array([location[0], location[1]])
        location_list = location_list.T.tolist()
        my_map = folium.Map(location_list[0], zoom_start=15)
        folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
        folium.Marker(location_list[0],popup='start',icon=folium.Icon(color='red',icon='star')).add_to(my_map)
        
        for lat_lon in location_list:
            folium.CircleMarker(lat_lon, radius=1, color='blue').add_to(my_map)
        else:
            folium.Marker(lat_lon, popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
        my_map.save(save_path)

    def __drow_maps_overlay(self, trajectory_files, save_path):
        """
        trajectry_files = [a.csv,b.csv.....]

        save_path = ./hoge/fuga.html
        """

        my_map = folium.Map()
        is_first_file = True

        for i in trajectory_files:
            print(i)
            file_extension = i.split('.')[-1] 
            # load data
            if file_extension == 'tsv':
                # delete all rows which has NaN
                df = pd.read_table(i)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            else:
                continue

            location_list = np.array([df[self.lat_name], df[self.long_name]])
            location_list = location_list.T.tolist()
            if is_first_file:
                my_map = folium.Map(location_list[0], zoom_start=15)
                is_first_file = False
            
            folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
            folium.Marker(location_list[0], popup='start', icon=folium.Icon(color='red', icon='star')).add_to(my_map)
            
            for lat_lon in location_list:   
                folium.CircleMarker(lat_lon, radius=1, color='blue').add_to(my_map)
            else:
                folium.Marker(lat_lon, popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
        
        my_map.save(save_path)
        

    def drow_maps(self, trajectories_path, save_path):
        """
        trajectories_path = 'hoge/trajectories/'

        save_path = 'hoge/maps/'
        """
        # data
        files = glob.glob(trajectories_path + '*')
        
        if self.overlay:
            save_for = save_path + 'all_plot_' + '{0:%y%m%d%H%M}'.format(datetime.datetime.now()) + '.html'
            self.__drow_maps_overlay(files, save_for)
            
        else:
            # for all data
            for i in files:
                print(i)
                file_extension = i.split('.')[-1] 
                # load data
                if file_extension == 'tsv':
                    # delete all rows which has NaN
                    df = pd.read_table(i)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                elif file_extension == 'csv':
                    # delete all rows which has NaN
                    df = pd.read_csv(i)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                else:
                    continue
                
                save_for = save_path + os.path.splitext(i.split('/')[-1])[0] + '.html'
                self.drow_map([df[self.lat_name], df[self.long_name]], save_for)

    def plot_coordinate(self, location, save_path):
        """
        location = [df_lat, df_long]

        save_path = 'hoge/hogehoge.html'
        """
        
        plt.figure()
        plt.plot(location[1], location[0],linewidth=0.1)
        plt.ylabel('latitude')
        plt.xlabel('longitude')
        plt.axis('scaled')
        plt.tick_params(labelsize=5)
        plt.savefig(save_path)
    
    def plot_coordinates(self, trajectories_path, save_path):
        """
        trajectories_path = 'hoge/trajectories/'

        save_path = 'hoge/maps/'
        """
        # data
        files = glob.glob(trajectories_path + '*')
        
        if self.overlay:
            save_for = save_path + 'all_plot_' + '{0:%y%m%d%H%M}'.format(datetime.datetime.now()) + '.eps'
            self.__plot_coordinates_overlay(files, save_for)
            
        else:
            # for all data
            for i in files:
                print(i)
                file_extension = i.split('.')[-1] 
                # load data
                if file_extension == 'tsv':
                    # delete all rows which has NaN
                    df = pd.read_table(i)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                elif file_extension == 'csv':
                    # delete all rows which has NaN
                    df = pd.read_csv(i)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                else:
                    continue
                
                save_for = save_path + os.path.splitext(i.split('/')[-1])[0] + '.eps'
                self.plot_coordinate([df[self.lat_name], df[self.long_name]], save_for)

    def __plot_coordinates_overlay(self, trajectory_files, save_path):
        """
        trajectry_files = [a.csv,b.csv.....]

        save_path = ./hoge/fuga.html
        """

        plt.figure()
        
        for i in trajectory_files:
            print(i)
            file_extension = i.split('.')[-1] 
            # load data
            if file_extension == 'tsv':
                # delete all rows which has NaN
                df = pd.read_table(i)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            else:
                continue

            plt.plot(df[self.long_name], df[self.lat_name], linewidth=0.1)
            
        plt.ylabel('latitude')
        plt.xlabel('longitude')
        plt.axis('scaled')
        plt.tick_params(labelsize=5)
        plt.savefig(save_path)            
            
    def plot_histgram(self, trajectories_path, column_names,_bins, save_path):
        """
        ディレクトリ内の系列データ(csv,tsv)の指定カラムのヒストグラム作成

        trajectories_path = 'hoge/trajectories/'

        column_names = ['speed','acceleration']

        save_path = 'hoge/'

        """
        # data
        files = glob.glob(trajectories_path + '*')

        df_all  = pd.DataFrame(columns=column_names)
        # for all data
        for i in files:
            print(i)
            file_extension = i.split('.')[-1] 
            # load data
            if file_extension == 'tsv':
                # delete all rows which has NaN
                df = pd.read_table(i)
                df = df.loc[:, column_names].dropna()
                df_all = pd.concat([df_all,df])
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i)
                df = df.loc[:, column_names].dropna()
                df_all = pd.concat([df_all,df])
            else:
                continue
        
        for j in column_names:
            plt.figure()
            plt.hist(df_all[j], bins=_bins)
            plt.title(j)
            save_for = save_path + 'hist_' + j + '{0:%y%m%d%H%M}'.format(datetime.datetime.now()) + '.eps' 
            plt.savefig(save_for)

    def highlight_patterns_on_map(self, df, patterns, column_names, thresholds, save_path, colors=['red', 'blue', 'green', 'black']):
        """
        df = dataframe

        patterns = ['1:1:1 0:1:2 2:3:1','1:1:1 0:1:2 2:3:1',.....] : left is higher priority. max:5 patterns. if you'd like to apply more, Please increase color list.  

        column_names = ['hoge','huga','kazy'] : only columns using symbolization

        thresholds = [[5, 40, 60], [-0.05, 0.05], [-0.01, 0.01]]

        save_path = 'hoge/maps/'

        colors = ['red', 'blue', 'green', 'black']
        """
        # reverse in order to take priority over left
        patterns.reverse()
        pattern_lengths = []

        for ptn in patterns:
            pattern_lengths.append(len(ptn.split(' ')))

        min_pattern_length = min(pattern_lengths)

        sbl = symbolization.Symbolization(column_names, thresholds, False)

        symbol_list = sbl.symbolize(df)
        symbol_list_length = len(symbol_list)

        # -1 means no mark
        marker_color_list = ['gray'] * symbol_list_length

        for i in range(symbol_list_length):
            if (i + min_pattern_length) > symbol_list_length:
                break
            else:
                for (j, c) in zip(patterns, colors):
                    ptn = j.split(' ')
                    ptn_len = len(ptn)
                    if ptn == symbol_list[i:i + ptn_len]:
                        marker_color_list[i:i + ptn_len] = [c] * ptn_len
        
        # 確認,あとで消す
        print(marker_color_list)                                        
                    
        my_map = folium.Map()
        # is_head = True
        location_list = np.array([df[self.lat_name], df[self.long_name]])
        location_list = location_list.T.tolist()
        
        my_map = folium.Map(location_list[0], zoom_start=15)
        folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
        folium.Marker(location_list[0],popup='start',icon=folium.Icon(color='red',icon='star')).add_to(my_map)
        
        for (lat_lon,c) in zip(location_list,marker_color_list):
            folium.CircleMarker(lat_lon, radius=1, color=c).add_to(my_map)
        else:
            folium.Marker(lat_lon, popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
        my_map.save(save_path)

    def __highlight_patterns_on_maps_overlay(self, trajectory_files, patterns, column_names, thresholds, save_path, colors=['red', 'blue', 'green', 'black','yellow']):        
        """
        trajectry_files = [a.csv,b.csv.....]

        patterns = [['1:1:1 0:1:2 2:3:1'],['1:1:1 0:1:2 2:3:1'],.....] : left is higher priority. max:5 patterns. if you'd like to apply more, Please increase color list.  

        column_names = ['hoge','huga','kazy'] : only columns using symbolization

        thresholds = [[5, 40, 60], [-0.05, 0.05], [-0.01, 0.01]]

        save_path = ./hoge/fuga.html

        colors = ['red', 'blue', 'green', 'black']
        """

        my_map = folium.Map()
        is_first_file = True
        patterns.reverse()
        pattern_lengths = []

        for ptn in patterns:
            pattern_lengths.append(len(ptn.split(' ')))

        min_pattern_length = min(pattern_lengths)

        
        sbl = symbolization.Symbolization(column_names, thresholds, False)

        for i in trajectory_files:
            print(i)
            file_extension = i.split('.')[-1] 
            # load data
            if file_extension == 'tsv':
                # delete all rows which has NaN
                df = pd.read_table(i)
                df = df.dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i)
                df = df.dropna()
            else:
                continue

            
            symbol_list = sbl.symbolize(df)
            symbol_list_length = len(symbol_list)

            # -1 means no mark
            marker_color_list = ['gray'] * symbol_list_length

            for i in range(symbol_list_length):
                if (i + min_pattern_length) > symbol_list_length:
                    break
                else:
                    for (j,c) in zip(patterns,colors):
                        ptn = j.split(' ')
                        ptn_len = len(ptn)
                        if ptn == symbol_list[i:i + ptn_len]:
                            marker_color_list[i:i + ptn_len] = [c] * ptn_len                                      

            location_list = np.array([df[self.lat_name], df[self.long_name]])
            location_list = location_list.T.tolist()

            if is_first_file:
                my_map = folium.Map(location_list[0], zoom_start=15)
                is_first_file = False
            
            folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
            folium.Marker(location_list[0], popup='start', icon=folium.Icon(color='red', icon='star')).add_to(my_map)
            
            for (lat_lon,c) in zip(location_list,marker_color_list):   
                folium.CircleMarker(lat_lon, radius=1, color=c).add_to(my_map)
            else:
                folium.Marker(lat_lon, popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
        
        my_map.save(save_path)

    def highlight_patterns_on_maps(self, trajectories_path, patterns, column_names, thresholds, save_path, colors=['red', 'blue', 'green', 'black','yellow']):
        """
        trajectories_path = 'hoge/trajectories/'

        patterns = [['1:1:1 0:1:2 2:3:1'],['1:1:1 0:1:2 2:3:1'],.....] : left is higher priority

        thresholds = [[5, 40, 60], [-0.05, 0.05], [-0.01, 0.01]]

        column_names = ['hoge','huga','kazy']

        save_path = 'hoge/maps/'

        colors = ['red', 'blue', 'green', 'black'] (default)
        """
        # data
        files = glob.glob(trajectories_path + '*')
        
        if self.overlay:
            save_for = save_path + 'overlay_highlight_patterns_' + '{0:%y%m%d%H%M}'.format(datetime.datetime.now()) + '.html'
            self.__highlight_patterns_on_maps_overlay(files, patterns, column_names, thresholds, save_for, colors)
            
        else:
            # for all data
            for i in files:
                print(i)
                file_extension = i.split('.')[-1] 
                # load data
                if file_extension == 'tsv':
                    # delete all rows which has NaN
                    df = pd.read_table(i)
                    df = df.dropna()
                elif file_extension == 'csv':
                    # delete all rows which has NaN
                    df = pd.read_csv(i)
                    df = df.dropna()
                else:
                    continue
                
                save_for = save_path + 'highlght_patterns_' +os.path.splitext(i.split('/')[-1])[0] + '.html'
                self.highlight_patterns_on_map(df, patterns, column_names, thresholds, save_for, colors) 

