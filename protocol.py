import json
import _sqlite3

# Function to handle client commands
def client_handler(client_socket):
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
            elif data["command"] == "login":
                response = login_handling(data)
            elif data["command"] == "add_product":
                response = add_product(data)
            elif data["command"] == "view_products":
                response = view_products()
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
        c.execute("INSERT INTO products (name, description, price, owner) VALUES (?, ?, ?, ?)",
                  (product_data["name"], product_data["description"], product_data["price"], product_data["owner"]))
        conn.commit()
        return "Product added successfully"
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()


# View products function
def view_products():
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        return json.dumps(products)
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    finally:
        conn.close()
