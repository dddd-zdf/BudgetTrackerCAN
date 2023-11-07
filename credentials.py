import keyring
import base64

def get_credentials(name):
    try:
        # Retrieve the Base64 encoded credentials from keyring
        encoded_credentials = keyring.get_password(name, name)
        if encoded_credentials:
            # Base64 decode the credentials
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            # Split the credentials at the first colon to get the username and password. username never has colons
            username, password = decoded_credentials.split(':', 1)
            return username, password
        else:
            print(f"No credentials found for {name}.")
            return None, None
    except Exception as e:
        print(f"An error occurred while retrieving credentials for {name}: {e}")
        return None, None
