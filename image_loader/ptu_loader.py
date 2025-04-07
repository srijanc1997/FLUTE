import numpy as np
import ptufile

from image_loader import ImageLoader

class PtuLoader(ImageLoader):
	
	def load_image(self, filename):
		ptu = ptufile.PtuFile(filename)
		data = ptu[::-1,...,0,:]
		return data