import numpy as np
import matplotlib.pyplot as plt
import basic_file_app


class CalibrationFit:
    def __init__(self, reference_points, order, file_name):
        self.name = file_name
        self.reference_points = reference_points
        self.order = order
        # print(reference_points_x_y)
        self.poly_coefficients = self.fit_refernce_points()
        self.poly_reciproce = self.fit_reciproce()
        # print(self.poly_coefficients, 'coefficients')

    def fit_refernce_points(self):
        fit_parameter = np.polyfit(self.reference_points[:, 1], self.reference_points[:, 0], self.order)
        np.savetxt(self.name + "_quadratic_fit" + ".txt", fit_parameter, fmt='%.3E', delimiter='\t')
        return fit_parameter


    def fit_reciproce(self):
        return np.polyfit(self.reference_points[:, 0], self.reference_points[:, 1], self.order)

    def give_fit(self):
        return self.poly_coefficients


    def compare_fit(self):
        x_axis = np.linspace(0, 2048, 2048)
        fit_y = np.linspace(0, 2048,2048)
        for counter, value in enumerate(x_axis):
            fit_y[counter] = self.poly_coefficients[-1] + self.poly_coefficients[-2] * x_axis[counter] \
                             +self.poly_coefficients[-3] * x_axis[counter] **2
        plt.figure(1)
        plt.scatter(self.reference_points[:, 1], self.reference_points[:, 0])
        plt.plot(x_axis, fit_y)
        plt.plot()


reference_path = "data/S2_reference_points_20210412.txt"
reference_eV= basic_file_app.load_1d_array(reference_path, 0, 2)
reference_px = basic_file_app.load_1d_array(reference_path, 1, 2)
reference_points = basic_file_app.stack_arrays(reference_eV, reference_px, 1)
print(reference_points)

Test_Ni = CalibrationFit(reference_points, 2, "S2_Ni+SiNi_20210412")
Test_Ni.fit_reciproce()
Test_Ni.compare_fit()
print(Test_Ni.give_fit())

plt.show()