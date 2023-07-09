const { exec } = require('child_process');
const readline = require('readline');

// Create a new terminal
const terminal = exec('cmd.exe');

// Create a readline interface for user input
const rl = readline.createInterface({
  input: process.stdin,
  output: terminal.stdin,
  terminal: false
});

rl.on('line', (input) => {
  console.log(input);

  if (input === 'quit') {
    // Close the terminal and exit the program
    terminal.stdin.end();
    terminal.kill();
    process.exit();
  }

  // Print the user-entered message in the terminal
  terminal.stdin.write(`${input}\n`);
});
