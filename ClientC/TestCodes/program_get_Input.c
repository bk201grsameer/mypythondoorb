#include <stdio.h>
#include <windows.h>

int APIENTRY WinMain(HINSTANCE hInst, HINSTANCE hInstPrev, PSTR cmdline, int cmdshow)
{
    HWND stealth;
    AllocConsole();

    // Display a message in the console
    printf("Hello, world from the console!\n");

    // Read user input from the console
    char userInput[256];
    printf("Enter something: ");
    fgets(userInput, sizeof(userInput), stdin);
    // Display the user's input
    printf("You entered: %s\n", userInput);
    MessageBox(NULL, "hello, world", "caption", 0);
}
