""" Handles master password authentication and verification for the password manager. """


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