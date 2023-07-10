import socket
import wave

# Server details
server_ip = "192.168.0.151"  # Replace with the server's IP address
server_port = 5000  # Replace with the server's port number

# Create a socket and bind it to the server address
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(1)
print("Server listening on {}:{}".format(server_ip, server_port))

# Accept a client connection
client_socket, client_address = server_socket.accept()
print("Client connected:", client_address)

# Receive command from the client
command = client_socket.recv(1024).decode()
print("Command received:", command)

if command == "record":
    # Instruct the client to record audio
    client_socket.sendall("start".encode())

    # Receive and process audio data
    received_data = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_data += data

    # Save the received audio to a file
    output_file = "received_audio.wav"
    with wave.open(output_file, "wb") as file:
        file.setnchannels(2)  # Stereo audio
        file.setsampwidth(2)  # 2 bytes per sample
        file.setframerate(44100)  # Sample rate: 44100 Hz
        file.writeframes(received_data)
    print("Audio saved to", output_file)

# Close the client socket and server socket
client_socket.close()
server_socket.close()
