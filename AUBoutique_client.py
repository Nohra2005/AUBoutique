from socket import *
import json

# Client setup
client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 8888))

# Function to send a command to the server
def send_command(command, data=None):
    message = {"command": command}
    if data:
        message.update(data)
    client.send(json.dumps(message).encode('utf-8'))
    return client.recv(1024).decode('utf-8')

while True:
    # Registration
    print("1. Register")
    print("2. Login")
    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter name: ")
        email = input("Enter email: ")
        username = input("Enter username: ")
        password = input("Enter password: ")
        registration_data = {
            "name": name,
            "email": email,
            "username": username,
            "password": password
        }
        result = send_command("register", registration_data)
        print(result)

    elif choice == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_data = {"username": username, "password": password}
        result = send_command("login", login_data)
        print(result)
        if result == "Login successful":
            break
    
while True:
    print("\n1. Add a product")
    print("2. View all products")
    print("3. View products by owner")
    print("4. Check if owner is online")
    print("5. Message owner")
    print("6. Quit")
    action = input("Choose an action: ")

    if action == "1":
        product_name = input("Enter product name: ")
        product_description = input("Enter product description: ")
        product_price = input("Enter product price: ")
        product_data = {
            "name": product_name,
            "description": product_description,
            "price": product_price,
            "owner": username
        }
        result = send_command("add_product", product_data)
        print(result)

    elif action == "2":
        products = send_command("view_products")
        print("Available products:", products)

    elif action == "3":
        owner = input("Enter owner's username: ")
        products_by_owner = send_command("view_products_by_owner", {"owner": owner})
        print(f"Products by {owner}:", products_by_owner)
    
    elif action == "4":
        owner = input("Enter owner's username: ")
        online_status = send_command("check_online_status", {"owner": owner})
        print(online_status)
        
    elif action == "5":
        owner = input("Enter the username you want to message: ")
        msg = input("Enter your message: ")
        rcpt_status = send_command("send_message", ({"owner": owner}, {"message": msg}))
        print(rcpt_status)
        
    elif action == "6":
        print("Thank you for using AUBoutique!")
        send_command("quit")
        break
    else:
        print("Invalid option.")
