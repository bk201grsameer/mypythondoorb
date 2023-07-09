import subprocess

# Create a new terminal
terminal = subprocess.Popen(['powershell', '-NoExit'], stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE)

while True:
    msg = input("askmessage: ")
    print(msg)

    # Print the user-entered message in the terminal
    terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
    terminal.stdin.flush()
