import numpy as np
import math

import Algorithms.create_reducted_polygon as redpol
import Algorithms.centrogram_spacing_func as centrogram_finder


def index(array, item):
    """
    Function finds the index in the array where item is equal to the array entry.

    INPUT:
    array (NxN array) : array of any size to be checked
    item (float) : number to find inside array

    OUTPUT:
    idx (integer) : index value where "item" is found inside "array"
    """
    for idx, val in np.ndenumerate(array):
        if val == item:
            return idx


def fuel_limits(fuel_bounds, centrogram, centrogram_CG):
    """
    Function finds the strictest limits for take off and landing of all the inputted configurations.

    INPUT:
    fuel_bounds (2x8x4 array) : array of takeoff and landing weights and CGs for each configuration and SF
    centrogram (Nx3 array) : array of fuel weights and moments for fuel flow
    centrogram_CG (8xNx3 array) : new centrogram with weight (fuel + configuration), CG_x, and CG_y

    OUTPUT:
    TO_moment (1x3 array) : fuel weight, x moment, and y moment from centrogram at takeoff fuel limit
    landing_moment (1x3 array) : fuel weight, x moment, and y moment from centrogram at landing fuel limit
    """
    take_off_fuel = np.amin(fuel_bounds[:, :, 2])
    landing_fuel = np.amax(fuel_bounds[:, :, 0])

    # find index of max and min points within centrogram_CG array
    TO_index = index(centrogram_CG[:, :, 0], take_off_fuel)
    landing_index = index(centrogram_CG[:, :, 0], landing_fuel)

    # find corresponding fuel weight and moments for min and max fuel points
    TO_moment = centrogram[TO_index[1], :]
    landing_moment = centrogram[landing_index[1], :]

    print(TO_moment, landing_moment)
    return TO_moment, landing_moment


def fuel_in_envelope(
    envelope_x,
    envelope_y,
    empty_weight_CG,
    W_SF,
    CG_SF_x,
    CG_SF_y,
    fuel_flow,
    desired_interval,
):
    """
    This function takes an envelope and an input centrogram, then calls the
    interpolation function to create an evenly spaced, more detailed centrogram.
    Then it checks where that centrogram is within the envelope and chooses
    the largest area inside the envelope and returns the start and end points
    of that section.

    INPUT:
    envelope_x (Nx2 array) : array of weight and CG_x points that make up the envelope
    envelope_y (Nx2 array) : array of weight and CG_y points that make up the envelope
    empty_weight_CG (1x3 array) : plane zero-fuel weight, CG_x, CG_y
    fuel_flow (Nx3 array) : array of fuel flow (weight, X moment, Y moment)
    desired_interval (float) : desired interval of new centrogram in lb

    OUTPUT:
    centrogram_CG (8xNx3 array) : new centrogram with weight (fuel + configuration), CG_x, and CG_y
    """
    SF_points = redpol.apply_safety_factors(W_SF, CG_SF_x, CG_SF_y, empty_weight_CG)
    centrogram = centrogram_finder.centrogram_spacing(
        fuel_flow, desired_interval
    )  # outputs Nx3 array (weight, x moment, y moment)
    centrogram_CG = np.zeros(shape=(8, len(centrogram), 3))
    for k in range(8):
        for n in range(len(centrogram)):  # convert centrogram to weight and CG
            centrogram_CG[k][n][0] = centrogram[n][0] + SF_points[k][0]
            centrogram_CG[k][n][1] = (
                (SF_points[k][0] * SF_points[k][1]) + (centrogram[n][1])
            ) / centrogram_CG[k][n][0]
            centrogram_CG[k][n][2] = (
                (SF_points[k][0] * SF_points[k][2]) + (centrogram[n][2])
            ) / centrogram_CG[k][n][0]

    fuel_bounds = np.empty(
        shape=(2, 8, 4)
    )  # start and end points of largest section of each centrogram run, both x and y
    # *** should only be 2x4x4 because 4 are the same in each run when running both x (right/left) and y (forward/aft)

    for p in range(1, 3):  # check first in x-axis, then y-axis
        # check where centrogram is within envelope
        if p == 1:
            fuel_inside_envelope = redpol.check_point_in_polygon(
                envelope_x, centrogram_CG[:, :, [0, p]]
            )
        if p == 2:
            fuel_inside_envelope = redpol.check_point_in_polygon(
                envelope_y, centrogram_CG[:, :, [0, p]]
            )

        # Desired function so points aren't run twice unnecessarily
        # if p == 1:
        #     fuel_inside_envelope = redpol.check_point_in_polygon(envelope_x, centrogram_CG[[0, 1, 2, 3], :, [0, p]])
        # if p == 2:
        #     fuel_inside_envelope = redpol.check_point_in_polygon(envelope_y, centrogram_CG[[0, 1, 4, 5], :, [0, p]])
        # find largest area of centrogram within envelope

        for k in range(8):
            inside_length = 0
            change_points = np.zeros(shape=(1, 2))
            for n in range(len(centrogram)):
                if fuel_inside_envelope[k][n] == True:  # if point is within envelope
                    inside_length += 1
                # if point is outside envelope, but previous point was within envelope
                elif fuel_inside_envelope[k][n] == False and inside_length >= 1:
                    change_points = np.append(
                        change_points, [np.append(n - 1, inside_length)], axis=0
                    )
                    inside_length = 0

            # find index of end point of largest centrogram area inside
            if (
                fuel_inside_envelope[k].all() == True
            ):  # if entire centrogram is within envelope
                start_index = int(0)
                end_index = int(
                    len(fuel_inside_envelope[k]) - 1
                )  # requires -1 to avoid index overrrun
            else:  # if any part of centrogram is outside envelope
                max_pts = np.amax(change_points[:, 1])
                max_pts_index = np.where(change_points == np.amax(change_points[:, 1]))
                max_coords = list(zip(max_pts_index[0]))
                for cord in max_coords:
                    k_max_val = change_points[cord, 0]
                # find start and end points of centrogram area inside envelope
                start_index = int(
                    k_max_val - max_pts + 1
                )  # Requires +1 to avoid index of -1
                end_index = int(k_max_val)

            start_fuel = np.zeros(
                shape=(1, 2)
            )  # if all of centrogram is outside envelope
            end_fuel = np.zeros(shape=(1, 2))
            if (
                fuel_inside_envelope.any() != False
            ):  # if any part of centrogram is within envelope
                start_fuel = centrogram_CG[k, start_index, [0, p]]
                end_fuel = centrogram_CG[k, end_index, [0, p]]

            if end_fuel.any() == 0:
                # raise ValueError("Entire centrogram is outside envelope.")
                print("Entire centrogram is outside envelope.")

            fuel_bounds[p - 1, k, [0, 1]] = start_fuel
            fuel_bounds[p - 1, k, [2, 3]] = end_fuel
            # print(start_fuel, end_fuel)
    print(fuel_bounds)

    takeoff_fuel, landing_fuel = fuel_limits(fuel_bounds, centrogram, centrogram_CG)

    return centrogram_CG


def fuel_in_envelope_bisection(
    envelope_x,
    envelope_y,
    empty_weight_CG,
    W_SF,
    CG_SF_x,
    CG_SF_y,
    fuel_flow,
    desired_interval,
):
    """
    This function takes an envelope and an input centrogram, then calls the
    interpolation function to create an evenly spaced, more detailed centrogram.
    Then it checks where that centrogram is within the envelope and chooses
    the largest area inside the envelope and returns the start and end points
    of that section.

    INPUT:
    envelope_x (Nx2 array) : array of weight and CG_x points that make up the envelope
    envelope_y (Nx2 array) : array of weight and CG_y points that make up the envelope
    empty_weight_CG (1x3 array) : plane zero-fuel weight, CG_x, CG_y
    fuel_flow (Nx3 array) : array of fuel flow (weight, X moment, Y moment)
    desired_interval (float) : desired interval of new centrogram in lb

    OUTPUT:
    centrogram_CG (8xNx3 array) : new centrogram with weight (fuel + configuration), CG_x, and CG_y
    """
    SF_points = redpol.apply_safety_factors(W_SF, CG_SF_x, CG_SF_y, empty_weight_CG)
    centrogram = centrogram_finder.centrogram_spacing(
        fuel_flow, desired_interval
    )  # outputs Nx3 array (weight, x moment, y moment)
    centrogram_CG = np.zeros(shape=(8, len(centrogram), 3))
    for k in range(8):
        for n in range(len(centrogram)):  # convert centrogram to weight and CG
            centrogram_CG[k][n][0] = centrogram[n][0] + SF_points[k][0]
            centrogram_CG[k][n][1] = (
                (SF_points[k][0] * SF_points[k][1]) + (centrogram[n][1])
            ) / centrogram_CG[k][n][0]
            centrogram_CG[k][n][2] = (
                (SF_points[k][0] * SF_points[k][2]) + (centrogram[n][2])
            ) / centrogram_CG[k][n][0]

    fuel_bounds = np.empty(
        shape=(2, 8, 4)
    )  # start and end points of largest section of each centrogram run, both x and y
    # *** should only be 2x4x4 because 4 are the same in each run when running both x (right/left) and y (forward/aft)

    for p in range(1, 3):  # check first in x-axis, then y-axis
        # check where centrogram is within envelope
        if p == 1:
            fuel_inside_envelope = redpol.check_point_in_polygon(
                envelope_x, centrogram_CG[:, :, [0, p]]
            )
        if p == 2:
            fuel_inside_envelope = redpol.check_point_in_polygon(
                envelope_y, centrogram_CG[:, :, [0, p]]
            )

        #  # Desired function so points aren't run twice unnecessarily
        # if p == 1:
        #     fuel_inside_envelope = redpol.check_point_in_polygon(envelope_x, centrogram_CG[[0, 1, 2, 3], :, [0, p]])
        # if p == 2:
        #     fuel_inside_envelope = redpol.check_point_in_polygon(envelope_y, centrogram_CG[[0, 1, 4, 5], :, [0, p]])
        # find largest area of centrogram within envelope
        for k in range(8):
            # inside_length = 0
            change_points = np.zeros(shape=(1, 2))
            # find index of end point of largest centrogram area inside
            if (
                fuel_inside_envelope[k].all() == True
            ):  # if entire centrogram is within envelope
                start_index = int(0)
                end_index = int(
                    len(fuel_inside_envelope[k]) - 1
                )  # requires -1 to avoid index overrrun
            # elif fuel_inside_envelope[k].all() == False:
            #     # raise ValueError("Entire centrogram is outside envelope.")
            #     print("Entire centrogram is outside envelope.")
            else:  # if any part of centrogram is outside envelope
                # find change points
                bisection(
                    k, 0, len(centrogram) - 1, fuel_inside_envelope, change_points
                )
                max_pts = np.amax(change_points[:, 1])
                max_pts_index = np.where(change_points == np.amax(change_points[:, 1]))
                max_coords = list(zip(max_pts_index[0]))
                for cord in max_coords:
                    k_max_val = change_points[cord, 0]
                # find start and end points of centrogram area inside envelope
                start_index = int(
                    k_max_val - max_pts + 1
                )  # Requires +1 to avoid index of -1
                end_index = int(k_max_val)

            start_fuel = np.zeros(
                shape=(1, 2)
            )  # if all of centrogram is outside envelope
            end_fuel = np.zeros(shape=(1, 2))
            if (
                fuel_inside_envelope.any() != False
            ):  # if any part of centrogram is within envelope
                start_fuel = centrogram_CG[k, start_index, [0, p]]
                end_fuel = centrogram_CG[k, end_index, [0, p]]

            if end_fuel.any() == 0:
                # raise ValueError("Entire centrogram is outside envelope.")
                print("Entire centrogram is outside envelope.")

            fuel_bounds[p - 1, k, [0, 1]] = start_fuel
            fuel_bounds[p - 1, k, [2, 3]] = end_fuel
            # print(start_fuel, end_fuel)
    print(fuel_bounds)

    takeoff_fuel, landing_fuel = fuel_limits(fuel_bounds, centrogram, centrogram_CG)

    return centrogram_CG


def bisection(k, n1, n2, fuel_inside_envelope, change_points):
    """
    This function iteratively find the change points of the centogram using a bisection method 

    INPUT:
    k (float): an index 
    n1 (float): the smaller index
    n2 (float): the bigger index
    fuel_inside_envelope (2x8x4 array) : array of boolean values pointing if a point in the centrogram is in the envelope
    change_points (1x2 array): array of change point of the centrogram

    OUTPUT:
    change_points (1x2 array): updated array of change point of the centrogram 
    """
    if fuel_inside_envelope[k][n1] == fuel_inside_envelope[k][n2]:
        return change_points
    # setting the middle index
    n = round((n2 - n1) / 2) + n1
    if fuel_inside_envelope[k][n] == True:  # the middle point is still in the envelope
        if (
            fuel_inside_envelope[k][n + 1] == False
        ):  # check if the middle point is the change point
            change_points = np.append(change_points, [np.append(n, n + 1)], axis=0)
            return change_points
        else:
            bisection(k, n, n2, fuel_inside_envelope, change_points)  # iteration
    elif (
        fuel_inside_envelope[k][n - 1] == True
    ):  # check if the middle point is the change point
        change_points = np.append(change_points, [np.append(n - 1, n)], axis=0)
        return change_points
    else:
        bisection(k, n1, n, fuel_inside_envelope, change_points)  # iteration
