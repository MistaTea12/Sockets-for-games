import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 5555))
client.sendall(bytes("Hello, I am client.",'UTF-8'))
while True:
    in_data =  client.recv(1024)
    print("\n-----[SERVER]-----\n" ,in_data.decode(),"\n------------------\n")
    out_data = input("Send: ")
    while out_data == '':
        out_data = input("Send: ")
    client.sendall(bytes(out_data,'UTF-8'))
    if out_data=='bye':
        break
client.close()

    