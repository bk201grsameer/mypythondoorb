# Controlling Terminal Window with Python and subprocess

The following example demonstrates how to control a terminal window using Python and the `subprocess` module. Specifically, it shows how to create a new terminal window, send commands to it, and interact programmatically with the terminal.

## Example Code

```python
import subprocess

# Create a new terminal
terminal = subprocess.Popen(['powershell', '-NoExit'], stdin=subprocess.PIPE, creationflags=subprocess.CREATE_NEW_CONSOLE)

while True:
    msg = input("Enter Message: ")
    print(msg)

    if msg == "quit":
        # Close the terminal and exit the program
        terminal.stdin.close()
        terminal.terminate()
        break

    # Print the user-entered message in the terminal
    terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
    terminal.stdin.flush()

```
## Explanation
```python
   terminal = subprocess.Popen(['powershell', '-NoExit'], stdin=subprocess.PIPE,
   creationflags=subprocess.CREATE_NEW_CONSOLE)
``` 
### Usage
   1) This line creates a new terminal window using subprocess.Popen(). It launches the PowerShell command (powershell) with the -NoExit flag to keep the terminal window open. The stdin=subprocess.PIPE parameter sets up a pipe to write to the terminal's standard input. Finally, creationflags=subprocess.CREATE_NEW_CONSOLE creates a new console window for the PowerShell process.
