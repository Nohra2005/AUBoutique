from socket import*
import json
import _sqlite3
from protocol import registration_handling

server = socket(AF_INET, socket.SOCK_STREAM)
server_host = 'localhost'
server_port = 8888
server.bind((server_host, server_port))
server.listen(5)

while True:
    client, client_address = server.accept()
    #Send option to register or login
    menu = "\nWelcome to AUBoutique! Please choose:\n1. Register\n2. Login\n"
    client.send(menu.encode('utf-8'))
    #Receive client's choice
    choice = client.recv(1024).decode('utf-8')
 
    #Handle registration
    if choice == '1':
        # Receive registration data from client
        registration_data = client.recv(1024).decode('utf-8')
        registration_data = json.loads(registration_data)  # Convert JSON string to dictionary
        # Call registration handling from protocol
        result = registration_handling(registration_data)
        if result is True:
            client.send(b"Registration successful!\n")
        elif result is False:
            client.send(b"Username already taken. Please try again.\n")
        else:
            # If it's an error message, send it to the client
            client.send(result.encode('utf-8'))  # Send the error message to the client
    
    #Handle Login
    elif choice == '2':
        client.send(b"Login feature coming soon!\n")
        
    #If client doesn't enter 1 or 2
    else:
        client.send(b"Invalid choice. Try again.\n")
        