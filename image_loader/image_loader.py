from abc import ABC

class ImageLoader(ABC):
	def __init__(self):
		pass
	
	@abstract_method
	def load_image(self, filename):
		""" Loads the image and returns as 3D array.
		
		:param filename: Name of the image file.
		...
		:return: numpy ndarray
		"""
		pass