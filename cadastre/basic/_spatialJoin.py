# spatial join

import  arcpy

def spatialJoin(newParcels, parcelPtsFinal, newParcelsFinal):

    if arcpy.Exists(newParcelsFinal):
        arcpy.Delete_management(newParcelsFinal)

    print('Creating Spatial Join Layer', newParcelsFinal)

    arcpy.SpatialJoin_analysis(newParcels, parcelPtsFinal, newParcelsFinal)
