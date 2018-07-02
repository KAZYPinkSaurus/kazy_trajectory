import folium
import numpy as np
import pandas as pd
import sys
import glob
import os.path


class VisualizeTrajectory(object):
    def __init__(self,name_lat_long=['latitude','longitude']):
        """
        name_lat_long = ['lat', 'long']

        I reference dataframe with name_lat_long

        (e.g. df['lat'], df['long'])
        """
        self.lat_name = name_lat_long[0]
        self.long_name = name_lat_long[1]

    def drow_map(self, location, save_path):
        """
        location = [df_lat, df_long]

        save_path = 'hoge/hogehoge.html'
        """
        my_map = folium.Map()
        is_first = True
        location_list = np.array([location[0], location[1]])
        location_list = location_list.T.tolist()
        
        
        for (row_lat, row_lon) in zip(location[0], location[1]):
            if is_first:
                my_map = folium.Map([row_lat, row_lon], zoom_start=15)
                folium.PolyLine(location_list,opacity=0.3, color='gray').add_to(my_map)
                folium.Marker([row_lat, row_lon],popup='start',icon=folium.Icon(color='red',icon='star')).add_to(my_map)
                is_first=False
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
            save_for = save_path+os.path.splitext(i.split('/')[-1])[0]+'.html'
            self.drow_map([df[self.lat_name], df[self.long_name]], save_for)