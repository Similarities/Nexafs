import basic_file_app
import numpy as np
import matplotlib.pyplot as plt


class CalibrateSpectrum:
    def __init__(self, array, fit_parameter, name):
        self.y_array = array
        self.fit_coefficients = fit_parameter
        self.name = name
        self.nm_array = np.empty([])
        self.ev_array = np.linspace(0, len(self.y_array), len(self.y_array))

    def calibrate_x_axis(self, px_shift):
        x_axis = np.linspace(0, len(self.y_array), len(self.y_array))
        for counter, value in enumerate(x_axis):  # self.fit_coefficients[0] * value ** 2) +
            self.ev_array[counter] = self.fit_coefficients[-2] * (value+px_shift) + self.fit_coefficients[-1] + self.fit_coefficients[-3] *((value+px_shift)**2)
        self.plot_result_ev()
        return self.ev_array

    def plot_result_ev(self):
        plt.figure(1)
        plt.plot(self.ev_array, self.y_array, label=self.name[:-4], marker=".", ms=3)
        plt.xlabel('eV')
        plt.ylabel('counts/s')
        plt.legend()

    def spectral_range(self):
        print(np.amax(self.ev_array), np.amin(self.ev_array), 'spectral range in eV')

    def reference_points(self, list):

        for x in list:
            plt.figure(1)
            plt.vlines(x =x, ymin = 0, ymax = np.amax(self.y_array))


    def prepare_header(self, description1):
        # insert header line and change index
        result = np.column_stack((self.ev_array, self.y_array))
        header_names = (['eV', 'counts/s'])
        names = (['file' + str(self.name), 'fit: ' + str(self.fit_coefficients)])
        parameter_info = (
            ['description:', description1])
        return np.vstack((parameter_info, names, header_names, result))

    def save_data(self, description1):
        result = self.prepare_header(description1)
        print('...saving:', self.name)
        plt.figure(1)
        plt.savefig(self.name + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(self.name + '_calibration' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')



input_file = "data/985ms_Ni_stack_pre_processing.txt"
counts_input = basic_file_app.load_1d_array(input_file, 1, 4)

input_calibration = "data/S3_Ni_20210412_quadratic_fit.txt"
fit = basic_file_app.load_1d_array(input_calibration, 0, 0)

#reference in eV
fit_points = "data/S3_20210412_reference.txt"
reference_points = basic_file_app.load_1d_array(fit_points, 0,2)


calibrate_Ni = CalibrateSpectrum(counts_input, fit, "20210414_Ni_S3_low")
# px_shift
calibrate_Ni.calibrate_x_axis(14)
calibrate_Ni.reference_points(reference_points)
plt.xlim(700, 900)
#plt.ylim(0.E6, 1.E6)
calibrate_Ni.save_data("20210414_cal_Ni_S3_low")

plt.show()
