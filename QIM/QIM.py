from PIL import Image
import cprint as cp
import functions
import filters
import histograms
import metrics

def main():
	"""
    The main function to interact with the user and perform embedding/extraction tasks.
    """
	cp.bprint("Enter the name of the input file (the file should be saved in the /in_img folder)")
	name = input()
	path_to_inp_image = "in_img/" + name

	try:
		input_img = Image.open(path_to_inp_image)
		start_img = input_img
		cp.bprint("What do you want to do with the input file:"
					"\n1 - embedding;"
					"\n2 - extraction.")

		TODO = int(input())
		while TODO != "exit":
			match TODO:
				case 1:
					cp.bprint("Enter the message to embed in the file; it should be saved in the /message folder")
					mes_name = input()
					mes_path = "message/" + mes_name
					file = open(mes_path, "r")
					message = file.readline()
					file.close()

					cp.bprint("Enter the quantization step:")
					q = int(input())

					output_image = embedding(input_img, message, q)
					cp.bprint("=====================")
					cp.bprint("MSE")
					MSE = metrics.obscurity_MSE(start_img, output_image)
					cp.gprint(MSE)
					cp.bprint("---------------------")
					cp.bprint("PSNR")
					PSNR = metrics.obscurity_PSNR(MSE)
					cp.gprint(PSNR)
					cp.bprint("---------------------")
					cp.bprint("RMSE")
					RMSE = metrics.obscurity_RMSE(MSE)
					cp.gprint(RMSE)
					cp.bprint("---------------------")
					cp.bprint("SSIM")
					SSIM = metrics.obscurity_SSIM(start_img, output_image)
					cp.gprint(SSIM)
					cp.bprint("---------------------")
					cp.bprint("EC")
					input_message_binary = functions.string_to_binary(message)
					EC = metrics.capacity(input_img, input_message_binary)
					cp.gprint(EC)
					cp.bprint("---------------------")
					cp.bprint("=====================")

					cp.bprint("Evaluate the robustness of embedding against destructive effects?")
					cp.bprint("Yes - 1")
					cp.bprint("No - 2")
					TODO_destr = int(input())

					while TODO_destr != "exit":
						match TODO_destr:
							case 1:
								cp.bprint("---------------------")
								# Blur
								cp.bprint("BER_blur")
								BER_blur = filters.blur_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_blur)
								cp.bprint("---------------------")
								# Sharpen
								cp.bprint("BER_sharpen")
								BER_sharpen = filters.sharpen_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_sharpen)
								cp.bprint("---------------------")
								# Smooth
								cp.bprint("BER_smooth")
								BER_smooth = filters.smooth_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_smooth)
								cp.bprint("---------------------")
								# Edge Detection
								cp.bprint("BER_contour")
								BER_contour = filters.contour_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_contour)
								cp.bprint("---------------------")
								# Detail Extraction
								cp.bprint("BER_detail")
								BER_detail = filters.detail_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_detail)
								cp.bprint("---------------------")
								# Emboss
								cp.bprint("BER_emboss")
								BER_emboss = filters.emboss_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_emboss)
								cp.bprint("---------------------")
								# Grayscale
								cp.bprint("BER_grayscale")
								BER_grayscale = filters.grayscale_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_grayscale)
								cp.bprint("---------------------")
								# Black and White
								cp.bprint("BER_0")
								BER_0 = filters.zero_and_check(q, input_message_binary, output_image)
								cp.gprint(BER_0)
								cp.bprint("---------------------")
								cp.bprint("=====================")
								cp.bprint("---------------------")
								TODO_destr = "exit"

							case 2:
								TODO_destr = "exit"
							case _:
								cp.rprint("Enter either 1 (Yes) or 2 (No).")
								TODO_destr = int(input())

					cp.bprint("Create histograms?")
					cp.bprint("Yes - 1")
					cp.bprint("No - 2")
					TODO_hist = int(input())

					while TODO_hist != "exit":
						match TODO_hist:
							case 1:
								histograms.show_histograms(start_img, output_image)
								TODO_hist = "exit"
							case 2:
								TODO_hist = "exit"
							case _:
								cp.rprint("Enter either 1 (Yes) or 2 (No).")
								TODO_hist = int(input())

					TODO = "exit"
					functions.save_img(output_image, "main")
				case 2:
					cp.bprint("Enter the quantization step:")
					q = int(input())
					message = ""
					message = extraction(input_img, q)
					cp.bprint(message)
					TODO = "exit"
				case _:
					cp.rprint("Enter either 1 (embedding) or 2 (extraction)")
					TODO = int(input())
	except FileNotFoundError:
		cp.rprint("File not found. Please note that the input file should be in the /in_img folder.")


def embedding(input_img: Image, input_message: str, q: int) -> Image:
	"""
    Embeds a message into an image using quantization.

    Args:
        input_img (Image): The input image.
        input_message (str): The message to be embedded.
        q (int): The quantization step.

    Returns:
        Image: The image with the embedded message.
    """
	input_img = input_img.convert('RGB')
	size_of_input_img = (input_img.size)
	can_insert = functions.check_size(size_of_input_img, input_message)

	if can_insert:
		input_message_binary = functions.string_to_binary(input_message)
		index_message = 0

		for y in range(size_of_input_img[1]):
			for x in range(size_of_input_img[0]):
				pos = (x, y)
				r, g, b = input_img.getpixel(pos)

				if index_message != len(input_message_binary):
					r_modified = q * (r // q) + (q // 2) * input_message_binary[index_message]
					input_img.putpixel(pos, (r_modified, g, b))
					index_message += 1

	else:
		cp.rprint("This message is too large to be embedded."
					"\nTherefore, the message has not been modified.")

	return input_img

def extraction(stego_img: Image, q: int) -> str:
	"""
    Extracts a message from a stego image using quantization.

    Args:
        stego_img (Image): The stego image.
        q (int): The quantization step.

    Returns:
        str: The extracted message.
    """
	stego_img = stego_img.convert('RGB')
	size_of_input_img = (stego_img.size)
	ext_message_binary = []

	for y in range(size_of_input_img[1]):
		for x in range(size_of_input_img[0]):
			pos = (x, y)
			r_modified, g, b = stego_img.getpixel(pos)
			P_0 = q * (r_modified // q)
			P_1 = q * (r_modified // q) + (q // 2)

			m_i = min(abs(r_modified - P_0), abs(r_modified - P_1))
			if abs(r_modified - P_0) < abs(r_modified - P_1):
				ext_message_binary.append(0)
			else:
				ext_message_binary.append(1)

	ext_message_str = ""
	ext_message_str = functions.binary_to_string(ext_message_binary)
	return ext_message_str

if __name__ == "__main__":
    main()