# 240104
import Rhino
import Rhino.Geometry as geo

def extract_data_to_dict():
    layers = Rhino.RhinoDoc.ActiveDoc.Layers
    object_list = Rhino.RhinoDoc.ActiveDoc.Objects

    object_by_layer = {}

    for layer in layers:
        object_by_layer[layer.Name] = []

    for obj in object_list:
        for layer in layers:
            if layer.Index == obj.Attributes.LayerIndex:
                object_by_layer[layer.Name].append(obj)
    return object_by_layer

def get_area(curve):
    geometry_area = Rhino.Geometry.AreaMassProperties.Compute(curve)
    if geometry_area:
        area = geometry_area.Area
        return area
    else:
        raise Exception("something wrong")
    
def get_text_point(text_entity):
    center_point = text_entity.Plane.Origin
    return center_point

def is_pt_inside_curve(pt, curve):
    containment = curve.Contains(pt,geo.Plane.WorldXY, 0.001)
    if containment == geo.PointContainment.Inside:
        return True
    return False