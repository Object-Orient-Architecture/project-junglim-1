print(room)
import Rhino.Geometry as geo
import sys
print(sys.path)
path = "C:\\Users\\hmw94\\OneDrive\\Python\\07 Git Setting"
sys.path.append(path)
from funcs.extract import is_pt_inside

box = room.GetBoundingBox(geo.Plane.WorldXY)
width = box.Max.X - box.Min.X
height = box.Max.Y - box.Min.Y
# print(box.Min)
origin_point = box.Min
# print(height, width)
step = 1000
vec_x = geo.Vector3d(step,0,0)
vec_y = geo.Vector3d(0,step,0)

import math
x_count = math.ceil(width/step)
y_count = math.ceil(height/step)
# print(x_count, y_count)

points = []
for x_index in range(x_count):
    for y_index in range(y_count):
        point = origin_point + x_index*vec_x + y_index*vec_y
        if is_pt_inside(point,room):
            points.append(point)

point_score_tuple_list = []
for check_point in points:
    lines_on_point = []
    for point2 in points:
        if check_point != point2:
            check_line = geo.LineCurve(check_point, point2)
            curve_intersections = geo.Intersect.Intersection.CurveCurve(check_line,obstacle,0.1,0.1)
            if curve_intersections.Count == 0:
                lines_on_point.append(check_line)
    score = len(lines_on_point)
    point_score_tuple_list.append((check_point,score))
# print(point_score_tuple)

scores = [score_tuple[1] for score_tuple in point_score_tuple_list]
# print(scores)
max_score=max(scores)
min_score=min(scores)

score_minus_min = [score -min_score for score in scores]
score_normalized = [score /max(score_minus_min) for score in score_minus_min]
# print(score_minus_min)
# print(score_normalized)

print("*"*30 + "score" + "*"*30)

score_for_color = [int(score * 255) for score in score_normalized]
print(score_for_color)

radius = step/2
circles = [geo.Circle(point, radius) for point in points]

height = 5
circle_extrusions = [geo.Extrusion.Create(circle.ToNurbsCurve(), height, True) for circle in circles]
print(circle_extrusions)