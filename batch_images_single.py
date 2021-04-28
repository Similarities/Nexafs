import basic_image_app
import basic_file_app
import numpy as np
import matplotlib.pyplot as plt
import process_raw_images_sum_then_back
import px_shift_on_picture_array


path_background = "data/straylight_985ms_NiO/"
name_background = path_background

#laser_gate_time_data = 105  # ms
#per_second_correction = 1000 / laser_gate_time_data

# create input pictures
file_list_background = basic_image_app.get_file_list(path_background)
batch_background = basic_image_app.ImageStackMeanValue(file_list_background, path_background)
my_background = batch_background.average_stack()

path_picture = "data/S3_NiO_105ms_raw_pos2/"
file_list_raws = basic_image_app.get_file_list(path_picture)


roi_list1 = ([0, 585, 2048, 1362])

def batch_single_pictures_background():

    for x in file_list_raws:
        open_stack_raws = basic_image_app.SingleImageOpen(x, path_picture)
        my_single_picture = open_stack_raws.return_single_image()
        scaled_straylight_correction = process_raw_images_sum_then_back.ImagePreProcessing(my_single_picture, x[:-4], my_background, "straylight", roi_list1)
        scaled_straylight_correction.main()
        scaled_straylight_correction.save_data("single_image_sum_and_then_back")



#batch_single_pictures_background()


path = "data/SiN_105ms_variant_2/"
binned_file_list = basic_file_app.get_file_list(path)
reference_points = (1128, 980)
def batch_pixel_correction():
    reference_array = basic_file_app.load_2d_array(path + binned_file_list[0], 0, 1, 4)
    PixelCorrection = px_shift_on_picture_array.PixelShift(reference_array, reference_points)
    my_result = reference_array

    for x in binned_file_list[1:]:
        my_array = basic_file_app.load_2d_array(path+  x, 0, 1, 4)
        corrected_array = PixelCorrection.evaluate_shift_for_input_array(my_array)
        my_result[:,1] = my_result[:,1] + corrected_array[:,1]

    my_result[:,1] = my_result[:,1]/len(binned_file_list)
    return my_result

plt.close()

def batch_without_px_correction():
    reference_array = basic_file_app.load_2d_array(path + binned_file_list[0], 0, 1, 4)
    my_result = reference_array
    for x in binned_file_list[:]:
        my_array = basic_file_app.load_2d_array(path+  x, 0, 1, 4)
        my_result[:,1] = my_result[:,1] + my_array[:,1]
    my_result[:,1] = my_result[:,1]/len(binned_file_list)
    return my_result



def save_data( description1, array):
    plt.figure(4)
    plt.savefig(description1 + ".png", bbox_inches="tight", dpi=500)
    print('...saving:', description1)
    np.savetxt(description1 +  ".txt", array, delimiter=' ',
               header='string', comments='',
               fmt='%s')

my_result = batch_without_px_correction()
plt.figure(4)
plt.plot(my_result[:,0], my_result[:,1], label="px corrected SiN 105ms_wo")
plt.legend()

save_data("S3_SiN_px_corrected_105ms_avg_variant_2_wo", my_result)




# roi on image ( [x1, y1, x2, y2])




plt.show()