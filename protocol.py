import json
import _sqlite3

#Name is self explanatory
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
            return False
        # If username doesn't exist, insert the new user into the database
        c.execute("INSERT INTO users (name, email, username, password) VALUES (?, ?, ?, ?)", (name, email, username, password))
        conn.commit()
        return True
    
    except _sqlite3.Error as e:
        return f"Database error: {e}"
    
    finally:
        conn.close()