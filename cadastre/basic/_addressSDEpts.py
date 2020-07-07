#

import arcpy

def addressSDEpts(fips, addrPts, parcelFld):
    print(' ** Getting addresses from SDE Address Points')

    exp = "{0} = {2} and Not {1} IS Null and {1} != '' and {1} != ' '".format('CountyID', 'ParcelID', fips)
    print(exp, 'is exp')

    arcpy.MakeFeatureLayer_management(addrPts, 'addrFl', exp)

    count = int(arcpy.GetCount_management('addrFl').getOutput(0))
    print(str(count), 'features in SDE Address Points Feature Layer')

    addrDict = dict([(r[0], r[1]) for r in arcpy.da.SearchCursor('addrFl', ['ParcelID', 'FullAdd'])])

    with arcpy.da.UpdateCursor('parFl', [parcelFld, 'PT_ADDRESS', 'PARCEL_ADD']) as urows:
        for urow in urows:

            if urow[0] in addrDict:
                urow[1] = addrDict[urow[0]]
                urow[2] = addrDict[urow[0]]
            urows.updateRow(urow)

    arcpy.Delete_management('parFl')
    arcpy.Delete_management('addrFl')







### DAVIS FIX
##def addressSDEpts(fips, addrPts, parcelFld):
##    print(' ** Getting addresses from SDE Address Points')
##
####    exp = "{0} = {2} and Not {1} IS Null and {1} != '' and {1} != ' '".format('CountyID', 'ParcelID', fips)
####    print(exp, 'is exp')
##
##    arcpy.MakeFeatureLayer_management(addrPts, 'addrFl')#, exp)
##
##    addrDict = dict([(r[0], r[1]) for r in arcpy.da.SearchCursor('addrFl', ['ParcelID', 'MasterAddr'])])
##
##    with arcpy.da.UpdateCursor('parFl', [parcelFld, 'PT_ADDRESS', 'PARCEL_ADD']) as urows:
##        for urow in urows:
##
##            if urow[0] in addrDict:
##                urow[1] = addrDict[urow[0]]
##                urow[2] = addrDict[urow[0]]
##            urows.updateRow(urow)
##
##    arcpy.Delete_management('parFl')