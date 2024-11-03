# src/network/rpc.py

import json
import socket
import threading

class RPCServer:
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.methods = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"RPC Server listening on {self.host}:{self.port}")

        # Start the server thread
        threading.Thread(target=self.accept_connections, daemon=True).start()

    def accept_connections(self):
        """Accept incoming RPC requests."""
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"RPC connection from {address} has been established.")
            threading.Thread(target=self.handle_request, args=(client_socket,), daemon=True).start()

    def handle_request(self, client_socket):
        """Handle incoming RPC requests."""
        while True:
            try:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break
                response = self.process_request(request)
                client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                print(f"Error handling request: {e}")
                break
        client_socket.close()

    def process_request(self, request):
        """Process an RPC request."""
 try:
            request_data = json.loads(request)
            method_name = request_data['method']
            method_args = request_data.get('args', [])
            method_kwargs = request_data.get('kwargs', {})
            if method_name in self.methods:
                result = self.methods[method_name](*method_args, **method_kwargs)
                return json.dumps({'result': result})
            else:
                return json.dumps({'error': f"Method '{method_name}' not found"})
        except Exception as e:
            return json.dumps({'error': str(e)})

    def register_method(self, method_name, method_func):
        """Register an RPC method."""
        self.methods[method_name] = method_func

    def close(self):
        """Close the RPC server socket."""
        self.server_socket.close()

class RPCClient:
    def __init__(self, host='localhost', port=5001):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def invoke(self, method_name, *args, **kwargs):
        """Invoke an RPC method on the server."""
        request = json.dumps({'method': method_name, 'args': args, 'kwargs': kwargs})
        self.client_socket.sendall(request.encode('utf-8'))
        response = self.client_socket.recv(1024).decode('utf-8')
        response_data = json.loads(response)
        if 'error' in response_data:
            raise Exception(response_data['error'])
        return response_data['result']

    def close(self):
        """Close the RPC client socket."""
        self.client_socket.close()
