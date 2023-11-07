import keyring
import base64
import getpass

#in keyring we store {name} as {username} and store {username:password} as {password} to protect our username, assuming you have only one account with one institution.
while True:
    name = input("input bank name: ")
    username = getpass.getpass("input username: ")
    password = getpass.getpass("input password: ")

    # Combine the username and password
    credentials_combined = f"{username}:{password}"

    # Base64 encode the combined credentials
    credentials_encoded = base64.b64encode(credentials_combined.encode('utf-8')).decode('utf-8')

    # Store the Base64 encoded credentials in keyring
    keyring.set_password(name, name, credentials_encoded)