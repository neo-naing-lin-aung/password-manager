import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import getpass 
import hashlib
import json
import os 
import secrets


def master_exists():
    """ Check wheter master password exists and return True / False. """
    if os.path.exists('data/master.json') and os.path.getsize('data/master.json') > 0:
        return True
    else:
        return False


def create_master_password():
    """ Create master password and store in 'master.json'. """
    # Let the user know to create the master password 
    print("\nYou haven't created master password yet, so create one first!")

    # Keep asking until the user inputs matching passwords 
    while True:
        master_password = getpass.getpass("\nEnter Master Password: ")
        confirm = getpass.getpass("Confirm Master Password: ")

        if master_password != confirm:
            print("\nPasswords do not match!\n")
            continue
        else:
            print("\nMaster password created successfully! Please log in to your account.")
            break 

    # Convert password string to bytes required for hashing 
    master_password = master_password.encode('utf-8')
    # Generate 16 random bytes to use as salt 
    salt = secrets.token_bytes(16)
    # Set high iteration count to protect against brute-force attacks
    iterations = 600000
    # Generate secure PBKDF2 hash and convert to hex string
    hash_password = hashlib.pbkdf2_hmac('sha256', master_password, salt, iterations).hex()

    # Structured master data for saving 
    master_data = {
        'salt': salt.hex(),
        'iterations': iterations,
        'hash_password': hash_password,
    }

    # Save the master data to 'master.json' file 
    with open('data/master.json', 'w') as file:
        json.dump(master_data, file, indent=4)

def get_master_data():
    """Retrieve salt, iterations, and stored hash from master.json and return them."""
    # Load master data from the file 
    with open('data/master.json', 'r') as file:
        master_data = json.load(file)

    # Convert stored hex values back into raw bytes 
    salt = bytes.fromhex(master_data['salt'])
    iterations = master_data['iterations']
    stored_hash = bytes.fromhex(master_data['hash_password'])

    return salt, iterations, stored_hash

def authenticate():
    """ Authenticate the password. """
    # Prompt the user for master password 
    master_password = getpass.getpass("\nEnter Your Master Password: ").encode('utf-8')

    # Get salt, iterations, and stored hash from master.json using get_master_data()
    salt, iterations, stored_hash = get_master_data()

    # Hash user input password using retrieved salt and iterations 
    hash_password = hashlib.pbkdf2_hmac('sha256', master_password, salt, iterations)

    # Check hashes match  
    if stored_hash == hash_password:
        # Return key to use in encryption for passwords 
        key = hashlib.pbkdf2_hmac('sha256', master_password, salt, iterations, 32)
        return key 
    else:
        return None
        

def menu():
    """ Display menu choices (1-5) on the CLI. """
    print(f"\n\n{'='*21}")
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

def encrypt_password(key, password):
    """ Encrypt the password and return nonce & ciphertext. """
    nonce = secrets.token_bytes(12)
    password = password.encode()
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, password, None)

    # Change the nonce and ciphertext into a readable Base64 string 
    nonce = base64.b64encode(nonce).decode()
    ciphertext = base64.b64encode(ciphertext).decode()
    return nonce, ciphertext

def decrypt_password(key, nonce, ciphertext):
    """ Decrypt the password stored in the passwords.json. """
    nonce = base64.b64decode(nonce)
    ciphertext = base64.b64decode(ciphertext)
    aesgcm = AESGCM(key)
    password = aesgcm.decrypt(nonce, ciphertext, None)

    return password.decode()

def add_password(key):
    """ Prompt the user for website, username, and password and update & save them into the 'passwords.json'."""
    # Collect user inputs 
    website = input("\nWebsite: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
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


def view_passwords(key):
    """ Display a formatted table of stored websites and usernames, and reveal the password for user selected website. """
    try:
        passwords = load_passwords()

        # Display table header 
        print(f"\n {'Website':<15} {'Username'}")
        print("-" * 25)

        # Display website and username neatly in the table 
        for website, value in passwords.items():
            username = value['username']
            print(f" {website:<15} {username}")

        # Prompt user to reveal a specific password 
        website = input("Enter the website to reveal the password: ")
        if website in passwords:
            nonce = passwords[website]['nonce']
            ciphertext = passwords[website]['ciphertext']
            password = decrypt_password(key, nonce, ciphertext)
            print(f"Password: {password}")
        else:
            print("There is no website with that name!")
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!\n")


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
                nonce = passwords[site]['nonce']
                ciphertext = passwords[site]['ciphertext']
                password = decrypt_password(key, nonce, ciphertext)
                print(f"Password: {password}")
        else:
            print("There is no website with that name!")
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!")


def delete_password():
    """ Delete a specific stored website from 'passwords.json'. """
    try: 
        passwords = load_passwords()
        website = input("\nDelete Website: ")

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


def main():
    """ Main execution loop for password manager."""
    while True:
        # Check if a master password has been created 
        if master_exists():
            attempts = 0

            # Allow 3 authentication attempts
            while (attempts < 3):
                key = authenticate()
                if key is not None:
                    # User menu loop 
                    while True: 
                        choice = menu()

                        if choice == 1:
                            add_password(key)
                        elif choice == 2:
                            view_passwords(key)
                        elif choice == 3:
                            search_password(key)
                        elif choice == 4: 
                            delete_password()
                        elif choice == 5:
                            # Logout and reset attempts to 0
                            key = None
                            attempts = 0
                            break 
                        elif choice == 6:
                            # Exit the program 
                            return
                else: 
                    # Failed attempt 
                    print("Incorrect Password!")
                    attempts += 1

            # Exit the program after 3 failed attempts
            if attempts == 3:
                print("\nYour attempt limit has been reached. Run the program again!\n")
                return

        else:
            # Create master password for the first time 
            create_master_password()
            continue

if __name__ == "__main__":
    main()