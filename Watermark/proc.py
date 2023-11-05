from PIL import Image
import cprint as cp
from math import log10
import numpy as np
from skimage.metrics import structural_similarity as ssim

def check(h_img, w_img, h_wat, w_wat) -> bool:
	"""
	Check if the image and watermark dimensions are valid.

	Args:
		h_img (int): Height of the image.
		w_img (int): Width of the image.
		h_wat (int): Height of the watermark.
		w_wat (int): Width of the watermark.

	Returns:
		bool: True if dimensions are valid, False otherwise.
	"""
	if (h_img != w_img or 
		h_wat != w_wat or 
		h_img // 8 != h_wat):    
		return False
	
	return True


def get_image_path() -> str:
    """
    Get the path to the input image from the user.

    Returns:
        str: Path to the input image.
    """
    cp.bprint("Enter the name of the input file (the file must be saved in the /in_image folder)")
    image_name = input()
    path_to_inp_image = "in_image/" + image_name
    return path_to_inp_image


def task() -> int:
    """
    Get the task choice from the user.

    Returns:
        int: Task choice (1 for embedding, 2 for extraction).
    """
    cp.bprint("What do you want to do with the input file:")
    cp.bprint("1 - Embed a watermark;")
    cp.bprint("2 - Extract a watermark.")
    task = int(input())
    return task


def get_watermark_type() -> str:
    """
    Get the watermark type from the user.

    Returns:
        str: Watermark type (chosen option or custom filename).
    """
    cp.bprint("Select a watermark:")
    cp.bprint("1 - 32x32 watermark (for 256x256 images);")
    cp.bprint("2 - 16x16 watermark (for 128x128 images);")
    cp.bprint("3 - 8x8 watermark (for 64x64 images).")
    cp.bprint("Or enter the filename for your watermark.")
    typeW = input()
    return typeW


def insert_to_start(container: Image, h_image: int, w_image: int, matrix: list) -> Image:
    """
    Insert a watermark into the image.

    Args:
        container (Image): The container image.
        h_image (int): Height of the image.
        w_image (int): Width of the image.
        matrix (list): Watermark matrix.

    Returns:
        Image: Image with the embedded watermark.
    """
    container = container.convert('RGB')
    for row in range(h_image):
        for col in range(w_image): 
            pos = (col,row)
            r, g, b = container.getpixel(pos)
            b_mod = int(matrix[row][col])
            container.putpixel(pos, (r, g, b_mod))
    return container


def arnold_transformation(watermark_matrix: np.array, watermark_size: int, iter_val: int) -> np.array:
	"""
	Apply Arnold Transformation to the watermark matrix.

	Args:
		watermark_matrix (np.array): Watermark matrix.
		watermark_size (int): Size of the watermark.
		iter_val (int): Number of iterations.

	Returns:
		np.array: Transformed watermark matrix.
	"""

	arnold_matrix = np.zeros((watermark_matrix.shape[0], watermark_matrix.shape[1]))
	multiplication_matrix = np.array([[1, 1], [1, 2]])

	for iter_counter in range(iter_val):
		for i in range(watermark_size):
			for j in range(watermark_size): 
				new_coord = np.matmul(multiplication_matrix, np.array([[i], [j]]))
				new_i = int(new_coord[0] % (watermark_size))
				new_j = int(new_coord[1] % (watermark_size))
				arnold_matrix[new_i][new_j] = watermark_matrix[i][j]

	arnold_matrix = np.array(arnold_matrix)
	return arnold_matrix


def inv_arnold_transformation(arnold_watermark_matrix: np.array, watermark_size: int, iter_val: int) -> np.array:
	"""
	Apply inverse Arnold Transformation to the watermark matrix.

	Args:
		arnold_watermark_matrix (np.array): Transformed watermark matrix.
		watermark_size (int): Size of the watermark.
		iter_val (int): Number of iterations.

	Returns:
		np.array: Inverse transformed watermark matrix.
	"""

	inv_arnold_matrix = np.zeros((arnold_watermark_matrix.shape[0], arnold_watermark_matrix.shape[1]))
	multiplication_matrix = np.array([[2, -1], [-1, 1]])

	for iter_counter in range(iter_val):
		for i in range(watermark_size):
			for j in range(watermark_size): 
				new_coord = np.matmul(multiplication_matrix, np.array([[i], [j]]))
				new_i = int(new_coord[0] % (watermark_size))
				new_j = int(new_coord[1] % (watermark_size))
				inv_arnold_matrix[new_i][new_j] = arnold_watermark_matrix[i][j]

	inv_arnold_matrix = np.array(inv_arnold_matrix)
	return inv_arnold_matrix


def to_watermark_matrix(dwm: list, step: int) -> np.array:
	"""
	Convert a 1D watermark to a 2D matrix.

	Args:
		dwm (list): 1D watermark.
		step (int): Size of the watermark matrix.

	Returns:
		np.array: Watermark matrix.
	"""

	matrix_dwm = []
	st = 0

	for i in range(step): 
		row = []
		for j in range(st, st+step): 
			row.append(dwm[j])
		matrix_dwm.append(row)
		st += step
	return np.array(matrix_dwm)


def get_mse(old_img: Image, new_img: Image) -> float:
	"""
	Calculate Mean Squared Error (MSE) between two images.

	Args:
		old_img (Image): Original image.
		new_img (Image): Processed image.

	Returns:
		float: MSE value.
	"""

	old_img = old_img.convert('RGB')
	new_img = new_img.convert('RGB')
	size_of_img = (old_img.size)
	size = size_of_img[0] * size_of_img[1]
	delta_sum = 0

	for y in range(size_of_img[1]):
		for x in range(size_of_img[0]):
			pos = (x,y)
			r_old, g_old, b_old = old_img.getpixel(pos)
			r_new, g_new, b_new = new_img.getpixel(pos)
			
			delta = b_old - b_new

			delta_sum += pow(delta,2)

	MSE = delta_sum / (size)
	return MSE


def get_psnr(MSE: float) -> float:
	"""
	Calculate Peak Signal-to-Noise Ratio (PSNR) from MSE.

	Args:
		MSE (float): Mean Squared Error.

	Returns:
		float: PSNR value.
	"""

	PSNR = 10 * log10((255*255)/MSE)
	return PSNR


def get_rmse(MSE: float) -> float:
	"""
	Calculate Root Mean Squared Error (RMSE) from MSE.

	Args:
		MSE (float): Mean Squared Error.

	Returns:
		float: RMSE value.
	"""

	RMSE = pow(MSE, 0.5)
	return RMSE


def get_ssim(old_img: Image, new_img: Image) -> float:
	"""
	Calculate Structural Similarity Index (SSIM) between two images.

	Args:
		old_img (Image): Original image.
		new_img (Image): Processed image.

	Returns:
		float: SSIM value.
	"""
	
	old_arr = np.array(old_img)
	new_arr = np.array(new_img)

	b_old = old_arr[:, :, 2]
	b_new = new_arr[:, :, 2]

	SSIM = ssim(b_old, b_new)
	return SSIM
