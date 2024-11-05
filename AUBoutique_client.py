from socket import *
import json
import threading
import time

# Client setup
client = socket(AF_INET, SOCK_STREAM)
client.connect(('localhost', 8888))


# Function to send a command to the server
def send_command(command, data=None):
    message = {"command": command}
    if data:
        message.update(data)
    client.send(json.dumps(message).encode('utf-8'))
    while len(responses)==0:
        time.sleep(0.1)
    return responses.pop()

responses=[]

# Function to listen for incoming messages
def listen_for_responses():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith("\nNew message from"):
                print(message) # Add the message to the shared list
            else:
                responses.append(message)
        except BlockingIOError:
            time.sleep(0.1)  # Wait a bit if no messages are available to avoid CPU overuse
        except:
            print("Connection to the server was lost.")
            break

listener_thread = threading.Thread(target=listen_for_responses, daemon=True)
listener_thread.start()

print("AUBoutique: Where Quality Meets Convenience - Discover our unique finds!\n")
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
        if result.startswith("Login successful"):
            break

print(f"\nWelcome {username}!")
while True:
    
    print("\n1. Add a product")
    print("2. View my product's buyers")
    print("3. View all products")
    print("4. View products by owner")
    print("5. Buy product")
    print("6. Check if owner is online")
    print("7. Message owner")
    print("8. Quit")
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
        my_buyers = send_command("view_buyers")
        buyer_list = json.loads(my_buyers) 
        if len(buyer_list) != 0:
            
            print("My product's buyers:")
            for buyer in buyer_list:
                product_name, buyer_name, buyer_username, buyer_email = buyer  
                print(f"Product: {product_name} | Buyer Name: {buyer_name} | Username: {buyer_username} | Email: {buyer_email}")
        else:
            print("None of your products have been bought.")


    elif action == "3":
        products = send_command("view_products")
        product_list = json.loads(products)  
        if len(product_list)!=0:
            print("Available products:")
            
            for product in product_list:
                product_id, name, description, price, owner, _ = product  
                print(f"ID: {product_id} | Name: {name} | Description: {description} | Price: ${price} | Owner: {owner}")
        else:
            "We are all out of products."

    elif action == "4":
        owner = input("Enter owner's username: ")
        products_by_owner = send_command("view_products_by_owner", {"owner": owner})
        product_list = json.loads(products_by_owner)
        if len(product_list) != 0:
              
            print(f"Products by {owner}:")
            for product in product_list:
                product_id, name, description, price, owner, buyer = product
                if buyer==None: buyer="Not bought yet"
                print(f"ID: {product_id} | Name: {name} | Description: {description} | Price: ${price} | Buyer: {buyer}")
        else:
            print(f"No products found for '{owner}'.")

    
    elif action == "5":
        product = input("Enter product name: ")
        result = send_command("buy_product", {"product": product})
        print(result)
    
    elif action == "6":
        owner = input("Enter owner's username: ")
        online_status = send_command("check_online_status", {"owner": owner})
        print(online_status)
        
    elif action == "7":
        owner = input("Enter the username you want to message: ")
        msg = input("Enter your message: ")
        rcpt_status = send_command("send_message", {"owner": owner, "message": msg})
        print(rcpt_status)
        
    elif action == "8":
        print("Thank you for using AUBoutique!")
        send_command("quit")
        break
    else:
        print("Invalid option.")
