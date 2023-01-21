from labelwriter import Labelwriter
import cv2
from PIL import Image
import numpy as np


def main():
    print("Running program to connect to printer!")
    mylabelwriter = Labelwriter('192.168.1.80', 9100)

    # will tell printer to print and confirms a connection
    # mylabelwriter.send_print_command()

    # will tell printer to print text only in IPL
    # mylabelwriter.send_text_command()

    # will tell the printer to print the bitmap image
    mylabelwriter.send_print_bitmap_image_command("one-bit/logo.bmp")

    #get_pixel_data("one-bit/land.bmp")


if __name__ == '__main__':
    main()
