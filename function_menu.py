""" Provides the main menu for adding, searching, viewing, and deleting passwords. """


import json 
import os 
import pyperclip

from encryption import *
from password_generator import * 


def menu():
    """ Display menu choices (1-5) on the CLI. """
    print(f"\n{'='*21}")
    print("   Password Manager  ")
    print("="*21)
    text = "1. Add Password\n2. View Passwords\n3. Search Passwords\n4. Delete Password\n5. Log out\n6. Exit"
    print(text)

    # Handle user choice input 
    try:
        choice = input("\nEnter (1-6): ")
        choice = int(choice)
    except:
        print("Invaild Response!!\n")

    return choice


def load_passwords():
    """ Read and return the stored passwords data from 'password.json'. """
    with open('data/passwords.json', 'r') as file:
        passwords = json.load(file)

    return passwords

        
def add_password(key):
    """ Prompt the user for website, username, and password and update & save them into the 'passwords.json'."""
    # Collect user inputs 
    website = input("\nWebsite: ")
    username = input("Username: ")

    # Create random or custom password 
    password = random_or_custom()

    # Encrypt the password 
    nonce, ciphertext = encrypt_password(key, password)

    # Check the file exists and stores data before attpemting to load
    if os.path.exists('data/passwords.json') and os.path.getsize('data/passwords.json') > 0:
        passwords = load_passwords()
    else:
        passwords = {}

    # Store username and password under website name 
    passwords[website] = {
        "username": username,
        "nonce": nonce,
        "ciphertext": ciphertext,
    }

    # Save updated dictionary back to 'passwords.json'
    with open('data/passwords.json', 'w') as file:
        json.dump(passwords, file, indent=4)


def copy_password(password):
    """ Prompt the user to copy the password. """
    copy = input("\nDo you want to copy the password?(y/n) ").lower()
    if copy == 'y':
        print("Done!")
        pyperclip.copy(password)
    elif copy == 'n':
        pass 
    else:
        print("\nInvalid Response!")


def view_passwords(key):
    """ Display a formatted table of stored websites and usernames, and reveal the password for user selected website. """
    try:
        passwords = load_passwords()
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!\n")
    else:
        # Display table header 
        print(f"\n {'Website':<15} {'Username'}")
        print("-" * 25)

        # Display website and username neatly in the table 
        for website, value in passwords.items():
            username = value['username']
            print(f" {website:<15} {username}")

        # Prompt user to reveal a password with the website name
        website = input("\nEnter the website to reveal the password (enter 'q' to quit!): ")
        if website in passwords:
            nonce = passwords[website]['nonce']
            ciphertext = passwords[website]['ciphertext']
            password = decrypt_password(key, nonce, ciphertext)
            print(f"Password: {password}")

            # Prompt the user to copy the password 
            copy_password(password)

        elif website == 'q':
            pass 
        else:
            print("There is no website with that name!")


def search_password(key):
    """ Search for sotred website name (case-insensitive). """
    try:
        passwords = load_passwords()
        site = input("\nSearch: ").lower()

        sites = []
        for website in passwords:
            if site in website.lower():
                sites.append(website)

        if sites:
            for site in sites: 
                print(f"\nWebsite: {site}")
                print(f"Username: {passwords[site]['username']}")

            # Prompt user to reveal a password with the website name
            website = input("\nEnter the website to reveal the password (enter 'q' to quit!): ")
            if website in sites:
                nonce = passwords[website]['nonce']
                ciphertext = passwords[website]['ciphertext']
                password = decrypt_password(key, nonce, ciphertext)
                print(f"Password: {password}")

                # Prompt the user to copy the password
                copy_password(password)
            elif website == 'q':
                pass
            else:
                print("There is no website with that name!")
        else:
            print("There is no website with that name!")
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!")


def delete_password():
    """ Delete a specific stored website from 'passwords.json'. """
    try: 
        passwords = load_passwords()
        website = input("\nWebsite: ")

        # Confirm deleteion if website exists 
        if website in passwords:
            confirmation = input(f"Delete {website}? (y/n): ")
            if confirmation == 'y':
                del passwords[website]
                print("Done!") 
            elif confirmation == 'n':
                pass 
            else:
                print("Invalid Response!")
        else:
            print("There is no website with that name!")

        # Save the updated dictionary back to the 'passwords.json'
        with open('data/passwords.json', 'w') as file:
            json.dump(passwords, file, indent=4)
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!")