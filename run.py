from qgis.core import QgsProject, QgsVectorLayer, QgsRasterLayer, QgsCoordinateTransform, QgsProperty
import os
from qgis import processing

from DEMto3DRigdelineMap.functions.gather_information import get_information
from DEMto3DRigdelineMap.functions.extract_layer_extent import get_shape_size
from DEMto3DRigdelineMap.functions.grid import create_grid

# Replace the following paths with the actual paths in your Docker container
# shape_path = '/app/Data/*.geojson'
# raster_path = '/app/your_folder/*.tif'

shape_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/departement-74-haute-savoie.geojson'
raster_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/OUTPUT.tif'
info_file_path = 'C:/Users/arnau//Documents//DEMto3DRigdelineMap/Data/info.txt'  

# Now you have the value of maximum_map_size
real_maximum_map_size, real_width = get_information(info_file_path)
physical_millimiters = 300

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
map_height = get_shape_size(layer1)     #441133m in example
print(f"Map height {map_height} meters")
m_per_mm = map_height / 300

# Step 7 & 8: Create Grid & Translate Grid
grid_extent = 'extent_layer_shape'
vertical_spacing = 3 * m_per_mm
horizontal_spacing = map_height
delta_y = -m_per_mm*1.5 
create_grid(grid_extent, vertical_spacing, horizontal_spacing, delta_y)

# Step 9: Clip the Grid

processing.runAndLoadResults("native:clip", {'INPUT':"Translaté",
                               'OVERLAY': shape_path,
                               'OUTPUT':'clipped_grid_boundary'})

# Step 10: Extract Vertices [Possibly Unnecessary]
processing.runAndLoadResults("native:extractvertices", {'INPUT':'clipped_grid_boundary',
                                                  'VERTICES':'0',
                                                  'OUTPUT':'clipped_grid_boundary_vertices'})

# Step 11: Points to Path [Possibly Unnecessary]

processing.runAndLoadResults("native:pointstopath", {'INPUT':'clipped_grid_boundary_vertices',
                                       'CLOSE_PATH':False,
                                       'ORDER_EXPRESSION':'"vertex_index"',
                                       'NATURAL_SORT':False,
                                       'GROUP_EXPRESSION':'"id"',
                                       'OUTPUT':'clipped_grid_vertices_to_path'})

# Step 12: Simplify [Possibly Unnecessary]

processing.runAndLoadResults("native:simplifygeometries", {'INPUT':'clipped_grid_vertices_to_path',
                                             'METHOD':0,
                                             'TOLERANCE':1,
                                             'OUTPUT':'simplified_clipped_grid_boundary'})

# Step 13: Points Along Geometry

processing.runAndLoadResults("native:pointsalonglines", {'INPUT':'simplified_clipped_grid_boundary',
                                           'DISTANCE':300,
                                           'START_OFFSET':0,
                                           'END_OFFSET':0,
                                           'OUTPUT':'points_along_clipped_gridlines_300m'})

# Step 14: Extract Specific Vertices

processing.runAndLoadResults("native:extractspecificvertices", {'INPUT':'simplified_clipped_grid_boundary.gpkg',
                                                  'VERTICES':'1',
                                                  'OUTPUT':'clipped_gridline_right_vertex'})

# Step 15: Merge Vector Layers

processing.runAndLoadResults("native:mergevectorlayers", {'LAYERS':['clipped_gridline_right_vertex.gpkg','points_along_clipped_gridlines_300m.gpkg'],
                                            'CRS':None,
                                            'OUTPUT':'merged_points_along_line'})

# Step 16: Sample Raster Values

processing.runAndLoadResults("native:rastersampling", {'INPUT':'merged_points_along_line.gpkg',
                                         'RASTERCOPY':raster_path,
                                         'COLUMN_PREFIX':'elevation_',
                                         'OUTPUT':'sampled_elevation_point_layer'})

# Step 17: Translate Points

processing.runAndLoadResults("native:arraytranslatedfeatures", {'INPUT':'sampled_elevation_point_layer.gpkg',
                                                  'COUNT':10,
                                                  'DELTA_X':0,
                                                  'DELTA_Y':QgsProperty.fromExpression('if("elevation_1"<=0,'+ str(-0.3*m_per_mm)+',"elevation_1"*'+str(real_width/100*m_per_mm)+'/maximum("elevation_1"))'),
                                                  'DELTA_Z':0,
                                                  'DELTA_M':0,
                                                  'OUTPUT':'translated_sampled_elevation_point_layer'})

# Step 18: Rewind: Translate an Earlier Layer

processing.runAndLoadResults("native:translategeometry", {'INPUT':'simplified_clipped_grid_boundary.gpkg',
                                            'DELTA_X':0,
                                            'DELTA_Y':-6*m_per_mm,
                                            'DELTA_Z':0,
                                            'DELTA_M':0,
                                            'OUTPUT':'translated_baseline_lines'})

# Step 19: More Extracted Vertices and Field Calculating!

processing.runAndLoadResults("native:extractvertices", {'INPUT':'translated_sampled_elevation_point_layer.gpkg',
                                          'OUTPUT':'baseline_points'})

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