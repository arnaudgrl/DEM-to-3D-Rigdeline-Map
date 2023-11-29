# File: extract_layer_extent.py

from qgis.core import QgsProject, QgsCoordinateTransform, QgsCoordinateReferenceSystem,  QgsRectangle, QgsVectorLayer, QgsFeature, QgsField, QgsGeometry

def get_shape_size(layer1):
    bounding_box_4326 = layer1.getFeature(0).geometry().boundingBox()
    transform = QgsCoordinateTransform(layer1.crs(), QgsCoordinateReferenceSystem('EPSG:3857'), QgsProject.instance())
    bounding_box_3857 = transform.transformBoundingBox(bounding_box_4326)

    # Calculate and print the width and height
    width = max(bounding_box_3857.width(), bounding_box_3857.height())

    # Create a temporary layer to display the bounding box
    temp_layer = QgsVectorLayer('Polygon?crs=EPSG:3857', 'extent_layer_shape', 'memory')
    temp_layer_data = temp_layer.dataProvider()

    # Add a feature with the bounding box geometry
    feature = QgsFeature()
    feature.setGeometry(QgsGeometry.fromRect(bounding_box_3857))
    temp_layer_data.addFeature(feature)

    # Add the temporary layer to the map canvas
    QgsProject.instance().addMapLayer(temp_layer)

    return width