# not working
import subprocess


def create_new_terminal():
    terminal = subprocess.Popen(
        ["powershell", "-NoExit"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    return terminal


# Create a new terminal
terminal = create_new_terminal()

while True:
    if terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_new_terminal()

    msg = input()

    if terminal.poll() is not None:
        print(f"[-] Terminal is closed")
        terminal = create_new_terminal()

    if msg == "quit":
        # Close the terminal and exit the program
        terminal.stdin.close()
        terminal.terminate()
        break

    # Print the user-entered message in the terminal
    terminal.stdin.write(f'"{msg}"\n'.encode())
    terminal.stdin.flush()

    # Read the output from the terminal
    output = terminal.stdout.readline().decode().strip()
    if output:
        print(output)
