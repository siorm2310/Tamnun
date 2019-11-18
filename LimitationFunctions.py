from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
import numpy as np


class LimitationFunctions:

    def __init__(self):
        pass

    @staticmethod
    def point_in_polygon(points, polygon):
        """
        This function checks wether a point (or points) are inside a polygon or envelope
        according to BAKAT definition
        :param points: (np.array(n,2)) an array of n points to be checked
        :param polygon:(np.array(1,m)) closed polygon or envelpoe
        :return: np.array(1,n) boolean list. True if point n is inside, false otherwise
        """
        poly = Polygon(polygon)

        if np.size(points[:][0]) == 1:
            checked_point = Point(points)
            if poly.contains(checked_point) or poly.intersects(checked_point) or poly.touches(checked_point):
                return np.array([True])
            else:
                return np.array([False])
        else:
            list_points = []
            for x, y in points:
                checked_point = Point(x, y)
                if poly.contains(checked_point) or poly.intersects(checked_point) or poly.touches(checked_point):
                    list_points.append(True)
                else:
                    list_points.append(False)
            return np.array(list_points)

    @staticmethod
    def apply_safety_factor(W_SF, CG_SF, point, MAC = None):
        """
        This function applies safety factors to a given point
        :param W_SF: (float) weight safety factor, given in [%]
        :param CG_SF: (float) CG safety factor, given either in [%MAC] or float number [%]
        :param point:(np.array) Desired point [weight, CG]
        :param MAC: (float) Wing property of A.C (if exist)
        :return: (np.array [2,4]) points with safety factors, ordered clockwise :
                [H & A , L & A , L & F , H & F]
        """
        if MAC is not None:
            CG_SF_MAC = (CG_SF/100) * MAC

            p1 = [point[0] * (1 + (W_SF / 100)), point[1] + CG_SF_MAC]  # HEAVY, AFT
            p2 = [point[0] * (1 - (W_SF / 100)), point[1] + CG_SF_MAC]  # LIGHT, AFT
            p3 = [point[0] * (1 - (W_SF / 100)), point[1] - CG_SF_MAC]  # LIGHT, FWD
            p4 = [point[0] * (1 + (W_SF / 100)), point[1] - CG_SF_MAC]  # HEAVY, FWD

            return np.array([p1, p2, p3, p4])

        else:
            p1 = [point[0] * (1 + (W_SF / 100)), point[1] + CG_SF]  # HEAVY, AFT
            p2 = [point[0] * (1 - (W_SF / 100)), point[1] + CG_SF]  # LIGHT, AFT
            p3 = [point[0] * (1 - (W_SF / 100)), point[1] - CG_SF]  # LIGHT, FWD
            p4 = [point[0] * (1 + (W_SF / 100)), point[1] - CG_SF]  # LIGHT, FWD

            return np.array([p1, p2, p3, p4])

    @staticmethod
    def create_centrogram(configuration, fuel):
        """
        This function creates a centrogram from fuel flow + configuration (dry A.C weight)
        :param configuration: (np.array(1,3)) the dry A.C data [weight, X moment, Y moment]
        :param fuel: (np.array(n,3)) fuel flow of A.C [weight, X moment, Y moment], ordered empty to full
        :return: centrogram (np.array(n,3)), ordered empty to full
        """
        centrogram = np.empty(shape=[0, 3])
        for weight, x_moment, y_moment in fuel:
            centrogram = np.append(centrogram, [[weight + configuration[0],
                                                x_moment + configuration[1], y_moment + configuration[2]]], axis=0)
        return centrogram


    @staticmethod
    def derive_fuel_limitaions():
        pass


    @staticmethod
    def derive_area_of_operation():
        '''
        This function is dedicated to heavy-cargo A.C. It produces the area of operation in an area graph,
        based on the chosen configutaion
        :return:
        '''
        pass

def main():
    pass

if __name__ == "__main__":
    main()
