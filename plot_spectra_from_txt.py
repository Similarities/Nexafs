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

    def substract_y(self, factor):
        self.array[:,1] = self.array[:,1] - factor
        return self.array



file_1_path = "data/20210426/210426_S2_mylar_high_98_stack_processing_Mylar.txt"
file_1_x = basic_file_app.load_1d_array(file_1_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_1_path,1,4)
file_1 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)


file_2_path = "data/reference_2021041_stack_pre_processing.txt"
file_1_x = basic_file_app.load_1d_array(file_2_path, 0, 4)
file_1_y = basic_file_app.load_1d_array(file_2_path,1,4)
file_2 = basic_file_app.stack_arrays(file_1_x, file_1_y, 1)






scale_1 = np.amax(file_1[:,1])
scale_2 = np.amax(file_2[:,1])



Test = OverlayPlot(file_1, "Mylar")
Test.scale_y(scale_2/scale_1)
Test.plot()

Test = OverlayPlot(file_2, "Ni_reference with Fe")

Test.plot()

#plt.xlim(525, 600)
#plt.ylim(0, 0.8)

plt.show()
