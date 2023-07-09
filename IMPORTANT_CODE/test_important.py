import subprocess

while True:
    msg = input("askmessage: ")
    print(msg)

    # Launch a new PowerShell process and execute "print('some result')" in it
    subprocess.Popen(['powershell', '-NoExit', '-Command', 'Write-Host "some result"'], creationflags=subprocess.CREATE_NEW_CONSOLE)
