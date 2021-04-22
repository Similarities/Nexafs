import matplotlib.pyplot as plt
import basic_file_app
import numpy as np

class OverlayPlot:
    def __init__(self, array, name):
        self.array = array
        self.name = name

    def plot(self):
        plt.figure(1)
        plt.plot(self.array[:,0], self.array[:,1], label = self.name)
        plt.xlabel("eV")
        plt.ylabel("counts/s")
        plt.legend()

    def scale_y(self, scale_factor):
        self.array[:,1] = self.array[:,1] * scale_factor
        return self.array




file_1_path= "data/calibrated/20210412_Ni+SiN_S2_reference_calibration.txt"
file_1_x = basic_file_app.load_1d_array(file_1_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_1_path,1,4)
file_1 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)

file_2_path = "data/calibrated/20210419_SiN_S2_high_calibration.txt"
file_1_x = basic_file_app.load_1d_array(file_2_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_2_path,1,4)
file_2 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)

file_3_path = "data/calibrated/20210419_SiN_S2_low_calibration.txt"
file_1_x = basic_file_app.load_1d_array(file_3_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_3_path,1,4)
file_3 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)

file_4_path = "data/calibrated/20210414_Ni+SiN_S2_low_calibration.txt"
file_1_x = basic_file_app.load_1d_array(file_4_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_4_path,1,4)
file_4 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)

file_5_path = "data/calibrated/20210414_NiO+SiN_S2_high_calibration.txt"
file_1_x = basic_file_app.load_1d_array(file_5_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_5_path,1,4)
file_5 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)


scale_1 = np.amax(file_1[:,1])
scale_2 = np.amax(file_2[:,1])
scale_3 = np.amax(file_3[:,1])
scale_4 = np.amax(file_4[:,1])
scale_5 = np.amax(file_5[:,1])



Test = OverlayPlot(file_1, "Ni on SiN reference")
Test.scale_y(scale_2/scale_1)
Test.plot()

Test = OverlayPlot(file_2, "SiN_high")
#Test.scale_y(scale_2/scale_3)
Test.plot()

Test = OverlayPlot(file_3, "SiN_low")
Test.scale_y(scale_2/scale_3)
Test.plot()

Test = OverlayPlot(file_4, "Ni_low")
Test.scale_y(scale_2/scale_4)
Test.plot()

Test = OverlayPlot(file_5, "NiO_high")
Test.scale_y(scale_2/scale_5)
Test.plot()

plt.show()