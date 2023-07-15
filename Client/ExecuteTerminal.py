import subprocess
import platform

""" 
The first code snippet is using the subprocess.Popen function to open a PowerShell session with a specific command. It passes the command as an argument to the powershell.exe executable and sets up the process to capture the output of the command. The shell=True parameter indicates that the command should be executed through the shell.
"""


class TermialExecutor:
    def __init__(self) -> None:
        pass
    
    def execute(self, command):
        try:
            if platform.system() == "Windows":
                terminal = subprocess.Popen(
                    ["powershell.exe", command],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )
            else:
                terminal = subprocess.Popen(
                    ["/bin/bash", "-c", command],
                    shell=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                )

            result = terminal.stdout.read() + terminal.stderr.read()
            result = result.decode()
            return result
        except Exception as e:
            print(f"[+] SOMETHING WENT WRONG: {str(e)}")