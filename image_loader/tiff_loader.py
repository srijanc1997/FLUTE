from skimage import io

from image_loader import ImageLoader

class TiffLoader(ImageLoader):
	
	def load_image(self, filename):
		im = io.imread(filename)
		return im