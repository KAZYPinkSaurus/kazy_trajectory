# 参考：http://hamasyou.com/blog/2010/09/07/post-2/
import pandas as pd
import numpy as np
import math

class HandleLonLat(object):

    def __init__(self):
        pass

    def cal_distance(self, aDf, precision):
        """
        precision は小数点以下の桁数（距離の精度）
        Dataframeごと距離を計算
        
        aDf['longitude'],aDf['latitude']を使用
        """
        lon1 = aDf['longitude']
        lon2 = lon1.shift(1)
        lat1 = aDf['latitude']
        lat2 = lat1.shift(1)
        
        dist = 0
        if False:#np.abs(lat1 - lat2) < 0.00001 and np.abs(lon1 - lon2) < 0.00001:
            dist = 0
        else:        
            lat1 = lat1 * np.pi / 180
            lat2 = lat2 * np.pi / 180
            lon1 = lon1 * np.pi / 180
            lon2 = lon2 * np.pi / 180
            a = 6378140
            b = 6356755
            f = (a - b) / a

            p1 = np.arctan((b   / a) * np.tan(lat1))
            p2 = np.arctan((b / a) * np.tan(lat2))
            x = np.arccos(np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(lon1 - lon2))
            l = (f / 8) * ((np.sin(x) - x) * np.power((np.sin(p1) + np.sin(p2)), 2) / np.power(np.cos(x/ 2), 2) - (np.sin(x) - x) * np.power(np.sin(p1) - np.sin(p2), 2) / np.power(np.sin(x), 2))

            dist = a * (x + l)
            decimal_no = math.pow(10, precision)
            dist = np.round(decimal_no * dist / 1) / decimal_no   #kmに変換するときは(1000で割る)
        return dist

    def cal_speed(self, aDf, precision, days_time=True):
        """
        speed(m/s)をDataframeごと計算
        dataframe中のlongitude,latitude,time(h:m:s)を使用
        """
        # 距離を取得
        dist_df = self.cal_distance(aDf[['longitude', 'latitude']], precision)
        if days_time:
            # daysとtime をtimedeltaとして一つにする
            days_time_df = pd.to_timedelta(aDf['days'].astype('str').str.cat(aDf['time'], ' days '))
        else:
            # 2014-11-10 10:00:00こんな感じのフォーマットの時
            days_time_df = pd.to_datetime(aDf['time'])
        
        # 経過秒に変換
        delta_time_df = (days_time_df - days_time_df.shift(1)).dt.total_seconds()

        # 距離/時間
        return dist_df / delta_time_df
         
    def cal_direction(self, aDf):
        """
        aDf['longitude'],aDf['latitude']から方向を計算
        北を0度で右回りの角度0~360度
        """
        lon1 = aDf['longitude']
        lon2 = lon1.shift(1)
        lat1 = aDf['latitude']
        lat2 = lat1.shift(1)
        
        # 緯度経度 lat1, lon1 の点を出発として、緯度経度 lat2, lon2 への方位
        
        Y = np.cos(lon2 * np.pi / 180) * np.sin(lat2 * np.pi / 180 - lat1 * np.pi / 180)
        X = np.cos(lon1 * np.pi / 180) * np.sin(lon2 * np.pi / 180) - np.sin(lon1 * np.pi / 180) * np.cos(lon2 * np.pi / 180) * np.cos(lat2 * np.pi / 180 - lat1 * np.pi / 180)
        # 東向きが０度の方向
        dirE0 = 180 * np.arctan2(Y, X) / np.pi 
        #0～360 にする。
        dirE0[dirE0<0] += 360
            
        #(dirE0+90)÷360の余りを出力 北向きが０度の方向
        dirN0 = (dirE0 + 90) % 360
        return dirN0

    
    def cal_delta_direction(self, aDf, aDf_shift):
        """
        aDf['theta'] - aDf_shift['theta'] = ΔDf['delta_theta']
        0を跨ぐところがやや面倒なので処理している
        aDf_shiftはdataframe.shift(1)したものとする
        thetaに関してdelta thetaを取る
        """

        out = pd.DataFrame(np.zeros(aDf.shape[0]),columns=['delta_theta'])
        for (i, j, k) in zip(aDf['theta'], aDf_shift['theta'], range(aDf.shape[0])):
            if (i >= 180 and (np.abs(i-j) >= 180)):
                out['delta_theta'][k] = i - (j + 360)
                # print('i:'+str(i)+' j:'+str(j)+'結果　'+str(i - (j + 360)))
            elif (j >= 180 and (np.abs(i-j) >= 180)):
                out['delta_theta'][k] = (i + 360) - j
                # print('i:'+str(i)+' j:'+str(j)+'結果　'+str((i + 360) - j))
            else:
                out['delta_theta'][k] = i - j
                # print('i:'+str(i)+' j:'+str(j)+'結果　'+str(i-j))
        return out