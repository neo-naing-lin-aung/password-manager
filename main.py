""" Runs the main program and coordinates the password manager components. """


from auth import *
from function_menu import *


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


# Ensure code execute only when the script is run directly 
if __name__ == "__main__":
    main()