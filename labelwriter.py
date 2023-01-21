from socketconn import SocketConnection
import struct
from PIL import Image

def bencmsg(msg):
    crlf = "\r\n"
    msg_ok = "\r\nOk\r\n"
    message = msg+crlf
    return message.encode()


class Labelwriter:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = SocketConnection()
        self._connected = False

        while not self._connected:
            try:
                self._socket.connect(self._ip, self._port)
                self._connected = True
                print("Established a connection to printer.")
            except ConnectionRefusedError:
                print("Unable to establish a connection to printer.")
                time.sleep(1)
                raise

    def print_bitmap_image_meta_data(self, bmp):
        print('Type:', bmp.read(2).decode())
        print('Size: %s' % struct.unpack('I', bmp.read(4)))
        print('Reserved 1: %s' % struct.unpack('H', bmp.read(2)))
        print('Reserved 2: %s' % struct.unpack('H', bmp.read(2)))
        print('Offset: %s' % struct.unpack('I', bmp.read(4)))
        print('DIB Header Size: %s' % struct.unpack('I', bmp.read(4)))
        print('Width: %s' % struct.unpack('I', bmp.read(4)))
        print('Height: %s' % struct.unpack('I', bmp.read(4)))
        print('Color Planes: %s' % struct.unpack('H', bmp.read(2)))
        print('Bits per Pixel: %s' % struct.unpack('H', bmp.read(2)))
        print('Compression Method: %s' % struct.unpack('I', bmp.read(4)))
        print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4)))
        print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4)))
        print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4)))
        print('Number of Color: %s' % struct.unpack('I', bmp.read(4)))
        print('Important Color: %s' % struct.unpack('I', bmp.read(4)))
        print("---------------------------------------")

    # Currently supports one bit bitmap images only
    def send_print_bitmap_image_command(self, image_path):
        img = Image.open(image_path)
        width = img.width
        height = img.height
        print("Weight:", width)
        print("Height:", height)

        img_coordinates = []

        black_threshold = 40
        dark_gray_threshold = 140
        light_gray_threshold = 240

        for y in range(height):
            columns = []
            for x in range(width):
                r = img.getpixel((x,y))[0]
                # print
                # check quad 1 range 
                if r <= black_threshold:
                    # assign the coordinates to black
                    columns.append('1')
                    # columns.append('00000000')
                # check quad 2 range 
                # assign the coordinates to dark gray
                elif r <= dark_gray_threshold:
                    # columns.append('00110010')
                    columns.append('1')
                # check quad 3 range
                    # assign the coordinates to light gray
                elif r <= light_gray_threshold:
                    # columns.append('110010000')
                    columns.append('0')
                # check quad 4 range
                else:
                    # assign the coordinates to light gray
                    # columns.append('11111111')
                    columns.append('0')


            print("Total columns:", len(columns))
            img_coordinates.append(columns)

        STX = "<STX>"
        ESC = "<ESC>"
        ETX = "<ETX>\n"

        IPL = ""
        IPL += "{}{}c{}".format(STX, ESC, ETX)
        IPL += "{}{}P{}".format(STX, ESC, ETX)
        IPL += "{}G1,item;x{};y{};{}".format(STX,
                                                 height, width, ETX)

        binary_row = ""
        binary_rows = []

        row_count = 0
        for y in range(height):
            for x in range(width):
                # Format HEX byte to binary
                # byte = 1 pixel
                # we want to take that byte and turn it into either black or white
                binary_row += img_coordinates[y][x]
                    
            binary_rows.append(binary_row)
            IPL += "{}u{},{};{}".format(STX, row_count, binary_row, ETX)
            row_count += 1
            binary_row = ""

        IPL += "{}R;{}".format(STX, ETX)
        self.send_single_command(IPL)
        self.send_single_command("""
            <STX><ESC>C<ETX>
            <STX><ESC>P<ETX>
            <STX>E8;F8<ETX>
            <STX>U2;o0,180;c1;w1;h1<ETX>
            <STX>R;<ETX>
            <STX><ESC>E8<ETX>
            <STX><ETB><ETX>
        """)

    def send_single_command(self, command):
        self._socket.send(bencmsg(command))

    def send_print_command(self):
        command = "<STX><ETB><ETX>"
        self.send_single_command(command)

    def send_text_command(self):
        command = """                                                                             
        <STX><ESC>E4<ETX>                                                                                                                             
        <STX><CAN><ETX>                                                                      
        <STX>THIS IS THE SAMPLE LABEL<CR><ETX>                           
        <STX><ETB><ETX>             
        """
