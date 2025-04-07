from abc import ABC, abstractmethod
import numpy as np
from skimage import io
import ptufile

class ImageLoader(ABC):
	def __init__(self):
		pass
	
	@abstractmethod
	def load_image(self, filename):
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
	def load(filename):
		return ImageLoader.from_file(filename).load_image(filename)

class TiffLoader(ImageLoader):
	def load_image(self, filename):
		im = io.imread(filename)
		return im

class PtuLoader(ImageLoader):
	def load_image(self, filename):
		ptu = ptufile.PtuFile(filename)
		data = ptu[::-1,...,0,:]
		data = np.transpose(data, (2, 1, 0))
		return data
