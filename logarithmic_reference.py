import basic_file_app
import numpy as np
import matplotlib.pyplot as plt


class OpticalDensity:
    def __init__(self, reference, sample, name_reference, name_sample):
        self.reference = reference # expects2D array [ev] [counts]
        self.sample = sample #same here
        self.name_reference = name_reference
        self.name_sample = name_sample
        self.result = np.zeros([len(reference),2])

    def shift_in_register(self):
        shift = self.reference[0,0]-self.sample[0,0]
        print(shift, 'shift')
        start_index = 10
        shift_index = np.where(self.sample[:,0] >= self.reference[start_index,0])[0][0]
        print(shift_index)
        return 10-shift_index, start_index


    def process_optical_density(self):
        self.result[:, 0] = self.reference[:,0]
        shift_index, start = self.shift_in_register()


        self.result[start:,1] = -np.log(self.sample[shift_index:-(start-shift_index),1]/self.reference[start:,1])
        plt.plot(self.result[:,0], self.result[:,1])



reference_path = "data/calibrated/20210419_SiN_high_S3_calibration.txt"
reference_x = basic_file_app.load_1d_array(reference_path, 0,4)
reference_y = basic_file_app.load_1d_array(reference_path, 1, 4)
reference = basic_file_app.stack_arrays(reference_x, reference_y, 1)

sample_path = "data/calibrated/20210414_985ms_calibration.txt"
sample_x = basic_file_app.load_1d_array(sample_path, 0,4)
sample_y = basic_file_app.load_1d_array(sample_path, 1, 4)
sample = basic_file_app.stack_arrays(sample_x, sample_y, 1)

Test = OpticalDensity(reference, sample, "SiN", "Ni")
Test.process_optical_density()

plt.ylim(0,3)
plt.show()