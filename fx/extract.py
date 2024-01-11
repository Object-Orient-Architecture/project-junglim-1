import Rhino
import Rhino.Geometry as geo
from typing import List, Dict, Tuple


def get_area(curve: geo.Curve) -> float:
    """폐곡선을 받아서 면적을 내보낸다."""
    area_properties = Rhino.Geometry.AreaMassProperties.Compute(curve)
    # 면적 출력
    if area_properties:
        area = round(area_properties.Area, 2)
        return area
    if not area_properties:
        raise Exception("something wrong")


def get_room_name_area_pairs(
    text_geometries: List[geo.TextEntity], area_curves: List[geo.Curve]
) -> List[Tuple[str, float]]:
    """text geometry와 curve를 받아서, 매칭 시킨 후에, area pair로 리턴한다."""
    pairs = []
    for text_geometry in text_geometries:
        center_point = get_text_point(text_geometry)
        area_curves_selected = [
            crv for crv in area_curves if is_pt_inside(center_point, crv)
        ]
        if area_curves_selected:
            pairs.append((text_geometry.PlainText, get_area(area_curves_selected[0])))
    return pairs


def filter_texts(
    text_objects: List[Rhino.DocObjects.TextObject],
) -> List[Rhino.DocObjects.TextObject]:
    text_geometry_list = []
    for text_obj in text_objects:
        if type(text_obj) == Rhino.DocObjects.TextObject:
            text = text_obj.TextGeometry.PlainText
            # 텍스트 내용 필터.
            if "CH" in text or "FL" in text or "SL" in text:
                pass
            else:
                text_geometry_list.append(text_obj.TextGeometry)
    return text_geometry_list


def get_text_point(text_geometry: geo.TextEntity) -> geo.Point3d:
    bbox = text_geometry.GetBoundingBox(geo.Plane.WorldXY)
    center = bbox.Center
    return center


def is_pt_inside(pt: geo.Point3d, curve: geo.Curve) -> bool:
    containment = curve.Contains(pt, geo.Plane.WorldXY, 0.1)
    if containment == geo.PointContainment.Inside:
        return True
    return False


def extract_data_to_dict():
    layers = Rhino.RhinoDoc.ActiveDoc.Layers
    objects = Rhino.RhinoDoc.ActiveDoc.Objects

    object_by_layer = {}
    # key = layer.Name
    # value  = List[Object]
    for layer in layers:
        object_by_layer[layer.Name] = []

    for obj in objects:
        for layer in layers:
            if layer.Index == obj.Attributes.LayerIndex:
                object_by_layer[layer.Name].append(obj)
    return object_by_layer
