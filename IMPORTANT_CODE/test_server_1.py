import threading
import socket
import sys

# Shared variable to signal all threads to exit
exit_flag = False

# Lock to synchronize access to the exit flag
exit_flag_lock = threading.Lock()


class Server:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)

        # Create and start the handle client thread
        self.handle_client_thread = threading.Thread(target=self.handle_client_thread)
        self.handle_client_thread.start()

        # Start the network connection thread
        self.network_connection_thread = threading.Thread(
            target=self.network_connection_thread
        )
        self.network_connection_thread.start()

    def handle_client_thread(self):
        global exit_flag
        while True:
            # Simulate getting user input from the client
            user_input = input("Enter 'exit' to quit: ")

            if user_input == "exit":
                # Acquire the lock to safely access the exit flag
                with exit_flag_lock:
                    exit_flag = True
                break

    def network_connection_thread(self):
        while True:
            # Handle network connections and other tasks here
            print("Network connection thread is running")

            # Check if the exit flag is set
            with exit_flag_lock:
                if exit_flag:
                    print("Exiting the program")
                    sys.exit()

            # Continue with normal tasks if the exit flag is not set
            # ...

    def start(self):
        # Main thread
        while True:
            # Do other tasks in the main thread
            print("Main thread is running")

            # Check if the exit flag is set
            with exit_flag_lock:
                if exit_flag:
                    print("Exiting the program")
                    break

            # Accept incoming requests with a timeout
            self.server.settimeout(1)  # Set a timeout value for server.accept()
            try:
                client, address = self.server.accept()
                print(f"Incoming request from {address}")
                # Process the accepted client connection
                # ...
            except socket.timeout:
                continue


# Create and start the server
server = Server("192.168.0.151", 8000)
server.start()
