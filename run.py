import sqlite3
from selenium import webdriver
# Import your modules here
import amex
# import tangerine
# import other_bank

# Configuration for each bank module
bank_modules = [
    {
        'module': amex,
        'cards': ['amex gold', 'amex cobalt']
    },
    # Uncomment and complete the configuration as you add more modules
    # {
    #     'module': tangerine,
    #     'cards': ['tangerine card']
    # },
    # {
    #     'module': other_bank,
    #     'cards': ['other bank card']
    # },
]

def setup_database():
        # Initialize the database for storing transactions
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    # Assuming all modules use the same table structure
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            date DATE,
            cent INTEGER,
            description TEXT,
            card TEXT
        )
    ''')
    conn.commit()
    return conn

def main():
    conn = setup_database()
    cursor = conn.cursor()
    driver = webdriver.Chrome()

    try:
        for bank in bank_modules:
            module = bank['module']
            module.login(driver)  # Assuming all modules have a login function
            for card in bank.get('cards', []):
                module.retrieve_transactions(driver, card, cursor, conn)  # Pass the card if necessary

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()
        conn.close()
        driver.quit()

if __name__ == "__main__":
    main()
