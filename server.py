import socket
from _thread import *
import threading
import sys

newConnect = threading.Lock()
currentPlayer = 0

player_data = []

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket, player_num):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
        self.player = player_num
        player_data.append([0,0])
        self.pos = player_data[self.player]

    def run(self):
        print ("Connection from:", clientAddress)
        self.csocket.send(bytes("Hi, I am Server.",'utf-8'))
        msg = ''
        while True:     
            data = self.csocket.recv(2048)
            msg = data.decode()
            player_data[self.player] = msg
            self.csocket.send(bytes(f"Current locations: {str(player_data)}\n",'UTF-8'))
            if msg=='bye':
              break
            print (f"Player {self.player} says:", msg)
            if len(player_data) > 1:
                if self.player == 0:
                    self.csocket.send(bytes(f"Player 2 location: {str(player_data[1])}",'UTF-8'))
                elif self.player == 1:
                    self.csocket.send(bytes(f"Player 1 location: {str(player_data[0])}",'UTF-8'))
            else:
                self.csocket.send(bytes(f"Not enough players connected.\nCurrent players: {len(player_data)}",'UTF-8'))
        print ("Client at", clientAddress , "has disconnected...")

LOCALHOST = socket.gethostname()
PORT = 5555
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client connection..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, currentPlayer)
    newthread.start()
    currentPlayer += 1
    