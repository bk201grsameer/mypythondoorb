import socket
import sounddevice as sd
import numpy as np

# Server details
server_ip = "192.168.0.151"  # Replace with the server's IP address
server_port = 5000  # Replace with the server's port number

# Create a socket and connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Send command to the server
command = "record"
client_socket.sendall(command.encode())

# Wait for the server's start command
start_command = client_socket.recv(1024).decode()
if start_command == "start":
    # Callback function for audio recording
    def callback(indata, frames, time, status):
        if status:
            print("Error:", status)
        client_socket.sendall(indata.tobytes())

    # Start audio recording for 10 seconds
    duration = 5  # Duration in seconds
    sample_rate = 44100  # Sample rate (adjust if needed)
    channels = 2  # Number of audio channels (adjust if needed)

    stream = sd.InputStream(
        callback=callback, channels=channels, samplerate=sample_rate
    )
    stream.start()
    sd.sleep(int(duration * 1000))
    stream.stop()

# Close the socket connection
client_socket.close()
