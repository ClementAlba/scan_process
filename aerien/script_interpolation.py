from grass.pygrass.modules import Module

from grass.script import core as grass


def create_new_location():
    grass.create_location("D:\\APPS\\WinGRASS", "location_heron", 2154)

    Module("g.mapset",
           flags="c",
           mapset="MAPSET_HERON",
           location="location_heron"
          )


def import_file():
    Module("v.in.lidar",
           flags="tbo",
           input="D:\\Documents\\MISSIONS\\interpolation_raster\\input\\heron_min2.las",
           output="heron_import@MAPSET_HERON",

           class_filter=2,

           overwrite=True
          )



def command():
    Module("g.region",
           vector="heron_import@MAPSET_HERON",
           n=7060385,
           s=7059161,
           e=713007,
           w=711393,
           res=0.3
          )


    Module("v.surf.rst",
           input="heron_import@MAPSET_HERON",
           elevation="heron_elevation",
           smooth=2,
           dmin=10,
           segmax=1200,
           npmin=1600
          )


    Module("r.out.gdal",
           input="heron_elevation@MAPSET_HERON",
           output="D:\\Documents\\MISSIONS\\interpolation_raster\\output\\heron.tif",
           format="GTiff"
          )



if __name__ == "__main__":
    create_new_location()
    import_file()
    command()