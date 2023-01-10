from labelwriter import Labelwriter


def main():
    print("Running program to connect to printer!")
    mylabelwriter = Labelwriter('192.168.1.215', 9100)
    mylabelwriter.beep()
    

if __name__ == '__main__':
    main()