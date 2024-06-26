import subprocess

def create_New_Terminal():
    terminal = subprocess.Popen(
        ["powershell", "-NoExit"],
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    return terminal


# Create a new terminal
terminal = create_New_Terminal()

while True:
    if terminal == None or terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_New_Terminal()
    msg = input("Enter Message:> ")
    if terminal == None or terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_New_Terminal()
    print(msg)

    if msg == "quit":
        # Close the terminal and exit the program
        terminal.stdin.close()
        terminal.terminate()
        break

    # Print the user-entered message in the terminal
    terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
    terminal.stdin.flush()
