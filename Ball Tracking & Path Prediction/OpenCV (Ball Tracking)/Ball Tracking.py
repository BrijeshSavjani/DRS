from matplotlib.figure import Figure
from FindBallBoundsYCrCb import GetBallBounds
from GetStumpLocation import GetStumpLocation
from TrackBall import BallTracker
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

side_video_path  = r"D:\Personal\Downloads\DRS\DRS\Orange Side - Edit.mp4"
front_video_path = r"D:\Personal\Downloads\DRS\DRS\Orange Front - Edit.mp4"

def DrawPitch(subplot:Axes3D,stumps_s,stumps_f,travel_length):
    #Stump location
    z  = min(stumps_s[0][1],stumps_s[1][1]) #Depth
    y  = min(stumps_f[0][0],stumps_f[1][0]) #Height
    x  = min(stumps_s[0][0],stumps_s[1][0]) #Width
    #Stump size
    dx = abs(stumps_s[0][0] - stumps_s[1][0])
    dy = abs(stumps_f[0][0] - stumps_f[1][0])
    dz = abs(stumps_f[0][1] - stumps_f[1][1])
    #Draw Stumps
    subplot.bar3d(x, y, z, dx, dy, dz, color='blue', edgecolor='yellow', shade=True, label="_nolegend_",)

    #Draw  Pitch
    subplot.bar3d(x,y-1.52,z-0.1,travel_length,y+1.52,0.1,color="DarkKhaki",label="_nolegend_")
    #Draw Impact Strip
    subplot.bar3d(x, y, z, travel_length,dy,0.05, color='GoldenRod', edgecolor='black', shade=True,alpha=0.5,label="_nolegend_")
    subplot.legend()

def CreateView(fig:Figure,loc:tuple[int,int,int],view:tuple[int,int],name:str,x:list,y:list,z:list,axes_bounds:tuple[float,float],stumps_s,stumps_f,ball_hit_pad:int):
    #Create subplot and setup
    subplot = fig.add_subplot(loc[0],loc[1],loc[2],projection='3d')
    subplot.set_title(name)
    subplot.view_init(elev=view[0], azim=view[1])
    
    #Set figure size
    min_val, max_val = axes_bounds
    subplot.set_xlim(min_val,max_val)
    subplot.set_ylim(min_val,max_val)
    subplot.set_zlim(min_val,max_val)
    
    #Work out what size to make points to accurately reperesent ball
    figure_size_in_points = subplot.figure.get_size_inches()[0] * 72
    points_per_m = figure_size_in_points / (max_val-min_val)
    plot_diameter = (points_per_m * 0.0726)**2
    
    #Plot values
    subplot.scatter(x[:ball_hit_pad],y[:ball_hit_pad],z[:ball_hit_pad],s=plot_diameter,marker="o",c="gray",label="Actual ball path")
    subplot.scatter(x[ball_hit_pad:],y[ball_hit_pad:],z[ball_hit_pad:],s=plot_diameter,marker="o",c="red",label="Predicted ball path")

    subplot.set_box_aspect([1,1,1])
    subplot.set_axis_off()
    DrawPitch(subplot,stumps_s,stumps_f,max(x)-min(x))

def IsOut(y:list,z:list,stumps_f,impact_frame:int)->str:
    #Figure if it hit stumps,pitching and impact
    bounce_frame = z.index(min(z))
    bounce_y = y[bounce_frame]
    impact_y = y[impact_frame] #Need to take in last frame observed

    pitching = bounce_y >= min(stumps_f[1][0],stumps_f[0][0]) #if pitching outisde leg not allowed but outside off or inline allowed
    impact   = min(stumps_f[1][0],stumps_f[0][0]) <= impact_y <= max(stumps_f[0][0],stumps_f[1][0]) 

    hitting_height = min(stumps_f[1][1],stumps_f[0][1]) <= z[-1] <= max(stumps_f[1][1],stumps_f[0][1])
    hitting_lateral = min(stumps_f[1][0],stumps_f[0][0]) <= y[-1] <= max(stumps_f[0][0],stumps_f[1][0]) 
    hitting = hitting_height & hitting_lateral

    return (f"Pitching: {"IN LINE/OUTSIDE OFF" if pitching else "OUT OF LINE"}\n" +
            f"Impact: {"IN LINE" if impact else "OUT OF LINE"}\n" + 
            f"Stumps: {"HITTING" if hitting else "MISSING"}")

#Get ball colour bounds
#bounds = GetBallBounds(side_video_path)
bounds = (np.uint8([0,160,0]),np.uint8([255,255,255]))

#Get stumps location - h
m_per_pixel_s,stumps_s = GetStumpLocation(side_video_path)
#Track - h
side_tracker = BallTracker(side_video_path,bounds[1],bounds[0],m_per_pixel_s,True)
dt_s,side_path,ball_hit_pad_s = side_tracker.TrackBall()
# #Get stumps location - f
m_per_pixel_f,stumps_f = GetStumpLocation(front_video_path)
#Track - f
front_tracker = BallTracker(front_video_path,bounds[1],bounds[0],m_per_pixel_f,False)
dt_f,front_path,ball_hit_pad_f = front_tracker.TrackBall()
#Check dt is equal
if(dt_s == dt_f):
    min_length = min(len(front_path),len(side_path)) 
    y = [fp[0] for fp in front_path[:min_length]]#Lateral position
    z = [sp[1] for sp in side_path[:min_length]]#Height
    x = [sp[0] for sp in side_path[:min_length]]#Depth downpitch
    
    axes_bounds = (min(min(x),min(y),min(z)),max(max(x),max(y),max(z))) 
    
    ball_hit_pad_frame = ((ball_hit_pad_f + ball_hit_pad_s) // 2) - 1 if (ball_hit_pad_f != -1 and ball_hit_pad_s !=-1) else max(ball_hit_pad_f,ball_hit_pad_s)
    
    if(ball_hit_pad_frame == -1):print("No impact data - Just graphing observed path")

    #Plot out
    fig = plt.figure()
    CreateView(fig,(1,3,1),(0,0),"Front on - Batter",x,y,z,axes_bounds,stumps_s,stumps_f,ball_hit_pad_frame)
    CreateView(fig,(1,3,2),(0,-90),"Side on",x,y,z,axes_bounds,stumps_s,stumps_f,ball_hit_pad_frame)
    CreateView(fig,(1,3,3),(90,-90),"Top Down",x,y,z,axes_bounds,stumps_s,stumps_f,ball_hit_pad_frame)
    #Write results on plot (pitching,impact and if hitting)
    plt.figtext(0.1,0.9,IsOut(y,z,stumps_f,ball_hit_pad_frame))

    
    plt.tight_layout()
    plt.show()
else:
    print("Frame rates of 2 cameras differ can't sync path")
