import subprocess


class log_Handler:
    def __init__(self) -> None:
        self.terminal = subprocess.Popen(
            ["powershell", "-NoExit"],
            stdin=subprocess.PIPE,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    def write(self, msg):
        # logic to handle terminal logs
        self.terminal.stdin.write(f'Write-Host "{msg}"\n'.encode())
        self.terminal.stdin.flush()

    def terminate(self):
        self.terminal.stdin.close()
        self.terminal.terminate()
