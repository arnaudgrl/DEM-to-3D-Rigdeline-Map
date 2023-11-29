# File: grid.py

from qgis.core import QgsCoordinateReferenceSystem
from qgis import processing

def create_grid(grid_extent, vertical_spacing, horizontal_spacing, delta_y):
    # Creates the grid
    processing.runAndLoadResults("native:creategrid", {'TYPE':1,
                                         'EXTENT':grid_extent,
                                         'HSPACING':horizontal_spacing,
                                         'VSPACING': vertical_spacing,
                                         'HOVERLAY':0,
                                         'VOVERLAY':0,
                                         'CRS':QgsCoordinateReferenceSystem('EPSG:3857'),
                                         'OUTPUT':'TEMPORARY_OUTPUT'
                                         })

    # Translate the grid
    processing.runAndLoadResults("native:translategeometry", {'INPUT':'Grille',
                                                'DELTA_X':0,
                                                'DELTA_Y':delta_y,
                                                'DELTA_Z':0,
                                                'DELTA_M':0,
                                                'OUTPUT':'TEMPORARY_OUTPUT'})
