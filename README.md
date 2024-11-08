# AUBoutique

**Created by:**  
- Christophe El Chabab
- Joey Saade
- Tatiana Nohra  

---

## Project Overview

**AUBoutique** is a simple socket-based client-server application that simulates an online boutique platform. Users can register, log in, add products for sale, browse available products, and send messages to other users. AUBoutique also includes features like managing pending messages for offline users, online status checking, and automated purchase instructions with scheduled pickups.

---

## Instructions for Running the Project

### Prerequisites
Ensure you have the following installed:
- Python 3.8 or higher
- SQLite3 (comes pre-installed with Python)

### Project Setup
1. **Clone the Repository** or download the provided files to your working directory.
   - Files included:
     - `AUBoutique_client.py`
     - `AUBoutique_server.py`
     - `protocol.py`
     - `auboutique.db` (pre-configured SQLite database)

2. **Setup the Database**
   - Ensure the `auboutique.db` file is in the same directory as the server script.
   - If you wish to clear existing entries in the database, you can run the following script:
     ```python
     import _sqlite3
     conn = _sqlite3.connect('auboutique.db')
     c = conn.cursor()
     c.execute("DELETE FROM users")
     c.execute("DELETE FROM products")
     c.execute("DELETE FROM messages")
     conn.commit()
     conn.close()
     ```

3. **Run the Server**
   - Open a terminal or command prompt.
   - Run the server script:
     ```bash
     python AUBoutique_server.py
     ```
   - The server will start listening for incoming client connections on port `8888`.

4. **Run the Client**
   - Open another terminal or command prompt.
   - Run the client script:
     ```bash
     python AUBoutique_client.py
     ```
   - Follow the on-screen instructions to register, log in, and interact with the application (GUI is the implementation of part of phase II)
     
5. **Multiple Clients**
   - You can run as many instances of the client as you want, allowing multiple users to interact with the server simultaneously. Open a new terminal for each client instance and run the same script.
   - Each client instance can represent a unique user interacting with the system.

---

## Features

- **User Registration and Login**: Users can create an account and log in securely.
- **Product Management**: Add products with details like name, description, price, and owner.
- **Buyer Management**: View buyers of your products.
- **Messaging**: Send messages to other users; offline users will receive them upon logging in.
- **Online Status**: Check if a user is online.
- **Purchase Confirmation**: Automated pickup scheduling and confirmation for product purchases.
- **Pending Messages**: Offline messages are queued and sent upon login.

---


## Dependencies

- **Standard Libraries**:
  - `socket`: For managing network connections.
  - `json`: For encoding and decoding client-server communication.
  - `sqlite3`: For database management.
  - `threading`: For handling asynchronous operations like response listening.
  - `datetime`: For managing and formatting dates in the application.
  - `time`: For delaying operations in loops.
---

## Notes
- The client and server must run on the same network for testing.
- Ensure the database file `auboutique.db` is always available in the server's working directory.
- Pickup schedules for purchases are automated to two days after the transaction date.

--- 
