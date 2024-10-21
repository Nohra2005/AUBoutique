from socket import*
import threading
from protocol import client_handler

# Server setup
server = socket(AF_INET, SOCK_STREAM)
server.bind(('localhost', 8888))  
server.listen(5)

while True:
    client, addr = server.accept()
    print(f"New connection from {addr}")
    
    # Start a new thread for each connected client
    client_thread = threading.Thread(target=client_handler, args=(client,))
    client_thread.start()

