def calibrate_x_axis(self, fit_coefficients):
    self.x_axis = np.linspace(0, 2048, 2048)
    for counter, value in enumerate(self.x_axis):
        self.x_axis[counter] = (fit_coefficients[0] * value ** 2) + fit_coefficients[1] * value + fit_coefficients[
            2]
    plt.figure(6)
    plt.plot(self.x_axis, self.binned_roi_y, label=self.filename[:-4], marker=".")
    plt.xlabel("nm")
    plt.ylabel('counts')
    return self.x_axis, self.binned_roi_y


def plot_x_axis_nm(self):
    plt.figure(6)
    plt.plot(self.x_axis_nm, self.binned_roi_y, label=self.filename[:-4] + "analytical", marker=".")
    plt.xlabel("nm")
    plt.ylabel("counts")
    plt.legend()


def plot_calibration_nm(self, lines):
    for x in lines:
        plt.figure(6)
        plt.vlines(x, ymin=0, ymax=1E7)


def plot_calibration_ev(self, lines, ymax, color):
    for x in lines:
        x = self.convert_single_value_nm_to_electron_volt(x)
        plt.figure(7)
        plt.vlines(x, ymin=0, ymax=ymax, linewidth=0.5, color=color)


def plot_result_ev(self):
    self.convert_array_nm_to_eV()
    plt.figure(7)
    plt.plot(self.x_axis_eV, self.binned_roi_y, label=self.filename[:-4], marker=".", ms=3)
    plt.xlabel('eV')
    plt.ylabel('counts')
    plt.legend()
    return self.x_axis_eV


def convert_single_value_nm_to_electron_volt(self, value_nm):
    planck_constant = 4.135667516 * 1E-15
    c = 299792458
    return planck_constant * c / (value_nm * 1E-9)


def convert_array_nm_to_eV(self):
    self.x_axis_eV = np.zeros([len(self.x_axis_nm)])
    self.x_axis_eV[:] = self.convert_single_value_nm_to_electron_volt(self.x_axis_nm[:])
    return self.x_axis_eV


def spectral_range(self):
    print(np.amax(self.x_axis_nm), np.amin(self.x_axis_nm), 'spectral range in nm')

def scale_array_per_second(self, constant):
        self.binned_roi_y = basic_file_app.constant_array_scaling(self.binned_roi_y, constant)
        return self.binned_roi_y

    def bin_in_y(self):
        self.binned_roi_y = np.sum(self.picture[self.roi_list[1]:self.roi_list[-1], self.roi_list[0]: self.roi_list[2]],
                                   axis=0)
        self.x_axis_nm = np.arange(0, self.roi_list[2] - self.roi_list[0]).astype(np.float32)
        plt.figure(3)
        plt.imshow(self.picture[self.roi_list[1]:self.roi_list[-1], self.roi_list[0]: self.roi_list[2]])
        plt.colorbar()
        return self.binned_roi_y, self.x_axis_eV
