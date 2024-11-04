import json
import _sqlite3

online_users = {}

# Function to handle client commands
def client_handler(client_socket):
    username = None
    while True:
        try:
            # Receive and decode the client's message
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break

            # Parse the message (JSON formatted)
            data = json.loads(message)

            # Dispatch the correct action based on the command
            if data["command"] == "register":
                response = registration_handling(data)
                if response=="Registration successful":
                    username = data["username"]
                    online_users[username] = None
            elif data["command"] == "login":
                response = login_handling(data)
                if response == "Login successful":
                    username = data["username"]
                    online_users[username] = client_socket # Add user to online list
                    pending_msgs = get_pending_messages(username)
                    if len(pending_msgs)!=0:
                        response += "\nYou have pending messages:\n" + "\n".join(pending_msgs)
            elif data["command"] == "add_product":
                response = add_product(data)
            elif data["command"] == "view_buyers":
                response = view_buyers(username)
            elif data["command"] == "view_products":
                response = view_products()
            elif data["command"] == "view_products_by_owner":
                response = view_products_by_owner(data)
            elif data["command"] == "buy_product":
                response = buy_product(username,data)
            elif data["command"] == "check_online_status":
                response = check_online_status(data)
            elif data["command"] == "send_message":
                response = send_message(username, data["owner"], data["message"])
            elif data["command"] == "quit":
                online_users[username]=None
                break
            else:
                response = "Invalid command"

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print("Client disconnected")
            break

    client_socket.close()


# Registration function
def registration_handling(registration_data):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        # Handle registration logic
        c.execute("SELECT * FROM users WHERE username=?", (registration_data["username"],))
        if c.fetchone():
            return "Username already taken"
        c.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)",
                  (registration_data["name"], registration_data["email"], registration_data["username"], registration_data["password"]))
        conn.commit()
        return "Registration successful"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()

# Login function
def login_handling(login_data):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM users WHERE username=?", (login_data["username"],))
        user = c.fetchone()
        if user and user[4] == login_data["password"]:
            return "Login successful"
        return "Invalid credentials"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()

# Add product function
def add_product(product_data):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO products (name, description, price, owner, buyer) VALUES (?, ?, ?, ?, NULL)",
                  (product_data["name"], product_data["description"], product_data["price"], product_data["owner"]))
        conn.commit()
        return "Product added successfully"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()

# View product buyers
def view_buyers(owner):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("""
        SELECT p.name, u.name, u.username, u.email 
        FROM products p 
        JOIN users u ON p.buyer = u.username 
        WHERE p.owner=? AND p.buyer IS NOT NULL
        """, (owner,))
        buyers = c.fetchall()
        return json.dumps(buyers)
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()
        
# View products function
def view_products():
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products WHERE buyer IS NULL")
        products = c.fetchall()
        return json.dumps(products)
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()

# View products by owner function (filter)
def view_products_by_owner(data):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products WHERE owner=?", (data["owner"],))
        products = c.fetchall()
        return json.dumps(products) if products else "No products found for this owner"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()
        
#Buy product
def buy_product(buyer,data):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT id, buyer FROM products WHERE name=?", (data["product"],))
        product = c.fetchone()
        if product==None:
            return "This product does not exist."
        elif product[1]!=None:
            return "This product has already been purchased."
        
        c.execute("UPDATE products SET buyer=? WHERE id=?", (buyer, product[0]))
        conn.commit()
        return "Product purchased successfully"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()
        
#Functions that allows client to check if a user is online
def check_online_status(user):
    user = user["owner"]
    if user in online_users:
        if online_users[user]!=False:
            return f"{user} is online"
        else:
            return f"{user} is offline"
    else:
        return f"{user} doesn't exist"

#Allows client to send a message to another user
def send_message(sender, receiver, message):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        status = "pending"
        if receiver in online_users and online_users[receiver] != None:
            rcv_socket = online_users[receiver]
            rcv_socket.send(f"\nNew message from {sender}:\n{message}".encode('utf-8'))
            status = "sent"
        
        c.execute("INSERT INTO messages (sender, receiver, message, status) VALUES (?, ?, ?, ?)", (sender, receiver, message, status))
        conn.commit()
        return f"Message to {receiver} {'sent' if status == 'sent' else 'queued for delivery'}."
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()
        
# Function to retrieve only pending messages from the database
def get_pending_messages(receiver):
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT message FROM messages WHERE receiver=? AND status='pending'", (receiver,))
        messages = [x.decode('utf-8') for x in c.fetchall()]
        c.execute("UPDATE messages SET status='sent' WHERE receiver=? AND status='pending'", (receiver,))
        conn.commit()
        return messages
    except _sqlite3.Error as e:
        print(f"Database error retrieving messages: {e}")
        return []
    finally:
        conn.close()