import basic_file_app
import numpy as np
import matplotlib.pyplot as plt


class OpticalDensity:
    def __init__(self, reference, sample, name_reference, name_sample):
        self.reference = reference  # expects2D array [ev] [counts]
        self.sample = sample  # same here
        self.name_reference = name_reference
        self.name_sample = name_sample
        self.resized_sample = np.empty([])
        self.resized_reference = np.empty([])
        self.result = np.empty([])

    def scale_y(self):
        self.reference[:, 1] = self.reference[:, 1] * (np.amax(self.sample[:, 1]) / np.amax(self.reference[:, 1]))
        return self.reference

    def shift_in_register(self):
        shift = self.reference[0, 0] - self.sample[0, 0]
        print(shift, 'shift')  #
        start_index =5
        shift_index = np.where(self.reference[:, 0] >= self.sample[start_index, 0])[0][0]
        print(shift_index, 'shift_index')

        if shift < 0:
            print(shift_index, 'neg', self.sample[start_index, 0], self.reference[shift_index, 0])
            self.resized_sample = self.sample[start_index: -(shift_index-start_index), :]
            print(len(self.resized_sample), 'sample', self.resized_sample[0, 0])
            self.resized_reference = self.reference[shift_index:, :]
            print(len(self.resized_reference), 'reference', self.resized_reference[0, 0])
            self.result = np.zeros([len(self.resized_sample), 2])




        elif shift > 0:

            self.resized_sample = self.sample[start_index:, :]
            print(len(self.resized_sample), 'sample', self.resized_sample[0, 0])
            self.resized_reference = self.reference[shift_index:-(start_index-shift_index), :]
            print(len(self.resized_reference), 'reference', self.resized_reference[0, 0])
            self.result = np.zeros([len(self.resized_sample), 2])
            print(len(self.result))

        elif shift == 0:
            self.resized_reference = self.reference
            self.resized_sample = self.sample
            self.result = np.zeros([len(self.resized_sample), 2])

        return self.result, self.resized_sample, self.resized_reference

    def process_optical_density(self):
        self.scale_y()
        self.shift_in_register()
        print(len(self.resized_sample), len(self.resized_reference))
        self.result[:, 1] = -np.log(self.resized_sample[:, 1] / self.resized_reference[:, 1])
        self.result[:, 0] = self.resized_sample[:, 0]
        return self.result

    def plot_result(self):
        plt.figure(1)
        plt.plot(self.result[:, 0], self.result[:, 1], label=str(self.name_sample) + '  ' + str(self.name_reference))
        plt.xlabel("eV")
        plt.ylabel("optical density i.a.u.")
        plt.legend()

    def prepare_header(self, description1):
        # insert header line and change index
        result = self.result
        header_names = (['eV', 'optical density i.a.u.'])
        names = (['sample: ' + self.name_sample, 'reference: ' + self.name_reference])
        parameter_info = (
            ['description:', description1])
        return np.vstack((parameter_info, names, header_names, result))

    def save_data(self, description1):
        result = self.prepare_header(description1)
        print('...saving:', description1)
        plt.figure(1)
        plt.savefig(description1 + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(description1 + '_optical_density' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')


reference_path = "data/stack_105ms/calibrated/SiN single_wo_calibration.txt"
reference_x = basic_file_app.load_1d_array(reference_path, 0, 4)
reference_y = basic_file_app.load_1d_array(reference_path, 1, 4)
reference = basic_file_app.stack_arrays(reference_x, reference_y, 1)

sample_path = "data/stack_105ms/calibrated/NiO single var 1_calibration.txt"
sample_x = basic_file_app.load_1d_array(sample_path, 0, 4)
sample_y = basic_file_app.load_1d_array(sample_path, 1, 4)
sample = basic_file_app.stack_arrays(sample_x, sample_y, 1)

Test = OpticalDensity(reference, sample, "SiN", "NiO")
Test.process_optical_density()
Test.plot_result()
plt.ylim(-0.2, 2.5)
plt.xlim(850, 890)
Test.save_data("S2_SiN_NiO_px_corrected_var1_with_wo")



plt.legend()


plt.show()
