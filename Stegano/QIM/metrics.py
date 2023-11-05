from PIL import Image, ImageFilter
from skimage.metrics import structural_similarity as ssim
from math import log10
import numpy as np


def obscurity_MSE(old_img: Image, new_img: Image) -> float:
	"""
	Calculate Mean Squared Error (MSE) between two images.

	Args:
		old_img (Image): The original image.
		new_img (Image): The modified image.

	Returns:
		float: The MSE value.
	"""
	size_of_img = (old_img.size)
	size = size_of_img[0] * size_of_img[1]
	delta_sum = 0

	for y in range(size_of_img[1]):
		for x in range(size_of_img[0]):
			pos = (x,y)
			r_old, g_old, b_old = old_img.getpixel(pos)
			r_new, g_new, b_new = new_img.getpixel(pos)

			delta = r_old - r_new

			delta_sum += pow(delta,2)

	MSE = delta_sum / (size)

	return MSE


def obscurity_PSNR(MSE: float) -> float:
	"""
	Calculate Peak Signal-to-Noise Ratio (PSNR) from MSE.

	Args:
		MSE (float): Mean Squared Error.

	Returns:
		float: The PSNR value.
	"""
	PSNR = 10 * log10((255*255)/MSE)

	return PSNR


def obscurity_RMSE(MSE: float) -> float:
	"""
	Calculate Root Mean Squared Error (RMSE) from MSE.

	Args:
		MSE (float): Mean Squared Error.

	Returns:
		float: The RMSE value.
	"""
	RMSE = pow(MSE, 0.5)

	return RMSE


def obscurity_SSIM(old_img: Image, new_img: Image) -> float:
	"""
	Calculate Structural Similarity Index (SSIM) between two images.

	Args:
		old_img (Image): The original image.
		new_img (Image): The modified image.

	Returns:
		float: The SSIM value.
	"""
	old_arr = np.array(old_img)
	new_arr = np.array(new_img)

	r_old = old_arr[:, :, 0]
	r_new = new_arr[:, :, 0]

	SSIM = ssim(r_old, r_new)

	return SSIM


def capacity(img: Image, bin_mes: list) -> float:
	"""
	Calculate the embedding capacity of an image.

	Args:
		img (Image): The image.
		bin_mes (list): The binary message to be embedded.

	Returns:
		float: The embedding capacity value.
	"""
	size_of_img = (img.size)
	EC = len(bin_mes) / (size_of_img[0] * size_of_img[1])

	return EC
