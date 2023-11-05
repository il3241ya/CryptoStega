from PIL import Image
import numpy as np

import cprint as cp
import DWM
import insert
import extract
import proc
import filters
import histograms


def main():
	"""
	Main function to perform watermark insert and extract.
	"""
	# Get the path to the input image from the user.
	image_path = proc.get_image_path()
	
	try: 
		image_cont = Image.open(image_path)
		start_img = image_cont
	except FileNotFoundError: 
		cp.rprint("Image file not found. Please note that the input file should be located in the /in_image folder.")
		main()

	# Get the width and height of the image.
	w_img, h_img = image_cont.size

	# Choose the main action.
	todo_main = proc.task()

	while todo_main != "exit": 
		match todo_main:
			case 1:
				todo_main = "exit"
				
				# Get the watermark type.
				type_w = proc.get_watermark_type()

				while type_w != "exit": 
					tp = DWM.get_watermark(type_w)
					if len(tp) == 0: 
						cp.rprint("Enter either a number from 1 to 3 or the name of an existing file in the in_watermark folder.")
						type_w = int(input())
					else: 
						watermark = tp
						type_w = "exit"
					
				h_wat, w_wat = watermark.shape
				if proc.check(h_img, w_img, h_wat, w_wat):
					cp.bprint("Do you want to apply Arnold Transformation?")
					cp.bprint("1 - Yes;")
					cp.bprint("2 - No.")
					arn = int(input())
					while arn != "exit": 
						match arn:
							case 1:
								cp.gprint("Enter the number of iterations")
								iter = int(input())
								watermark = proc.arnold_transformation(watermark, h_wat, iter)
								arn = "exit"
							case 2:
								arn = "exit"
							case _:
								cp.rprint("Enter either 1 or 2")
								arn = int(input())
					
					cp.bprint("Enter the value of the algorithm parameter (default value is 2):")
					z_inp = int(input())
					cp.bprint("Enter the values of parameters T and K (default values are 80 and 12):")
					t_inp = int(input("T: "))
					k_inp = int(input("K: "))
					out_matrix = insert.INSERT(image_cont, watermark, h_img, w_img, h_wat, w_wat, z_inp, t_inp, k_inp)
					#for row in out_matrix: cp.rprint(row)
					new_image = proc.insert_to_start(image_cont, h_img, w_img, out_matrix)
					new_image.save("out_img/watermark_ins.PNG")
					cp.bprint("Evaluate the embedding quality?")
					cp.bprint("1 - Yes;")
					cp.bprint("2 - No.")
					obs = int(input())
					while obs != "exit": 
						match obs:
							case 1:
								mse = proc.get_mse(start_img, new_image)
								rmse = proc.get_rmse(mse)
								psnr = proc.get_psnr(mse)
								ssim = proc.get_ssim(start_img, new_image)
								cp.bprint("=====================")
								cp.bprint("MSE")
								cp.gprint(round(mse, 3))
								cp.bprint("---------------------")
								cp.bprint("RMSE")
								cp.gprint(round(rmse, 3))
								cp.bprint("---------------------")
								cp.bprint("PSNR")
								cp.gprint(round(psnr, 3))
								cp.bprint("---------------------")
								cp.bprint("SSIM")
								cp.gprint(round(ssim, 3))
								cp.bprint("=====================")
								obs = "exit"
							case 2:
								obs = "exit"
							case _:
								cp.rprint("Enter either 1 (Yes) or 2 (No).")
								obs = int(input())
					
					cp.bprint("Evaluate the embedding robustness to destructive actions?")
					cp.bprint("Yes - 1")
					cp.bprint("No  - 2")
					destr = int(input())
					while destr != "exit": 
						match destr:
							case 1:
								ext_mes = extract.extraction(new_image, t_inp)
								watermark_l = filters.to_list(watermark)
								cp.bprint("=====================")
								cp.bprint("BER_0") 
								BER_0 = filters.CHECK(watermark_l, ext_mes)
								cp.gprint(BER_0)
								cp.bprint("---------------------")
								cp.bprint("BER_blur") 
								BER_blur = filters.blur_and_check(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_blur, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_sharpen") 
								BER_sharpen = filters.sharpen_and_check(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_sharpen, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_contour") 
								BER_contour = filters.contour_and_check(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_contour, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_smooth") 
								BER_smooth = filters.smooth_and_check(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_smooth, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_jpeg_90") 
								BER_jpeg_90 = filters.jpg_scale_90(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_jpeg_90, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_jpeg_60") 
								BER_jpeg_60 = filters.jpg_scale_60(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_jpeg_60, 3))
								cp.bprint("---------------------")
								cp.bprint("BER_jpeg_20") 
								BER_jpeg_20 = filters.jpg_scale_20(t_inp, watermark_l, new_image)
								cp.gprint(round(BER_jpeg_20, 3))
								cp.bprint("=====================")
								destr = "exit"
							case 2:
								destr = "exit"
							case _:
								cp.rprint("Enter either 1 (Yes) or 2 (No).")
								destr = int(input())
					
					cp.bprint("Generate histograms?")
					cp.bprint("Yes - 1")
					cp.bprint("No  - 2")
					hist = int(input())
					while hist != "exit": 
						match hist:
							case 1:
								histograms.show_histograms(start_img, new_image)
								hist = "exit"
							case 2:
								hist = "exit"
							case _:
								cp.rprint("Enter either 1 (Yes) or 2 (No).")
								hist = int(input())
				return 0

			case 2:
				cp.bprint("Enter the value of parameter T (default value is 80):")
				t_inp = int(input())
				ext_mes = extract.extraction(image_cont, t_inp)
				step = h_img // 8
				ext_mes_dwm = proc.to_watermark_matrix(ext_mes, step)
				cp.bprint("Was Arnold Transformation applied during embedding?")
				cp.bprint("1 - Yes;")
				cp.bprint("2 - No.")
				inv_arn = int(input())
				if inv_arn == 1: 
					cp.bprint("Enter the number of iterations:")
					iter = int(input())
					h_wat, w_wat = ext_mes_dwm.shape
					ext_mes_dwm = proc.inv_arnold_transformation(ext_mes_dwm, h_wat, iter)
				# for row in ext_mes_dwm: cp.bprint(row)
				image = Image.fromarray((ext_mes_dwm * 255).astype(np.uint8), 'L')
				# Display the image
				image.save(f"out_watermark/watermark.PNG")
				todo_main == "exit"
				return 0
			case _:
				cp.bprint("What to do with the input file:")
				cp.bprint("1 - Embed watermark;")
				cp.bprint("2 - Extract watermark.")
				cp.bprint("Enter either 1 or 2!")
				todo_main = int(input())


if __name__ == "__main__": 
	main()
