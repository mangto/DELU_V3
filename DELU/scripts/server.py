import socket
import threading

client_ids = {}  # Mapping of client sockets to their IDs

def handle_client(client_socket, address):
    # print(f"Accepted connection from {address}")

    # Ask the client to log in with an ID
    client_id = client_socket.recv(1024).decode('utf-8')

    # print(f"Client {client_id} logged in from {address}")
    client_ids[client_socket] = client_id

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            # print(f"Received message from {client_id}: {message}")

            # Check if the message is intended for a specific client
            if message.startswith('@'):
                recipient_id, message = message.split(' ', 1)
                send_direct_message(recipient_id[1:], message, client_socket)
            else:
                # Broadcast the message to all connected clients
                broadcast(message, client_socket)

        except Exception as e:
            print(f"Error handling client {client_id}: {e}")
            break

    print(f"Connection from {client_id} closed")
    del client_ids[client_socket]
    client_socket.close()

def broadcast(message, sender_socket):
    for client, client_id in client_ids.items():
        if client != sender_socket:
            try:
                client.send(f"{message}".encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message to {client_id}: {e}")

def send_direct_message(recipient_id, message, sender_socket):
    for client, client_id in client_ids.items():
        if client_id == recipient_id:
            try:
                client.send(message.encode('utf-8'))
                break  # Message sent, exit the loop
            except Exception as e:
                print(f"Error sending private message to {recipient_id}: {e}")

def start():
    # Set up the server
    host = '0.0.0.0'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on {host}:{port}")


    # Main server loop
    while True:
        client_socket, address = server_socket.accept()

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()
