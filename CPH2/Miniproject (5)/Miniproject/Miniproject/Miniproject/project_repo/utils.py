from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_password(password):
    """Encrypts the given password using Fernet encryption."""
    cipher = Fernet(settings.ENCRYPTION_KEY)
    encrypted_password = cipher.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password):
    """Decrypts the given password using Fernet encryption."""
    cipher = Fernet(settings.ENCRYPTION_KEY)
    decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
    return decrypted_password

def some_model_function():
    from .views import some_function
    some_function()

# utils.py
def some_function():
    print("This is some_function in utils.py")
