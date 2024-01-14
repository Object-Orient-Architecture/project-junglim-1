import Rhino.Geometry as geo
import math
import funcs
from funcs.area_table_def import is_pt_inside_curve

# 과제2
bbox1 = space1.GetBoundingBox(geo.Plane.WorldXY)
bbox2 = space2.GetBoundingBox(geo.Plane.WorldXY)
bbox = geo.BoundingBox.Union(bbox1,bbox2) 
width = bbox.Max.X-bbox.Min.X
height = bbox.Max.Y-bbox.Min.Y

step = 1000
vec_x = geo.Vector3d(step,0,0)
vec_y = geo.Vector3d(0,step,0)

x_count = math.ceil(width/step)
y_count = math.ceil(height/step)

origin_point = bbox.Min
points = []
for i in range(x_count):
    for j in range(y_count):
        point = origin_point + i*vec_x + j*vec_y
        if is_pt_inside_curve(point, space1):
            points.append(point)
        if is_pt_inside_curve(point, space2):
            points.append(point)

point_and_connectivity_tuple = []
for i in points:
    valid_lines =[]
    for j in points:
        if i != j:
            line = geo.LineCurve(i,j)
            intersection_check = geo.Intersect.Intersection.CurveCurve(line,obstacle,0.001,0.001)
            if intersection_check.Count == 0:
                valid_lines.append(line)
    valid_lines_count = len(valid_lines)
    point_and_connectivity_tuple.append((i,valid_lines_count))

connectivity_list = [point_and_connectivity[1] for point_and_connectivity in point_and_connectivity_tuple]
highest_value = max(connectivity_list)
lowest_value = min(connectivity_list)

normalized_connectiviey = []
minus_value = [value - lowest_value for value in connectivity_list]
nomalization = [value/max(minus_value) for value in minus_value]
colorlizing = [int(value*255) for value in nomalization]

rectangles =[]
half_width = step/2
half_height = step/2
for i in range(len(points)):
    pt1 = geo.Point3d(points[i].X - half_width, points[i].Y - half_height, points[i].Z)
    pt2 = geo.Point3d(points[i].X + half_width, points[i].Y - half_height, points[i].Z)
    pt3 = geo.Point3d(points[i].X + half_width, points[i].Y + half_height, points[i].Z)
    pt4 = geo.Point3d(points[i].X - half_width, points[i].Y + half_height, points[i].Z)
    rectangles.append(geo.PolylineCurve([pt1, pt2, pt3, pt4, pt1]))

height = 5
rec_extrusion = [geo.Extrusion.Create(rectangles[i], height, True).ToBrep() for i in range(len(rectangles))]
