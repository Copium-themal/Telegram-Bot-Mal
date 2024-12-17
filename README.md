# Malware Bot

Welcome to the Malware Bot! This bot allows you to generate and obfuscate malware payloads via a simple Telegram interface. It includes functionality to create custom payloads, obfuscate them using various techniques, and interact with infected machines by connecting to their IPs.

## Features

- **Generate Malware**: Allows the user to generate custom payloads with user-defined LHOST and LPORT.
- **Obfuscate Payload**: Apply multiple obfuscation techniques to make the payload harder to detect.
- **IP Details Lookup**: Interact with machines that have been infected by the payload (excluding the bot's own LHOST).
- **Creator Info**: Displays creator information when prompted.

## Setup

### Requirements

To run this bot, you need Python 3.x installed and the required dependencies. You can install them using the `requirements.txt` file.

### Installation

Clone this repository:

   ```bash
   git clone https://github.com/Copium-themal/Telegram-Bot-Mal.git
   cd Telegram-Bot-Mal
