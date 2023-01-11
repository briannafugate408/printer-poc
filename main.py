from labelwriter import Labelwriter


def main():
    print("Running program to connect to printer!")
    mylabelwriter = Labelwriter('192.168.1.215', 9100)
    
    # will tell printer to print and confirms a connection
    # mylabelwriter.send_print_command()

    # will tell printer to print text only in IPL
    mylabelwriter.send_text_command()
    

if __name__ == '__main__':
    main()