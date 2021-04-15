import matplotlib.pyplot as plt
import numpy as np
import basic_image_app
import basic_file_app
import math
import os


# make sure the image-array (picture, background) is in 32bit
class ImagePreProcessing:

    def __init__(self, picture, picture_name, background, background_name):
        self.filename = picture_name
        self.picture = picture
        self.background = background
        self.background_name = background_name
        # x1, y1, x2, y2
        self.back_roi = ([400, 1779, 2048, 2048])
        self.x_axis_px = np.empty([])
        self.roi_list = np.empty([])
        self.binned_roi_y = np.empty([])

    def reference_scaling(self):
        # opens tif is flipped vertical, array_image[y:y1, x:x1] (warum auch immer....)
        subarray_reference = self.background[self.back_roi[1]:self.back_roi[3], self.back_roi[0]:self.back_roi[2]]
        subarray_picture = self.picture[self.back_roi[1]:self.back_roi[3], self.back_roi[0]:self.back_roi[2]]
        bin_background_reference_x = np.sum(subarray_reference, axis=0)
        bin_background_picture_x = np.sum(subarray_picture, axis=0)
        scaling_factor = np.mean(bin_background_picture_x / bin_background_reference_x)
        print("scalingfactor", scaling_factor)
        self.background[::] = self.background[::] * scaling_factor
        return self.background

    def background_subtraction(self):
        for counter, x in enumerate(self.picture[0, ::]):
            self.picture[::, counter] = self.picture[::, counter] - self.background[::, counter]
        self.picture[self.picture < 0] = 0
        return self.picture

    def test_back_substraction(self):
        subarray_picture = self.picture[self.back_roi[1]:self.back_roi[3], 0:self.back_roi[2]]
        bin_test = np.mean(subarray_picture, axis=0)
        x_test = np.linspace(0, self.back_roi[2], (self.back_roi[2] - 0))
        plt.figure(2)
        plt.plot(x_test, bin_test, label=self.background_name)
        plt.legend()

    def another_background_substraction(self, new_background_array, name):
        self.background_name = name
        self.background = new_background_array
        self.reference_scaling()
        self.background_subtraction()

    def correct_for_stack_number(self, number):
        self.picture = self.picture / number
        return self.picture

    def bin_in_y(self, roi_list):
        self.roi_list = roi_list
        self.binned_roi_y = np.sum(self.picture[self.roi_list[1]:self.roi_list[-1], self.roi_list[0]: self.roi_list[2]],
                                   axis=0)
        self.x_axis_px = np.arange(0, self.roi_list[2] - self.roi_list[0]).astype(np.float32)
        plt.figure(3)
        plt.imshow(self.picture[self.roi_list[1]:self.roi_list[-1], self.roi_list[0]: self.roi_list[2]])
        plt.colorbar()
        return self.binned_roi_y, self.x_axis_px, self.roi_list

    def plot_binned_picture(self, name):
        plt.figure(4)
        plt.plot(self.x_axis_px, self.binned_roi_y, label=name)
        plt.legend()


    def prepare_header(self, description1, description2):
        # insert header line and change index
        result = np.column_stack((self.x_axis_nm, self.x_axis_eV, self.binned_roi_y))
        self.spectral_range()
        header_names = (['nm', 'eV', 'counts/s'])
        names = (['file' + str(self.filename), 'back:' + str(self.background_name), 'roi list:' + str(self.roi_list)])
        parameter_info = (
            ['description:', description1, description2])
        return np.vstack((parameter_info, names, header_names, result))

    def save_data(self, description1, description2):
        result = self.prepare_header(description1, description2)
        print('...saving:', self.filename[:-4])
        plt.figure(7)
        plt.savefig(self.filename[:-4] + ".png", bbox_inches="tight", dpi=500)
        np.savetxt(self.filename[:-4] + '_calibrated_analytical' + ".txt", result, delimiter=' ',
                   header='string', comments='',
                   fmt='%s')

    def view_control(self):
        plt.figure(1)
        plt.imshow(self.picture)
        plt.hlines(self.back_roi[1], xmax=self.back_roi[0], xmin=self.back_roi[2])
        # plt.hlines(self.back_roi[-1], xmax=2048, xmin=0)
        plt.vlines(self.back_roi[0], ymax=self.back_roi[3], ymin=self.back_roi[1])
        # plt.vlines(self.back_roi[2], ymax=2048, ymin=0)

    def figure_raw(self):
        plt.figure(8)
        plt.imshow(self.picture)
        plt.colorbar()


path_background = "data/straylight_985ms_Ni/"
name_background = path_background

laser_gate_time_data = 985  # ms
per_second_correction = 1000 / laser_gate_time_data

# create input pictures
file_list_background = basic_image_app.get_file_list(path_background)
batch_background = basic_image_app.ImageStackMeanValue(file_list_background, path_background)
my_background = batch_background.average_stack()

my_second_background_path = "data/back_2s_gauge_on/"
file_list_second_back = basic_image_app.get_file_list(my_second_background_path)
batch_second_background = basic_image_app.ImageStackMeanValue(file_list_second_back, my_second_background_path)
my_second_background = batch_second_background.average_stack()

path_picture = "data/985ms_Ni_raw/"
file_list_raws = basic_image_app.get_file_list(path_picture)

open_stack_raws = basic_image_app.ImageSumOverStack(file_list_raws, path_picture)
my_summed_stack, number_in_stack = open_stack_raws.sum_stack()

open_stack_raws_2 = basic_image_app.ImageStackMeanValue(file_list_raws, path_picture)
my_avg_picture = open_stack_raws_2.average_stack()

# roi on image ( [x1, y1, x2, y2])
roi_list = ([0, 852, 2048, 1528])

scaled_straylight_correction = ImagePreProcessing(my_summed_stack, path_picture[:-4], my_background, "stray light")
scaled_straylight_correction.reference_scaling()  #
scaled_straylight_correction.background_subtraction()
# scaled_straylight_correction.view_control()
scaled_straylight_correction.another_background_substraction(my_second_background, "dark ")
scaled_straylight_correction.correct_for_stack_number(number_in_stack)

scaled_straylight_correction.bin_in_y(roi_list)
scaled_straylight_correction.plot_binned_picture("straylight + dark sum avg")

scaled_straylight_correction = ImagePreProcessing(my_avg_picture, path_picture[:-4], my_background, "stray light")
scaled_straylight_correction.reference_scaling()  #
scaled_straylight_correction.background_subtraction()
scaled_straylight_correction.view_control()

scaled_straylight_correction.another_background_substraction(my_second_background, "dark ")

scaled_straylight_correction.bin_in_y(roi_list)
scaled_straylight_correction.plot_binned_picture("straylight + dark avg")

scaled_straylight_correction = ImagePreProcessing(my_summed_stack, path_picture[:-4], my_second_background, "dark")
scaled_straylight_correction.reference_scaling()  #
scaled_straylight_correction.background_subtraction()
# scaled_straylight_correction.view_control()
scaled_straylight_correction.another_background_substraction(my_background, "stray light")
scaled_straylight_correction.correct_for_stack_number(number_in_stack)

scaled_straylight_correction.bin_in_y(roi_list)
scaled_straylight_correction.plot_binned_picture("dark + straylight + sum avg")

scaled_straylight_correction = ImagePreProcessing(my_avg_picture, path_picture[:-4], my_second_background, "dark")
scaled_straylight_correction.reference_scaling()  #
scaled_straylight_correction.background_subtraction()
scaled_straylight_correction.view_control()

scaled_straylight_correction.another_background_substraction(my_background, "stay light")

scaled_straylight_correction.bin_in_y(roi_list)
scaled_straylight_correction.plot_binned_picture(" dark straylight avg")

plt.show()
