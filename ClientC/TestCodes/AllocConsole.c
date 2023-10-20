#include <windows.h>
#include <stdio.h>

// Function to write a message to the allocated console
void DebugLog(const char* message) {
    // Open the console output stream
    FILE* consoleStream = freopen("CONOUT$", "w", stdout);
    if (consoleStream) {
        printf("%s\n", message);
        fclose(consoleStream);
    }
}

int APIENTRY WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Allocate a console for debugging
    AllocConsole();

    // Display a message in the console
    DebugLog("Console is ready for debugging.");

    // Create a simple window for the GUI application (not the focus of this example)
    MessageBox(NULL, "This is a GUI window.", "GUI Window", MB_OK);

    // Write more debug messages to the console
    DebugLog("Debug message 1");
    DebugLog("Debug message 2");

    // Prompt the user for input
    char userInput[256];
    printf("Please enter something: ");
    fgets(userInput, sizeof(userInput), stdin);

    // Display the user's input in the console
    DebugLog("User entered: ");
    DebugLog(userInput);

    // Deallocate the console before exiting
    FreeConsole();

    return 0;
}
