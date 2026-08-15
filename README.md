# Password Manager

A command-line password manager built with Python that allows users to securely organize account credentials. The application stores website usernames and passwords in a structured format and provides features to add, view, search, and delete saved credentials.

This project was created to practice Python programming, file handling, data structures, authentication, encryption, and software organization while serving as the foundation for a more secure password manager.

## Features

* Master password authentication
* Add new website credentials
* View stored websites and usernames
* Reveal passwords for selected websites
* Search websites by name
* Delete saved credentials
* Copy passwords
* Generate passwords
* Check password strength
* Encrypt stored credentials
* Store data using JSON
* Command-line interface

## Technologies Used

* Python 3
* JSON
* `cryptography`
* `hashlib`
* File I/O
* Dictionaries
* Error handling
* Password hashing
* Encryption

## Project Structure

```text
password-manager/
│
├── data/
│   ├── passwords.json
│   └── master.json
│
├── auth.py
├── encryption.py
├── function_menu.py
├── main.py
├── password_generator.py
├── requirements.txt
└── README.md
```

### File Description

* **`main.py`** — Entry point of the application and controls the main program flow.
* **`auth.py`** — Handles master password authentication.
* **`encryption.py`** — Handles encryption and decryption of stored credentials.
* **`function_menu.py`** — Contains the main password-management operations.
* **`password_generator.py`** — Generates passwords and checks password strength.
* **`requirements.txt`** — Contains the external Python dependencies required by the project.
* **`data/passwords.json`** — Stores password-manager data.
* **`data/master.json`** — Stores authentication-related data.
* **`README.md`** — Contains project documentation and usage instructions.


## Installation

1. Clone the repository.

```bash
git clone https://github.com/neo-naing-lin-aung/password-manager.git
```

2. Navigate to the project directory.

```bash
cd password-manager
```

3. Install the required dependencies.

```bash
pip3 install -r requirements.txt
```

4. Run the application.

```bash
python3 main.py
```


## Usage

After successful master authentication, the user can choose from the main menu:

```text
1. Add Password
2. View Passwords
3. Search Passwords
4. Delete Password
5. Logout
6. Exit
```

Follow the prompts to manage your stored credentials.


## Security

The project uses a master-password authentication system and encryption to protect stored credentials. Password-related data is not intended to be stored as plain text. This project is primarily an educational project and should not be considered a production-ready password manager. 


## What I Learned

Through this project I practiced:

* Python functions and modules
* File handling
* JSON data storage
* Dictionaries and data structures
* Password hashing
* Encryption and decryption
* Authentication
* Error handling
* Modular software organization
* Building a complete command-line application

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.