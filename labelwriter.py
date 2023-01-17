from socketconn import SocketConnection
import struct


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
        with open(image_path, "rb") as bmp:
            # https://en.wikipedia.org/wiki/BMP_file_format
            self.print_bitmap_image_meta_data(bmp)

            # Getting offset position 10 - aka. where image starts
            bmp.seek(10, 0)
            offset = struct.unpack("I", bmp.read(4))[0]
            # Get the image height and width
            bmp.seek(18, 0)
            image_width = struct.unpack("I", bmp.read(4))[0]
            image_height = struct.unpack("I", bmp.read(4))[0]

            STX = "<STX>"
            ESC = "<ESC>"
            ETX = "<ETX>\n"

            IPL = ""
            IPL += "{}{}c{}".format(STX, ESC, ETX)
            IPL += "{}{}P{}".format(STX, ESC, ETX)
            IPL += "{}G1,item;x{};y{};{}".format(STX,
                                                 image_height, image_width, ETX)

            # Get the size of the image
            bmp.seek(34, 0)
            image_size = struct.unpack("I", bmp.read(4))[0]
            print("Image size:", image_size)

            # Get the number of bytes per row
            bytes_per_row = int(image_size / image_height)
            print("Bytes per row:", bytes_per_row)

            # Read picture data in binary
            bmp.seek(offset, 0)

            binary_row = ""
            binary_rows = []
            viewer = []

            row_count = 0
            for row in range(image_height):
                for byte in range(bytes_per_row):
                    # Format HEX byte to binary
                    binary_row += format(255 - struct.unpack("B",
                                         bmp.read(1))[0], "08b")

                binary = binary_row[:image_width]
                binary_rows.append(binary)
                IPL += "{}u{},{};{}".format(STX, row_count, binary, ETX)
                row_count += 1
                binary_row = ""

            IPL += "{}R;{}".format(STX, ETX)
            self.send_single_command(IPL)
            self.send_single_command("""
                <STX><ESC>C<ETX>
                <STX><ESC>P<ETX>
                <STX>E8;F8<ETX>
                <STX>U2;o0,0;c1;w5;h5;<ETX>
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
