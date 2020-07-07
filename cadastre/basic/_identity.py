# Point Identity Analysis on Land Ownership, Zip Codes, and Municipalities

import arcpy


def identity(parcelPts, landOwn, owner, zipCodes, zips, munis, parcelPtsFinal, newParcelsFinal):
    print('Point Identity Analysis on Land Ownership, Zip Codes, and Municipalities')

    fcs = [owner, zips, parcelPtsFinal, newParcelsFinal]

    for fc in fcs:

        if arcpy.Exists(fc):
            arcpy.Delete_management(fc)

    arcpy.Identity_analysis(parcelPts, landOwn, owner)

    arcpy.Identity_analysis(owner, zipCodes, zips)

    arcpy.Identity_analysis(zips, munis, parcelPtsFinal)
