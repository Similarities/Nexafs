import matplotlib.pyplot as plt
import numpy as np
import os


# make sure the image-array (picture, background) is in 32bit
class ImagePreProcessing:

    def __init__(self, picture, picture_name, background, background_name, roi_list):
        self.filename = picture_name
        self.picture = picture
        self.background = background
        self.background_name = background_name
        # x1, y1, x2, y2
        self.back_roi = ([400, 1779, 2048, 2048])
        self.roi_list = roi_list
        self.x_axis_px = np.arange(0, self.roi_list[2] - self.roi_list[0]).astype(np.float32)
        self.binned_roi_y = np.empty([])
        self.binned_roi_back = np.empty([])

    def main(self):
        self.reference_scaling()
        self.binned_roi_back= self.bin_in_y(self.background)
        self.binned_roi_y = self.bin_in_y(self.picture)
        self.background_subtraction()

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
        self.binned_roi_y[:] = self.binned_roi_y[:] - self.binned_roi_back[:]
        self.binned_roi_y[self.binned_roi_y < 0] = 0
        return self.binned_roi_y

    def correct_for_stack_number(self, number):
        self.picture = self.picture / number
        return self.picture

    def bin_in_y(self,  array):
        binned = np.sum(array[self.roi_list[1]:self.roi_list[-1], self.roi_list[0]: self.roi_list[-2]],axis=0)
        return binned

    def plot_binned_picture(self, name):
        plt.figure(4)
        plt.plot(self.x_axis_px, self.binned_roi_y, label=name)
        plt.legend()

    def prepare_header(self, description1):
        # insert header line and change index
        result = np.column_stack((self.x_axis_px, self.binned_roi_y))
        header_names = (['px', 'counts/s'])
        names = (['file' + str(self.filename), 'roi list:' + str(self.roi_list)])
        parameter_info = (
            ['description:', description1])
        return np.vstack((parameter_info, names, header_names, result))

    def save_data(self, description1):
        result = self.prepare_header(description1)
        print('...saving:', self.filename[:-4])
        np.savetxt(self.filename+ '_stack_single_variant_2' + ".txt", result, delimiter=' ',
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


