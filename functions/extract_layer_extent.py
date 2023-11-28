# File: extract_layer_extent.py

from qgis.core import QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem

def get_shape_size(layer1):
    bounding_box_4326 = layer1.getFeature(0).geometry().boundingBox()
    transform = QgsCoordinateTransform(layer1.crs(), QgsCoordinateReferenceSystem('EPSG:3857'), QgsProject.instance())
    bounding_box_3857 = transform.transformBoundingBox(bounding_box_4326)

    # Calculate and print the width and height
    width = max(bounding_box_3857.width(), bounding_box_3857.height())
    return width