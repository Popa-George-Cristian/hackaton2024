class UserManager:
    def __init__(self, save_directory):
        self.save_directory = save_directory
        os.makedirs(self.save_directory, exist_ok=True)

    def create_user(self, username, password):
        """Create a new user folder and encrypt the password."""
        user_folder = os.path.join(self.save_directory, username)

        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

            # Derive a key from the password using PBKDF2
            key = self.derive_key_from_password(password)

            # Save the hashed password (for verification)
            password_file = os.path.join(user_folder, "password.hash")
            with open(password_file, 'wb') as f:
                f.write(key)

            print(f"User {username} created successfully. Password file saved at: {password_file}")
        else:
            print(f"User {username} already exists.")
            messagebox.showerror("Error", f"User {username} already exists.")
    
    def authenticate_user(self, username, password):
        """Authenticate a user by verifying the password."""
        user_folder = os.path.join(self.save_directory, username)

        if not os.path.exists(user_folder):
            print("User does not exist.")
            messagebox.showerror("Error", "User does not exist.")
            return None

        password_file = os.path.join(user_folder, "password.hash")
        if not os.path.exists(password_file):
            print("Error: Missing password file.")
            messagebox.showerror("Error", "Missing password file.")
            return None

        with open(password_file, 'rb') as f:
            stored_key = f.read()

        # Derive the key from the entered password and compare
        entered_key = self.derive_key_from_password(password)

        if entered_key == stored_key:
            print(f"User {username} authenticated successfully.")
            return entered_key
        else:
            print("Incorrect password.")
            messagebox.showerror("Error", "Incorrect password.")
            return None

    def derive_key_from_password(self, password):
        """Derives a key from the password using PBKDF2 and SHA256."""
        salt = b"my_salt"  # In production, use a random salt
        kdf = PBKDF2HMAC(
            algorithm='sha256',
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = kdf.derive(password.encode())
        return key
