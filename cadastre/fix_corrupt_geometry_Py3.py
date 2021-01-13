'''
fix_corrupt_geometries.py

A module that contains code for fixing geometries that stubbornly refused to give you their WKT

This code assumes that the OBJECTIDs are sequential.

Example usage:
from fix_corrupt_geometries import fix

fix(r'path/to/data')
'''
import arcpy

sql_clause = (None, 'ORDER BY OBJECTID')
error_ids = []


def _try_next(cur, last_oid):
    try:
        oid, wkt = cur.next()
        return oid
    except RuntimeError:
        print('error with {}'.format(last_oid + 1))
        error_ids.append(str(last_oid + 1))
        return -1
    except StopIteration:
        return False


def fix(dataset):
    print('finding issues')
    with arcpy.da.SearchCursor(dataset, ['OID@', 'Shape@WKT'], sql_clause=sql_clause) as cur:
        status = _try_next(cur, 0)
        while status:
            status = _try_next(cur, status)

    if len(error_ids) > 0:
        print('fixing data NOT')
        with arcpy.da.UpdateCursor(dataset, ['OID@', 'Shape@'], 'OBJECTID IN ({})'.format(','.join(error_ids)), sql_clause=sql_clause) as ucur:
            print('OBJECTID IN ({})'.format(','.join(error_ids)))
            for oid, shape in ucur:
                ucur.updateRow((oid, shape))
    else:
        print('no issues found')


if __name__ == '__main__':
    import sys
    fix(sys.argv[1])
