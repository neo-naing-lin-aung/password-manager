import json
import os 


def master_exists():
    pass


def create_master_password():
    pass 


def authenticate():
    pass 


def menu():
    """ Display menu choices (1-5) on the CLI. """
    print(f"\n\n{'='*21}")
    print("   Password Manager  ")
    print("="*21)
    text = "1. Add Password\n2. View Passwords\n3. Search Passwords\n4. Delete Password\n5. Log out\n6. Exit"
    print(text)

    # Handle user choice input 
    try:
        choice = input("\nEnter (1-5): ")
        choice = int(choice)
    except:
        print("Invaild Response!!\n")

    return choice


def load_passwords():
    """ Read and return the stored passwords data from 'password.json'. """
    with open('data/passwords.json', 'r') as file:
        passwords = json.load(file)

    return passwords


def add_password():
    """ Prompt the user for website, username, and password and update & save them into the 'passwords.json'."""
    # Collect user inputs 
    website = input("\nWebsite: ")
    username = input("Username: ")
    password = input("Password: ")

    # Check the file exists and stores data before attpemting to load
    if os.path.exists('data/passwords.json') and os.path.getsize('passwords.json') > 0:
        passwords = load_passwords()
    else:
        passwords = {}

    # Store username and password under website name 
    passwords[website] = {
        "username": username,
        "password": password,
    }

    # Save updated dictionary back to 'passwords.json'
    with open('data/passwords.json', 'w') as file:
        json.dump(passwords, file, indent=4)


def view_passwords():
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
            print(f"Password: {passwords[website]['password']}")
        else:
            print("There is no website with that name!")
    except FileNotFoundError:
        # Handle if 'passwords.json' has not been created yet 
        print("Create a password first!!\n")


def search_password():
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
                print(f"Password: {passwords[site]['password']}")
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
                print("Invalid Response")
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
                is_authenticated = authenticate()
                if is_authenticated:
                    # User menu loop 
                    while True: 
                        choice = menu()

                        if choice == 1:
                            add_password()
                        elif choice == 2:
                            view_passwords()
                        elif choice == 3:
                            search_password()
                        elif choice == 4: 
                            delete_password()
                        elif choice == 5:
                            # Logout and reset attempts to 0
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
                return

        else:
            # Create master password for the first time 
            create_master_password()
            continue

if __name__ == "__main__":
    main()