import socket

class SocketConnection:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def send(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Socket connection was broken.")
            totalsent = totalsent + sent

    def receive(self):
        chunks = []
        bytes_recd = 0
        MSGLEN = 100
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == b'':
                raise RuntimeError("Socket connection was broken.")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            if chunk == msg_ok.encode():
                return b''.join(chunks)
        return b''.join(chunks)
