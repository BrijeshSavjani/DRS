import re
import copy
import numpy as np
ball_import = open(r"D:\Personal\Downloads\DRS\DRS\Github\Ball Tracking & Path Prediction\OpenCV (Ball Tracking)\ball_location_data.txt", "r")
side_ball_import = open(r"D:\Personal\Downloads\DRS\DRS\Github\Ball Tracking & Path Prediction\OpenCV (Ball Tracking)\side_ball_location_data.txt")
stump_import = open(r"D:\Personal\Downloads\DRS\DRS\Github\Ball Tracking & Path Prediction\OpenCV (Ball Tracking)\stump_location_data.txt", "r")

def GetCoordinates(positions):
    cleaned_positions = []
    coordinates = []
    for position in positions:
        cleaned = re.sub("\n|,|\(|array|\[|\]", "", position).split("       ")
        cleaned_positions.append(cleaned)
    for cleaned_position in cleaned_positions:
        group = []
        for coordinate in cleaned_position:
            xy = coordinate.split(" ")
            while len(xy) != 2:
                    try:
                        xy.remove('')
                    except:
                        break

            group.append(xy)
        coordinates.append(group)
    return coordinates
def RemoveOutliers(list):
        list.sort()
        q3 = np.percentile(list, 75 )
        q1 = np.percentile(list , 25 )   
        upper_bound = (1.5 * (q3-q1)) + q3
        lower_bound = q1 - (1.5* (q3-q1))
        for element in list:
            if element > upper_bound :
                list.remove(element) 
            if element < lower_bound :
                list.remove(element) 
        return list
def StumpHeights(coordinates):
    contours_with_area = copy.deepcopy(coordinates)
    height_values = []
    for coordinate in coordinates:
        if len(coordinate) < 2:
            contours_with_area.remove(coordinate)
        for i in range (1,len(coordinate)):
            height_values.append(abs(float(coordinate[0][1]) - float(coordinate[i][1])))    
    return height_values
def FinalStumpHeight(values):
        stump_heights = []
        for value in values:
            coordinates = GetCoordinates(value.split(", dtype=int32)"))
            stump_heights.extend(StumpHeights(coordinates))
        stump_heights = RemoveOutliers(stump_heights)
        return np.mean(stump_heights)
def BallCoordinates(frame,pixelspercm):
    relative_coordinates = []
    for coordinates in frame:
        contours = GetCoordinates(coordinates.split(", dtype=int32)"))
        x_vertices = []
        y_vertices = []
        for contour in contours:
            if len(contour) > 1:
                for vertice in contour:
                    x_vertices.append(float(vertice[0]))
                    y_vertices.append(float(vertice[1]))
                x_vertices = RemoveOutliers(x_vertices)
                y_vertices = RemoveOutliers(y_vertices)
                x = np.mean(x_vertices) * pixelspercm
                y = np.mean(y_vertices) * pixelspercm
                relative_coordinates.append([x,y])
    return relative_coordinates
pixelspercm = FinalStumpHeight(stump_import.read().split('/n')) / 71.12
pixelspercm = 60
Front = BallCoordinates(ball_import.read().split('/n'),pixelspercm)
Side = BallCoordinates(side_ball_import.read().split('/n'),pixelspercm)
coordinates = []
for i in range(0,len(Side)):
    coordinate = Front[i]
    coordinate.append(Side[i][0])
    coordinates.append(coordinate)
#print(pixelspercm)
print(coordinates)