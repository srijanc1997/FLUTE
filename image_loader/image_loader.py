from abc import ABC, abstractmethod
import numpy as np
from skimage import io
import ptufile
# DEBUG
import tifffile as t3f

class ImageLoader(ABC):
	def __init__(self):
		pass
	
	@abstractmethod
	def load_image(self, filename, channel=0):
		""" Loads the image and returns as 3D array.
		
		:param filename: Name of the image file.
		...
		:return: numpy ndarray
		"""
		pass
	
	@staticmethod
	def from_file(filename):
		extension = filename.split('.')[-1]
		match extension:
			case "tif" | "tiff":
				return TiffLoader()
			case "ptu":
				return PtuLoader()
			case _:
				print("Unsupported file format") # TODO
				return None
	
	@staticmethod
	def load(filename, channel=0):
		""" Loads the image and returns as 3D array. Automatically determines the correct loader to use.
		
		:param filename: Name of the image file.
		...
		:return: numpy ndarray
		"""
		return ImageLoader.from_file(filename).load_image(filename, channel)

class TiffLoader(ImageLoader):
	def load_image(self, filename, channel=0):
		im = io.imread(filename)
		return im

class PtuLoader(ImageLoader):
	def load_image(self, filename, channel=0):
		ptu = ptufile.PtuFile(filename)
		# TODO: Better error logging
		if channel >= ptu.shape[3]:
			print("FLIM data does not have channel %d! (Channel index is 0-based)" % channel)
			return None
		data = ptu[::-1,...,channel,:]
		data = np.transpose(data, (2, 1, 0)).astype(np.uint8)
		return data
