#

import arcpy, shutil, os
from arcpy import env


def createGDBreproject(inGDBpath, coPath, gdb, parcels, newParcels, utmprj):

    if not arcpy.Exists(coPath):
        os.mkdir(coPath)

    if arcpy.Exists(inGDBpath):

        print(' Deleting', inGDBpath)
        # arcpy.Delete_management(inGDBpath)
        shutil.rmtree(inGDBpath)

    print(' * Creating', inGDBpath)
    arcpy.CreateFileGDB_management(coPath, gdb, '10.0')

    print(' ** Checking Projection')
    parcelsPRJ = arcpy.Describe(parcels).spatialReference
    print('    ', parcelsPRJ.name)

    if parcelsPRJ.name != utmprj.name:
        print(' *** Different Projections!')
        print(' **** Reprojecting to ' + newParcels)
        arcpy.Project_management(parcels, newParcels, utmprj)

    else:
        arcpy.CopyFeatures_management(parcels, newParcels)

    env.workspace = newParcels