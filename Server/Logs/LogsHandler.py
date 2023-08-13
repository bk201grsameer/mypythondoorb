import subprocess
import platform


class log_Handler:
    def __init__(self) -> None:
        self.terminal = self.create_new_terminal()

    # Write to terminal
    def write(self, msg):
        # Before writing, check if the terminal is available for logging
        if self.terminal is None or self.terminal.poll() is not None:
            self.terminal = self.create_new_terminal()

        # Logic to handle terminal logs based on the platform
        if platform.system() == "Windows":
            self.terminal.stdin.write(
                f'Write-Host "{msg}" -ForegroundColor Green\n'.encode()
            )
        elif platform.system() == "Linux":
            self.terminal.stdin.write(f'echo -e "\\033[32m{msg}\\033[0m"\n'.encode())
        """ immediately console it """
        self.terminal.stdin.flush()

    # Close terminal
    def terminate(self):
        # Before terminating, check if the terminal is available for logging
        if self.terminal is None or self.terminal.poll() is not None:
            return
        self.terminal.stdin.close()
        self.terminal.terminate()

    # this will create a new terminal
    """ 
    The second code snippet also uses subprocess.Popen, but it opens a new PowerShell session without executing any specific command. It uses the subprocess.CREATE_NEW_CONSOLE flag to create a new console window for the PowerShell session. It also sets up the process to accept input from the standard input (stdin=subprocess.PIPE).
    """

    # Create a new terminal
    def create_new_terminal(self):
        if platform.system() == "Windows":
            terminal = subprocess.Popen(
                ["powershell", "-NoExit"],
                stdin=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        elif platform.system() == "Linux":
            terminal = subprocess.Popen(
                ["bash"],
                stdin=subprocess.PIPE,
            )
        else:
            raise NotImplementedError("Unsupported platform")

        return terminal
