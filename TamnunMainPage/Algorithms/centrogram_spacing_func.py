import numpy as np
import math
import time
import scipy.interpolate as sciInterp
import matplotlib.pyplot as plt

def centrogram_spacing(fuel_flow, desired_interval):
    '''
    This function takes a centrogram input with any interval spacing,
    including ones with unequal spacing between points, as well as a desired interval size.
    Then it creates a new centrogram output that is the same shape as the input centrogram,
    but with the spacing as specified by the desired interval input.
    
    INPUT:
    centrogram (Nx3 array) : array of weights (lb) and x, y moments (lb*in) for fuel use path
    desired_interval (float) : interval in weight at which the output centrogram will be made

    OUTPUT:
    output_centrogram (Mx3 array) : same width as input centrogram,
    but with more rows (length M) for points at desired interval spacing
    '''

    start = fuel_flow[0][0]
    end = fuel_flow[-1][0]
    length_of_output = int(round((end - start)/desired_interval)+1) # Need +1 because otherwise will be one short since index starts with 0
    # centrogram_output = np.arange(start, end, desired_interval)
    centrogram_output = np.zeros(shape = (length_of_output, 3))
    for n in range(length_of_output):
        centrogram_output[n][0] = fuel_flow[0][0] + desired_interval*n
    if centrogram_output[-1][0] > fuel_flow[-1][0]:
        centrogram_output = np.delete(centrogram_output, -1, axis=0)
    if centrogram_output[-1][0] != fuel_flow[-1][0]:
        centrogram_output = np.append(centrogram_output, [np.append(fuel_flow[-1][0], [0, 0])], axis=0)

    previous_counter = 0
    for n in range(len(centrogram_output)):
        counter = 0
        if previous_counter > 0:    # avoids running unnecessary loops
            counter = previous_counter
        
        if centrogram_output[n][0] == fuel_flow[counter][0]:
            centrogram_output[n][1] = fuel_flow[counter][1]
            centrogram_output[n][2] = fuel_flow[counter][2]
            continue
        elif centrogram_output[n][0] > fuel_flow[counter][0] and centrogram_output[n][0] < fuel_flow[counter+1][0]:
            fuel_flow_weight = [fuel_flow[counter][0], fuel_flow[counter+1][0]]
            fuel_flow_x = [fuel_flow[counter][1], fuel_flow[counter+1][1]]
            fuel_flow_y = [fuel_flow[counter][2], fuel_flow[counter+1][2]]
        elif centrogram_output[n][0] > fuel_flow[counter][0]:
            while centrogram_output[n][0] > fuel_flow[counter][0]:
                fuel_flow_weight = [fuel_flow[counter][0], fuel_flow[counter+1][0]]
                fuel_flow_x = [fuel_flow[counter][1], fuel_flow[counter+1][1]]
                fuel_flow_y = [fuel_flow[counter][2], fuel_flow[counter+1][2]]
                counter += 1
            previous_counter = counter
        
        centrogram_output[n][1] = np.interp(centrogram_output[n][0], fuel_flow_weight, fuel_flow_x)
        centrogram_output[n][2] = np.interp(centrogram_output[n][0], fuel_flow_weight, fuel_flow_y)

    return centrogram_output

if __name__ == "__main__":
    start = time.time()

    test_fuel_flow_Zik = np.array([[0, 0, 0], [8.5, 2883, 0], [22, 7410, 0],
        [29, 9718, 0], [37, 12325, 0], [44, 14577, 0],
        [57, 18713, 0], [69, 22480, 0], [79, 25564, 0],
        [88, 28301, 0], [97, 30924, 0], [105, 33149, 0]])
    desired_interval_Zik = 5   # lb (weight)

    test_fuel_flow_Baz = np.array([[0, 0, 0], [394, 216765, 0], [788, 433529, 0],
    [1084, 592162, 0], [1642, 903515, 0], [1971, 1088750, 0],
    [2365, 1310441, 0], [2867, 1592235, 0], [3347, 1809000, 0],
    [3547, 1916397, 0], [3941, 2127250, 0], [4335, 2338103, 0],
    [4729, 2549941, 0], [5124, 2761779, 0], [5518, 2972632, 0],
    [5912, 3183485, 0], [6306, 3395324, 0], [6700, 3607162, 0],
    [7094, 3818015, 0], [7488, 4028868, 0], [7882, 4240706, 0],
    [8276, 4452544, 0], [8671, 4663397, 0], [9065, 4874250, 0],
    [9459, 5086088, 0], [9853, 5297926, 0], [10247, 5508779, 0],
    [10641, 5719632, 0], [11035, 5931471, 0], [11429, 6143309, 0],
    [11993, 6444809, 0]])
    desired_interval_Baz = 10   # lb (weight)

    test_fuel_flow_Lavi = np.array([[0, 0, 0], [220, 41748, 0], [441, 84033, 0],
    [661, 138446, 0], [882, 190029, 0], [1102, 243047, 0],
    [1323, 294723, 0], [1543, 346351, 0], [1764, 402977, 0],
    [1984, 457205, 0], [2205, 515744, 0], [2425, 571533, 0],
    [2646, 628078, 0], [2866, 683778, 0], [3086, 739304, 0],
    [3307, 794201, 0], [3527, 846168, 0], [3748, 898027, 0],
    [3968, 952337, 0], [6190, 1488594, 0], [6411, 1543145, 0],
    [6649, 1600146, 0]])
    desired_interval_Lavi = 10   # lb (weight)

    test_fuel_flow_Peten = np.array([[0, 0, 0], [100, 14900, 0], [150, 27700, 0],
    [200, 40400, 0], [250, 53200, 0], [300, 66000, 0],
    [350, 78700, 0], [400, 91500, 0], [450, 99100, 0],
    [500, 111800, 0], [550, 119300, 0], [600, 132100, 0],
    [650, 139600, 0], [700, 152300, 0], [750, 159900, 0],
    [800, 172700, 0], [850, 180200, 0], [900, 193000, 0],
    [950, 200500, 0], [1000, 213300, 0], [1050, 220800, 0],
    [1100, 233500, 0], [1150, 241100, 0], [1200, 253900, 0],
    [1250, 261400, 0], [1300, 274100, 0], [1350, 281600, 0],
    [1400, 294400, 0], [1450, 302000, 0], [1500, 314700, 0],
    [1550, 322200, 0], [1600, 335000, 0], [1650, 342500, 0],
    [1700, 355200, 0], [1750, 362800, 0], [1800, 375600, 0],
    [1850, 383100, 0], [1900, 395800, 0], [1950, 404200, 0],
    [2000, 417000, 0], [2050, 425500, -97083], [3591, 725100, -97083],
    [3641, 737800, -97083], [3691, 746300, -97083], [3741, 759100, -97083],
    [3753, 761100, -97083], [3803, 773800, -97083], [3834, 778600, -97083],
    [3884, 791400, -97083], [3934, 804100, -97083], [3984, 816900, -97083],
    [4014, 824500, -97083], [4058, 835700, -97083]])
    desired_interval_Peten = 10   # lb (weight)

    # chosen test case:
    test_fuel_flow = test_fuel_flow_Peten
    desired_interval = desired_interval_Peten

    centrogram = centrogram_spacing(test_fuel_flow, desired_interval)
    
    # calculate x and y CG (moment / weight)
    fuel_CG = np.zeros(shape=(len(centrogram), 2))
    for p in range(2):
        for n in range(1, len(fuel_CG)):
            fuel_CG[n][p] = centrogram[n][p+1] / centrogram[n][0]
    fuel_CG[0][0] = fuel_CG[1][0]
    fuel_CG[0][1] = fuel_CG[1][1]

    test_fuel_CG = np.zeros(shape=(len(test_fuel_flow), 2))
    for p in range(2):
        for n in range(1, len(test_fuel_CG)):
            test_fuel_CG[n][p] = test_fuel_flow[n][p+1] / test_fuel_flow[n][0]
    test_fuel_CG[0][0] = test_fuel_CG[1][0]
    test_fuel_CG[0][1] = test_fuel_CG[1][1]

    end = time.time()
    print(centrogram)

    # plot weight vs moment in x and y
    fig1 = plt.figure(1)
    momentsX = fig1.add_subplot(211)
    momentsX.plot(test_fuel_flow[:, 0], test_fuel_flow[:, 1], 'r.', centrogram[:, 0], centrogram[:, 1], 'b-')
    momentsX.set_title('Weight (lb) vs Centrogram Moment_x (in)')
    momentsX.set_xlabel('Weight (lb)')
    momentsX.set_ylabel('Moment (in*lb)')
    momentsY = fig1.add_subplot(212)
    momentsY.plot(test_fuel_flow[:, 0], test_fuel_flow[:, 2], 'r.', centrogram[:, 0], centrogram[:, 2], 'b-')
    momentsY.set_title('Weight (lb) vs Centrogram Moment_y (in)')
    momentsY.set_xlabel('Weight (lb)')
    momentsY.set_ylabel('Moment (in*lb)')

    # plot fuel CG vs weight in x and y
    fig2 = plt.figure(2)
    CGx = fig2.add_subplot(211)
    CGx.plot(test_fuel_CG[:, 0], test_fuel_flow[:, 0], 'r.', fuel_CG[:, 0], centrogram[:, 0], 'b-')
    CGx.set_title('Centrogram CG_x (in) vs Weight (lb)')
    CGx.set_xlabel('CG (inch)')
    CGx.set_ylabel('Weight (lb)')
    CGy = fig2.add_subplot(212)
    CGy.plot(test_fuel_CG[:, 1], test_fuel_flow[: , 0], 'r.', fuel_CG[:, 1], centrogram[:, 0], 'b-')
    CGy.set_title('Centrogram CG_y (in) vs Weight (lb)')
    CGy.set_xlabel('CG (inch)')
    CGy.set_ylabel('Weight (lb)')
    
    
    print("-- %s seconds to run--" % (float(end - start)))
    plt.show()