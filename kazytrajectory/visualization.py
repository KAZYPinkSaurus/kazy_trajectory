import folium
import numpy as np
import pandas as pd
import sys
import glob
import os.path
import datetime
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt



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
        my_map = folium.Map()
        is_head = True
        location_list = np.array([location[0], location[1]])
        location_list = location_list.T.tolist()
        
        
        for (row_lat, row_lon) in zip(location[0], location[1]):
            if is_head:
                my_map = folium.Map([row_lat, row_lon], zoom_start=15)
                folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
                folium.Marker([row_lat, row_lon],popup='start',icon=folium.Icon(color='red',icon='star')).add_to(my_map)
                is_head=False
            else:   
                folium.CircleMarker([row_lat, row_lon], radius=1, color='blue').add_to(my_map)
        else:
            folium.Marker([row_lat, row_lon], popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
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
                df = pd.read_table(i,header=1)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i,header=1)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            else:
                continue

            is_head = True
            location_list = np.array([df[self.lat_name], df[self.long_name]])
            location_list = location_list.T.tolist()
            
            
            for (row_lat, row_lon) in zip(df[self.lat_name], df[self.long_name]):
                if is_head:
                    if is_first_file:
                        my_map = folium.Map([row_lat, row_lon], zoom_start=15)
                        is_first_file = False

                    folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
                    folium.Marker([row_lat, row_lon],popup='start',icon=folium.Icon(color='red',icon='star')).add_to(my_map)
                    is_head=False
                else:   
                    folium.CircleMarker([row_lat, row_lon], radius=1, color='blue').add_to(my_map)
            else:
                folium.Marker([row_lat, row_lon], popup='end',icon=folium.Icon(color='green',icon='flag')).add_to(my_map)
        
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
                    df = pd.read_table(i,header=1)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                elif file_extension == 'csv':
                    # delete all rows which has NaN
                    df = pd.read_csv(i,header=1)
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
                    df = pd.read_table(i,header=1)
                    df = df.loc[:,[self.lat_name,self.long_name]].dropna()
                elif file_extension == 'csv':
                    # delete all rows which has NaN
                    df = pd.read_csv(i,header=1)
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
                df = pd.read_table(i,header=1)
                df = df.loc[:,[self.lat_name,self.long_name]].dropna()
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i,header=1)
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
                df = pd.read_table(i,header=1)
                df = df.loc[:, column_names].dropna()
                df_all = pd.concat([df_all,df])
            elif file_extension == 'csv':
                # delete all rows which has NaN
                df = pd.read_csv(i,header=1)
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