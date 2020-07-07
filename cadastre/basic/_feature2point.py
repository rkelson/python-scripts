#

import arcpy


def feature2point(parcelPts, newParcels):

    print('Turning', newParcels, 'into Points')

    if arcpy.Exists(parcelPts):

        print(' Exists - Deleting', parcelPts)

        arcpy.Delete_management(parcelPts)

    arcpy.FeatureToPoint_management(newParcels, parcelPts, "INSIDE")


def feature2point_2(parcelPts, newParcels):

    if not arcpy.Exists(parcelPts):

        print('Turning', newParcels, 'into Points on second attempt')

        arcpy.FeatureToPoint_management(newParcels, parcelPts, "INSIDE")