from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def show_histograms(start_img: Image, stego_img: Image):
    """
    Show histograms of the red channel for the original and stego images.

    Args:
        start_img (Image): The original image.
        stego_img (Image): The stego image.
    """
    
    start_img_array = np.array(start_img)
    stego_img_array = np.array(stego_img)

    start_img_array_red = start_img_array[:, :, 2]
    stego_img_array_red = stego_img_array[:, :, 2]

    plt.figure(figsize=(10, 6))
    plt.hist(start_img_array_red.flatten(), bins=256, color='b', alpha=0.5)
    plt.title("Histogram of the original image (RED channel)")
    plt.xlabel("Pixel Value")
    plt.ylabel("Number of Pixels")
    plt.savefig("histograms/original_histogram.png")

    plt.figure(figsize=(10, 6))
    plt.hist(stego_img_array_red.flatten(), bins=256, color='r', alpha=0.5)
    plt.title("Histogram of the stego image (RED channel)")
    plt.xlabel("Pixel Value")
    plt.ylabel("Number of Pixels")
    plt.savefig("histograms/stego_histogram.png")