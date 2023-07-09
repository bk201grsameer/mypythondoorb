import subprocess

# Create a new terminal
terminal = subprocess.Popen(['powershell', '-NoExit'], stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE)

while True:
    msg = input("Enter Message:> ")
    print(msg)

    if msg == "quit":
        # Close the terminal and exit the program
        terminal.stdin.close()
        terminal.terminate()
        break

    # Print the user-entered message in the terminal
    terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
    terminal.stdin.flush()
