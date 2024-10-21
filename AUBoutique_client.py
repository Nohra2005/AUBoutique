from socket import*
import json
from protocol import register_client, login_client

# Client setup
client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 8888))

while True:
    print("1. Register")
    print("2. Login")
    choice = input("Enter your choice: ")

    if choice == "1":
        registration_data = register_client()
        client.send(json.dumps(registration_data).encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
    elif choice == "2":
        login_data = login_client()
        client.send(json.dumps(login_data).encode('utf-8'))
        response = client.recv(1024).decode('utf-8')
        print(response)
        
        if response == "Login successful":
            print("Proceeding to next task...")
            break
    else:
        print("Invalid choice. Try again.")
