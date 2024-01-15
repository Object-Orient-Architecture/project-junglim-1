import sys
import os
import Rhino.Geometry as geo

import math
our_path = "C:\\PythonWork\\3-1"
sys.path.append(our_path)
from funcs.extract import is_pt_inside

box = room.GetBoundingBox(geo.Plane.WorldXY)
origin_point = box.Min

height = box.Max.Y - box.Min.Y
width = box.Max.X - box.Min.X
step = 5000

vec_x = geo.Vector3d(step,0,0)
vec_y = geo.Vector3d(0,step,0)

x_count = math.ceil(width / step)
y_count = math.ceil(height / step)

points = []
for x_index in range(x_count):
    for y_index in range(y_count):
        point = origin_point + x_index*vec_x + y_index*vec_y
        if is_pt_inside(point, room):
            points.append(point)

point_score_tuple_list = []
for check_point in points:
    lines_on_point = []
    for point2 in points:
        if check_point !=point2:
            check_line = geo.LineCurve(check_point,point2)
            curve_intersections = geo.Intersect.Intersection.CurveCurve(check_line, obstacle, 0.1 ,0.1)
            if curve_intersections.Count == 0:
                lines_on_point.append(check_line)
    score = len(lines_on_point)
    point_score_tuple_list.append((check_point,score))

scores = [score_tuple[1] for score_tuple in point_score_tuple_list] 

max_core=max(scores)
min_score=min(scores)

score_minus_min = [score -min_score for score in scores]
score_normalized = [score /max(score_minus_min) for score in score_minus_min]

score_for_color = [int(score * 255) for score in score_normalized]

radius = step/2
circles = [geo.Circle(point, radius) for point in points]

height = 5
circle_extrusions = [geo.Extrusion.Create(circle.ToNurbsCurve(), height, True) for circle in circles]
print(circle_extrusions)
            

#room 과 obstacle이 같은 객체일때
#문으로 뚫린부분이 있는 경우까지 생각
