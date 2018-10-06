from osgeo import ogr, osr
from src.department import Department
from pyproj import Proj

department_shapefile_path = "provided-data/Dept_37-00027/37-00027_Shapefiles/APD_DIST.shp"
print("Hello")
department = Department(department_shapefile_path)

myproj = Proj(department.crs_string,preserve_units=True)

x = 10044935
y = 3115061
newcoord = myproj(y, x, inverse=True)
print(newcoord[1], newcoord[0])
print("Done")

# pointY = 3115061
# pointX = 10044935
#
# # Spatial Reference System
# inputEPSG = 3857
# outputEPSG = 4326
#
# # create a geometry from coordinates
# point = ogr.Geometry(ogr.wkbPoint)
# point.AddPoint(pointX, pointY)
#
# # create coordinate transformation
# inSpatialRef = osr.SpatialReference()
# inSpatialRef.ImportFromEPSG(inputEPSG)
#
# outSpatialRef = osr.SpatialReference()
# outSpatialRef.ImportFromEPSG(outputEPSG)
#
# coordTransform = osr.CoordinateTransformation(inSpatialRef, outSpatialRef)
#
# # transform point
# point.Transform(coordTransform)
#
# # print point in EPSG 4326
# print(point.GetX(), point.GetY())