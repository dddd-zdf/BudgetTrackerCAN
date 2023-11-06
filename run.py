import yaml
import importlib
import sqlite3
from selenium import webdriver

CONFIG_FILE = 'configs.yaml'

def setup_database():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date DATE,
            cent INTEGER,
            description TEXT,
            card TEXT
        )
        '''
    )
    conn.commit()
    return conn

def main():
    # Load the YAML configuration file into a dictionary
    with open(CONFIG_FILE, 'r') as file:
        configs = yaml.safe_load(file)

    # Setup database (if needed)
    conn = setup_database()
    cursor = conn.cursor()

    # Iterate over each configuration
    for config_name, config in configs.items():
        # Dynamically import the module using the config name
        module = importlib.import_module(config_name)

        # Extract the credentials and URL for the bank
        username = config['username']
        password = config['password']
        url = config['url']

        # Initialize the webdriver and pass it to the module's login function
        driver = webdriver.Chrome()  # Replace with your preferred browser

        try:
            # Assuming each module has a login function
            module.login(driver, url, username, password)

            # Assuming each module has a retrieve_transactions function
            for card in config['cards']:
                module.retrieve_transactions(driver, card, cursor, conn)

            # Commit after each bank's transactions are retrieved
            conn.commit()

        except Exception as e:
            print(f"An error occurred with {config_name}: {e}")

        finally:
            # Close the driver after each bank's transactions are handled
            driver.quit()

    # Close the database connection after all transactions have been retrieved
    conn.close()

if __name__ == "__main__":
    main()
