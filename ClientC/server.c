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
// #include<arpa/inet.h>
// #include<netinet/in.h>

#include <winsock2.h>
#include <ws2tcpip.h>

int main()
{
    int sock, client;
    char buffer[1024];
    char total_response[18384];
    struct sockaddr_in sa, ca;

    int i = 0;
    int optval = 1;

    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        printf("[+] Failed to initialize Winsock.\n");
        exit(1);
    }
    int client_length;
    sock = socket(AF_INET, SOCK_STREAM, 0);

    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, (const char *)&optval, sizeof(optval)) < 0)
    {
        printf("[+] SOMETHING WENT WRONG WHILE SETTING SOCKET OBJ");
        exit(1);
    }
    sa.sin_family = AF_INET;
    sa.sin_addr.s_addr = inet_addr("192.168.189.130");
    sa.sin_port = htons(8001);

    bind(sock, (struct sockaddr *)&sa, sizeof(sa));
    listen(sock, 5);

    client_length = sizeof(ca);

    client = accept(sock, (struct sockaddr *)&ca, client_length);
}