import subprocess
""" original logs handler """

class log_Handler:
    def __init__(self) -> None:
        self.terminal = self.create_New_Terminal()

    # write to terminal
    def write(self, msg):
        # before writing cehck if the terminal is there to log or not
        if self.terminal == None or self.terminal.poll() is not None:
            self.terminal = self.create_New_Terminal()
        # logic to handle terminal logs
        self.terminal.stdin.write(
            f'Write-Host "{msg}" -ForegroundColor Green\n'.encode()
        )
        self.terminal.stdin.flush()

    # close terminal
    def terminate(self):
        # before writing cehck if the terminal is there to log or not
        if self.terminal == None or self.terminal.poll() is not None:
            return
        self.terminal.stdin.close()
        self.terminal.terminate()

    # this will create a new terminal
    """ 
    The second code snippet also uses subprocess.Popen, but it opens a new PowerShell session without executing any specific command. It uses the subprocess.CREATE_NEW_CONSOLE flag to create a new console window for the PowerShell session. It also sets up the process to accept input from the standard input (stdin=subprocess.PIPE).
    """

    def create_New_Terminal(self):
        terminal = subprocess.Popen(
            ["powershell", "-NoExit"],
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        return terminal
