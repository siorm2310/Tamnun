import numpy as np
import math
from shapely.geometry import LineString, Point
from shapely.geometry.polygon import Polygon
import os

def is_nan(x):
    '''
    This function checks if the input value is not a number (NaN).

    INPUT:
    x (float) : number

    OUTPUT:
    True / False result of whether or not x is NaN
    '''
    return (x is np.nan or x != x)  # two ways to check if x is NaN

def perp(a):
    '''
    Function is used in find_lines_intersection function.

    INPUT:
    a (1x2 array) : x, y slope

    OUTPUT:
    b (1x2 array) : x, y slope perpendicular to input a
    '''
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b

def find_lines_intersection (a1,a2,b1,b2):
    '''
    This function finds the intersection point of 2 straight lines,
    which are defined by their endpoints

    INPUT:
    a1,a2 (2 arrays of size 1x2) : points of line A
    b1,b2 (2 arrays of size 1x2) : points of line B

    OUTPUT:
    intersect (1x2 array) : point of intersection
    '''
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    
    dap = perp(da)
    denom = np.dot(dap , db)
    num = np.dot(dap , dp)
    intersect = (num / denom.astype(float)) * db + b1

    return intersect

def calculate_distance (a, b):
    '''
    This function calculates the distance between two points.

    INPUT:
    a1, b1 (2 arrays of size 1x2) : two points with (x,y) coordinates

    OUTPUT:
    dist (float) : distance between a1 and b1
    '''
    x1 = a[0]
    y1 = a[1]
    x2 = b[0]
    y2 = b[1]

    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def check_point_in_polygon (polygon, points):
    '''
    This function checks if points are inside of polygon.
    The function returns True value for each point inside of the polygon
    and False value otherwise

    INPUT:
    polygon (Nx2 array) : x,y values of the points defining the polygon
    points (Nx2 array) : x,y values of the points tested

    OUTPUT:
    results (Nx1 array) : True \ False values for in polygon in order of points from input
    '''
    
    polygon = Polygon(polygon) # Coerce data to Shaply's POLYGON data type

    if len(points) > 2: # if more than one point is passed as an input to be checked
        results = np.zeros(shape = (len(points), 1), dtype = bool)
        for n in range(len(points)):
            point = Point(points[n][:])
            results[n] = polygon.contains(point)
            if results[n] == False: # if not within, does it intersect the boundaries
                results[n] = polygon.intersects(point)
                if results[n] == False: # if not within or intersecting, does it touch the edge
                    results[n] = polygon.touches(point)
                    if results[n] == False:
                        # if all of the above fail, likely a floating point precision error,
                        # so now we use distance to check if it's really on the line or not
                        if polygon.distance(point) <= 0.01:
                            results[n] = True

    else:   # if only one point is being checked
        point = Point(points)
        results = polygon.contains(point)
        if results == False:
            results = polygon.intersects(point)
            if results == False:
                results = polygon.touches(point)
                if results == False:
                    if polygon.distance(point) <= 0.01:
                        results = True
    return results

def apply_safety_factors (W_SF, CG_SF ,point, MAC = None):
    '''
    This function applies safety factors to a given point

    INPUT:
    W_SF (float) : weight safety factor, given in [%]
    CF_SF (float) : CG safety factor, given either in %MAC format or float number format
    point (1x2 array) : Desired point [weight, CG]
    RLE,MAC (float) : Wing properties of platform (if exist. by default is None)

    OUTPUT:
    SF_points (4x2 array) : points w\ safety factors. ordered clockwise, i.e:
        [HEAVY & AFT , LIGHT & AFT , LIGHT & FWD, HEAVY & FWD]
    '''

    if MAC is not None:
        CG_SF_MAC = (CG_SF/100) * MAC

        p1 = [point[0] * (1 + (W_SF/100)) , point[1] + CG_SF_MAC]   # heavy, aft
        p2 = [point[0] * (1 - (W_SF/100)) , point[1] + CG_SF_MAC]   # light, aft
        p3 = [point[0] * (1 - (W_SF/100)) , point[1] - CG_SF_MAC]   # light, forward
        p4 = [point[0] * (1 + (W_SF/100)) , point[1] - CG_SF_MAC]   # heavy, forward

        return np.array([p1, p2, p3, p4])

    else:
        p1 = [point[0] * (1 + (W_SF/100)) , point[1] + CG_SF]
        p2 = [point[0] * (1 - (W_SF/100)) , point[1] + CG_SF]
        p3 = [point[0] * (1 - (W_SF/100)) , point[1] - CG_SF]
        p4 = [point[0] * (1 + (W_SF/100)) , point[1] - CG_SF]

        return np.array([p1, p2, p3, p4])

def zero_point_case(k, original_polygon, reduced_polygon, possible_polygon_points):
    '''
    This function finds the proper point in the reduced polygon for the zero point case.

    INPUT:
    k (int) : vertex point number
    original_polygon (Nx2 array) : x,y coordinates of the original polygon with N vertices
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format, 
        but at this point only up to vertex k
    possible_polygon_points (4xNx2 array) : array of all SF points with x,y coordinates
    
    OUTPUT:
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format,
        where M is 1 greater than the input version of the reduced_polygon array
    '''
    zero_point = np.array([0, 0])
    point_number = 0
    intersect_points = np.empty(shape = (12, 2))
    no_vertex_point = np.zeros(shape = (12, 5), dtype = bool)
    for n in range(4):
        for z in range(1,4):
            if k==(len(original_polygon)-1):
                # if k is last point in polygon, then next point in sequence is 1
                # (2nd point in polygon, equivalent of k+1 for other points)
                # since last point and first point in polygon are same point
                intersect_points[point_number][:] = find_lines_intersection(possible_polygon_points[n][k-1][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][k][:], possible_polygon_points[n-z][1][:])
            elif k == 0:
                # if k is first point, then previous point is k = -2 (second to last point)
                intersect_points[point_number][:] = find_lines_intersection(possible_polygon_points[n][-2][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][k][:], possible_polygon_points[n-z][k+1][:])
            else:
                intersect_points[point_number][:] = find_lines_intersection(possible_polygon_points[n][k-1][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][k][:], possible_polygon_points[n-z][k+1][:])
            point_number += 1
    for m in range(len(intersect_points)):
        no_vertex_point[m][0] = check_point_in_polygon(original_polygon, intersect_points[m][:])
        for n in range(4):
            no_vertex_point[m][n+1] = check_point_in_polygon(possible_polygon_points[n][:][:], intersect_points[m][:])
    
    point_added = False # variable to track if intersect point was added to reduced polygon
    for p in range(len(intersect_points)):
        if no_vertex_point[p][:].all() == True:
            if is_nan(intersect_points[p][0]) == False and is_nan(intersect_points[p][1]) == False:
                if intersect_points[p][:].any() != 'inf' and intersect_points[p][:].any() != '-inf':
                    reduced_polygon = np.append(reduced_polygon, [np.append(intersect_points[p][:], 0)], axis=0)
                    point_added = True
    
    if point_added == False:
        # If not, go to next polygon line to make intersection lines (between k+1 and k+2)
        for cycle in range(2, len(original_polygon)):   # Go until point is found or full cycle of polygon has been completed
            if point_added == False:
                point_number = 0
                intersect_points_cycle = np.empty(shape = (16, 2))
                no_vertex_point_cycle = np.zeros(shape = (16, 5), dtype = bool)
                for n in range(4):
                    for z in range(4):
                        # if k + cycle is >= number of points in original_polygon,
                        # then k + cycle will overrun the index, must look at index of k + cycle - len(original_polygon)
                        if k + cycle >= len(original_polygon): 
                            difference = k + cycle - len(original_polygon)
                            intersect_points_cycle[point_number][:] = find_lines_intersection(possible_polygon_points[n][k-1][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][difference - 1][:], possible_polygon_points[n-z][difference][:])
                        elif k == 0:
                            intersect_points_cycle[point_number][:] = find_lines_intersection(possible_polygon_points[n][-2][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][k + cycle - 1][:], possible_polygon_points[n-z][k + cycle][:])
                        else:
                            intersect_points_cycle[point_number][:] = find_lines_intersection(possible_polygon_points[n][k-1][:], possible_polygon_points[n][k][:], possible_polygon_points[n-z][k + cycle - 1][:], possible_polygon_points[n-z][k + cycle][:])
                        point_number += 1
                for m in range(len(intersect_points_cycle)):
                    no_vertex_point_cycle[m][0] = check_point_in_polygon(original_polygon, intersect_points_cycle[m][:])
                    for n in range(4):
                        no_vertex_point_cycle[m][n+1] = check_point_in_polygon(possible_polygon_points[n][:][:], intersect_points_cycle[m][:])
                for p in range(len(intersect_points_cycle)):
                    if no_vertex_point_cycle[p][:].all() == True:
                        if is_nan(intersect_points_cycle[p][0]) == False and is_nan(intersect_points_cycle[p][1]) == False:
                            if intersect_points_cycle[p][:].any() != 'inf' and intersect_points_cycle[p][:].any() != '-inf':
                                reduced_polygon = np.append(reduced_polygon, [np.append(intersect_points_cycle[p][:], 0)], axis=0)
                                point_added = True
    return reduced_polygon

def one_point_case(k, reduced_polygon, points_passed, possible_polygon_points):
    '''
    This function finds the proper point in the reduced polygon for the single point case.

    INPUT:
    k (int) : vertex point number
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format, 
        but at this point only up to vertex k
    points passed (4xNx3 array) : array of all SF polygons with their x,y coordinates and an indicator if the point is within all 5 polygons
    possible_polygon_points (4xNx2 array) : array of all SF points with x,y coordinates
    
    OUTPUT:
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format,
        where M is 1 greater than the input version of the reduced_polygon array
    '''
    for n in range(4):
        if points_passed[n][k][2] == 1:     # 1 marks that point is within all polygons
            reduced_polygon = np.append(reduced_polygon, [np.append(possible_polygon_points[n][k][:], 0)], axis=0)
            break
    return reduced_polygon

def two_point_case(k, reduced_polygon, points_passed, possible_polygon_points):
    '''
    This function finds the proper point in the reduced polygon for the two point case.

    INPUT:
    k (int) : vertex point number
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format, 
        but at this point only up to vertex k
    points passed (4xNx3 array) : array of all SF polygons with their x,y coordinates and an indicator if the point is within all 5 polygons
    possible_polygon_points (4xNx2 array) : array of all SF points with x,y coordinates
    
    OUTPUT:
    reduced_polygon (Mx2 array) : array of points that make up the reduced polygon in x,y coordinate format,
        where M is 1 greater than the input version of the reduced_polygon array
    '''
    if reduced_polygon[0][0] == 0:
        for n in range(4):
            if points_passed[n][k][2] == 1:
                reduced_polygon = np.append(reduced_polygon, [np.append(possible_polygon_points[n][k][:], 1)], axis=0)
    else:
        point_A = np.zeros(shape = (1, 2))
        for n in range(4):
            if points_passed[n][k][2] == 1:
                if point_A[:][:].any() != 0:
                    point_B = possible_polygon_points[n][k][:]
                else:
                    point_A = possible_polygon_points[n][k][:]
        distance_1 = calculate_distance(reduced_polygon[-1][:], point_A)
        distance_2 = calculate_distance(reduced_polygon[-1][:], point_B)

        if distance_1 <= distance_2:
            reduced_polygon = np.append(reduced_polygon, [np.append(point_A, 0)], axis=0)
            reduced_polygon = np.append(reduced_polygon, [np.append(point_B, 0)], axis=0)
        else:
            reduced_polygon = np.append(reduced_polygon, [np.append(point_B, 0)], axis=0)
            reduced_polygon = np.append(reduced_polygon, [np.append(point_A, 0)], axis=0)
    return reduced_polygon

def reduce_polygon(original_polygon, W_SF, CG_SF, MAC = None):
    '''
    This function creates an array containing the points for each SF polygon
    and a 0 or 1 to show whether that point is found within all 5 polygons (0 = no, 1 = yes).
    Then it takes that array and checks using the (0, 1, 2 point) method to see what points make up the reduced polygon.
    The function finally outputs an array of points that make up the final reduced polygon.

    INPUT:
    original_polygon (Nx2 array) : x,y coordinates of the original polygon with N vertices
    W_SF (float) : weight safety factor, given in [%]
    CF_SF (float) : CG safety factor, given either in %MAC format or float number format
    MAC (float) (if applicable) : MAC of aircraft to be used to find SF points

    OUTPUT:
    possible_polygon_points (4xNx2 array) : array of all SF points (4 SF polygons of N points)
    reduced_polygon (Nx2 array) : array of points that make up the reduced polygon in x,y coordinate format
    '''
    points_passed = np.zeros(shape = (4, len(original_polygon), 3))
    possible_polygon_points = np.zeros(shape = (4, len(original_polygon), 2))
    point_check = np.zeros(shape = (4, len(original_polygon), 5), dtype = bool)

    for k in range(len(original_polygon)):    # creates array of SF points for each polygon
        point = np.array(original_polygon[k][:])
        if MAC is not None:
            SF_points = apply_safety_factors(W_SF, CG_SF, point, MAC)
        else:
            SF_points = apply_safety_factors(W_SF, CG_SF, point)
        for d in range(4):
            possible_polygon_points[d][k][:] = SF_points[d]

    for k in range(len(original_polygon)):    # check SF points against all 5 polygons; k = number of points in original polygon
        for p in range(4):  # p = number of SF polygons
            point_check[p][k][0] = check_point_in_polygon(original_polygon, possible_polygon_points[p][k][:])
            for n in range(4):
                point_check[p][k][n+1] = check_point_in_polygon(possible_polygon_points[n][:][:], possible_polygon_points[p][k][:])
                points_passed[n][k][0] = possible_polygon_points[n][k][0]   # assign X,Y coordinates of all points to proper place in points_passed array
                points_passed[n][k][1] = possible_polygon_points[n][k][1]
            # assign 1 values to third column of points_passed array to show which points are within all 5 polygons
            if point_check[p][k][:].all() == True:
                points_passed[p][k][2] = 1
    # At this point we have checked all the SF points to see if they are inside all 5 polygons.
    # Now we need to see if we have 0, 1, or 2 points inside at each vertex.

    reduced_polygon = np.empty(shape = (0, 3))

    for k in range(len(original_polygon)):
        point_sum = 0   # variable used to show which case is applicable (0, 1, or 2 point cases)
        for n in range(4):
            point_sum += points_passed[n][k][2]

        if point_sum == 0:    # if no SF points at vertex K are within all 5 polygons, use line intersection method
            reduced_polygon = zero_point_case(k, original_polygon, reduced_polygon, possible_polygon_points)

        elif point_sum == 1:  # if only 1 SF point is within all 5 polygons, then it is automatically part of the reduced polygon
            reduced_polygon = one_point_case(k, reduced_polygon, points_passed, possible_polygon_points)
            
        elif point_sum == 2:  # if 2 SF points are within all 5 polygons, must determine the order they appear in the reduced polygon
            # if 2 point case is the first point checked, then add them to the reduced polygon in the order they appear,
            # later go back and check that the points are in the correct order
            reduced_polygon = two_point_case(k, reduced_polygon, points_passed, possible_polygon_points)

        else:
            raise ValueError("Error: More than 3 SF points found inside all polygons at a single vertex. Not possible.")


    # if first point in reduced polygon was a 2 point case,
    # now check if points were added in correct order.
    if reduced_polygon[0][2] == 1:
        if reduced_polygon[1][2] == 1:
            point_A = np.array([reduced_polygon[0][:]])
            point_B = np.array([reduced_polygon[1][:]])

            distance_1 = calculate_distance(reduced_polygon[-1][:], point_A)
            distance_2 = calculate_distance(reduced_polygon[-1][:], point_B)

            if distance_2 < distance_1:
                reduced_polygon[0][:] = point_B
                reduced_polygon[1][:] = point_A
        else:
            # If only one point was marked as a 2 point case at start of point list, then there's an error.
            raise ValueError("Error: only one point marked as 2 point case at start of polygon. Must have 2 points marked, not just 1.")

    reduced_polygon = np.delete(reduced_polygon, 2, axis = 1)

    # check that first and last points in reduced_polygon are the same points so polygon can be a closed shape.
    if reduced_polygon[0][0] != reduced_polygon[-1][0] and reduced_polygon[0][1] != reduced_polygon[-1][1]:
        reduced_polygon = np.append(reduced_polygon, [reduced_polygon[0][:]], axis=0)

    return [possible_polygon_points, reduced_polygon]
    # return reduced_polygon


if __name__ == "__main__":
    weight = []
    cg = []
    with open('abc.txt','r') as polygon_file:
        for row in polygon_file:
            splitted_row = row.split()
            weight.append(float(splitted_row[0]))
            cg.append(float(splitted_row[1]))
        print(weight)
        print(cg)
