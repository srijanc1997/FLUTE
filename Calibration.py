# Calculates the calibration parameters and returns the phi and m offsets

# imports
import numpy as np
from skimage import io

from image_loader.image_loader import ImageLoader

def get_calibration_parameters(filename, channel, bin_width=0.2208, freq=80, harmonic=1, tau_ref=4):
	"""Opens the tiff image file and calculates the fft and gets the center coordinates of the g and s. Returns
	the angle and distance that these values need to be translated by to place the calibration measurement
	at the position expected by the user"""
	im = ImageLoader.load(filename, channel)
	image = np.moveaxis(im, 0, 2)
	bins = image.shape[2]
	t_arr = bin_width * (np.arange(bins) + 0.5)

	integral = np.sum(image, axis=2, dtype=np.float64)
	integral[integral == 0] = 1e-5  # Avoid division by zero

	omega_t = 2 * np.pi * freq / 1000 * harmonic * t_arr
	cos_omega_t = np.cos(omega_t)
	sin_omega_t = np.sin(omega_t)

	g = np.tensordot(image, cos_omega_t, axes=(2, 0)) / integral
	s = np.tensordot(image, sin_omega_t, axes=(2, 0)) / integral

	# Flatten and calculate mean directly
	coor_x = np.mean(g)
	coor_y = np.mean(s)

	# Known sample parameters based on tau and freq
	omega_tau = 2 * np.pi * freq / 1000 * tau_ref
	x_ideal = 1 / (1 + omega_tau ** 2)
	y_ideal = omega_tau / (1 + omega_tau ** 2)

	phi_ideal = np.arctan2(y_ideal, x_ideal)
	m_ideal = np.hypot(x_ideal, y_ideal)

	# Our sample's coordinates
	phi_given = np.arctan2(coor_y, coor_x)
	m_given = np.hypot(coor_x, coor_y)

	# Calibration parameters
	theta = phi_ideal - phi_given
	m = m_ideal / m_given

	return theta, m