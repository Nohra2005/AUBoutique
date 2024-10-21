import json
import _sqlite3

#Server function that handles the clients
def client_handler(client_socket):
    while True:
        try:
            # Receive message from client
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            
            # Parse the message (assume it's JSON formatted)
            data = json.loads(message)
            
            if data["command"] == "register":
                response = registration_handling(data)
            elif data["command"] == "login":
                response = login_handling(data)
            else:
                response = "Invalid command"

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))

        except ConnectionResetError:
            print("Client disconnected")
            break

    client_socket.close()
    
#Client side registration
def register_client():
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    username = input("Enter you username: ")
    password = input("Enter your password: ")
    
    #Write the registration data in a json readable format
    registration_data = {
        "command": "register",
        "name": name,
        "email": email,
        "username": username,
        "password": password
    }
    
    return registration_data
   
#Server handling registration
def registration_handling(registration_data):
    #Open database
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor()
    
    #Extract client registration data
    name = registration_data["name"]
    email = registration_data["email"]
    username = registration_data["username"]
    password = registration_data["password"]
    
    try:
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        
        #Check if username if in database
        if user:
            return "Username already taken"
        # If username doesn't exist, insert the new user into the database
        c.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)", (name, email, username, password))
        conn.commit()
        return "Registration successfull"
    
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    
    finally:
        conn.close()
        
#Client side login
def login_client():
    username = input("Enter you username: ")
    password = input("Enter your password: ")
    
    #Write the login data in a json readable format
    login_data = {
        "command": "login",
        "username": username,
        "password": password
    }
    
    return login_data

#Server handling login
def login_handling(login_data):
    #Open database
    conn = _sqlite3.connect('auboutique.db')
    c = conn.cursor() 
    #Extract client registration data
    username = login_data["username"]
    password = login_data["password"]
    
    #Search for username in database
    try:
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        #If username is found, check if password is matching
        if user:
            stored_password = user[4]  # Extract password from database (4th column)
            if password == stored_password:
                return "Login successful"  
            else:
                return "Incorrect password"
        else:
            return "Username not found"  
        
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    
    finally:
        conn.close()
    
