# src/network/peer_to_peer.py

import socket
import threading
import json

class PeerToPeer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.peers = set()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Listening for connections on {self.host}:{self.port}")

        # Start the server thread
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        """Accept incoming connections from peers."""
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Connection from {address} has been established.")
            self.peers.add(address)
            threading.Thread(target=self.handle_peer, args=(client_socket, address), daemon=True).start()

    def handle_peer(self, client_socket, address):
        """Handle communication with a connected peer."""
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                self.process_message(message, address)
            except ConnectionResetError:
                break
        client_socket.close()
        self.peers.remove(address)
        print(f"Connection from {address} has been closed.")

    def process_message(self, message, address):
        """Process incoming messages from peers."""
        print(f"Received message from {address}: {message}")
        # Here you can add logic to handle different types of messages

    def broadcast(self, message):
        """Broadcast a message to all connected peers."""
        for peer in self.peers:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect(peer)
                    sock.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"Failed to send message to {peer}: {e}")

    def connect_to_peer(self, peer_address):
        """Connect to a specified peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(peer_address)
                self.peers.add(peer_address)
                print(f"Connected to peer: {peer_address}")
        except Exception as e:
            print(f"Failed to connect to {peer_address}: {e}")

    def close(self):
        """Close the server socket."""
        self.server_socket.close()
