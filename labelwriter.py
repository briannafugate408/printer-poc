from socketconn import SocketConnection

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
        self.send_single_command(command)


