# File: grid.py

from qgis.core import QgsCoordinateReferenceSystem
from qgis import processing

def create_grid(grid_extent, vertical_spacing, horizontal_spacing):
    processing.run("native:creategrid", {'TYPE':1,
                                         'EXTENT':grid_extent,
                                         'HSPACING':horizontal_spacing,
                                         'VSPACING': vertical_spacing,
                                         'HOVERLAY':0,
                                         'VOVERLAY':0,
                                         'CRS':QgsCoordinateReferenceSystem('EPSG:3857'),
                                         'OUTPUT':'memory'
                                         })