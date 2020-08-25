""" centrogram spacing algorithm and calculation of single centrogram's limits on a single envelope"""

import numpy as np
import math
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point


def index(array, item):
    """
    Matches index with array value
    """
    for idx, val in np.ndenumerate(array):
        if val == item:
            return idx


def centrogram_spacing(centrogram, desired_interval):
    """Interpolates centrogram data to a desired spacing

    Arguments:
        centrogram {list[Weights,[moments]]} -- centrogram to be interpolated (Weight-Moment)
        desired_interval {float} -- spacing required for centrogram

    Returns:
        list[[weights],[moments]] evenly-spaced centrogram
    """
    start_weight = centrogram[0][0]
    end_weight = centrogram[0][-1]
    length_of_output = int(round((end_weight - start_weight)/desired_interval) + 1)

    weights = [start_weight + desired_interval * n for n in range(length_of_output)]

    if weights[-1] > end_weight:
        weights.pop()
    if weights[-1] < end_weight:
        weights.append(end_weight)

    moments = np.interp(weights, centrogram[0], centrogram[1])

    return [weights, list(moments)]


def check_point_in_polygon(polygon_input, point_input):
    """Checks whether a point is within a closed polygon, according to BAKAT's definition

    Arguments:
        polygon_input {list(tuple(Weight,CG))} -- list containing tuple pairs of Weight, CG values
        point_input {tuple(x,y)} 
    Returns:
        [boolean] -- True if within polygon, false otherwise
    """
    DISTANCE_TOL = 0.01
    polygon = Polygon(polygon_input)
    point = Point(point_input)

    if polygon.contains(point) or polygon.intersects(point) or polygon.touches(point) or polygon.distance(point) <= DISTANCE_TOL:
        return True
    return False


def bisection(n1, n2, fuel_inside_envelope, change_points):
    """
    This function iteratively find the change points of the centogram using a bisection method 

    INPUT:
    n1 (float): the smaller index
    n2 (float): the bigger index
    fuel_inside_envelope (2x8x4 array) : array of boolean values pointing if a point in the centrogram is in the envelope
    change_points (1x2 array): array of change point of the centrogram

    OUTPUT:
    change_points (1x2 array): updated array of change point of the centrogram 
    """
    if fuel_inside_envelope[n1] == fuel_inside_envelope[n2]:
        return change_points
    n = round((n2 - n1) / 2) + n1  # setting the middle index

    if fuel_inside_envelope[n] == True:  # the middle point is still in the envelope
        if (fuel_inside_envelope[n + 1] == False):  # check if the middle point is the change point
            change_points = np.append(
                change_points, [np.append(n, n + 1)], axis=0)
            return change_points
        else:
            bisection(n, n2, fuel_inside_envelope,
                      change_points)  # Recursive call
    elif (fuel_inside_envelope[n - 1] == True):  # check if the middle point is the change point
        change_points = np.append(change_points, [np.append(n - 1, n)], axis=0)
        return change_points
    else:
        bisection(n1, n, fuel_inside_envelope, change_points)  # Recursive call


def fuel_limits_finder(envelope, centrogram):

    centrogram_status = []

    for point in centrogram:
        centrogram_status.append(check_point_in_polygon(envelope, point))

    if all(centrogram_status) == True:
        print("Full fuel")
        return [centrogram[0], centrogram[-1]]

    if all(centrogram_status) == False:
        print("No fuel")
        return [0, 0]

    change_points = np.zeros(shape=(1, 2))
    fuel_limits = bisection(
        0, centrogram_status.__len__(), centrogram_status, change_points)
    return fuel_limits
