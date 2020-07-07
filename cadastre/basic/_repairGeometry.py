#

import arcpy, time

def repairGeometry(newParcels, startTime):

    stopTime1 = time.clock();
    elapsedTime = stopTime1 - startTime;
    elapsedTime = elapsedTime / 60

    print('Time for operation:', str(round(elapsedTime, 1)), 'minutes')

    print('Repairing Geometry - Orig data')
    arcpy.RepairGeometry_management(newParcels, "DELETE_NULL")

    stopTime2 = time.clock();
    elapsedTime = stopTime2 - startTime;
    elapsedTime = elapsedTime / 60

    print('Time for operation:', str(round(elapsedTime, 1)), 'minutes')
