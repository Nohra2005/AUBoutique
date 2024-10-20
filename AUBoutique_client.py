from socket import*
import json
from protocol import register_client

client = socket(AF_INET, SOCK_STREAM)
server_host = 'localhost'  
server_port = 8888  
try:
    client.connect((server_host, server_port))
    message = client.recv(1024).decode('utf-8')
    print(message)  

    #Client choses if he wants to register or log in
    choice = input("Enter your choice (1 or 2): ")
    client.send(choice.encode('utf-8'))


    #Register
    if choice == "1":
        registration_data = register_client()
         #Convert to json and send registration information to server
        registration_message = json.dumps(registration_data).encode('utf-8')
        client.send(registration_message)
        registration_status = client.recv(1024).decode('utf-8')
        print(registration_status)

except ConnectionRefusedError:
    print("Failed to connect to the server.")

finally:
    # Close the connection
    client.close()