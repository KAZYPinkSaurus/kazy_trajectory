import sys
from kazytrajectory import visualization as vt
from kazytrajectory import symbolization as sb
import time


if __name__ == '__main__':
    """
    python main.py data/hoge/ output/fuga/
    """
    args = sys.argv
    # input datapath, parameter
    
    #path of trajectories directory 
    trajectories_path = args[1]

    #path of save directory
    save_path = args[2]
    
    start = time.time()

    # drow map
    # map_drower = vt.Visualization(name_lat_long=['LAT','LONG'],overlay=True)
    # map_drower.drow_maps(trajectories_path, save_path)

    # plot coordinates
    # plt_c = vt.Visualization(name_lat_long=['LAT','LONG'],overlay=True)
    # plt_c.plot_coordinates(trajectories_path,save_path)

    #plot histgram
    # plt_hist = vt.Visualization(name_lat_long=['LAT','LONG'])
    # plt_hist.plot_histgram(trajectories_path,['EST_SPEED','EST_FB_ACCEL','EST_LR_ACCEL'],100,save_path)
    
    # make sequenace
    columns = ['EST_SPEED', 'EST_FB_ACCEL', 'EST_LR_ACCEL']
    thresholds = [[5, 40, 60], [-0.05, 0.05], [-0.01, 0.01]]
    label = 1
    sb1 = sb.Symbolization(columns, thresholds,label)
    sb1.symbolize_trajectories(trajectories_path, save_path)
    
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    