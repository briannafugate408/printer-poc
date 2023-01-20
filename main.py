from labelwriter import Labelwriter

from PIL import Image
import numpy as np



def get_pixel_data(image_path):
    image = Image.open(image_path, 'r')
    print(image)
    pixels = list(image.getdata())
    width = image.size[0]
    height = image.size[1]
    print(image.mode)
    print(width)
    print(height)

    img_data = []
    thresh = 127
    for y in range(0, height):
        for x in range(0, width):
            (r, g, b) = image.getpixel((x, y))
            print(r, g, b)



    array = np.array(img_data, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save('new.png')




 # print("Image mode: ", image.mode)
    # print('Width', width)
    # print('Height', height)
    # for i in range(0, len(pixels), 4):
        # if (pixels[i] <= 20 or pixels[i+1] <= 20 or pixels[i+2] < 20): 
        #     pixels[i] = 0
        #     pixels[i+1] = 0
        #     pixels[i+2] = 0
        # else:
        #     pixels[i] = 255
        #     pixels[i+1] = 255
        #     pixels[i+2] = 255

def main():
    print("Running program to connect to printer!")
    mylabelwriter = Labelwriter('192.168.1.80', 9100)

    # will tell printer to print and confirms a connection
    # mylabelwriter.send_print_command()

    # will tell printer to print text only in IPL
    # mylabelwriter.send_text_command()

    # will tell the printer to print the bitmap image
    mylabelwriter.send_print_bitmap_image_command("one-bit/land.bmp")

    # get_pixel_data("one-bit/land.bmp")


if __name__ == '__main__':
    main()
