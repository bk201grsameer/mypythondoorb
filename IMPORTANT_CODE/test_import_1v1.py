import subprocess

def create_new_terminal():
    terminal = subprocess.Popen(
        ["powershell", "-NoExit"],
        stdin=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    return terminal

# Create a new terminal
terminal = create_new_terminal()

while True:
    if terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_new_terminal()

    msg = input("Enter Message:> ")

    if terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_new_terminal()

    print(msg)

    if msg == "quit":
        # Close the terminal and exit the program
        terminal.stdin.close()
        terminal.terminate()
        break


    # Print the user-entered message in the terminal
    terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
    terminal.stdin.flush()
    # Clear the current line in the terminal
    # terminal.stdin.write(b'\r' + b' ' * 100 + b'\r')
    # terminal.stdin.flush()