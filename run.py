from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateTransform
import os

from DEMto3DRigdelineMap.functions.gather_information import get_information
from DEMto3DRigdelineMap.functions.extract_layer_extent import get_shape_size

# Replace the following paths with the actual paths in your Docker container
# shape_path = '/app/Data/*.geojson'
# raster_path = '/app/your_folder/*.tif'

shape_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/departement-74-haute-savoie.geojson'
raster_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/OUTPUT.tif'
info_file_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/info.txt'  

# Now you have the value of maximum_map_size
real_maximum_map_size, real_width = get_information(info_file_path)

# Now you have the values of maximum_map_size and width
print(f"Maximum Map Size: {real_maximum_map_size}")
print(f"Width: {real_width}")

osm_layer_name = 'OSM Standard'
for layer_id, layer in QgsProject.instance().mapLayers().items():
    if osm_layer_name not in layer.name():
        QgsProject.instance().removeMapLayer(layer_id)

# Load vector layer into QGIS
layer1 = QgsVectorLayer(shape_path, 'Shape', 'ogr')

# Load raster layer into QGIS
layer2 = QgsRasterLayer(raster_path, 'Raster')
crs = QgsCoordinateReferenceSystem('IGNF:LAMB93')
layer2.setCrs(crs)

# Check if layers are loaded successfully
if not layer1.isValid():
    print(f"Error: Could not load vector layer from {shape_path}")
else:
    # Add vector layer to the project
    QgsProject.instance().addMapLayer(layer1)

if not layer2.isValid():
    print(f"Error: Could not load raster layer from {raster_path}")
else:
    # Add raster layer to the project
    QgsProject.instance().addMapLayer(layer2)



# Step 6: Extract Layer Extent --> Check extract_layer_extent for more information
width = get_shape_size(layer1)
print(f"Maximum size {width} meters")

# Step 7: Create Grid

# Step 8: Translate Grid

# Step 9: Clip the Grid

# Step 10: Extract Vertices [Possibly Unnecessary]

# Step 11: Points to Path [Possibly Unnecessary]

# Step 12: Simplify [Possibly Unnecessary]

# Step 13: Points Along Geometry

# Step 14: Extract Specific Vertices

# Step 15: Merge Vector Layers

# Step 16: Sample Raster Values

# Step 17: Translate Points

# Step 18: Rewind: Translate an Earlier Layer

# Step 19: More Extracted Vertices and Field Calculating!

# Step 20: Merge Layers

# Step 21: Points to Path

# Step 22: Lines to Polygons

# Step 23: Translate Polygons

# Step 24: More Translation!

# Step 25: Alignment Lines

# Step 26: Line Intersections

# Step 27: Even More Translating

# Step 28: Buffering

# Step 29: More Vertex Extraction

# Step 30: Making Rectangles

# Step 31: Making a Difference (in a Polygon)

# Step 32: Polygons to Lines

# Step 33: Extracting the Last Vertex and Labels

# Step 34: Exporting!