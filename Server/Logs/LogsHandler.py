import subprocess


class log_Handler:
    def __init__(self) -> None:
        self.terminal = self.create_New_Terminal()

    # write to terminal
    def write(self, msg):
        # before writing cehck if the terminal is there to log or not
        if self.terminal == None or self.terminal.poll() is not None:
            self.terminal = self.create_New_Terminal()
        # logic to handle terminal logs
        self.terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
        self.terminal.stdin.flush()

    # close terminal
    def terminate(self):
        self.terminal.stdin.close()
        self.terminal.terminate()

    def create_New_Terminal(self):
        terminal = subprocess.Popen(
            ["powershell", "-NoExit"],
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )
        return terminal
