""" Provides password generation and password strength validation functions. """

import getpass
import secrets
import string


def check_password_strength(password):
    """ Check the password strength for custom password. """
    while True:
        # Check the password contins at least 8 characters, one lowercase, 1 upper case, 1 number, and one special 
        if (len(password) >= 8
            and any(c.islower() for c in password) 
            and any(c.isupper() for c in password) 
            and any(c in string.punctuation for c in password)
            and any(c.isdigit() for c in password)):
            # Exit the loop 
            break
        else:
            # Prompt the user for the password 
            text = "\nYour password must contains:\n\t~ At least 8 characters\n\t~ One uppercase letter\n\t"
            text += "~ One lowercase letter\n\t~ One number\n\t~ One special character\n"
            print(text)
            password = getpass.getpass("Password: ")
            continue


def random_password_generator():
    """ 
    Generate a sixteen digits password with at least one lowercase, one uppercase, three special characters, 
    and three numbers radomly and return it.
    """
    # Combine letters, special characters, and  numbers in one variable 
    characters = string.ascii_letters + string.punctuation + string.digits

    # Loop until a generated password meets all requirements
    while True:
        password = ''.join(secrets.choice(characters) for i in range(16))
        if (any(c.islower() for c in password) 
                and any(c.isupper() for c in password) 
                and sum(c in string.punctuation for c in password) >= 3
                and sum(c.isdigit() for c in password) >= 3):
                break # Exit the loop 
        
    return password
    

def random_or_custom():
    """ 
    Ask the user whether he/she wants random sixteen digits passwords or wants to create his/her custom password, and 
    return the password. 
    """
    print("\nDo you want to create random sixteen digits password or your own custom password?")

    # Keep asking until the user enters a vaild choice 
    while True:
        answer = input("Enter 'random' or 'custom': ").lower()

        # Decide random or custom password based on the user input  
        if answer == 'random':
            password = random_password_generator()
        elif answer == 'custom':
            text = "\nPassword requirements:\n\t~ At least 8 characters\n\t~ One uppercase letter\n\t"
            text += "~ One lowercase letter\n\t~ One number\n\t~ One special character\n"
            print(text)
            password = getpass.getpass("Password: ")

            # Check the password strength 
            check_password_strength(password)
        else:
            print("Invalid Response!\n")
            continue

        break # Exit the loop 

    # Display the successful message 
    print("\nSuccessful!")

    return password