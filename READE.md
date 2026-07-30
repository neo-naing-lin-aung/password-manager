# 🔐 Password Manager

A command-line password manager built with Python that allows users to securely organize account credentials. The application stores website usernames and passwords in a structured format and provides features to add, view, search, and delete saved credentials.

This project was created to practice Python programming, file handling, data structures, and software organization while serving as the foundation for a more secure password manager.

---

## Features

- Add new website credentials
- View stored websites and usernames
- Reveal passwords for selected websites
- Search websites by name
- Delete saved credentials
- Store data using JSON
- Simple command-line interface

---

## Technologies Used

- Python 3
- JSON
- File I/O
- Dictionaries
- Error Handling

---

## Project Structure

```
password-manager/
│
├── data/
│   └── passwords.json
│
├── main.py
└── README.md
```

---

## Installation

1. Clone the repository.

```bash
git clone https://github.com/neo-naing-lin-aung/password-manager.git
```

2. Navigate to the project directory.

```bash
cd password-manager
```

3. Run the application.

```bash
python3 main.py
```

---

## Usage

Choose an option from the main menu:

1. Add Password
2. View Passwords
3. Search Passwords
4. Delete Password
5. Exit

Follow the prompts to manage your stored credentials.

---

## How It Works

1. The program stores passwords credentials in a JSON file.
2. Each website contains a username and a password.
3. Users can add, search, view, and delete credentials through the menu interface.
4. Changes are automatically saved after modifications.

---

## Current Limitations

This version is intended as a learning project and **does not yet implement advanced security features**.

Currently:

- Passwords are stored in plain text.
- No master password authentication.
- No encryption.
- No password generator.

These features are planned for future versions.

---

## Planned Improvements

- Master password authentication
- Password encryption
- Secure password generator
- Password strength checker
- Edit existing credentials
- Graphical User Interface (GUI)
- Automatic backup
- Import and export encrypted data

---

## What I Learned

Through this project I practiced:

- Python functions
- Dictionaries
- JSON data storage
- File handling
- Error handling
- Program organization
- Building a complete command-line application

---

## Future Goals

The long-term goal of this project is to transform it into a secure password manager by implementing modern security practices such as encryption, authentication, and cryptographically secure password generation.

---

## License

This project is licensed under the MIT License.