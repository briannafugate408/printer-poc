from labelwriter import Labelwriter
import cv2
import PIL.Image
import PIL.ImageFont
import PIL.ImageDraw
import numpy as np
from tkinter import *
from tkinter import Canvas, PhotoImage
import io
import os
import sys


def draw_canvas():
    #Create Image object
    im = PIL.Image.open("one-bit/whitebackground.png")

    #Draw circle
    draw = PIL.ImageDraw.Draw(im)
    draw.ellipse((20, 20, 180, 180), fill = 'blue', outline ='blue')

    #Draw text
    font = PIL.ImageFont.load_default()
    draw = PIL.ImageDraw.Draw(im)
    draw.text((60, 250), "Hello World", font=font)

    #Draw from an image
    logo = PIL.Image.open('one-bit/logo.png')
    im.paste(logo, (200, 50))


    #Save image
    im.save('one-bit/my-awesome-image.bmp')




def main():
    print("Running program to connect to printer!")
    mylabelwriter = Labelwriter('192.168.1.215', 9100)

    # will tell printer to print and confirms a connection
    # mylabelwriter.send_print_command()

    # will tell printer to print text only in IPL
    # mylabelwriter.send_text_command()

    # will tell the printer to print the bitmap image

    #get_pixel_data("one-bit/land.bmp")

    draw_canvas()
    mylabelwriter.send_print_bitmap_image_command("one-bit/my-awesome-image.bmp")



if __name__ == '__main__':
    main()
