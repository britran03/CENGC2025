# Code Cracker

Welcome to the most advanced code cracker since Y2K.

## Features

- Caesar Cipher: Decode the hardest caesar ciphers known to man with Caesar mode (warning: May also output a salad)
- Depth first base search: Search through different base codes at multiple depths
- Automatic Password Checking: Check your password automatically against the zip
- Agentic AI: Use AI to help guide you in your cipher searchin

## Installation

To install, simply clone the repository from GitHub and and use the command `python3 -m pip install .` to install the tool on your system.

## Usage

Code cracker comes with a rich command line interface. You can run it using the command `python3 -m base_cracker.cli`. The tool is meant to aid in deciphering messages through caesar cipher transformations, base changes, and AI support
- You must provide a zip file to check the success of the tool against using the `--zip` argument, and a code to start from using the `--code` argument. The code will have transformations performed on it and be checked against the zip
- To use the caesar cipher, run the program with the `--caesar <shift>` command, which will print the message shifted by `<shift>` letters
- The program will attempt a variety of transformations of base. To determine the maxiumum number of transformations to apply in a row, use the `--depth <depth>` flag

## References

[1] "ChatGPT." OpenAI [Online]. Available: https://chat.openai.com/chat (accessed Nov. 15, 2025).
